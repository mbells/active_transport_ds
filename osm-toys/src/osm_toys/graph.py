import networkx as nx
import numpy as np
import osmnx as ox

from scipy.spatial import KDTree


def filter_graph_within_radius(G, center_point, search_radius=1000):
    """
    Returns a subgraph of all nodes and edges within `search_radius` meters
    of the `center_point`, based on shortest path distance.

    Parameters:
        center_point (tuple): (latitude, longitude)
        search_radius (int): Radius in meters for inclusion in subgraph (shortest-path based)
        download_radius (int): Radius in meters to download OSM graph
        network_type (str): 'walk', 'drive', 'bike', or 'all'

    Returns:
        networkx.MultiDiGraph: Subgraph of nodes/edges within shortest path distance
    """

    # Find the nearest node to the center point
    center_node = ox.distance.nearest_nodes(G, X=center_point[1], Y=center_point[0])

    # Use Dijkstra to find all nodes within search_radius (in meters)
    lengths = nx.single_source_dijkstra_path_length(
        G, center_node, cutoff=search_radius, weight="length"
    )

    # Get the nodes within the radius
    nearby_nodes = set(lengths.keys())

    # Extract the subgraph
    subgraph = G.subgraph(nearby_nodes).copy()

    return subgraph


# https://stackoverflow.com/questions/79271245/osmnx-python-network-type-filters
HIGHWAYS_BY_NETWORK_TYPE = {
    "bike": {
        "cycleway",
        "primary",
        "primary_link",
        "secondary",
        "secondary_link",
        "tertiary",
        "tertiary_link",
        "unclassified",
        "residential",
        "living_street",
        "service",
        "path",
        "road",
        "track",
    },
    "drive": {
        "motorway",
        "trunk",
        "primary",
        "secondary",
        "tertiary",
        "unclassified",
        "residential",
        "motorway_link",
        "trunk_link",
        "primary_link",
        "secondary_link",
        "tertiary_link",
        "living_street",
        "road",
        "service",
    },
    "walk": {
        "footway",
        "pedestrian",
        "path",
        "steps",
        "residential",
        "living_street",
        "service",
        "cycleway",
        "road",
    },
}


def filter_graph_by_network_type(G, network_type="all"):
    if network_type == "all":
        return G
    allowed_highways = HIGHWAYS_BY_NETWORK_TYPE[network_type]
    edges_to_keep = []
    for u, v, k, data in G.edges(keys=True, data=True):
        highway = data.get("highway")
        if highway:
            if isinstance(highway, list):
                if any(h in allowed_highways for h in highway):
                    edges_to_keep.append((u, v, k))
            elif highway in allowed_highways:
                edges_to_keep.append((u, v, k))

    G_filtered = G.edge_subgraph(edges_to_keep).copy()
    # G_simplified = ox.simplify_graph(G_filtered)
    # return G_simplified
    return G_filtered


def calc_reachable_graph_with_penalty(
    G,
    center_point,
    search_radius=1000,
    download_radius=2000,
    network_type="walk",
    traffic_signal_penalty=30,
    proximity_threshold=15,
    crossing_max=20,
):
    """
    Returns a subgraph of all nodes/edges within a search radius from a center point,
    applying a penalty to edges connected to traffic lights.

    Parameters:
        G
        center_point (tuple): (latitude, longitude)
        search_radius (int): Distance in meters for inclusion in subgraph (Dijkstra-based)
        download_radius (int): Distance in meters for OSM download area
        network_type (str): 'walk', 'drive', 'bike', or 'all'
        traffic_signal_penalty (float): Meters added to edge weight if connected to a traffic signal
        proximity_threshold (float): Distance threshold (in meters) to consider a crossing 'near' a light
        crossing_max (float): Max distance for a crossing, otherwise assumed to be a street section

    Returns:
        networkx.MultiDiGraph: Penalized subgraph
    """
    # Step 1: Download the graph
    # G = ox.graph_from_point(center_point, dist=download_radius, network_type=network_type)
    G = filter_graph_by_network_type(G, network_type)

    # Step 2: Find all traffic signals nodes
    crossings = {
        node for node, data in G.nodes(data=True) if data.get("highway") == "crossing"
    }

    traffic_signals = {
        node
        for node, data in G.nodes(data=True)
        if data.get("highway") == "traffic_signals"
    }

    # Step 3: Build a KDTree of traffic signals for efficient spatial lookup
    node_coords = {}
    for node, data in G.nodes(data=True):
        x, y = data["x"], data["y"]
        node_coords[node] = (x, y)
    signal_points = np.array([node_coords[n] for n in traffic_signals])
    signal_tree = KDTree(signal_points) if len(traffic_signals) else None

    # 4. Mark penalties on crossing nodes that are near traffic signals
    if signal_tree:
        for cross_node in crossings:
            cross_point = node_coords[cross_node]
            distance, _ = signal_tree.query(
                cross_point, distance_upper_bound=proximity_threshold
            )
            if np.isfinite(distance):
                G.nodes[cross_node]["penalty"] = traffic_signal_penalty
                # print(f"crossing near signal {cross_node}")

    # 5. Apply penalties to edge weights (both in and out get half)
    for u, v, k, data in G.edges(keys=True, data=True):
        base_length = data.get("length", 1)
        node_penalty_u = G.nodes[u].get("penalty", 0)
        node_penalty_v = G.nodes[v].get("penalty", 0)
        node_penalty = max(node_penalty_u, node_penalty_v) / 2
        if base_length > crossing_max:
            node_penalty = 0
        data["penalized_length"] = base_length + node_penalty
    """
    # Step 4: Assign custom weights to edges
    for u, v, key, data in G.edges(keys=True, data=True):
        base_length = data.get('length', 1)  # default fallback
        # Penalize if either node is a traffic light
        if u in crossings or v in crossings:
            data['penalized_length'] = base_length + traffic_signal_penalty
        else:
            data['penalized_length'] = base_length
    """

    # Step 6: Compute shortest path distances using penalized weights
    center_node = ox.distance.nearest_nodes(G, X=center_point[1], Y=center_point[0])
    lengths = nx.single_source_dijkstra_path_length(
        G, center_node, cutoff=search_radius, weight="penalized_length"
    )

    # Step 7: Build and return the subgraph
    nearby_nodes = set(lengths.keys())
    subgraph = G.subgraph(nearby_nodes).copy()
    return subgraph

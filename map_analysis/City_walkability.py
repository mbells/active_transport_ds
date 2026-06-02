# %%
import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from scipy.spatial import KDTree

# %%
# 2. Define center coordinates for King & Victoria in Kitchener, ON
# Coordinates obtained via geocoding
center_point = (43.4516, -80.4925)  # (latitude, longitude)

# 3. Define search radius in meters
radius = 2000  # in meters

# 4. Download street network within the specified radius
G = ox.graph_from_point(center_point, dist=radius, network_type='all')

# %%
# 5. Plot the map
fig, ax = ox.plot_graph(G, node_size=5, edge_color='#555555', bgcolor='white')

# %%

def filter_and_simplify_graph(G, network_type='walk'):
    """
    Simplify an existing OSMnx graph to match a given network_type.

    Parameters:
        G (networkx.MultiDiGraph): The full graph
        network_type (str): 'drive', 'walk', 'bike', etc.

    Returns:
        networkx.MultiDiGraph: Simplified and filtered graph
    """
    # 1. Get the set of highway types allowed for the network_type
    # This is an internal OSMnx helper for filtering
    # OLD CODE -- does not work!
    filters = ox.settings.all_oneway_network_types[network_type]['highway']

    # 2. Filter edges by 'highway' tag
    edges_to_keep = []
    for u, v, k, data in G.edges(keys=True, data=True):
        highway = data.get('highway')
        if highway:
            if isinstance(highway, list):
                if any(h in filters for h in highway):
                    edges_to_keep.append((u, v, k))
            elif highway in filters:
                edges_to_keep.append((u, v, k))

    # 3. Create a subgraph with only those edges
    G_filtered = G.edge_subgraph(edges_to_keep).copy()

    # 4. Simplify the graph topology
    #G_simplified = ox.simplify_graph(G_filtered)

    #return G_simplified
    return G_filtered


def get_graph_within_radius(G, center_point, search_radius=1000):
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
    lengths = nx.single_source_dijkstra_path_length(G, center_node, cutoff=search_radius, weight='length')

    # Get the nodes within the radius
    nearby_nodes = set(lengths.keys())

    # Extract the subgraph
    subgraph = G.subgraph(nearby_nodes).copy()

    return subgraph

# https://stackoverflow.com/questions/79271245/osmnx-python-network-type-filters
HIGHWAYS_BY_NETWORK_TYPE ={
    'bike': {
      'cycleway',
      'primary', 'primary_link',
      'secondary', 'secondary_link',
      'tertiary', 'tertiary_link',
      'unclassified', 'residential',
      'living_street', 'service',
      'path', 'road', 'track',
    },
    'drive': {
      'motorway', 'trunk', 'primary', 'secondary', 'tertiary',
      'unclassified', 'residential', 'motorway_link', 'trunk_link',
      'primary_link', 'secondary_link', 'tertiary_link', 'living_street',
      'road', 'service'
    },
    'walk': {
      'footway', 'pedestrian',
      'path', 'steps',
      'residential', 'living_street',
      'service',
      'cycleway', 'road',
    }
}

def filter_graph_by_network_type(G, network_type='all'):
    if network_type == 'all':
        return G
    allowed_highways = HIGHWAYS_BY_NETWORK_TYPE[network_type]
    edges_to_keep = []
    for u, v, k, data in G.edges(keys=True, data=True):
        highway = data.get('highway')
        if highway:
            if isinstance(highway, list):
                if any(h in allowed_highways for h in highway):
                    edges_to_keep.append((u, v, k))
            elif highway in allowed_highways:
                edges_to_keep.append((u, v, k))

    G_filtered = G.edge_subgraph(edges_to_keep).copy()
    #G_simplified = ox.simplify_graph(G_filtered)
    #return G_simplified
    return G_filtered


# %%
def get_traffic_lights(G):
    """
    Returns a list of node IDs that are traffic lights in the graph G.

    Parameters:
        G (networkx.MultiDiGraph): The OSMnx graph.

    Returns:
        list: Node IDs of traffic lights.
    """
    traffic_lights = [
        node for node, data in G.nodes(data=True)
        if data.get('highway') == 'traffic_signals'
    ]
    return traffic_lights

def plot_traffic_lights(ax, G, lights):
  # Extract coordinates for plotting
  x = [G.nodes[n]['x'] for n in lights]
  y = [G.nodes[n]['y'] for n in lights]

  # Plot traffic lights in red
  ax.scatter(x, y, c='red', s=40, alpha=0.5, label='Traffic Lights')
  ax.legend()


def get_crossings(G):
    """
    Returns a list of node IDs that are traffic lights in the graph G.

    Parameters:
        G (networkx.MultiDiGraph): The OSMnx graph.

    Returns:
        list: Node IDs of traffic lights.
    """
    crossings = [
        node for node, data in G.nodes(data=True)
        if data.get('highway') == 'crossing'
    ]
    return crossings

def plot_crossings(ax, G, crossings):
  # Extract coordinates for plotting
  x = [G.nodes[n]['x'] for n in crossings]
  y = [G.nodes[n]['y'] for n in crossings]

  # Plot traffic crossings in red
  ax.scatter(x, y, c='gold', s=40, alpha=0.5, label='Crossings')
  ax.legend()
# -------------------
def get_nodes_of_type(G, node_type):
    """
    Returns a list of node IDs that are in the graph G of a particular type.

    Parameters:
        G (networkx.MultiDiGraph): The OSMnx graph.

    Returns:
        list: Node IDs of traffic lights.
    """
    nodes = [
        node for node, data in G.nodes(data=True)
        if data.get('highway') == node_type
    ]
    return nodes

def plot_nodes(ax, G, node_type, color, size, alpha, label=None):
  nodes = get_nodes_of_type(G, node_type)
  print(f"Found {len(nodes)} of type {node_type}.")

  # Extract coordinates for plotting
  x = [G.nodes[n]['x'] for n in nodes]
  y = [G.nodes[n]['y'] for n in nodes]

  if label is None:
    label = node_type

  # Plot traffic crossings in red
  ax.scatter(x, y, c=color, s=size, alpha=alpha, label=label)
  ax.legend()

# %%
# Coordinates of King & Victoria, Kitchener, ON
center = (43.4516, -80.4925)

G_sub = G

G_sub = get_graph_within_radius(G_sub, center_point, search_radius=500)

#G_sub = filter_and_simplify_graph(G_sub, network_type='walk')
#G_sub = ox.utils_graph.graph_from_gdfs(G_sub.nodes, G_sub.edges, network_type='walk')
#G_sub = filter_graph_by_network_type(G_sub, network_type='walk')

# Get subgraph within 1km shortest-path distance
G_sub = get_graph_within_radius(G_sub, center_point=center, search_radius=1000)

# Plot the result
ox.plot_graph(G_sub, node_size=5, edge_color='black', bgcolor='white')

# %%
# Get traffic lights in the subgraph
lights = get_traffic_lights(G_sub)
print(f"Found {len(lights)} traffic lights.")

fig, ax = ox.plot_graph(G_sub, node_size=5, node_color='gray', edge_color='lightgray', bgcolor='white', show=False, close=False)

plot_nodes(ax, G_sub, 'traffic_signals', color='red', size=40, alpha=0.5)
plot_nodes(ax, G_sub, 'crossing', color='gold', size=20, alpha=0.5)

#plot_traffic_lights(ax, G_sub, lights)
"""
# Extract coordinates for plotting
x = [G_sub.nodes[n]['x'] for n in lights]
y = [G_sub.nodes[n]['y'] for n in lights]

# Plot traffic lights in red
ax.scatter(x, y, c='red', s=30, label='Traffic Lights')
ax.legend()
"""
plt.show()

# %%

def dl_get_graph_within_radius_with_penalty(center_point,
                                         search_radius=1000,
                                         download_radius=2000,
                                         network_type='walk',
                                         traffic_light_penalty=30):
    """
    Returns a subgraph of all nodes/edges within a search radius from a center point,
    applying a penalty to edges connected to traffic lights.

    Parameters:
        center_point (tuple): (latitude, longitude)
        search_radius (int): Distance in meters for inclusion in subgraph (Dijkstra-based)
        download_radius (int): Distance in meters for OSM download area
        network_type (str): 'walk', 'drive', 'bike', or 'all'
        traffic_light_penalty (float): Meters added to edge weight if connected to a traffic signal

    Returns:
        networkx.MultiDiGraph: Penalized subgraph
    """
    # Step 1: Download the graph
    G = ox.graph_from_point(center_point, dist=download_radius, network_type=network_type)

    # Step 2: Find all traffic light nodes
    traffic_lights = {
        node for node, data in G.nodes(data=True)
        if data.get('highway') == 'traffic_signals'
    }

    # Step 3: Assign custom weights to edges
    for u, v, key, data in G.edges(keys=True, data=True):
        base_length = data.get('length', 1)  # default fallback
        # Penalize if either node is a traffic light
        if u in traffic_lights or v in traffic_lights:
            data['penalized_length'] = base_length + traffic_light_penalty
        else:
            data['penalized_length'] = base_length

    # Step 4: Compute shortest path distances using penalized weights
    center_node = ox.distance.nearest_nodes(G, X=center_point[1], Y=center_point[0])
    lengths = nx.single_source_dijkstra_path_length(
        G, center_node, cutoff=search_radius, weight='penalized_length'
    )

    # Step 5: Build and return the subgraph
    nearby_nodes = set(lengths.keys())
    subgraph = G.subgraph(nearby_nodes).copy()
    return subgraph


def get_graph_within_radius_with_penalty(G,
                                         center_point,
                                         search_radius=1000,
                                         download_radius=2000,
                                         network_type='walk',
                                         traffic_signal_penalty=30,
                                         proximity_threshold=15,
                                         crossing_max=20):
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
    #G = ox.graph_from_point(center_point, dist=download_radius, network_type=network_type)
    G = filter_graph_by_network_type(G, network_type)

    # Step 2: Find all traffic signals nodes
    crossings = {
        node for node, data in G.nodes(data=True)
        if data.get('highway') == 'crossing'
    }

    traffic_signals = {
        node for node, data in G.nodes(data=True)
        if data.get('highway') == 'traffic_signals'
    }

    # Step 3: Build a KDTree of traffic signals for efficient spatial lookup
    node_coords = {}
    for node, data in G.nodes(data=True):
        x, y = data['x'], data['y']
        node_coords[node] = (x, y)
    signal_points = np.array([node_coords[n] for n in traffic_signals])
    signal_tree = KDTree(signal_points) if len(traffic_signals) else None

    # 4. Mark penalties on crossing nodes that are near traffic signals
    if signal_tree:
        for cross_node in crossings:
            cross_point = node_coords[cross_node]
            distance, _ = signal_tree.query(cross_point, distance_upper_bound=proximity_threshold)
            if np.isfinite(distance):
                G.nodes[cross_node]['penalty'] = traffic_signal_penalty
                #print(f"crossing near signal {cross_node}")

    # 5. Apply penalties to edge weights (both in and out get half)
    for u, v, k, data in G.edges(keys=True, data=True):
        base_length = data.get('length', 1)
        node_penalty_u = G.nodes[u].get('penalty', 0)
        node_penalty_v = G.nodes[v].get('penalty', 0)
        node_penalty = max(node_penalty_u, node_penalty_v) / 2
        if base_length > crossing_max:
          node_penalty = 0
        data['penalized_length'] = base_length + node_penalty
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
        G, center_node, cutoff=search_radius, weight='penalized_length'
    )

    # Step 7: Build and return the subgraph
    nearby_nodes = set(lengths.keys())
    subgraph = G.subgraph(nearby_nodes).copy()
    return subgraph





# %%
# Coordinates of King & Victoria
center = (43.4516, -80.4925)

# Get subgraph with traffic light penalties
G_penalized = get_graph_within_radius_with_penalty(G, center_point=center, search_radius=333, traffic_signal_penalty=70)

# Plot it
fig, ax = ox.plot_graph(
    G_penalized,
    node_size=10, node_color='blue',
    edge_color='black', bgcolor='white',
    show=False, close=False
)

#lights = get_traffic_lights(G_penalized)
#print(f"Found {len(lights)} traffic lights.")
#plot_traffic_lights(ax, G_penalized, lights)
#
#crossings = get_crossings(G_penalized)
#print(f"Found {len(crossings)} traffic lights.")
#plot_crossings(ax, G_penalized, crossings)

plot_nodes(ax, G_sub, 'traffic_signals', color='red', size=40, alpha=0.5)
plot_nodes(ax, G_sub, 'crossing', color='gold', size=40, alpha=0.5)

plt.show()

# %%
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from matplotlib.collections import LineCollection

def plot_graph_with_penalties(G, penalty_attr='penalized_length', base_attr='length'):
    """
    Plot the graph with penalized edges in red.

    Parameters:
        G (networkx.MultiDiGraph): The graph to plot
        penalty_attr (str): Edge attribute used to represent penalized weight
        base_attr (str): Original weight attribute for comparison
    """
    # 1. Plot base graph in light gray
    fig, ax = ox.plot_graph(G, show=False, close=False, node_size=0, edge_color="#bbbbbb", edge_linewidth=0.5, bgcolor='white',)

    # 2. Identify penalized edges (where penalized_length > length)
    penalized_edges = []
    for u, v, k, data in G.edges(keys=True, data=True):
        if data.get(penalty_attr, 0) > data.get(base_attr, 0):
            penalized_edges.append((u, v, k))

    # 3. Draw penalized edges in red
    lines = []
    for u, v, k in penalized_edges:
        edge_data = G.edges[u, v, k]
        if 'geometry' in edge_data:
            lines.append(edge_data['geometry'])
        else:
            point_u = (G.nodes[u]['x'], G.nodes[u]['y'])
            point_v = (G.nodes[v]['x'], G.nodes[v]['y'])
            lines.append(LineString([point_u, point_v]))

    if lines:
        #from descartes import PolygonPatch

        #

        lc = LineCollection([list(line.coords) for line in lines], colors='red', linewidths=1.5)
        ax.add_collection(lc)

    plt.title("Graph with Penalized Crossings Near Traffic Lights")
    plt.show()


plot_graph_with_penalties(G_penalized)

# %%
plot_graph_with_penalties(G_penalized)

# %%
for edge_u, edge_v, data in G_penalized.edges(data=True):
#  print(data)
  #if edge.get('highway') is not None:
  #  print(data)
  if data.get('geometry', None) is not None:
    myline = data['geometry']
    break


# %%
#str(myline.centroid)
mydata
#dir(mydata["geometry"].centroid)
#mydata["geometry"].centroid.x

# %%
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from matplotlib.collections import LineCollection

def plot_graph_with_penalties_and_nodes(G, penalty_attr='penalized_length', base_attr='length'):
    """
    Plot the graph with penalized edges in red, crossing nodes in orange, and traffic signals in blue.

    Parameters:
        G (networkx.MultiDiGraph): The graph to plot
        penalty_attr (str): Edge attribute used to represent penalized weight
        base_attr (str): Original weight attribute for comparison
    """
    # 1. Base plot
    fig, ax = ox.plot_graph(G, show=False, close=False, node_size=0, edge_color="#cccccc", edge_linewidth=0.5, bgcolor='white',)

    # 2. Extract positions
    node_x = {n: data['x'] for n, data in G.nodes(data=True)}
    node_y = {n: data['y'] for n, data in G.nodes(data=True)}

    # 3. Identify and plot traffic signals
    signal_nodes = [n for n, data in G.nodes(data=True) if data.get('highway') == 'traffic_signals']
    signal_coords = [(node_x[n], node_y[n]) for n in signal_nodes]
    if signal_coords:
        x, y = zip(*signal_coords)
        ax.scatter(x, y, c='blue', s=20, label='Traffic Signals', zorder=3)

    # 4. Identify and plot penalized crossings
    penalized_nodes = [n for n, data in G.nodes(data=True) if data.get('penalty', 0) > 0]
    penalized_coords = [(node_x[n], node_y[n]) for n in penalized_nodes]
    if penalized_coords:
        x, y = zip(*penalized_coords)
        ax.scatter(x, y, c='orange', s=20, label='Penalized Crossings', zorder=3)

    # 5. Penalized edges
    penalized_edges = []
    for u, v, k, data in G.edges(keys=True, data=True):
        if data.get(penalty_attr, 0) > data.get(base_attr, 0):
            if 'geometry' in data:
                penalized_edges.append(data['geometry'])
            else:
                x1, y1 = G.nodes[u]['x'], G.nodes[u]['y']
                x2, y2 = G.nodes[v]['x'], G.nodes[v]['y']
                penalized_edges.append(LineString([(x1, y1), (x2, y2)]))

    if penalized_edges:
        lc = LineCollection([list(line.coords) for line in penalized_edges], colors='red', linewidths=1.5, label='Penalized Edges')
        ax.add_collection(lc)

    # 6. Final formatting
    ax.legend()
    plt.title("Graph with Penalized Crossings Near Traffic Lights")
    plt.show()

plot_graph_with_penalties_and_nodes(G_penalized)

# %%




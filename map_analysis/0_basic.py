%pip install osmnx matplotlib

----

How far can you walk in 15min? 1km. (avg speed 4km/h)

How far can you bike in 15min? 3km. (avg speed 10-15km/h)

The cycle length is the time between signals. It is 45-120s usually.
Assume this is 60s from any point until a green worst case.
1/15 of the distance = 66 round to 70.

----


import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx

----

network_type='all'
network_type='walk'
network_type='bike'
network_type='drive'


# 2. Define center coordinates for King & Victoria in Kitchener, ON
# Coordinates obtained via geocoding
center_point = (43.4516, -80.4925)  # (latitude, longitude)

# 3. Define search radius in meters
radius = 4000  # 4 km

# 4. Download street network within the specified radius
G = ox.graph_from_point(center_point, dist=radius, network_type='all')

# 5. Plot the map
fig, ax = ox.plot_graph(G, node_size=5, edge_color='#555555', bgcolor='white')

----

def get_graph_within_radius(center_point, search_radius=1000, download_radius=3000, network_type='walk'):
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
    # Download a graph large enough to cover the search radius
    G = ox.graph_from_point(center_point, dist=download_radius, network_type=network_type)
    
    # Find the nearest node to the center point
    center_node = ox.distance.nearest_nodes(G, X=center_point[1], Y=center_point[0])
    
    # Use Dijkstra to find all nodes within search_radius (in meters)
    lengths = nx.single_source_dijkstra_path_length(G, center_node, cutoff=search_radius, weight='length')
    
    # Get the nodes within the radius
    nearby_nodes = set(lengths.keys())
    
    # Extract the subgraph
    subgraph = G.subgraph(nearby_nodes).copy()
    
    return subgraph

----
# usage:
    
# Coordinates of King & Victoria, Kitchener, ON
center = (43.4516, -80.4925)

# Get subgraph within 1km shortest-path distance
G_sub = get_graph_within_radius(center_point=center, search_radius=1000)

# Plot the result
ox.plot_graph(G_sub, node_size=5, edge_color='black', bgcolor='white')

----



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

# Get traffic lights in the subgraph
lights = get_traffic_lights(G_sub)

print(f"Found {len(lights)} traffic lights.")

# Optional: Plot them on the graph
import matplotlib.pyplot as plt

fig, ax = ox.plot_graph(G_sub, node_size=5, node_color='gray', edge_color='lightgray', show=False, close=False)

# Extract coordinates for plotting
x = [G_sub.nodes[n]['x'] for n in lights]
y = [G_sub.nodes[n]['y'] for n in lights]

# Plot traffic lights in red
ax.scatter(x, y, c='red', s=30, label='Traffic Lights')
ax.legend()
plt.show()

----

from geopy.geocoders import Nominatim

def get_intersection_coordinates(intersection_query, city='Kitchener, ON, Canada'):
    """
    Geocodes an intersection using Nominatim and returns (lat, lon) coordinates.
    
    Parameters:
        intersection_query (str): Description of the intersection (e.g., 'King St & Victoria St')
        city (str): Optional city context to help the geocoder
    
    Returns:
        tuple: (latitude, longitude) or None if not found
    """
    geolocator = Nominatim(user_agent="intersection_locator")
    query = f"{intersection_query}, {city}"
    location = geolocator.geocode(query)
    
    if location:
        return (location.latitude, location.longitude)
    else:
        return None
    
    
----
import osmnx as ox
import networkx as nx

def get_graph_within_radius_with_penalty(center_point, 
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


----

# Coordinates of King & Victoria
center = (43.4516, -80.4925)

# Get subgraph with traffic light penalties
G_penalized = get_graph_within_radius_with_penalty(center_point=center, traffic_light_penalty=30)

# Plot it
ox.plot_graph(G_penalized, node_size=5, edge_color='black')


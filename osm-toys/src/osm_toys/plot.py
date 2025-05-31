import matplotlib.pyplot as plt
import osmnx as ox

from matplotlib.collections import LineCollection
from matplotlib.patches import Circle
from shapely.geometry import LineString

# This project:
import osm_toys


def plot_nodes(ax, G, node_type, color, size, alpha, label=None):
    nodes = osm_toys.get_nodes_of_type(G, node_type)
    print(f"Found {len(nodes)} of type {node_type}.")

    # Extract coordinates for plotting
    x = [G.nodes[n]["x"] for n in nodes]
    y = [G.nodes[n]["y"] for n in nodes]

    if label is None:
        label = node_type

    # Plot nodes
    ax.scatter(x, y, c=color, s=size, alpha=alpha, label=label)
    ax.legend()


def plot_point(ax, point, color, size, alpha, label=None):
    # Extract coordinates for plotting
    x = [point[1]]
    y = [point[0]]

    # Plot point
    ax.scatter(x, y, c=color, s=size, alpha=alpha, label=label)
    # ax.legend()


def plot_traffic_signals(ax, G, lights):
    plot_nodes(ax, G, "traffic_signals", color="red", size=40, alpha=0.5, label=None)


def plot_crossings(ax, G, crossings):
    plot_nodes(ax, G, "crossing", color="gold", size=40, alpha=0.5, label=None)


def plot_walkable_debug(G, center, search_radius, filename):
    # Plot it
    fig, ax = ox.plot_graph(
        G,
        node_size=10,
        node_color="blue",
        edge_color="black",
        bgcolor="white",
        show=False,
        close=False,
    )

    # lights = get_traffic_lights(G)
    # print(f"Found {len(lights)} traffic lights.")
    # plot_traffic_lights(ax, G, lights)
    #
    # crossings = get_crossings(G)
    # print(f"Found {len(crossings)} traffic lights.")
    # plot_crossings(ax, G, crossings)

    plot_nodes(ax, G, "traffic_signals", color="red", size=40, alpha=0.5)
    plot_nodes(ax, G, "crossing", color="gold", size=40, alpha=0.5)

    plot_point(ax, center, color="green", size=50, alpha=0.8)

    # plt.show()
    plt.savefig(filename)


def plot_graph_with_penalties_and_nodes(
    G, filename, penalty_attr="penalized_length", base_attr="length"
):
    """
    Plot the graph with penalized edges in red, crossing nodes in orange, and traffic signals in blue.

    Parameters:
        G (networkx.MultiDiGraph): The graph to plot
        penalty_attr (str): Edge attribute used to represent penalized weight
        base_attr (str): Original weight attribute for comparison
    """
    # 1. Base plot
    fig, ax = ox.plot_graph(
        G,
        show=False,
        close=False,
        node_size=0,
        edge_color="#cccccc",
        edge_linewidth=0.5,
        bgcolor="white",
    )

    # 2. Extract positions
    node_x = {n: data["x"] for n, data in G.nodes(data=True)}
    node_y = {n: data["y"] for n, data in G.nodes(data=True)}

    # 3. Identify and plot traffic signals
    signal_nodes = [
        n for n, data in G.nodes(data=True) if data.get("highway") == "traffic_signals"
    ]
    signal_coords = [(node_x[n], node_y[n]) for n in signal_nodes]
    if signal_coords:
        x, y = zip(*signal_coords)
        ax.scatter(x, y, c="blue", s=20, label="Traffic Signals", zorder=3)

    # 4. Identify and plot penalized crossings
    penalized_nodes = [
        n for n, data in G.nodes(data=True) if data.get("penalty", 0) > 0
    ]
    penalized_coords = [(node_x[n], node_y[n]) for n in penalized_nodes]
    if penalized_coords:
        x, y = zip(*penalized_coords)
        ax.scatter(x, y, c="orange", s=20, label="Penalized Crossings", zorder=3)

    # 5. Penalized edges
    penalized_edges = []
    for u, v, k, data in G.edges(keys=True, data=True):
        if data.get(penalty_attr, 0) > data.get(base_attr, 0):
            if "geometry" in data:
                penalized_edges.append(data["geometry"])
            else:
                x1, y1 = G.nodes[u]["x"], G.nodes[u]["y"]
                x2, y2 = G.nodes[v]["x"], G.nodes[v]["y"]
                penalized_edges.append(LineString([(x1, y1), (x2, y2)]))

    if penalized_edges:
        lc = LineCollection(
            [list(line.coords) for line in penalized_edges],
            colors="red",
            linewidths=1.5,
            label="Penalized Edges",
        )
        ax.add_collection(lc)

    # 6. Final formatting
    ax.legend()
    plt.title("Graph with Penalized Crossings Near Traffic Lights")
    # plt.show()
    plt.savefig(filename)


# plot_graph_with_penalties_and_nodes(G_penalized)


# Alernative idea: project a number of points that are radius m away


def plot_radius(ax, center_point, radius):
    """
    Plot a projected graph and overlay a search radius circle.

    Parameters:
        ax
        center_point (tuple): (lat, lon)
        radius (float): radius in meters
    """
    from matplotlib.patches import Circle
    from matplotlib.patches import Ellipse
    from shapely.geometry import Point

    center_geom = Point(center_point[1], center_point[0])  # lon, lat
    center_proj, _ = ox.projection.project_geometry(center_geom, to_crs=G.graph["crs"])
    center_x, center_y = center_proj.xy[0][0], center_proj.xy[1][0]

    meters_per_deg_lat = 111_320  # constant
    meters_per_deg_lon = 40075000 * np.cos(np.radians(center_point[0])) / 360
    width_deg = 2 * radius / meters_per_deg_lon
    height_deg = 2 * radius / meters_per_deg_lat

    # circle = Circle((center_x, center_y), radius, color='green', alpha=0.3, fill=True, lw=2, zorder=4)
    # ax.add_patch(circle)
    circle = Ellipse(
        (center_x, center_y),
        width=width_deg,
        height=height_deg,
        color="green",
        alpha=0.3,
        fill=True,
        lw=2,
        zorder=4,
    )
    ax.add_patch(circle)

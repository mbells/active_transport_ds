import matplotlib.pyplot as plt
import osmnx as ox

# This project:
import osm_toys

# from .graph import calc_reachable_graph_with_penalty


def download_map(filepath):
    G = ox.graph_from_point(center_point, dist=radius, network_type="all")
    ox.save_graphml(G, filepath=filepath)
    return G


def load_dtk():
    return ox.load_graphml(filepath="tests/testdata/Kitchener-dtk.graphml")


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

    osm_toys.plot_nodes(ax, G, "traffic_signals", color="red", size=40, alpha=0.5)
    osm_toys.plot_nodes(ax, G, "crossing", color="gold", size=40, alpha=0.5)

    # plt.show()
    plt.savefig(filename)


from shapely.geometry import LineString
from matplotlib.collections import LineCollection


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

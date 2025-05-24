def get_nodes_of_type(G, node_type):
    """
    Returns a list of node IDs that are in the graph G of a particular type.

    Parameters:
        G (networkx.MultiDiGraph): The OSMnx graph.

    Returns:
        list: Node IDs of traffic lights.
    """
    nodes = [
        node for node, data in G.nodes(data=True) if data.get("highway") == node_type
    ]
    return nodes


def plot_nodes(ax, G, node_type, color, size, alpha, label=None):
    nodes = get_nodes_of_type(G, node_type)
    print(f"Found {len(nodes)} of type {node_type}.")

    # Extract coordinates for plotting
    x = [G.nodes[n]["x"] for n in nodes]
    y = [G.nodes[n]["y"] for n in nodes]

    if label is None:
        label = node_type

    # Plot traffic crossings in red
    ax.scatter(x, y, c=color, s=size, alpha=alpha, label=label)
    ax.legend()


# -------------------


def get_traffic_signals(G):
    """
    Returns a list of node IDs that are traffic signals in the graph G.

    Parameters:
        G (networkx.MultiDiGraph): The OSMnx graph.

    Returns:
        list: Node IDs of traffic signals.
    """
    return get_nodes_of_type(G, "traffic_signals")


def plot_traffic_signals(ax, G, lights):
    plot_nodes(ax, G, "traffic_signals", color="red", size=40, alpha=0.5, label=None)


def get_crossings(G):
    """
    Returns a list of node IDs that are traffic lights in the graph G.

    Parameters:
        G (networkx.MultiDiGraph): The OSMnx graph.

    Returns:
        list: Node IDs of traffic lights.
    """
    return get_nodes_of_type(G, "crossing")


def plot_crossings(ax, G, crossings):
    plot_nodes(ax, G, "crossing", color="gold", size=40, alpha=0.5, label=None)

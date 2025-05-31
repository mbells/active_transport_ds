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


def get_crossings(G):
    """
    Returns a list of node IDs that are traffic lights in the graph G.

    Parameters:
        G (networkx.MultiDiGraph): The OSMnx graph.

    Returns:
        list: Node IDs of traffic lights.
    """
    return get_nodes_of_type(G, "crossing")

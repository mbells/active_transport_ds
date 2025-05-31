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
    return ox.load_graphml(filepath="../data/osm-toys/Kitchener-dtk.graphml")

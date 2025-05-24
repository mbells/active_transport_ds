import osmnx as ox
import pytest

# This project:
import osm_toys as ot

def load_dtk():
    return ox.load_graphml(filepath="../data/osm-toys/Kitchener-dtk.graphml")

def test_filter_graph_within_radius_500():
    center = (43.4516, -80.4925)
    G = load_dtk()
    G_sub = ot.filter_graph_within_radius(G, center_point=center, search_radius=500)
    stats = ox.stats.basic_stats(G_sub, clean_int_tol=15)

    assert stats['edge_length_total'] == pytest.approx(54583.54)
    assert stats['m'] == 2239
    assert stats['n'] == 730
    
#def test_filter_graph_within_radius_1000():
    #G_sub = get_graph_within_radius(G_sub, center_point=center, search_radius=1000)

def test_filter_graph_within_radius_500():
    center = (43.4516, -80.4925)
    G = load_dtk()
    G_sub = ot.filter_graph_within_radius(G, center_point=center, search_radius=500)
    traffic_signals = ot.get_traffic_signals(G_sub)

    assert len(traffic_signals) == 19
    assert 293302284 in traffic_signals

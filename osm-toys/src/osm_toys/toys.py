import matplotlib.pyplot as plt
import osmnx as ox
import re

from shapely.geometry import Polygon

# This project:
import osm_toys


PEDESTRIAN_BUFFER = 1000
CYCLIST_BUFFER = 4000


def download_map(query, data_path, buffer_meters=CYCLIST_BUFFER):
    safename = make_filename_safe(query)

    district = ox.geocode_to_gdf(query)
    district.plot()
    plt.savefig(data_path / f"{safename}.png")
    # district.to_file(data_path / f"{safename}.shp")
    district.to_file(data_path / f"{safename}.geojson", driver="GeoJSON")

    poly = district.geometry.values[0]
    poly = poly.buffer(buffer_meters)
    #poly = poly.unary_union.convex_hull.buffer(buffer_meters)

    G = ox.graph_from_polygon(poly, network_type="all")

    filepath = data_path / f"{safename}.graphml"
    ox.save_graphml(G, filepath=filepath)
    return G


def download_map_circle(center_point, radius, name, data_path):
    G = ox.graph_from_point(center_point, dist=radius, network_type="all")
    # G = ox.graph_from_bbox(bbox, network_type="all", simplify=False, retain_all=True)

    safename = make_filename_safe(name)
    filepath = data_path / f"{safename}.graphml"
    ox.save_graphml(G, filepath=filepath)


def download_waterloo_region():
    # https://www.openstreetmap.org/search?query=waterloo+region&zoom=19&minlon=-80.5235865712166&minlat=43.463405184274315&maxlon=-80.51861375570299&maxlat=43.46511443691805#map=11/43.4786/-80.5292
    bbox = [
        -80.5235865712166,
        43.463405184274315,
        -80.51861375570299,
        43.46511443691805,
    ]  # left, bottom, right, top
    filepath = outputpath / "wateroo-region.graphml"
    G = ox.graph_from_bbox(bbox, network_type="all", simplify=False, retain_all=True)
    ox.save_graphml(G, filepath=filepath)


def load_dtk():
    return ox.load_graphml(filepath="../data/osm-toys/Kitchener-dtk.graphml")


def make_filename_safe(query):
    return re.sub(r"[^a-zA-Z0-9-]+", "-", query)

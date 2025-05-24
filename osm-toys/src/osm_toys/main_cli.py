from pathlib import Path

# This project:
import osm_toys


def main_cli():
    outputpath = Path("output/")
    # Coordinates of King & Victoria
    center = (43.4516, -80.4925)
    search_radius = 333
    G = osm_toys.load_dtk()

    # Get subgraph with traffic light penalties
    G_penalized = osm_toys.calc_reachable_graph_with_penalty(
        G, center_point=center, search_radius=search_radius, traffic_signal_penalty=70
    )
    # Plots:
    osm_toys.plot_walkable_debug(
        G_penalized,
        center,
        search_radius=search_radius,
        filename=outputpath / "King-Vic-walkable-debug.png",
    )
    osm_toys.plot_graph_with_penalties_and_nodes(
        G_penalized, filename=outputpath / "King-Vic-penalties.png"
    )


def download_waterloo_region():
    # https://www.openstreetmap.org/search?query=waterloo+region&zoom=19&minlon=-80.5235865712166&minlat=43.463405184274315&maxlon=-80.51861375570299&maxlat=43.46511443691805#map=11/43.4786/-80.5292
    bbox = [
        -80.5235865712166,
        43.463405184274315,
        -80.51861375570299,
        43.46511443691805,
    ]  # left, bottom, right, top
    G = ox.graph_from_bbox(bbox, network_type="all", simplify=False, retain_all=True)
    ox.save_graphml(G, filepath=filepath)


if __name__ == "__main__":
    main_cli()

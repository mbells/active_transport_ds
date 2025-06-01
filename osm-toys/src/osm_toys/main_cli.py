from pathlib import Path

# This project:
import osm_toys


def main_cli():
    output_path = Path("output/")
    data_path = Path("../data/osm-toys/")
    # Coordinates of City Hall
    # location="Kitchener-city-hall"
    # center = (43.4516, -80.4925)

    # location="King-Gaukel"
    # center=(43.45116514320735, -80.49251978500772)
    """
    location = "King-Victoria"
    center = (43.45281567737296, -80.49833279176819)

    search_radius = 333
    G = osm_toys.load_dtk()

    #plot1(G, location, center)
    plot3(G, location, center)
    """
    # osm_toys.download_map("Kitchener, ON", data_path)
    # osm_toys.download_map("Waterloo, ON", data_path)
    osm_toys.download_map("Cambridge, ON", data_path)


def plot1(G, location, center):
    # Get subgraph with traffic light penalties
    G_penalized = osm_toys.calc_reachable_graph_with_penalty(
        G, center_point=center, search_radius=search_radius, traffic_signal_penalty=70
    )
    # Plots:
    osm_toys.plot_walkable_debug(
        G_penalized,
        center,
        search_radius=search_radius,
    )
    plt.savefig(output_path / f"{location}.walkable-debug.png")

    osm_toys.plot_graph_with_penalties_and_nodes(
        G_penalized,
    )
    plt.savefig(output_path / f"{location}.penalties.png")


def plot3(G, location, center):
    # Get subgraph with traffic light penalties
    Gs_penalized = osm_toys.calc_reachable_graphs_with_penalty(
        G, center_point=center, traffic_signal_penalty=70
    )
    # Plots:
    osm_toys.plot_walkable_debug(
        Gs_penalized,
        center,
        search_radius=search_radius,
    )
    plt.savefig(output_path / f"{location}.3-walkable-debug.png")


if __name__ == "__main__":
    main_cli()

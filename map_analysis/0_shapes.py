# %%

import matplotlib.pyplot as plt
import networkx as nx
import os
import osmnx as ox
import sys

from pathlib import Path

#sys.path.insert(0, f"{os.getcwd()}/../osm-toys/src")

from osm_toys.toys import make_filename_safe, cwd_git_root

os.chdir(cwd_git_root())
DATA_PATH = Path("./output/demo")
DATA_PATH.mkdir(parents=True, exist_ok=True)

# %%
def plot_gdf(query, buffer_meters=4000):
    safename = make_filename_safe(query)

    gdf = ox.geocode_to_gdf(query)
    gdf.to_file(DATA_PATH / f"{safename}.geojson", driver="GeoJSON")

    if gdf.crs is None:
        raise ValueError("Expected geocoded GeoDataFrame to include a CRS")

    # Buffer in a projected CRS so distances are interpreted in meters.
    gdf_projected = gdf.to_crs(gdf.estimate_utm_crs())

    fig, ax = plt.subplots(figsize=(8, 8))

    poly = gdf_projected.geometry.buffer(buffer_meters).to_crs(gdf.crs)
    poly.plot(ax=ax, alpha=0.5)

    gdf.plot(ax=ax)

        
    #plt.show()
    plt.savefig(DATA_PATH / f"{safename}-gdf.png")

plot_gdf("Kitchener, ON, Canada")
plot_gdf("Waterloo, ON, Canada")
plot_gdf("Cambridge, ON, Canada")


# %%
def plot_together(queries, colors):
    safename = "all"
    fig, ax = plt.subplots(figsize=(8, 8))
    for q, c in zip(queries, colors):
        gdf = ox.geocode_to_gdf(q)
        gdf.plot(ax=ax, alpha=0.5, label=q, color=c)

    #plt.show()
    plt.savefig(DATA_PATH / f"{safename}-gdf.png")

queries = ["Kitchener, ON, Canada", "Waterloo, ON, Canada", "Cambridge, ON, Canada"]
colors = ["red", "green", "blue"]
plot_together(queries, colors)

# %%
plot_gdf("Firenze, Toscana, Italia")
# %%
plot_gdf("Florence, Italy")

# %%
plot_gdf("Municipality of Athens, Attica, Greece")
#plot_gdf("Αθήνα, Ελλάδα")
#plot_gdf("Δήμος Αθηναίων")
# %%
plot_gdf("Amsterdam, Netherlands")
plot_gdf("Hoi-An, Vietnam")
# %%
plot_gdf("Hội An Ward, Đà Nẵng, Vietnam")
# %%
plot_gdf("Utrecht, Netherlands")
plot_gdf("Delft, Netherlands")
plot_gdf("Houten, Netherlands")
plot_gdf("London, ON, Canada")
plot_gdf("Houston, Texas, USA")
plot_gdf("Montreal, Quebec, Canada")

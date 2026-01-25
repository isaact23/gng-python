# Layers
# Biome Points
# Biome Compositions
# Hill Points
# Altitudes
# Terrain

from generate_chunk import *
from generate_cluster import *
from generate_job import *
from settings import LAYERS

# Generate C# Burst code for one layer.
def generate_layer(layer_name):
    generate_cluster(layer_name)
    generate_chunk(layer_name)
    generate_job(layer_name)

# Generate C# Burst code for the entire project (all layers).
def generate_code():
    for layer_name in LAYERS:
        generate_layer(layer_name)

if __name__ == "__main__":
    #generate_code()
    generate_layer("biome_points")
    generate_layer("biome_compositions")

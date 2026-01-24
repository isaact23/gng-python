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
def generate_layer(layer):
    generate_cluster(layer)
    generate_chunk(layer)
    generate_job(layer)

# Generate C# Burst code for the entire project (all layers).
def generate_code():
    for layer in LAYERS:
        generate_layer(layer)

if __name__ == "__main__":
    #generate_code()
    generate_layer(LAYERS[0])

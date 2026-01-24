# Layers
# Biome Points
# Biome Compositions
# Hill Points
# Altitudes
# Terrain

from generate_chunk import *
from generate_cluster import *
from generate_job import *

# Any types defined here should be defined manually in a C# file (i.e. enums)
layers = [
    {
        "name": "biome_points",
        "class_prefix": "BiomePoints",
        "chunk_size": 256,
        "dimensions": 2,
        "point_sparsity": 24,
        "point_data": {"type": "BiomeLocalPoint"} # This type must be defined manually.
    },
    {
        "name": "biome_compositions",
        "class_prefix": "BiomeCompositions",
        "chunk_size": 128,
        "dimensions": 2,
        "point_sparsity": 1,
        "dependencies": [
            {
                "name": "biome_points",
                "dependency_range": 64
            }
        ],
        "point_data": {"type": "BiomeComposition"}
    },
    {
        "name": "hill_points",
        "class_prefix": "HillPoints",
        "dimensions": 2,
        "point_sparsity": 24,
        "dependencies": [
            {
                "name": "biome_compositions",
                "dependency_range": 0
            }
        ]
    },
    {
        "name": "altitudes",
        "class_prefix": "Altitudes",
        "dimensions": 2,
        "point_sparsity": 1,
        "dependencies": [
            {
                "name": "hill_points",
                "dependency_range": 16
            }
        ]
    },
    {
        "name": "terrain",
        "class_prefix": "Terrain",
        "dimensions": 3,
        "point_sparsity": 1,
        "dependencies": [
            {
                "name": "altitudes",
                "dependency_range": 0
            }
        ],
        "point_data": {"type": "Block"}
    }
]

# Generate C# Burst code for one layer.
def generate_layer(layer):
    generate_cluster(layer)
    generate_chunk(layer)
    generate_job(layer)

# Generate C# Burst code for the entire project (all layers).
def generate_code():
    for layer in layers:
        generate_layer(layer)

if __name__ == "__main__":
    #generate_code()
    generate_layer(layers[0])

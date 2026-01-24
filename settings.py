CHUNK_WIDTH = 32

# Any types defined here should be defined manually in a C# file (i.e. enums)
LAYERS = [
    {
        "name": "biome_points",
        "class_prefix": "BiomePoints",
        "dimensions": 2,
        "point_sparsity": 24,
        "point_data": "BiomeLocalPoint", # This type must be defined manually.
        "routine": "BiomePointRoutine.cs"
    },
    {
        "name": "biome_compositions",
        "class_prefix": "BiomeCompositions",
        "dimensions": 2,
        "point_sparsity": 1,
        "dependencies": [
            {
                "name": "biome_points",
                "dependency_range": 64
            }
        ],
        "point_data": "BiomeComposition"
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
        ],
        "point_data": "int"
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
        ],
        "point_data": "int"
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
        "point_data": "Block"
    }
]
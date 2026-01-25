CHUNK_WIDTH = 32

# Any types defined here should be defined manually in a C# file (i.e. enums)
LAYERS = {
    "biome_points": {
        "class_prefix": "BiomePoints",
        "dimensions": 2,
        "point_sparsity": 24,
        "point_data": "BiomeLocalPoint", # This type must be defined manually.
        "routine": "BiomePointRoutine.cs"
    },
    "biome_compositions": {
        "class_prefix": "BiomeCompositions",
        "dimensions": 2,
        "point_sparsity": 1,
        "dependencies": {
            "biome_points": {
                "dependency_range": 64
            }    
        },
        "point_data": "BiomeComposition",
        "routine": "BiomeCompositionRoutine.cs"
    },
    "hill_points": {
        "class_prefix": "HillPoints",
        "dimensions": 2,
        "point_sparsity": 24,
        "dependencies": {
            "biome_compositions": {
                "dependency_range": 0
            }    
        },
        "point_data": "int"
    },
    "altitudes": {
        "class_prefix": "Altitudes",
        "dimensions": 2,
        "point_sparsity": 1,
        "dependencies": {
            "hill_points": {
                "dependency_range": 64
            }    
        },
        "point_data": "int"
    },
    "terrain": {
        "class_prefix": "Terrain",
        "dimensions": 3,
        "point_sparsity": 1,
        "dependencies": {
            "biome_compositions": {
                "dependency_range": 0
            },
            "altitudes": {
                "dependency_range": 0
            }
        },
        "point_data": "Block"
    }
}

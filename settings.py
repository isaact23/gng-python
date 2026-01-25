CHUNK_WIDTH = 32

# Any types defined here should be defined manually in a C# file (i.e. enums)
# TODO: Write helper functions to inject prefixes automatically
LAYERS = {
    "biome_points": {
        "camel_prefix": "biomePoints",
        "pascal_prefix": "BiomePoints",
        "const_prefix": "BIOME_POINTS",
        "dimensions": 2,
        "point_sparsity": 24,
        "point_data": "Biome", # This type must be defined manually.
        "routine": "BiomePointRoutine.cs"
    },
    "biome_compositions": {
        "camel_prefix": "biomeCompositions",
        "pascal_prefix": "BiomeCompositions",
        "const_prefix": "BIOME_COMPOSITIONS",
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
        "camel_prefix": "hillPoints",
        "pascal_prefix": "HillPoints",
        "const_prefix": "HILL_POINTS",
        "dimensions": 2,
        "point_sparsity": 24,
        "dependencies": {
            "biome_compositions": {
                "dependency_range": 0
            }    
        },
        "point_data": "int",
        "routine": "HillPointRoutine.cs"
    },
    "altitudes": {
        "camel_prefix": "altitudes",
        "pascal_prefix": "Altitudes",
        "const_prefix": "ALTITUDES",
        "dimensions": 2,
        "point_sparsity": 1,
        "dependencies": {
            "hill_points": {
                "dependency_range": 64
            }    
        },
        "point_data": "int",
        "routine": "AltitudesRoutine.cs"
    },
    "terrain": {
        "camel_prefix": "terrain",
        "pascal_prefix": "Terrain",
        "const_prefix": "TERRAIN",
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
        "point_data": "Block",
        "routine": "TerrainRoutine.cs"
    }
}

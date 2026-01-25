from math import ceil
from code_writer import *
from settings import CHUNK_WIDTH, LAYERS

# Generate the job code that generates a chunk (a portion of the world) for a layer.
def generate_job(layer_name):
    layer = LAYERS[layer_name]
    class_name = layer["pascal_prefix"] + "Job"
    w = CodeWriter(layer, class_name + ".cs")

    # Includes
    w.put("using Unity.Burst;\n")
    w.put("using Unity.Collections;\n")
    w.put("using Unity.Jobs;\n")
    w.put("using Unity.Mathematics;\n")
    w.put("\n")

    # Struct definition
    w.put("[BurstCompile]\n")
    w.put("public struct " + class_name + " : IJob\n")
    w.open_func()

    # Fields
    w.put("public " + layer["pascal_prefix"] + "Chunk chunkData;\n")
    w.put("[ReadOnly] public int chunkX;\n")
    w.put("[ReadOnly] public int chunkY;\n")
    if (layer["dimensions"] == 3):
        w.put("[ReadOnly] public int chunkZ;\n")
    w.put("[ReadOnly] public int seed;\n")
    w.put("\n")

    # Constants
    w.put("private const int CHUNK_WIDTH = " + str(CHUNK_WIDTH) + ";\n")

    # Constant chunk dependency ranges
    dependency_range_consts = {}
    if "dependencies" in layer:
        for dependency in layer["dependencies"]:
            if LAYERS[dependency]["dimensions"] > 2:
                raise NotImplementedError("Three-dimensional dependency detected - this case is not handled yet")

            block_range = layer["dependencies"][dependency]["dependency_range"]
            chunk_range = ceil(block_range / CHUNK_WIDTH)
            dependency_prefix = LAYERS[dependency]["const_prefix"]
            const_name = dependency_prefix + "_CHUNK_RANGE"
            w.put("private const int " + const_name + " = " + str(chunk_range) + ";\n")
            dependency_range_consts[dependency] = {
                "variable": const_name,
                "value": chunk_range
            }
    w.put("\n")

    # Helper methods to access data from previous layer
    if "dependencies" in layer:
        for dependency in layer["dependencies"]:
            # Generate some names
            chunk_name = LAYERS[dependency]["pascal_prefix"] + "Chunk"
            array_name = LAYERS[dependency]["camel_prefix"] + "Chunks"
            point_name = LAYERS[dependency]["point_data"]

            # Helper method adds dependency chunks to this job
            w.put("[BurstCompile]\n")
            w.put("public static void Add" + chunk_name + "(ref " + class_name + " job, " + chunk_name + " chunk, " + "in int2 chunkPos)\n")
            w.open_func()
            w.put("job." + array_name + "[Get" + LAYERS[dependency]["pascal_prefix"] + "Index(chunkPos)] = chunk;\n")
            w.close_func()
            w.put("\n")

            # Helper method gets index of a chunk in the dependency array
            w.put("[BurstCompile]\n")
            w.put("private static int Get" + LAYERS[dependency]["pascal_prefix"] + "Index(in int2 chunkPos)\n")
            w.open_func()
            dep_range = dependency_range_consts[dependency]["value"]
            w.put("return (chunkPos.x + " + str(dep_range) + ") + ((chunkPos.y + " + str(dep_range) + ") * " + str(1 + (dep_range * 2)) + ");\n")
            w.close_func()
            w.put("\n")

            # Helper method fetches relative points from nearby dependency chunks
            w.put("[BurstCompile]\n")
            w.put("private static void Fetch" + LAYERS[dependency]["pascal_prefix"] + "From(ref " + class_name + " job, " +
                "ref NativeList<" + point_name + "> points, in int2 offset)\n")
            w.open_func()
            w.put(chunk_name + " chunk = job." + array_name + "[Get" + LAYERS[dependency]["pascal_prefix"] + "Index(chunkPos)] = chunk;\n")
            w.put("\n")
            w.put("foreach (" + point_name + " point in chunk.points)\n")
            w.open_func()
            w.put("int chunkX = job.chunkX + offset.x;\n")
            w.put("int chunkY = job.chunkY + offset.y;\n")
            w.put("\n")
            w.put(point_name + " newPoint = point;\n")
            w.put("newPoint.localX = point.localX + (chunkX * " + str(CHUNK_WIDTH) + ");\n")
            w.put("newPoint.localY = point.localY + (chunkY * " + str(CHUNK_WIDTH) + ");\n")
            w.put("points.Add(newPoint);\n")
            w.close_func()
            w.close_func()
            w.put("\n")

    # Routine
    w.put("[BurstCompile]\n")
    w.put("public void Execute()\n")
    w.put("{\n")
    w.shift_right()

    # Skip if already generated
    w.put("if (chunkData.isGenerated.Value) return;\n")
    w.put("\n")

    # Fetch points from dependency chunks
    if "dependencies" in layer:
        for dependency in layer["dependencies"]:
            point_name = LAYERS[dependency]["point_data"]
            dep_range = dependency_range_consts[dependency]["value"]

            w.put("NativeList<" + point_name + "> " + LAYERS[dependency]["camel_prefix"] + " = new(100, Allocator.TempJob);\n")
            w.put("for (int x = -" + str(dep_range) + "; x < " + str(dep_range) + "; x++)\n")
            w.open_func()
            w.put("for (int y = -" + str(dep_range) + "; y < " + str(dep_range) + "; y++)\n")
            w.open_func()
            w.put("Fetch" + LAYERS[dependency]["pascal_prefix"] + "From(ref this, ref " + LAYERS[dependency]["camel_prefix"] + ", new int2(x, y));\n")
            w.close_func()
            w.close_func()
            w.put("\n")

    # Load user-provided routine
    w.load_routine(layer["routine"])
    w.put("\n")

    # Dispose of dependency data
    if "dependencies" in layer:
        for dependency in layer["dependencies"]:
            w.put(LAYERS[dependency]["camel_prefix"] + ".Dispose();\n")

    # Finish job
    w.put("chunkData.isGenerated.Value = true;\n")
    w.close_func()
    w.close_func()

    w.close()
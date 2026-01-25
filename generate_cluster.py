from code_writer import *
from settings import CHUNK_WIDTH, LAYERS

# Generate the cluster struct for a layer (stores all data for the entire world).
def generate_cluster(layer_name):
    # Calculate some names
    layer = LAYERS[layer_name]
    class_name = layer["pascal_prefix"] + "Cluster"
    chunk_name = layer["pascal_prefix"] + "Chunk"
    job_name = layer["pascal_prefix"] + "Job"
    vec_type = "int2"
    if (layer["dimensions"] == 3):
        vec_type = "int3"

    w = CodeWriter(layer, class_name + ".cs")

    # Includes
    w.put("using System;\n")
    w.put("using System.Collections.Generic;\n")
    w.put("using Unity.Burst;\n")
    w.put("using Unity.Collections;\n")
    w.put("using Unity.Jobs;\n")
    w.put("using Unity.Mathematics;\n")
    w.put("using UnityEngine;\n")
    w.put("\n")

    # Struct definition
    w.put("[BurstCompile]\n")
    w.put("public struct " + class_name + "\n")
    w.open_func()

    # Fields
    w.put("private NativeHashMap<" + vec_type + ", " + chunk_name + "> chunks;\n")
    w.put("private NativeHashMap<" + vec_type + ", JobHandle> jobs;\n")
    w.put("private int seed;\n")
    w.put("\n")

    # Constants
    w.put("private const int CHUNK_WIDTH = " + str(CHUNK_WIDTH) + ";\n")
    w.put("\n")

    # Initialization routine
    w.put("[BurstCompile]\n")
    w.put("public static void Initialize(int seed, out " + class_name + " cluster)\n")
    w.open_func()
    w.put("cluster = new " + class_name + "\n")
    w.open_func()
    w.put("chunks = new (1000, Allocator.Persistent),\n")
    w.put("jobs = new (1000, Allocator.Persistent),\n")
    w.put("seed = seed\n")
    w.shift_left()
    w.put("};\n")
    w.close_func()

    # Did start generating method
    w.put("[BurstCompile]\n")
    w.put("public static bool DidStartGeneratingChunk(ref " + class_name + " cluster, " + vec_type + " chunkPos)\n")
    w.open_func()
    w.put("return cluster.chunks.ContainsKey(chunkPos);\n")
    w.close_func()

    # Did finish generating method
    w.put("[BurstCompile]\n")
    w.put("public static bool DidFinishGeneratingChunk(ref " + class_name + " cluster, " + vec_type + " chunkPos)\n")
    w.open_func()
    w.put("return cluster.chunks.TryGetValue(chunkPos, out " + chunk_name + " chunk) && chunk.isGenerated;\n")
    w.close_func()

    # Chunk getter method
    w.put("[BurstCompile]\n")
    w.put("public static " + chunk_name + " GetChunk(ref " + class_name + " cluster, " + vec_type + " chunkPos)\n")
    w.open_func()
    w.put("return cluster.chunks[chunkPos];\n");
    w.close_func()

    # Chunk setter method
    w.put("[BurstCompile]\n")
    w.put("public static " + chunk_name + " SetChunk(ref " + class_name + " cluster, " + vec_type + " chunkPos, " + chunk_name + " chunk)\n")
    w.open_func()
    w.put("cluster.chunks[chunkPos] = chunk;\n");
    w.close_func()

    # Chunk generator method
    w.put("[BurstCompile]\n")
    w.put("public static bool GenerateChunk(ref " + class_name + " cluster, " + vec_type + " chunkPos, out JobHandle handle)\n")
    w.open_func()
    w.put("if (" + class_name + ".DidStartGeneratingChunk(ref cluster, chunkPos))\n")
    w.open_func()
    w.put("handle = new JobHandle {};\n")
    w.put("return false;\n")
    w.close_func()

    w.put(chunk_name + ".Initialize(out " + chunk_name + " chunk);\n")
    w.put("cluster.chunks[chunkPos] = chunk;\n")
    w.put(job_name + " job = new " + job_name + "\n")
    w.open_func()
    w.put("chunk = chunk,\n")
    w.put("chunkX = chunkPos.x,\n")
    w.put("chunkY = chunkPos.y,\n")
    if (layer["dimensions"] == 3):
        w.put("chunkZ = chunkPos.z,\n")
    w.put("seed = cluster.seed\n")
    w.close_func()

    w.put("handle = job.Schedule();\n")
    w.put("cluster.jobs[chunkPos] = handle;\n")
    w.put("return true;\n")
    w.close_func()

    # Disposal routine
    w.put("[BurstCompile]\n")
    w.put("public static void Dispose(ref " + class_name + " cluster)\n")
    w.open_func()
    w.put("if (cluster.chunks.Count > 0)\n")
    w.open_func()
    w.put("NativeArray<" + chunk_name + "> chunksToDispose = cluster.chunks.GetValueArray(Allocator.Temp);\n")
    w.put("foreach (" + chunk_name + " chunk in chunksToDispose)\n")
    w.open_func()
    w.put(chunk_name + ".Dispose(chunk);\n")
    w.close_func()
    w.put("chunksToDispose.Dispose();\n")
    w.close_func()
    w.put("cluster.chunks.Dispose();\n")
    w.put("cluster.jobs.Dispose();\n")
    w.close_func()

    w.close_func()
    w.close()
from code_writer import *

# Generate the cluster struct for a layer (stores all data for the entire world).
def generate_cluster(layer):
    # Calculate some names
    class_name = layer["class_prefix"] + "Cluster"
    chunk_name = layer["class_prefix"] + "Chunk"
    job_name = layer["class_prefix"] + "Job"
    vec_type = "int2"
    if (layer["dimensions"] == 3):
        vec_type = "int3"

    w = CodeWriter(layer, class_name + ".cs")

    # Includes
    w.write("using System;\n")
    w.write("using System.Collections.Generic;\n")
    w.write("using Unity.Burst;\n")
    w.write("using Unity.Collections;\n")
    w.write("using Unity.Jobs;\n")
    w.write("using Unity.Mathematics;\n")
    w.write("using UnityEngine;\n")
    w.write("\n")

    # Struct definition
    w.write("[BurstCompile]\n")
    w.write("public struct " + class_name + "\n")
    w.open_func()

    # Fields
    w.write("private NativeHashMap<" + vec_type + ", " + chunk_name + "> chunks;\n")
    w.write("private NativeHashMap<" + vec_type + ", JobHandle> jobs;\n")
    w.write("private int seed;\n")
    w.write("\n")

    # Initialization routine
    w.write("[BurstCompile]\n")
    w.write("public static void Initialize(int seed, out " + class_name + " cluster)\n")
    w.open_func()
    w.write("cluster = new " + class_name + "\n")
    w.open_func()
    w.write("chunks = new (1000, Allocator.Persistent),\n")
    w.write("jobs = new (1000, Allocator.Persistent),\n")
    w.write("seed = seed\n")
    w.shift_left()
    w.write("};\n")
    w.close_func()

    # Did start generating method
    w.write("[BurstCompile]\n")
    w.write("public static bool DidStartGeneratingChunk(ref " + class_name + " cluster, " + vec_type + " chunkPos)\n")
    w.open_func()
    w.write("return cluster.chunks.ContainsKey(chunkPos);\n")
    w.close_func()

    # Did finish generating method
    w.write("[BurstCompile]\n")
    w.write("public static bool DidFinishGeneratingChunk(ref " + class_name + " cluster, " + vec_type + " chunkPos)\n")
    w.open_func()
    w.write("return cluster.chunks.TryGetValue(chunkPos, out " + chunk_name + " chunk) && chunk.isGenerated;\n")
    w.close_func()

    # Chunk getter method
    w.write("[BurstCompile]\n")
    w.write("public static " + chunk_name + " GetChunk(ref " + class_name + " cluster, " + vec_type + " chunkPos)\n")
    w.open_func()
    w.write("return cluster.chunks[chunkPos];\n");
    w.close_func()

    # Chunk setter method
    w.write("[BurstCompile]\n")
    w.write("public static " + chunk_name + " SetChunk(ref " + class_name + " cluster, " + vec_type + " chunkPos, " + chunk_name + " chunk)\n")
    w.open_func()
    w.write("cluster.chunks[chunkPos] = chunk;\n");
    w.close_func()

    # Chunk generator method
    w.write("[BurstCompile]\n")
    w.write("public static bool GenerateChunk(ref " + class_name + " cluster, " + vec_type + " chunkPos, out JobHandle handle)\n")
    w.open_func()
    w.write("if (" + class_name + ".DidStartGeneratingChunk(ref cluster, chunkPos))\n")
    w.open_func()
    w.write("handle = new JobHandle {};\n")
    w.write("return false;\n")
    w.close_func()

    w.write(chunk_name + ".Initialize(out " + chunk_name + " chunk);\n")
    w.write("cluster.chunks[chunkPos] = chunk;\n")
    w.write(job_name + " job = new " + job_name + "\n")
    w.open_func()
    w.write("chunk = chunk,\n")
    w.write("chunkX = chunkPos.x,\n")
    w.write("chunkY = chunkPos.y,\n")
    if (layer["dimensions"] == 3):
        w.write("chunkZ = chunkPos.z,\n")
    w.write("seed = cluster.seed\n")
    w.close_func()

    w.write("handle = job.Schedule();\n")
    w.write("cluster.jobs[chunkPos] = handle;\n")
    w.write("return true;\n")
    w.close_func()

    # Disposal routine
    w.write("[BurstCompile]\n")
    w.write("public static void Dispose(ref " + class_name + " cluster)\n")
    w.open_func()
    w.write("if (cluster.chunks.Count > 0)\n")
    w.open_func()
    w.write("NativeArray<" + chunk_name + "> chunksToDispose = cluster.chunks.GetValueArray(Allocator.Temp);\n")
    w.write("foreach (" + chunk_name + " chunk in chunksToDispose)\n")
    w.open_func()
    w.write(chunk_name + ".Dispose(chunk);\n")
    w.close_func()
    w.write("chunksToDispose.Dispose();\n")
    w.close_func()
    w.write("cluster.chunks.Dispose();\n")
    w.write("cluster.jobs.Dispose();\n")
    w.close_func()

    w.close_func()
    w.close()
from math import ceil
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
    w.put("using Unity.Burst;\n")
    w.put("using Unity.Collections;\n")
    w.put("using Unity.Jobs;\n")
    w.put("using Unity.Mathematics;\n")
    w.put("\n")

    # Struct definition
    w.put("[BurstCompile]\n")
    w.put("public struct " + class_name + "\n")
    w.open_func()

    # Fields
    for dependency in layer["dependencies"]:
        cluster_class = LAYERS[dependency]["pascal_prefix"] + "Cluster"
        cluster_name = LAYERS[dependency]["camel_prefix"] + "Cluster"
        w.put("[ReadOnly] public " + cluster_class + " " + cluster_name + ";\n")

    w.put("private NativeHashMap<" + vec_type + ", " + chunk_name + "> chunks;\n")
    w.put("private NativeHashMap<" + vec_type + ", JobHandle> jobs;\n")
    w.put("private int seed;\n")
    w.put("\n")

    # Constants
    #w.put("private const int CHUNK_WIDTH = " + str(CHUNK_WIDTH) + ";\n")

    # Constant chunk dependency ranges
    # TODO: Remove redundancy between this and generate_job.py
    dependency_range_consts = {}
    if "dependencies" in layer:
        for dependency in layer["dependencies"]:
            block_range = layer["dependencies"][dependency]["dependency_range"]
            chunk_range = ceil(block_range / CHUNK_WIDTH)
            dependency_prefix = LAYERS[dependency]["const_prefix"]
            const_name = dependency_prefix + "_CHUNK_RANGE"
            #w.put("private const int " + const_name + " = " + str(chunk_range) + ";\n")
            dependency_range_consts[dependency] = {
                "variable": const_name,
                "value": chunk_range
            }

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
    w.put("\n")

    w.put("[BurstCompile]\n")
    w.put("public static void Initialize(int seed, in NativeHashMap<" + vec_type + ", " + chunk_name + "> chunks, out " + class_name + " cluster)\n")
    w.open_func()
    w.put("cluster = new " + class_name + "\n")
    w.open_func()
    w.put("chunks = chunks,\n")
    w.put("jobs = new (1000, Allocator.Persistent),\n")
    w.put("seed = seed\n")
    w.shift_left()
    w.put("};\n")
    w.close_func()
    w.put("\n")

    # Did start generating method
    w.put("[BurstCompile]\n")
    w.put("public static bool DidStartGeneratingChunk(ref " + class_name + " cluster, " + vec_type + " chunkPos)\n")
    w.open_func()
    w.put("return cluster.chunks.ContainsKey(chunkPos);\n")
    w.close_func()
    w.put("\n")

    # Did finish generating method
    w.put("[BurstCompile]\n")
    w.put("public static bool DidFinishGeneratingChunk(ref " + class_name + " cluster, " + vec_type + " chunkPos)\n")
    w.open_func()
    w.put("return cluster.chunks.TryGetValue(chunkPos, out " + chunk_name + " chunk) && chunk.isGenerated.Value;\n")
    w.close_func()
    w.put("\n")

    # Chunk getter method
    w.put("[BurstCompile]\n")
    w.put("public static void GetChunk(ref " + class_name + " cluster, in " + vec_type + " chunkPos, out " + chunk_name + " chunk)\n")
    w.open_func()
    w.put("chunk = cluster.chunks[chunkPos];\n")
    w.close_func()
    w.put("\n")

    # Chunk setter method
    w.put("[BurstCompile]\n")
    w.put("public static void SetChunk(ref " + class_name + " cluster, in " + vec_type + " chunkPos, in " + chunk_name + " chunk)\n")
    w.open_func()
    w.put("cluster.chunks[chunkPos] = chunk;\n")
    w.close_func()
    w.put("\n")

    # Point getter method
    w.put("[BurstCompile]\n")
    w.put("public static bool GetPoint(ref " + class_name + " cluster, " + vec_type + " pointPos, out " + layer["point_data"] + " data)\n")
    w.open_func()
    w.put("CoordConvert.GetChunkCoord(pointPos, out " + vec_type + " chunkPos);\n")
    w.put("if (DidFinishGeneratingChunk(ref cluster, chunkPos))\n")
    w.open_func()
    w.put("CoordConvert.GetLocalCoord(pointPos, out " + vec_type + " localPos);\n")
    w.put(chunk_name + " chunk = cluster.chunks[chunkPos];\n")
    w.put("return " + layer["pascal_prefix"] + "Chunk.GetPoint(ref chunk, localPos, out data);\n")
    w.close_func()
    w.put("data = new();\n")
    w.put("return false;\n")
    w.close_func()
    w.put("\n")

    # Point setter method
    w.put("[BurstCompile]\n")
    w.put("public static bool SetPoint(ref " + class_name + " cluster, " + vec_type + " pointPos, in " + layer["point_data"] + " data)\n")
    w.open_func()
    w.put("CoordConvert.GetChunkCoord(pointPos, out " + vec_type + " chunkPos);\n")
    w.put("if (DidFinishGeneratingChunk(ref cluster, chunkPos))\n")
    w.open_func()
    w.put("CoordConvert.GetLocalCoord(pointPos, out " + vec_type + " localPos);\n")
    w.put(chunk_name + " chunk = cluster.chunks[chunkPos];\n")
    w.put(layer["pascal_prefix"] + "Chunk.SetPoint(ref chunk, localPos, data);\n")
    w.put("return true;\n")
    w.close_func()
    w.put("return false;\n")
    w.close_func()
    w.put("\n")

    # Chunk generator method
    w.put("[BurstCompile]\n")
    w.put("public static bool GenerateChunk(ref " + class_name + " cluster, " + vec_type + " chunkPos, out JobHandle handle)\n")
    w.open_func()
    w.put("if (DidStartGeneratingChunk(ref cluster, chunkPos))\n")
    w.open_func()
    w.put("handle = new JobHandle {};\n")
    w.put("return false;\n")
    w.close_func()
    w.put("\n")

    w.put(chunk_name + ".Initialize(out " + chunk_name + " chunk);\n")
    w.put("cluster.chunks[chunkPos] = chunk;\n")
    w.put(job_name + " job = new " + job_name + "\n")
    w.open_func()
    w.put("chunk = chunk,\n")

    # Set up dependency arrays
    for dependency in layer["dependencies"]:
        chunk_name = LAYERS[dependency]["pascal_prefix"] + "Chunk"
        array_name = LAYERS[dependency]["camel_prefix"] + "Chunks"
        chunk_dep_radius = dependency_range_consts[dependency]["value"]
        chunk_dep_diameter = (chunk_dep_radius * 2 + 1) ** 2
        w.put(array_name + " = new NativeArray<" + chunk_name + ">(" + str(chunk_dep_diameter) + ", Allocator.Persistent),\n")
            
    w.put("chunkX = chunkPos.x,\n")
    w.put("chunkY = chunkPos.y,\n")
    if layer["dimensions"] == 3:
        w.put("chunkZ = chunkPos.z,\n")
    w.put("seed = cluster.seed\n")
    
    w.shift_left()
    w.put("};\n")
    w.put("\n")
    
    # Schedule dependency generation and populate dependencies
    for dependency in layer["dependencies"]:
        if LAYERS[dependency]["dimensions"] > 2:
            raise NotImplementedError("Three-dimensional dependency detected - this case is not handled yet")
            
    if len(layer["dependencies"]) > 0:
        w.put("NativeList<JobHandle> handles = new(20, Allocator.Persistent);\n")
    for dependency in layer["dependencies"]:
        dim = LAYERS[dependency]["dimensions"]
        dep_radius = dependency_range_consts[dependency]["value"]
        cluster_class = LAYERS[dependency]["pascal_prefix"] + "Cluster"
        cluster_name = LAYERS[dependency]["camel_prefix"] + "Cluster"
        array_name = LAYERS[dependency]["camel_prefix"] + "Chunks"
        job_class = LAYERS[dependency]["pascal_prefix"] + "Job"

        w.put("for (int x = -" + str(dep_radius) + "; x <= " + str(dep_radius) + "; x++)\n")
        w.open_func()
        w.put("for (int y = -" + str(dep_radius) + "; y <= " + str(dep_radius) + "; y++)\n")
        w.open_func()
        w.put("int globalX = chunkPos.x + x;\n")
        w.put("int globalY = chunkPos.y + y;\n")
        if (dim == 2):
            w.put("int2 globalPos = new int2(globalX, globalY);\n")
        else:
            w.put("int globalZ = chunkPos.z + z;\n")
            w.put("int3 globalPos = new int3(globalX, globalY, globalZ);\n")
        w.put("\n")

        w.put("if (" + cluster_class + ".GenerateChunk(ref cluster." + cluster_name + ", globalPos, out JobHandle innerHandle))\n")
        w.open_func()
        w.put("handles.Add(innerHandle);\n")
        w.close_func()

        #w.put("job." + array_name + "[" + layer["pascal_prefix"] + "Job.Get" + LAYERS[dependency]["pascal_prefix"] + "Index(globalPos)] = \n")
        #w.put("    " + cluster_class + ".GetChunk(ref cluster." + cluster_name + ", globalPos);\n")

        w.put(cluster_class + ".GetChunk(ref cluster." + cluster_name + ", globalPos, out " + LAYERS[dependency]["pascal_prefix"] + "Chunk depChunk);\n")
        if dim == 2:
            w.put("int2 relativePos = new int2(x, y);\n")
        else:
            w.put("int3 relativePos = new int3(x, y, z);\n")
        w.put("job." + array_name + "[" + layer["pascal_prefix"] + "Job.Get" + LAYERS[dependency]["pascal_prefix"] + "Index(relativePos)] = depChunk;\n")

        w.close_func()
        w.close_func()
    
    if len(layer["dependencies"]) == 0:
        w.put("handle = job.Schedule();\n")
    else:
        w.put("JobHandle combinedDeps = JobHandle.CombineDependencies(handles.AsArray());\n")
        w.put("handle = job.Schedule(combinedDeps);\n")
        w.put("handles.Dispose();\n")
    w.put("cluster.jobs[chunkPos] = handle;\n")
    w.put("return true;\n")
    w.close_func()
    w.put("\n")

    # Disposal routine
    w.put("[BurstCompile]\n")
    w.put("public static void Dispose(ref " + class_name + " cluster)\n")
    w.open_func()
    w.put("if (cluster.chunks.Count > 0)\n")
    w.open_func()
    w.put("NativeArray<" + vec_type + "> keys = cluster.chunks.GetKeyArray(Allocator.Temp);\n")
    w.put("foreach (" + vec_type + " key in keys)\n")
    w.open_func()
    w.put(layer["pascal_prefix"] + "Chunk.Dispose(cluster.chunks[key]);\n")
    #w.put("cluster.chunks[key].points.Dispose();\n")
    #w.put("cluster.chunks[key].isGenerated.Dispose();\n")
    w.close_func()
    w.put("keys.Dispose();\n")
    w.close_func()
    w.put("cluster.chunks.Dispose();\n")
    w.put("cluster.jobs.Dispose();\n")
    w.close_func()

    w.close_func()
    w.close()
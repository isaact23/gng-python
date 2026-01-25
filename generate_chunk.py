from code_writer import *
from settings import CHUNK_WIDTH, LAYERS

# Generate the chunk struct for a layer (stores data for a portion of the world).
def generate_chunk(layer_name):
    layer = LAYERS[layer_name]
    class_name = layer["pascal_prefix"] + "Chunk"
    point_name = layer["point_data"]

    w = CodeWriter(layer, class_name + ".cs")

    # Includes
    w.put("using Unity.Burst;\n")
    w.put("using Unity.Collections;\n")
    w.put("\n")

    # Struct definition
    w.put("[BurstCompile]\n")
    w.put("public struct " + class_name + "\n")
    w.open_func()

    # Fields
    # TODO: If sparsity is 1, use an array instead of a hash map
    w.put("public NativeHashMap<int" + str(layer["dimensions"]) + ", " + point_name + "> points;\n")
    w.put("public NativeReference<bool> isGenerated;\n")
    w.put("\n")

    # Constants
    w.put("private const int CHUNK_WIDTH = " + str(CHUNK_WIDTH) + ";\n")
    w.put("\n")

    # Initialization
    w.put("[BurstCompile]\n")
    w.put("public static void Initialize(out " + class_name + " chunk)\n")
    w.open_func()
    w.put("chunk = new " + class_name + "\n")
    w.open_func()
    w.put("points = new(100, Allocator.Persistent),\n")
    w.put("isGenerated = false\n")
    w.shift_left()
    w.put("};\n")
    w.close_func()
    w.put("\n")

    # Disposal routine
    w.put("[BurstCompile]\n")
    w.put("public static void Dispose(in " + class_name + " chunk)\n")
    w.open_func()
    w.put("chunk.points.Dispose();\n")
    w.close_func()

    w.close_func()
    w.close()
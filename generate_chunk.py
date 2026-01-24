from code_writer import *

# Generate the chunk struct for a layer (stores data for a portion of the world).
def generate_chunk(layer):
    class_name = layer["class_prefix"] + "Chunk"
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
    # TODO: If point sparsity is 1, store points in a tightly-packed NativeArray for quick lookup.
    # Otherwise, store points in a list for quick traversal of non-null points.
    w.put("public NativeList<" + point_name + "> points;\n")
    w.put("public NativeReference<bool> isGenerated;\n")
    w.put("\n")

    # Initialization
    w.put("[BurstCompile]\n")
    w.put("public static void Initialize(out " + class_name + " chunk)\n")
    w.open_func()
    w.put("chunk = new " + class_name + "\n")
    w.open_func()
    w.put("points = new(10, Allocator.Persistent),\n")
    w.put("isGenerated = false\n")
    w.shift_left()
    w.put("};\n")
    w.close_func()

    # Disposal routine
    w.put("[BurstCompile]\n")
    w.put("public static void Dispose(in " + class_name + " chunk)\n")
    w.open_func()
    w.put("chunk.points.Dispose();\n")
    w.close_func()

    w.close_func()
    w.close()
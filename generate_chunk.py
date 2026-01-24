from code_writer import *

# Generate the chunk struct for a layer (stores data for a portion of the world).
def generate_chunk(layer):
    class_name = layer["class_prefix"] + "Chunk"
    point_name = layer["point_data"]["type"]

    w = CodeWriter(layer, class_name + ".cs")

    # Includes
    w.write("using Unity.Burst;\n")
    w.write("using Unity.Collections;\n")
    w.write("\n")

    # Struct definition
    w.write("[BurstCompile]\n")
    w.write("public struct " + class_name + "\n")
    w.open_func()

    # Fields
    # If point sparsity is 1, store points in a tightly-packed NativeArray for quick lookup.
    # Otherwise, store points in a list for quick traversal of non-null points.
    w.write("public NativeList<" + point_name + "> points;\n")
    w.write("public bool isGenerated;\n")
    w.write("\n")

    # Initialization
    w.write("[BurstCompile]\n")
    w.write("public static void Initialize(out " + class_name + " chunk)\n")
    w.open_func()
    w.write("chunk = new " + class_name + "\n")
    w.open_func()
    w.write("points = new(10, Allocator.Persistent),\n")
    w.write("isGenerated = false\n")
    w.shift_left()
    w.write("};\n")
    w.close_func()

    # Disposal routine
    w.write("[BurstCompile]\n")
    w.write("public static void Dispose(in " + class_name + " chunk)\n")
    w.open_func()
    w.write("chunk.points.Dispose();\n")
    w.close_func()

    w.close_func()
    w.close()
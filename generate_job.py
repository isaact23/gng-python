from code_writer import *

# Generate the job code that generates a chunk (a portion of the world) for a layer.
def generate_job(layer):
    class_name = layer["class_prefix"] + "Job"
    w = CodeWriter(layer, class_name + ".cs")

    # Includes
    w.write("using Unity.Burst;\n")
    w.write("using Unity.Collections;\n")
    w.write("using Unity.Jobs;\n")
    w.write("using Unity.Mathematics;\n")
    w.write("\n")

    # Struct definition
    w.write("[BurstCompile]\n")
    w.write("public struct " + class_name + " : IJob\n")
    w.open_func()

    # Fields
    w.write("public " + layer["class_prefix"] + "Chunk chunkData;\n")
    w.write("[ReadOnly] public int chunkX;\n")
    w.write("[ReadOnly] public int chunkY;\n")
    if (layer["dimensions"] == 3):
        w.write("[ReadOnly] public int chunkZ;\n")
    w.write("[ReadOnly] public int seed;\n")
    w.write("\n")

    # Routine
    w.write("[BurstCompile]\n")
    w.write("public void Execute()\n")
    w.write("{\n")
    w.shift_right()

    # Skip if already generated
    w.write("if (chunkData.isGenerated) return;\n")
    w.write("\n")

    w.close()
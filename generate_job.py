from code_writer import *
from settings import CHUNK_WIDTH

# Generate the job code that generates a chunk (a portion of the world) for a layer.
def generate_job(layer):
    class_name = layer["class_prefix"] + "Job"
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
    w.put("public " + layer["class_prefix"] + "Chunk chunkData;\n")
    w.put("[ReadOnly] public int chunkX;\n")
    w.put("[ReadOnly] public int chunkY;\n")
    if (layer["dimensions"] == 3):
        w.put("[ReadOnly] public int chunkZ;\n")
    w.put("[ReadOnly] public int seed;\n")
    w.put("\n")

    # Constants
    w.put("private const int CHUNK_WIDTH = " + str(CHUNK_WIDTH) + ";\n")
    w.put("\n")

    # Routine
    w.put("[BurstCompile]\n")
    w.put("public void Execute()\n")
    w.put("{\n")
    w.shift_right()

    # Skip if already generated
    w.put("if (chunkData.isGenerated.Value) return;\n")
    w.put("\n")

    # Load user-provided routine
    w.load_routine(layer["routine"])

    # Finish job
    w.put("chunkData.isGenerated.Value = true;\n")
    w.close_func()
    w.close_func()

    w.close()
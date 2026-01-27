from code_writer import *
from settings import LAYERS

# Generate the code that initializes layers and their dependencies.
def generate_layer_stack():
    w = CodeWriter(None, "LayerStack.cs")

    w.put("using Unity.Burst;\n")
    w.put("\n")
    w.put("[BurstCompile]\n")
    w.put("public struct LayerStack\n")
    w.open_func()

    # Fields
    for layer in LAYERS:
        cluster_class = LAYERS[layer]["pascal_prefix"] + "Cluster"
        w.put("public " + cluster_class + " " + cluster_class + " {get; private set;}\n")
    w.put("\n")

    # Initialization routine
    w.put("[BurstCompile]\n")
    w.put("public static void Initialize(int seed, out LayerStack stack)\n")
    w.open_func()
    for layer in LAYERS:
        cluster_name = LAYERS[layer]["camel_prefix"] + "Cluster"
        cluster_class = LAYERS[layer]["pascal_prefix"] + "Cluster"
        w.put(cluster_class + ".Initialize(seed, out " + cluster_class + " " + cluster_name + ");\n")
        for dep in LAYERS[layer]["dependencies"]:
            dep_name = LAYERS[dep]["camel_prefix"] + "Cluster"
            w.put(cluster_name + "." + dep_name + " = " + dep_name + ";\n")
        w.put("\n")
    
    # Create a new LayerStack object with all layers in it
    w.put("stack = new LayerStack\n")
    w.open_func()
    for layer in LAYERS:
        cluster_name = LAYERS[layer]["camel_prefix"] + "Cluster"
        cluster_class = LAYERS[layer]["pascal_prefix"] + "Cluster"
        w.put(cluster_class + " = " + cluster_name + ",\n")

    w.shift_left()
    w.put("};\n")

    w.close_func()
    w.put("\n")

    # Disposal routine
    w.put("[BurstCompile]\n")
    w.put("public static void Dispose(ref LayerStack stack)\n")
    w.open_func()
    for layer in LAYERS:
        cluster_class = LAYERS[layer]["pascal_prefix"] + "Cluster"
        w.put(cluster_class + ".Dispose(ref stack." + cluster_class + ");\n")
    w.close_func()

    w.close_func()

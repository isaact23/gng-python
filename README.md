# Python Terrain Source Generator

Z is up (optional dimension)

Generates Burst-compilable voxel terrain generator  
Later: Could create independent language that transpiles to C#  
OR use partial structs and add the remaining methods at compile time  
Roslyn source generation (define a separate solution, build it, then import the object into Unity)  

Need to use this pattern:  
```
NativeList<int> nums = new NativeList<int>(1000, Allocator.TempJob);

// The parallel writer shares the original list's AtomicSafetyHandle.
var job = new MyParallelJob {NumsWriter = nums.AsParallelWriter()};
```
/* Partial routine - injected into job script by source generator */

// Get the local positions of biome compositions relative to this chunk
NativeArray<int2> biomeCompPositions = biomeCompositions.GetKeyArray(Allocator.Temp);

// Iterate through all biome compositions, choosing a few to be hill points
foreach (int2 pos in biomeCompPositions)
{
    BiomeComposition comp = biomeCompositions[pos];
    BiomeComposition.GetHillGeneratorSettings(ref comp, out HillGeneratorSettings settings);
    // TODO: Implement getting hill generator settings
}

biomeCompPositions.Dispose();

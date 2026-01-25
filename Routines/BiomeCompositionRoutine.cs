/* Partial routine - injected into job script by source generator */

// Calculate biome compositions for all tiles in the biome chunk
for (int localX = 0; localX < ClusterChunkSettings.UTILITY_CHUNK_WIDTH; localX++)
{
    for (int localZ = 0; localZ < ClusterChunkSettings.UTILITY_CHUNK_WIDTH; localZ++)
    {
        BiomeComposition comp = new BiomeComposition
        {
            biomeCount = 0
        };
        foreach (BiomeLocalPoint biomePoint in biomePoints)
        {
            float distSquared = math.distancesq(new int2(localX, localZ), new int2(biomePoint.localX, biomePoint.localZ));
            if (distSquared > ClusterChunkSettings.BIOME_POINT_INFLUENCE_RADIUS * ClusterChunkSettings.BIOME_POINT_INFLUENCE_RADIUS)
            {
                continue;
            }

            // Influence is the reciprocal square root of squared distance,
            // which is the reciprocal of the distance.
            float influence = math.rsqrt(distSquared);

            BiomeComposition.AddBiome(ref comp, biomePoint.biome, influence);
        }
        BiomeComposition.Normalize(ref comp);
        BiomeCompositionChunk.SetComposition(ref biomeCompChunk, localX, localZ, comp);
    }
}

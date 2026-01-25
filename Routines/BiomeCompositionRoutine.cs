/* Partial routine - injected into job script by source generator */

NativeArray<int2> biomePointPositions = biomePoints.GetKeyArray(Allocator.Temp);

// Calculate biome compositions for all tiles in the biome chunk
for (int localX = 0; localX < CHUNK_WIDTH; localX++)
{
    for (int localY = 0; localY < CHUNK_WIDTH; localY++)
    {
        BiomeComposition comp = new BiomeComposition
        {
            biomeCount = 0
        };
        foreach (int2 biomePointPos in biomePointPositions)
        {
            float distSquared = math.distancesq(new int2(localX, localY), biomePointPos);
            if (distSquared > ClusterChunkSettings.BIOME_POINT_INFLUENCE_RADIUS * ClusterChunkSettings.BIOME_POINT_INFLUENCE_RADIUS)
            {
                continue;
            }

            // Influence is the reciprocal square root of squared distance,
            // which is the reciprocal of the distance.
            float influence = math.rsqrt(distSquared);

            Biome biome = biomePoints[biomePointPos];
            BiomeComposition.AddBiome(ref comp, biome, influence);
        }
        BiomeComposition.Normalize(ref comp);
        BiomeCompositionChunk.SetComposition(ref chunk, localX, localY, comp);
    }
}

biomePointPositions.Dispose();

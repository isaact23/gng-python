/* Partial routine - injected into job script by source generator */

// Store LOCAL coordinates of points
NativeList<int2> pointPositions = new(ClusterChunkSettings.BIOME_POINTS_PER_CHUNK, Allocator.Temp);

for (int i = 0; i < ClusterChunkSettings.BIOME_POINTS_PER_CHUNK; i++)
{
    // Get random x/z value
    int randX = Hasher.Hash(seed, chunkX, chunkY, i);
    int randY = Hasher.Hash(seed, chunkX, chunkY, i + 1);
    randX = math.abs(randX);
    randY = math.abs(randY);
    randX %= CHUNK_WIDTH - (ClusterChunkSettings.MIN_DISTANCE_BETWEEN_BIOMES * 2);
    randY %= CHUNK_WIDTH - (ClusterChunkSettings.MIN_DISTANCE_BETWEEN_BIOMES * 2);
    randX += ClusterChunkSettings.MIN_DISTANCE_BETWEEN_BIOMES;
    randY += ClusterChunkSettings.MIN_DISTANCE_BETWEEN_BIOMES;

    // Make sure x/z value is far enough away from other points
    bool isValidSpot = true;
    foreach (int2 pos in pointPositions)
    {
        int dist = math.abs(pos.x - randX) + math.abs(pos.y - randY);
        if (dist < ClusterChunkSettings.MIN_DISTANCE_BETWEEN_BIOMES)
        {
            isValidSpot = false;
            break;
        }
    }
    // If the BiomePoint is valid, append it to the chunk.
    if (isValidSpot)
    {
        float absoluteX = (chunkX * CHUNK_WIDTH) + randX;
        float absoluteY = (chunkY * CHUNK_WIDTH) + randY;

        float altitude = Altitude.Get(seed, absoluteX, absoluteY);
        float moisture = Moisture.Get(seed, absoluteX, absoluteY);
        float temperature = Temperature.Get(seed, absoluteX, absoluteY);

        int biome = BiomeChooser.Choose(altitude, moisture, temperature);

        int2 pos = new int2(randX, randY);
        chunk.points.Add(pos, biome);
        pointPositions.Add(pos);
    }
}

pointPositions.Dispose();

using UnityEngine;
using Unity.Burst;
using Unity.Collections;

[BurstCompile]
public unsafe struct BiomeComposition
{
    public const int MAX_BIOMES = 5;

    public int biomeCount;
    public fixed int biomes[MAX_BIOMES];
    public fixed float biomeInfluences[MAX_BIOMES];

    [BurstCompile]
    public static void Create(out BiomeComposition biomeComp)
    {
        biomeComp = new BiomeComposition
        {
            biomeCount = 0
        };
    }

    [BurstCompile]
    // Get the top biome from this biome composition.
    public static int GetTopBiome(ref BiomeComposition comp)
    {
        if (comp.biomeCount == 0)
        {
            return Biome.Grassland;
        }

        return comp.biomes[0];
    }

    [BurstCompile]
    // Add to a biome's influence. If the biome is not in this BiomeComposition, add it.
    public static void AddBiome(ref BiomeComposition comp, int biome, float influence)
    {
        // Try to find the biome
        int i;
        for (i = 0; i < comp.biomeCount; i++)
        {
            if (comp.biomes[i] == biome) break;
        }

        // Biome not found - add it, maintaining descending influence order
        if (i == comp.biomeCount)
        {
            // Find the first biome with less influence
            for (i = 0; i < comp.biomeCount; i++)
            {
                if (comp.biomeInfluences[i] < influence) break;
            }

            // If all biomes have higher influence and we're out of space, exit.
            if (i == MAX_BIOMES) return;

            // Remember index to insert element
            int insertIndex = i;

            // Shift biomes down
            for (i = comp.biomeCount; i > insertIndex; i--)
            {
                // Don't overrun the array
                if (i >= MAX_BIOMES) continue;

                comp.biomes[i] = comp.biomes[i - 1];
                comp.biomeInfluences[i] = comp.biomeInfluences[i - 1];
            }

            // Insert the new biome
            comp.biomes[i] = biome;
            comp.biomeInfluences[i] = influence;

            // Increment biome counter capped at MAX_BIOMES.
            comp.biomeCount++;
            if (comp.biomeCount >= MAX_BIOMES)
            {
                comp.biomeCount = MAX_BIOMES;
            }
            else
            {
                // BiomeCount was incremented. Zero out the next NativeArray element.
                comp.biomeInfluences[comp.biomeCount] = 0f;
            }
        }

        // If the biome already exists, add to its influence and shift it up in the list.
        else
        {
            float newInfluence = comp.biomeInfluences[i] + influence;
            for (; i > 0; i--)
            {
                if (comp.biomeInfluences[i - 1] > newInfluence) break;

                comp.biomes[i] = comp.biomes[i - 1];
                comp.biomeInfluences[i] = comp.biomeInfluences[i - 1];
            }

            comp.biomes[i] = biome;
            comp.biomeInfluences[i] = newInfluence;
        }
    }

    [BurstCompile]
    // Normalize the BiomeComposition so the influence percentages add up to 100%.
    public static void Normalize(ref BiomeComposition comp)
    {
        // If the BiomeComposition is empty, make it 100% grassland
        if (comp.biomeCount == 0)
        {
            comp.biomeCount = 1;
            comp.biomes[0] = Biome.Grassland;
            comp.biomeInfluences[0] = 1;
            return;
        }

        // Get the total influence of all biomes
        float totalInf = 0f;
        for (int i = 0; i < comp.biomeCount; i++)
        {
            totalInf += comp.biomeInfluences[i];
        }

        // If the total influence is small, only use the first biome.
        if (totalInf < 0.001f)
        {
            comp.biomeCount = 1;
            comp.biomeInfluences[0] = 1;
            return;
        }

        // Normalize so all influences add up to 1.
        for (int i = 0; i < comp.biomeCount; i++)
        {
            comp.biomeInfluences[i] /= totalInf;
        }
    }

    [BurstCompile]
    // Reduce the number of biomes and normalize influences.
    public static void Truncate(ref BiomeComposition comp, int biomeCount)
    {
        comp.biomeCount = biomeCount;
        Normalize(ref comp);
    }

    public static void Print(ref BiomeComposition comp)
    {
        Debug.Log("Biome Composition - " + comp.biomeCount + " biomes");
        for (int i = 0; i < comp.biomeCount; i++)
        {
            Debug.Log("Biome " + i + ": " + comp.biomes[i].ToString() + " " + comp.biomeInfluences[i]);
        }
    }

    [BurstCompile]
    public static void Dispose(ref BiomeComposition comp)
    {
        //comp.biomes.Dispose();
        //comp.biomeInfluences.Dispose();
    }
}

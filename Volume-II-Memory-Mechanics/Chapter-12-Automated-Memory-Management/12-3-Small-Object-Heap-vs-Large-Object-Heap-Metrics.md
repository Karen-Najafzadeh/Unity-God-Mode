# Small Object Heap vs Large Object Heap Metrics

---

#### 1. Introduction and Core Architectural Concept

We have previously established that the game engine divides the computer's memory into structured rooms. In our exploration of the Generational GC Model, we learned that objects are organized based on their *age* or *lifetime bands* (Generation 0, 1, and 2). However, age is not the only metric the engine uses to sort objects. The engine also look at their **physical size**.

Inside the Heap warehouse floor, the engine maintains two entirely separate runtime zones governed by completely different mechanical physics and rules:

* **The Small Object Heap (SOH):** This is the default zone where almost all standard game objects reside. It houses things like localized vectors, short structural lists, strings, and individual enemy data instances.
* **The Large Object Heap (LOH):** This is a specialized vault reserved exclusively for giant data payloads. In the .NET / Mono runtime environment utilized by engines like Unity, an object is classified as a "Large Object" the exact microsecond its single, unified size reaches or exceeds **85,000 bytes** (approximately 83 Kilobytes).

If an object meets this size threshold, it completely bypasses the generational pipeline we discussed before. It is not placed into the Generation 0 nursery; instead, it is manifested directly inside the Large Object Heap vault as an adult object.

---

#### 2. The Computer Science Lore: The Cost of Heavy Lifting

To understand why computer scientists separated objects by size, we have to look at how memory is physically rearranged during a cleanup pass.

When the automated janitor removes dead items from the Small Object Heap (SOH), the remaining live objects are left scattered across the floor, leaving irregular empty spaces between them. To maximize storage, the SOH janitor executes an operation called **Compaction**. The janitor literally slides all the remaining live objects across the floor, packing them tightly against one another to form one continuous block of clean, unfragmented space.

Moving a 24-byte or 64-byte object across memory is practically instantaneous. But imagine if the janitor had to slide a massive, multi-megabyte array containing all the vertices of an entire mountain mesh or an ultra-high-definition texture buffer. Moving millions of bytes of continuous data from one physical RAM address to another requires massive CPU effort. The computer would spend all its time copying bytes back and forth, grinding your game's frame rate down to zero.

The lore of the LOH is a story of optimization via isolation: computer scientists decided that **large objects are too heavy to move**. Therefore, the automated janitor agrees never to rearrange them. They are dropped into their own zone and left exactly where they land until they die.

---

#### 3. The Original Problem: The Swiss Cheese Phenomenon (Memory Fragmentation)

While leaving large objects in one fixed place avoids the cost of copying heavy data blocks, it introduces a severe structural flaw called **Memory Fragmentation**.

Imagine the Large Object Heap floor as a long parking lot.

1. At the start of your game, three massive 100KB data arrays (Array A, Array B, and Array C) are allocated right next to each other. They occupy 300KB of continuous space.
2. An hour later, Array B is no longer needed and is successfully deleted by the janitor. The parking space where Array B sat is now empty, leaving a 100KB gap between Array A and Array C.
3. Your game script now attempts to load a brand new, ultra-detailed 150KB audio track buffer into memory.

The engine looks at the LOH floor. It technically has 100KB of free space where Array B used to be, plus more free space at the very end of the parking lot. But because the janitor is forbidden from sliding Array C downward to merge the free space, the 100KB gap is too small to fit the new 150KB audio track. The engine cannot split the audio track across two separate gaps—it must reside in one single, continuous block of bytes.

As this cycle repeats thousands of times, the LOH floor becomes full of tiny, unusable gaps. The heap begins to resemble a block of Swiss cheese. Even though the computer might have 500 Megabytes of total free space scattered across these tiny gaps, if a script requests a single continuous block of 2 Megabytes and no single gap is big enough, the application will instantly crash with an **OutOfMemoryException**.

---

#### 4. How it Solves the Problem: Architectural Boundaries and Persistent Pools

To prevent the LOH from fragmenting and crashing your game, developers cannot rely on the Garbage Collector to clean up after them. Because the engine will not compact the LOH, the developer must design architecture that ensures large objects are either **immortal** (allocated once at startup and never destroyed) or **pre-segmented**.

By closely monitoring LOH metrics, developers ensure that large memory chunks are recycled manually via object pools, or broken down into collections of smaller objects that fit safely inside the self-compacting Small Object Heap.

---

#### 5. Comprehensive Code Examples

Let’s analyze a script that destroys game performance by continuously generating LOH trash versus an optimized framework that keeps the LOH perfectly stable.

##### ❌ The LOH Demolisher (Continuous Fragmentation Allocator)

This script simulates a procedural world generator that updates map data dynamically. Every time the player crosses a boundary, it allocates a giant array to calculate new terrain coordinates, immediately causing LOH fragmentation.

```csharp
using UnityEngine;

public class LOHDemolisher : MonoBehaviour
{
    // A simple structural class to hold data values
    private class TerrainChunkData
    {
        // An array of 22,000 floats. 
        // Since each float occupies 4 bytes of memory, 
        // 22,000 * 4 = 88,000 bytes! This instantly crosses the 85,000-byte LOH threshold.
        public float[] heightMap = new float[22000];
    }

    void Update()
    {
        // Triggering this heavy allocation frequently during gameplay
        if (Input.GetKeyDown(KeyCode.Space))
        {
            GenerateProceduralTerrain();
        }
    }

    void GenerateProceduralTerrain()
    {
        // ❌ PITFALL: Instantiating an 88,000-byte object directly onto the LOH floor.
        TerrainChunkData temporaryChunk = new TerrainChunkData();
        
        // Perform localized calculations
        for (int i = 0; i < temporaryChunk.heightMap.Length; i++)
        {
            temporaryChunk.heightMap[i] = Random.value;
        }

        SendToRenderEngine(temporaryChunk);

        // ❌ PITFALL: The variable goes out of scope here. 
        // This massive 88KB block is abandoned, creating a fixed, unmovable gap in the LOH.
    }

    void SendToRenderEngine(TerrainChunkData data)
    {
        // Simulation of pass-through logic...
    }
}

```

* **Behind the Scenes Mechanistic Failure:** Because `heightMap` is exactly 88,000 bytes, the runtime completely ignores Generation 0 and places it straight into the LOH. The moment `GenerateProceduralTerrain` finishes executing, that 88,000-byte block becomes garbage. Because the janitor cannot move objects in the LOH to close up the space, pressing the spacebar repeatedly quickly turns your RAM into unmanageable Swiss cheese, leading to an inevitable system crash.

##### ━━━━

##### The LOH Sentinel (Persistent Vault Pre-Allocation)

To resolve this issue completely, we implement an architectural pattern that preallocates a single, permanent storage matrix on startup. Instead of creating and abandoning large arrays, we repeatedly write over the exact same memory addresses.

```csharp
using UnityEngine;

public class LOHSentinel : MonoBehaviour
{
    //  OPTIMIZATION: Pre-allocating a single, permanent buffer array at game initialization.
    // This object enters the LOH once when the game loads and stays fixed in place forever.
    private float[] persistentHeightMapBuffer = new float[22000];

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            GenerateOptimizedTerrain();
        }
    }

    void GenerateOptimizedTerrain()
    {
        //  ZERO-ALLOCATION ADVANTAGE: We do not use the 'new' keyword.
        // We reuse the exact same physical memory footprint already allocated on the LOH.
        int totalElements = persistentHeightMapBuffer.Length;
        
        for (int i = 0; i < totalElements; i++)
        {
            // Overwriting existing data slots in place
            persistentHeightMapBuffer[i] = Random.value;
        }

        SendToOptimizedRenderEngine(persistentHeightMapBuffer);
        
        // When this method ends, zero bytes of garbage are generated. 
        // The LOH remains completely pristine, with no gaps created.
    }

    void SendToOptimizedRenderEngine(float[] dataBuffer)
    {
        // Process data directly out of the persistent buffer safely
    }
}

```

### **Summary of the Architectural Shift:**

By shifting from transient, mid-game large allocations to a persistent, pre-allocated buffer system, your code eliminates Large Object Heap fragmentation. The heavy 88,000-byte array is created exactly once at startup, securing its spot in the parking lot and never leaving. During gameplay, data is updated inside those exact same memory addresses. As a result, no empty gaps are left behind, the automated janitor never has to inspect the LOH vault, and your game runs flawlessly with zero risk of an unexpected out-of-memory crash.


### [Next: Incremental GC Pipelines Execution Pauses](./12-4-Incremental-GC-Pipelines-Execution-Pauses.md)
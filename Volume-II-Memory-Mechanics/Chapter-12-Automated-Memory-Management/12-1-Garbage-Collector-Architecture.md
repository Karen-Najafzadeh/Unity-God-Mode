# Garbage Collector Architecture

---

#### 1. Introduction and Architectural Context

When engineering video games in Unity using C#, data is divided across two primary operational zones within your computer's RAM: **The Stack** and **The Heap**.

* **The Stack (The Local Workbench):** Imagine this as a hyper-fast, highly organized physical workbench right next to the CPU. When a localized method or function executes, a temporary workspace is allocated instantly, values are used, and the moment the method completes, the workbench is entirely wiped clean automatically with zero tracking overhead.


* **The Heap (The Massive Factory Warehouse):** When you create dynamic objects that need to persist across multiple frames—such as a spawning enemy entity, a player status class, or a complex array of weapons—the localized Stack workbench isn't enough. These objects are sent out to a massive, sprawling storage warehouse called the Heap.



Because the warehouse floor is infinitely more complex than a small, neat workbench, managing its space requires a highly methodical strategy. This is where the engine's automated infrastructure comes into play.

---

#### 2. The Computer Science Lore: The Rise of the Automatic Janitor


In the older, tribal eras of low-level software engineering (such as with raw C or traditional C++), developers were given total, unregulated, and dangerous control over the warehouse floor. If a system architect wanted to spawn an object, they had to manually type instructions to allocate a physical chunk of memory. Crucially, when that object fulfilled its purpose (for example, a projectile hit an obstacle and vanished), the programmer was explicitly responsible for writing the code to dismantle that object and manually hand the memory space back to the hardware.

If a programmer forgot to write the clean-up code for even a tiny, single-byte structure, that memory stayed permanently blocked out on the warehouse floor forever. As the code looped millions of times during gameplay, these abandoned blocks would continuously accumulate. This catastrophic phenomenon is known as a **Memory Leak**. If a game leaked memory continuously, it would eventually starve the computer of its available RAM, forcing the entire operating system to violently crash the application.

To relieve engineers of this manual tracking burden, computer scientists engineered a brilliant piece of automated middleware: **The Garbage Collector (GC)**. The GC acts as an automated, background warehouse janitor. Instead of relying on the developer to manually clean the floors, the automated janitor periodically wakes up, walks across the warehouse, calculates which objects are genuinely abandoned, and purges them from the memory map safely.

---

#### 3. The Original Problem: Finding the "Ghost" Objects

The core mechanical challenge for an automated janitor is that **it cannot read your mind**. A machine does not inherently understand the creative intent of your gameplay loop.

If the janitor accidentally sweeps up an object that a script is still actively trying to read or write to on the next frame, the hardware will try to access a pointer leading to empty space. This produces an immediate, fatal memory violation, resulting in an instantaneous runtime crash. Therefore, the system needs an unyielding, mathematically foolproof strategy to differentiate a live, connected object from an abandoned "ghost" object floating on the floor.

---

#### 4. How it Solves the Problem: The Root Tracking System 

The Garbage Collector solves this existential verification crisis through an architectural pattern called **Mark and Sweep**.

To trace connections without guessing, the runtime maps out a series of definitive anchors known as **GC Roots**. Think of these roots as iron anchors secured to your ultra-fast workbench (the Stack) or deep within static global systems. Tied to these anchors are strong structural "strings" (memory references) that stretch out onto the warehouse floor (the Heap), tying into objects.

When a cleanup pass is initiated, the automated janitor executes a strict, two-phase operation:

1. **The Mark Phase:** The janitor starts at the **GC Roots** and walks down every single connected string. Every object the janitor successfully touches gets a metaphorical "bright green sticker" slapped onto it, marking it as **Alive**. If Object A has a sticker and holds a reference string pointing to Object B, the janitor follows that secondary string and marks Object B as well.


2. **The Sweep Phase:** Once all reference paths have been explored, the janitor walks linearly across the entire physical warehouse floor. If the janitor encounters an object that **does not** possess a green sticker, it proves the object is entirely disconnected from any active root system. It is a ghost object. The janitor safely breaks down its structures, clears the location, and updates its internal registry to show that this specific address space is free to accept new allocations.



---


#### 6. How does it work?

previously, we've introduced The Swiss-Cheese Effect (Memory Fragmentation) in chapter 10 when we talked about [Heap Memory Architecture Fragmentation Hazards](/Volume-II-Memory-Mechanics/Chapter-10-Virtual-Machine-and-Type/Heap-Memory-Architecture-Fragmentation-Hazards.md)


##### The CS Lore: The Tetris Janitor (Compaction)
In the early days of manual memory management (like C++), the computer was like a landlord who let tenants (data) move into an apartment building. When a tenant moved out, the room stayed empty. If the landlord wasn't careful, you’d end up with a building where every other room was empty, but because they were scattered, you couldn't move a large family (a large data array) into the building even if you had 50 empty rooms in total.

To solve this, computer scientists gave the **Garbage Collector (GC)** a second job. He isn't just a janitor who throws away trash; he is also a **Tetris Master**. This process is called **Compaction**.

---

##### 1. The Original Problem: The "Swiss Cheese" Warehouse
When your game runs, it constantly asks the **Heap** (the massive warehouse) for space.
*   You spawn a 4-byte integer.
*   You spawn a 16-byte struct.
*   You spawn an 8-byte small string.

If you then delete the objects in between, you are left with "holes." This is called **Memory Fragmentation**. 
The problem is the **Out of Memory Paradox**: Your Profiler might say you have 100MB of free RAM, but if that 100MB is split into a million tiny 1-byte holes, you can't even store a 2-byte piece of data! The engine will crash with an `OutOfMemoryException` despite having plenty of "total" free space.

---

##### 2. The Solution: The Small Object Heap (SOH) Mechanics

> Don't panic if you don't understand SOH and LOH, they are explained in detail in [article 12-3](./12-3-Small-Object-Heap-vs-Large-Object-Heap-Metrics.md)

For the small bytes (4, 16, and 8 bytes), these live in the **Small Object Heap (SOH)**. Here, the GC performs a **Mark-Sweep-Compact** routine:

1.  **Mark:** It puts "green stickers" on the 4, 16, and 8-byte blocks because your code is still using them.
2.  **Sweep:** It identifies the 4-byte and 1-byte holes as "dead air".
3.  **Compact:** This is exactly what you guessed! The CPU physically copies the bits of the 16-byte and 8-byte blocks and "slides" them across the RAM so they sit right next to the 4-byte block.

**The Result:**
*   **Before:** `[[4B][4B hole][16B][1B hole][8B]]` (Total size: 33 bytes)
*   **After:** `[[4B][16B][8B][5B Free Space]]` (Total size: 28 bytes of data + 5 bytes of usable, continuous "parking space").

---

##### 3. The "Heavy Cargo" Exception: The Large Object Heap (LOH)

> Don't panic if you don't understand SOH and LOH, they are explained in detail in [article 12-3](./12-3-Small-Object-Heap-vs-Large-Object-Heap-Metrics.md)

Now, here is the secret that separates a novice from a "God Mode" engineer. If those numbers were much larger—specifically **85,000 bytes or more** the GC will not do the compaction.

**The Lore of the Heavy Cargo:** 
Imagine trying to slide a coffee mug (4 bytes) across a table. It's instant. Now imagine trying to slide a 50-story skyscraper (a 1MB vertex array) across a city block.
Moving massive amounts of data is incredibly taxing for the CPU. If the GC tried to "compact" (slide) large objects every time it cleaned the warehouse, your game would freeze for several seconds.

**The Rule:** 
The **Large Object Heap (LOH)** is **never compacted**. If you have a "hole" in the LOH, it stays there forever like a permanent "Swiss cheese" gap until another large object of the *exact same size or smaller* fits into that specific hole.

---

##### 4. Code Simulation: Visualizing the "Holes"
While we can't see the physical RAM addresses easily in high-level C#, we can simulate the "Fragmented" vs. "Pooled" mindset that avoids this problem:

```csharp
// ❌ THE FRAGMENTER: Creating holes in the warehouse
void CreateHoles() {
    // 1. Allocate three items
    byte[] smallA = new byte;   // [4 Byte]
    byte[] smallB = new byte;  // [16 Byte]
    byte[] smallC = new byte;   // [8 Byte]

    // 2. The middle items are "lost" (no one points to them)
    // This creates "holes" that the GC will eventually have to slide/compact.
    smallB = null; 
}

// ✅ THE ARCHITECT: Zero-Allocation (No holes created)
// We pre-allocate a continuous block once, and never move it.
byte[] persistentBuffer = new byte; 

void ProcessData() {
    // Instead of creating new arrays (and holes), we write 
    // directly into our pre-existing "parking lot."
    WriteToBuffer(persistentBuffer, 0, 4);   // Use first 4 bytes
    WriteToBuffer(persistentBuffer, 4, 16);  // Use next 16 bytes
    // No GC Janitor needed! No sliding required.
}
```

##### Summary:
If your objects are tiny (4, 16, 8 bytes), the Unity/C# GC **will** slide them together, exactly as we illustrated, to turn those scattered holes into one solid block of "free space" at the end of the line. This keeps your "Workbench" (the Stack) and your "Warehouse" (the Heap) organized and ready for the next big allocation.


#### 5. How Often is a GC Pass Initiated?

The short answer is: **The Garbage Collector does not run on a clock or a calendar; it runs on a budget.** It does *not* trigger every frame or every second by default. Instead, it triggers **when the Heap runs out of space to accommodate a new allocation request.**

To understand this under modern engine parameters, let's look at how the automated janitor schedules their clean-up rounds:

1. **The Allocation Trigger (The Classic Threshold):** When Unity launches your game, the virtual machine (Mono or IL2CPP runtime) claims a chunk of system RAM for its Heap warehouse (e.g., 16 MB). Every time you call `new`, a slice of that 16 MB is filled. If your game requests a new allocation (e.g., a 200-byte array) but the current free slots cannot hold it, a **GC collection pass is instantly triggered right then and there.** If it sweeps up enough junk to fit your new object, execution resumes. If the warehouse remains full even after cleaning, the runtime expands the Heap (e.g., to 32 MB), which is a very heavy hardware operation.
2. **The Modern Factor: Incremental GC**
By default in modern Unity, the collector operates in **Incremental Mode**. Instead of locking the whole game loop to sweep the entire warehouse at once when it fills up (the classic "Stop-the-World" freeze), the engine slices the Mark-and-Sweep workload into tiny, fractions-of-a-millisecond time blocks distributed across consecutive frames. It still triggers based on allocation pressure, but it spreads out the execution pause to prevent frame rate hitching.
3. **Manual Forced Collection:**
You *can* manually order the janitor to sweep by calling `System.GC.Collect()`. However, this is an expensive operation and should generally only be executed during non-gameplay transitions, such as loading screens or opening a menu.

---

#### 6. Comprehensive Code Examples

To understand how careless architecture forces this automatic janitor to work excessive overtime—causing severe performance drops—let's examine a problematic script versus a clean, high-performance optimization pattern.

##### ❌ The Messy Allocator (High Garbage Collection Overhead)

The script below simulates an unoptimized real-time UI tracking system that displays combat telemetry during a frantic battle. Because it builds temporary array structures and string concatenations inside a repeatedly executing frame update loop, it creates an enormous trail of trash for the GC.

```csharp
using UnityEngine;

public class TelemetryMessyAllocator : MonoBehaviour
{
    public int playerCurrentXP = 5230;
    public int playerLevel = 42;

    // This updates 60 to 120 times every single second
    void Update()
    {
        ExecuteTelemetryUpdate();
    }

    void ExecuteTelemetryUpdate()
    {
        // ❌ PITFALL 1: Allocating a brand new array container on the Heap EVERY frame
        int[] statsSnapshot = new int[2];
        statsSnapshot[0] = playerCurrentXP;
        statsSnapshot[1] = playerLevel;

        // ❌ PITFALL 2: String manipulation creates temporary reference allocations.
        // The old strings are immediately abandoned on the Heap warehouse floor.
        string telemetryDisplayString = "LVL: " + statsSnapshot[1].ToString() + " | XP: " + statsSnapshot[0].ToString();
        
        // Outputting to an imaginary display receiver
        SimulateTextOutput(telemetryDisplayString);
    }

    void SimulateTextOutput(string output)
    {
        // Internal processing logic...
    }
}

```

> **Behind the Scenes:** Even though this code works perfectly without throwing compiler errors, it forces allocations onto the Heap *every single frame*. Within seconds, the warehouse is completely filled with thousands of discarded `int[]` arrays and abandoned string characters. Eventually, the Heap fills up entirely, forcing the Unity GC to step in, halt execution briefly to trace strings (causing a noticeable frame stutter), and sweep up the mess.



##### ━━━━

##### can Be Better: The Architectural Champion (Zero Allocation Execution)

To protect our frame budget, we can rewrite the tracking logic to rely on preallocated, persistent containers. By reusing existing structures, we ensure that the automated janitor never needs to wake up or scan our system.

```csharp
using UnityEngine;
using System.Text;

public class TelemetryZeroAllocation : MonoBehaviour
{
    public int playerCurrentXP = 5230;
    public int playerLevel = 42;

    //  OPTIMIZATION 1: Pre-allocating a persistent, reusable data array on initialization
    private int[] cachedStatsSnapshot = new int[2];

    //  OPTIMIZATION 2: Utilizing a pre-allocated StringBuilder to handle string building without trash
    private StringBuilder telemetryBuilder = new StringBuilder(64);
    private string finalOutputString;

    void Start()
    {
        // Explicitly format container dimensions once at startup
        cachedStatsSnapshot[0] = 0;
        cachedStatsSnapshot[1] = 0;
    }

    void Update()
    {
        ExecuteOptimizedTelemetry();
    }

    void ExecuteOptimizedTelemetry()
    {
        // We reuse the exact same physical warehouse slots without requesting a new shipment
        cachedStatsSnapshot[0] = playerCurrentXP;
        cachedStatsSnapshot[1] = playerLevel;

        // Clear the reusable string construction desk without throwing away the desk itself
        telemetryBuilder.Clear();
        
        // Append characters directly to the buffer. Zero temporary objects are created on the Heap.
        telemetryBuilder.Append("LVL: ");
        telemetryBuilder.Append(cachedStatsSnapshot[1]);
        telemetryBuilder.Append(" | XP: ");
        telemetryBuilder.Append(cachedStatsSnapshot[0]);

        // Hand the clean reference directly down the pipeline
        SimulateTextOutput(telemetryBuilder);
    }

    void SimulateTextOutput(StringBuilder outputBuffer)
    {
        // Process character arrays directly from the buffer safely
    }
}

```

---

#### 7. Advanced architectural Examples

Let's dive into two more complex scenarios where seemingly clean C# and Unity features create hidden heap garbage, followed by production-grade architecture to eliminate them completely.

#### Example 1: The Event System Trap (Lambda Captures & Closures)

A common pattern in larger games is registering to events or passing instructions dynamically using closures or lambda expressions (`=>`). However, if a lambda references a localized variable from its parent method, the compiler is forced to dynamically generate a hidden "closure class" on the Heap to store those variables.

##### ❌ The Messy Allocator (Hidden Closure Allocations)

In this unoptimized example, a combat system registers damage-tracking actions dynamically inside a loop.

```csharp
using UnityEngine;
using System;

public class DamageNotifierMessy : MonoBehaviour
{
    // A standard delegate event system
    public static event Action<int> OnPlayerDamaged;

    private int criticalHitMultiplier = 2;

    void Update()
    {
        // Simulating a frame loop checking combat states
        if (Input.GetKeyDown(KeyCode.Space))
        {
            TriggerDamageSequence();
        }
    }

    void TriggerDamageSequence()
    {
        int baseDamage = 50;

        // ❌ HIDDEN PITFALL: The lambda captures 'baseDamage' and 'criticalHitMultiplier'
        // To pass this function context down the line, the C# compiler builds a hidden
        // structural container object on the Heap every single time this is executed!
        ExecuteCombatAction((calculatedDamage) => 
        {
            int total = calculatedDamage * baseDamage * criticalHitMultiplier;
            Debug.Log($"Dealing dynamic damage: {total}");
        });
    }

    void ExecuteCombatAction(Action<int> combatCallback)
    {
        // Execute the delegate with an input modifier
        combatCallback?.Invoke(5);
    }
}

```

##### 👑 The Architectural Champion (Static Non-Allocating Callback Cache)

To fix this without abandoning decoupled event logic, we remove the lambda capture. We pass values explicitly or utilize a static configuration interface to avoid creating closure containers on the Heap.

```csharp
using UnityEngine;
using System;

public class DamageNotifierOptimized : MonoBehaviour
{
    // Define a clean, strongly-typed interface delegate that accepts state parameters
    // preventing the need for closures to carry local variables
    public delegate void CombatDelegate(int calculatedDamage, int baseDamage, int multiplier);

    private int criticalHitMultiplier = 2;

    // 👑 OPTIMIZATION: We cache a static, immutable delegate reference 
    // pointing to a clean, non-capturing method layout.
    private static readonly CombatDelegate CachedCombatLogic = EvaluateDamageStatic;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            TriggerDamageSequence();
        }
    }

    void TriggerDamageSequence()
    {
        int baseDamage = 50;

        // Pass the cached delegate and the raw parameters down the execution path.
        // No closure objects or transient reference containers are allocated on the Heap.
        ExecuteOptimizedCombatAction(CachedCombatLogic, baseDamage, criticalHitMultiplier);
    }

    // By keeping the function logic self-contained, it doesn't drop any garbage
    private static void EvaluateDamageStatic(int calculatedDamage, int baseDamage, int multiplier)
    {
        int total = calculatedDamage * baseDamage * multiplier;
        // In actual production, output directly to a UI text buffer instead of string parsing
    }

    void ExecuteOptimizedCombatAction(CombatDelegate combatCallback, int dmg, int mult)
    {
        // Process data over local stack contexts
        combatCallback?.Invoke(5, dmg, mult);
    }
}

```

---

#### Example 2: Spatial Physics Overruns (`Physics.OverlapSphere`)

Many games check for objects in a radius (e.g., explosions checking for hit targets or enemies checking for the player) using Unity’s built-in physics query methods like `Physics.OverlapSphere`.

##### ❌ The Messy Allocator (Transient Array Instantiations)

The standard version of this query creates a newly allocated array of `Collider[]` references every single time it runs. If you have dozens of enemies querying the world on every frame, the Heap warehouse will be overwhelmed within seconds.

```csharp
using UnityEngine;

public class RadarMessyAllocator : MonoBehaviour
{
    public float scanRadius = 15f;
    public LayerMask targetLayer;

    void Update()
    {
        ScanForTargets();
    }

    void ScanForTargets()
    {
        // ❌ CRITICAL PITFALL: OverlapSphere hits the hardware physics system,
        // discovers what's nearby, instantiates a fresh Collider[] array on the Heap,
        // populates it, and hands it back. The array is instantly discarded on the next line!
        Collider[] hitColliders = Physics.OverlapSphere(transform.position, scanRadius, targetLayer);

        for (int i = 0; i < hitColliders.Length; i++)
        {
            // Do logic with targets...
            Transform targetTransform = hitColliders[i].transform;
        }
    }
}

```

##### 👑 The Architectural Champion (Non-Allocating Pre-Allocated Buffer)

To completely secure our performance framework, we use Unity’s dedicated **Non-Allocating alternative (`Physics.OverlapSphereNonAlloc`)**. This pattern populates an array we've already created, making it completely invisible to the Garbage Collector.

```csharp
using UnityEngine;

public class RadarZeroAllocation : MonoBehaviour
{
    public float scanRadius = 15f;
    public LayerMask targetLayer;

    // 👑 OPTIMIZATION: Pre-allocate a persistent array container at startup.
    // We size this to match the maximum realistic targets our system can track at once.
    private Collider[] rawCollidersBuffer = new Collider[32];

    void Update()
    {
        ScanForTargetsOptimized();
    }

    void ScanForTargetsOptimized()
    {
        // Clear references from the previous frame to avoid holding onto dead instances
        System.Array.Clear(rawCollidersBuffer, 0, rawCollidersBuffer.Length);

        // 👑 OPTIMIZATION: OverlapSphereNonAlloc doesn't create a new array.
        // It writes directly over the existing memory addresses of our 'rawCollidersBuffer'.
        // It simply returns an integer stating exactly how many slots were filled.
        int targetsFoundCount = Physics.OverlapSphereNonAlloc(transform.position, scanRadius, rawCollidersBuffer, targetLayer);

        // Clamp our loop bounds to ensure we never run past what the physics pass actually filled
        int loopLimit = Mathf.Min(targetsFoundCount, rawCollidersBuffer.Length);

        for (int i = 0; i < loopLimit; i++)
        {
            // Read target data cleanly directly out of our pre-allocated workspace
            Collider targetCollider = rawCollidersBuffer[i];
            if (targetCollider != null)
            {
                Transform targetTransform = targetCollider.transform;
                // Execute combat or tracking logic with absolutely zero allocations!
            }
        }
    }
}

```


> By shifting from a transient "Messy Allocator" pattern to a persistent "Zero Allocation" model, your code completely stops generating trash. Because no new boxes are dropped onto the warehouse floor, the reference strings remain unchanging. As a result, the automated janitor remains asleep, frame rendering intervals remain uniformly flat, and your game avoids unexpected performance dips.


### [Next: Generational GC Model Object Lifetime Bands](./12-2-Generational-GC-Model-Object-Lifetime-Bands.md)
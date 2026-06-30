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

#### 5. Comprehensive Code Examples

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

> By shifting from a transient "Messy Allocator" pattern to a persistent "Zero Allocation" model, your code completely stops generating trash. Because no new boxes are dropped onto the warehouse floor, the reference strings remain unchanging. As a result, the automated janitor remains asleep, frame rendering intervals remain uniformly flat, and your game avoids unexpected performance dips.


### [Next: Generational GC Model Object Lifetime Bands](./12-2-Generational-GC-Model-Object-Lifetime-Bands.md)
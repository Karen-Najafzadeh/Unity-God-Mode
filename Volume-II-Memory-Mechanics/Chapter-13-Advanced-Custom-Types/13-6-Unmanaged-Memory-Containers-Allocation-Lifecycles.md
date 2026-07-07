<div align="center">

[ به فارسی بخوانید](./FA/13-6-Unmanaged-Memory-Containers-Allocation-Lifecycles-FA.md)

</div>



# Unmanaged Memory Containers & Allocation Lifecycles

---

### 1. Introduction: Breaking Out of the Velvet Prison

Up until now, our architectural journey through Unity memory management has taken place within the safe, cushioned walls of the Managed Heap. Even when optimizing with generics, object pools, or custom structs, our code was still governed by the C# Virtual Machine. This setup resembles a velvet prison: highly comfortable because an automated janitor (the Garbage Collector) watches your every move and cleans up your messes, but deeply restrictive because crossing the border to communicate with Unity’s raw C++ core incurs a translation toll.

**Unmanaged Memory Containers & Allocation Lifecycles** represents our ultimate jailbreak. By stepping out of the managed runtime, we bypass the Garbage Collector entirely. We begin building data containers directly in raw, unmanaged C++ hardware memory lanes using Unity’s **Native Collections** (`NativeArray<T>`, `NativeList<T>`, etc.).

To make this system work without causing catastrophic leaks or hard crashes, Unity introduces strict **Allocation Lifecycles** (`Allocator.Temp`, `Allocator.TempJob`, and `Allocator.Persistent`). These function like deterministic operational permissions, giving developers absolute control over the precise millisecond a piece of hardware memory is born, utilized, and destroyed.

---

### 2. The Computer Science Lore: The Sovereign Memory Realms

In the primordial era of computer systems programming, there was no "managed runtime" or "automatic memory cleaning". Languages like C and C++ required programmers to interact directly with the operating system using commands like `malloc()` (Memory Allocate) and `free()`. If you wanted space to hold an array of 1,000 integers, you asked the hardware for raw bytes. Once you were done, you had to call `free()` manually.

If you forgot to call `free()`, the memory remained blocked forever, a bug known as a **Memory Leak**. If your code ran continuously, it would slowly eat up all the system's RAM until the operating system violently terminated the process. Conversely, if you freed the memory but accidentally tried to read from it again later, you encountered a **Dangling Pointer** or **Use-After-Free** flaw, leading to memory corruption or security breaches.

To eliminate this human error, modern environments created Managed Memory, shifting the responsibility to software. However, real-time engines like Unity are hybrid systems. The gameplay logic is written in user-friendly C#, while the high-performance rendering, physics, and asset pipelines are written in raw C++.

Unmanaged Containers are the bridges across this divide. They allow you to allocate raw memory from the C++ side but access it directly inside C# using specialized pointers, eliminating GC overhead.

---

### 3. The Original Problem: The Interop Toll and Cache Scattering

When writing high-performance Unity code entirely within standard C# structures, two critical bottlenecks emerge:

1. **The Interop Bridge Cost:** Every time standard gameplay arrays (like an array of enemy positions) are sent over to the internal C++ systems for physics calculations or rendering, they must be copied or translated across the managed/unmanaged boundary. This "Managed-to-Native Interop Bridge" serves as a bottleneck that slows down performance.
2. **Cache Line Scattering (The Pointer-Chasing Problem):** Standard managed arrays inside the Heap hold reference types. These objects can be scattered across different locations in your computer's RAM. When the CPU tries to read them sequentially, it struggles to locate the data efficiently, resulting in a **Cache Miss** that slows processing down.

If you attempt to avoid these issues by allocating large arrays on the Managed Heap, the Garbage Collector will eventually be forced to scan them, resulting in frame rate stutters.

---

### 4. The Salvation: Native Allocations & Explicit lifecycles

The solution is the **Unity Native Collections Framework** combined with **Explicit Allocator Lifecycles**. Instead of allocating a standard C# array (`int[]`), we allocate a `NativeArray<int>`. This array is created entirely inside the unmanaged memory zone, arranging its data consecutively like a pristine block of concrete. This allows both the C# script and the native C++ engine to read and write to it with minimal translation overhead.

Because the Garbage Collector cannot see this unmanaged space, Unity requires developers to explicitly specify how long this memory should live by passing an `Allocator` rule upon creation.

#### The Three Sovereign Allocation Lifecycles

| Allocator Lifecycle | Allocation Speed | Intended Lifespan | Disposal Rule | Thread/Job Safety |
| --- | --- | --- | --- | --- |
| **`Allocator.Temp`** | **Ultra-Fast** (1-2 clock cycles via Bump Allocator) | **1 Frame Max** (Very short-lived) | **Automatic** (Cleared at frame end; manual `Dispose` is a no-op) | Main Thread Only (Cannot be passed into asynchronous Jobs) |
| **`Allocator.TempJob`** | **Fast** (Pre-allocated pool buckets) | **4 Frames Max** (Short-lived job bursts) | **Manual** (Must call `Dispose()` within 4 frames) | **Job Safe** (Can be safely sent to multi-threaded worker jobs) |
| **`Allocator.Persistent`** | **Slow** (Direct Operating System `malloc`) | **Indefinite** (Lives until application exit if needed) | **Strictly Manual** (Must explicitly call `Dispose()` or cause leak) | **Job Safe** (Persistent background tracking matrix) |

---

### 5. A Gentle Introduction: Basic `NativeArray` Management

Up until now, our arrays were managed by the Garbage Collector (GC). When we used a standard `int[]`, the GC automatically allocated the memory when we created it and cleaned it up when no one was referencing it anymore.

With unmanaged containers like `NativeArray<T>`, **we take over the responsibility** of the GC. We must tell the engine exactly when to allocate the memory on the machine's hardware and exactly when to free it. If we don't free it, we get a memory leak, which will slowly consume all system RAM.

#### The Unmanaged Lifecycle: Allocate -> Use -> Dispose

```csharp
using Unity.Collections;
using UnityEngine;

public class SimpleNativeExample : MonoBehaviour
{
    // 1. ALLOCATION: We need a persistent container to hold our data.
    NativeArray<int> _myNumbers;

    private void Start()
    {
        // Allocate space for 10 integers in unmanaged hardware memory.
        // We use Allocator.Persistent because this data should persist across frames.
        _myNumbers = new NativeArray<int>(10, Allocator.Persistent);

        // 2. USE: Directly modify raw memory using familiar loop structures.
        for (int i = 0; i < _myNumbers.Length; i++)
        {
            _myNumbers[i] = i * 2;
        }
    }

    private void Update()
    {
        // Access our unmanaged data directly.
        Debug.Log($"Current value: {_myNumbers[0]}");
    }

    private void OnDestroy()
    {
        // 3. DISPOSAL: CRITICAL!
        // We must manually return this memory to the system.
        // Failing to call Dispose() will result in a permanent memory leak.
        if (_myNumbers.IsCreated)
        {
            _myNumbers.Dispose();
        }
    }
}
```

This approach bypasses the GC, providing a performance gain because the engine does not need to scan this unmanaged memory to determine if it should be cleaned up.

---

### 6. Comprehensive Architectural Examples (Advanced)

#### ❌ The Allocation-Heavy Managed Approach (Performance Bottleneck)

This script performs a localized visibility calculation every frame, creating a temporary managed array that generates considerable garbage collection overhead.

```csharp
using UnityEngine;

public class ManagedVisibilitySystem : MonoBehaviour
{
    [SerializeField] private Transform[] targetEntities;

    private void Update()
    {
        // ❌ CRITICAL ALLOCATION: Allocates an array on the Heap every frame.
        // The Garbage Collector will eventually have to freeze the frame to sweep this up.
        Vector3[] relativePositions = new Vector3[targetEntities.Length];

        for (int i = 0; i < targetEntities.Length; i++)
        {
            if (targetEntities[i] != null)
            {
                relativePositions[i] = targetEntities[i].position - transform.position;
            }
        }

        // Process positions...
        Debug.Log($"Processed {relativePositions.Length} entities via managed heap.");
    }
}

```

#### 👑 The Sovereign Unmanaged Architecture (Zero Allocation & Optimized Lifecycles)

Below is the highly optimized architectural solution. It uses `Allocator.Temp` for instant, single-frame calculations and handles multi-threaded math using `Allocator.TempJob` combined with deferred asynchronous cleanup.

```csharp
using UnityEngine;
using Unity.Collections;
using Unity.Jobs;

public class UnmanagedLifecycleManager : MonoBehaviour
{
    [SerializeField] private Transform[] targetEntities;
    
    // Persistent Allocator: Lives for the entire lifecycle of this component
    private NativeArray<Vector3> _persistentTargetCache;

    private void Awake()
    {
        // 👑 PERSISTENT ALLOCATION: Allocated once at startup. Slow to create, but infinite lifespan.
        _persistentTargetCache = new NativeArray<Vector3>(100, Allocator.Persistent); //
    }

    private void Update()
    {
        ExecuteSingleFrameCalculation();
        ScheduleMultiThreadedJobBurst();
    }

    /// <summary>
    /// Demonstrates Allocator.Temp - Single frame memory burst with absolute zero allocation.
    /// </summary>
    private void ExecuteSingleFrameCalculation()
    {
        int entityCount = targetEntities.Length;

        // 👑 TEMP ALLOCATION: Super fast bump allocator. Valid ONLY for the duration of this frame.
        // We don't even need to call Dispose() because Unity resets the frame allocator automatically.
        NativeArray<Vector3> localizedOffsets = new NativeArray<Vector3>(entityCount, Allocator.Temp, NativeArrayOptions.UninitializedMemory); //

        for (int i = 0; i < entityCount; i++)
        {
            if (targetEntities[i] != null)
            {
                localizedOffsets[i] = targetEntities[i].position;
            }
        }

        // The memory is read instantly with zero GC tracking overhead.
        Vector3 frameAverage = Vector3.zero;
        for (int i = 0; i < localizedOffsets.Length; i++)
        {
            frameAverage += localizedOffsets[i];
        }
        frameAverage /= entityCount;
        
        // localizedOffsets.Dispose(); // Optional/No-Op for Allocator.Temp!
    }

    /// <summary>
    /// Demonstrates Allocator.TempJob - Temporary allocation that lives slightly longer than one frame.
    /// Even without the Job System, TempJob is useful when you need to hand memory off
    /// and clean it up manually at a later, safer time.
    /// </summary>
    private void ScheduleTask()
    {
        // 👑 TEMPJOB ALLOCATION: Lives longer than a single frame, but must be disposed.
        NativeArray<Vector3> buffer = new NativeArray<Vector3>(targetEntities.Length, Allocator.TempJob); 

        // Populate our unmanaged buffer
        for (int i = 0; i < targetEntities.Length; i++)
        {
            if (targetEntities[i] != null) buffer[i] = targetEntities[i].position;
        }

        // Perform some calculation (in this simple example, on the main thread)
        for (int i = 0; i < buffer.Length; i++)
        {
            buffer[i] = buffer[i] * 2.0f;
        }

        // 👑 DISPOSAL: We must manually dispose of TempJob.
        buffer.Dispose();
    }

    private void OnDestroy()
    {
        // 👑 CRITICAL CLEANUP: Since Persistent allocations live indefinitely,
        // failing to call Dispose here results in a native memory leak outside the GC's vision.
        if (_persistentTargetCache.IsCreated)
        {
            _persistentTargetCache.Dispose(); //
        }
    }
}

```

---

### 6. Architectural Summary

By shifting from managed arrays to unmanaged containers and understanding these lifecycles, you gain direct control over your data's memory profile:

* **Use `Allocator.Temp**` when you need a temporary list, buffer, or array inside a single function block that completes execution on the main thread within the same frame.
* **Use `Allocator.TempJob**` when you need a temporary allocation to pass into a multi-threaded C# Job, and configure it with deferred disposal (`Dispose(jobHandle)`) to ensure it cleans itself up immediately upon completion.
* **Use `Allocator.Persistent**` for long-lived, foundational game databases, tracking matrices, or spatial frameworks created at startup, and remember to explicitly free them during `OnDestroy`.


### [Next: Volume III Engine Core Runtime](/Volume-III-Engine-Core-Runtime/README.md)
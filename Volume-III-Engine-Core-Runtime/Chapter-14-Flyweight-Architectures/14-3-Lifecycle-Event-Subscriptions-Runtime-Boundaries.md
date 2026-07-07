<div align="center">

[ به فارسی بخوانید](./FA/14-3-Lifecycle-Event-Subscriptions-Runtime-Boundaries-FA.md)

</div>


# Lifecycle Event Subscriptions across Runtime Boundaries

---

#### 1. Introduction: The Border Control of the Engine Core

Welcome to one of the most intellectually thrilling territories of high-performance engine architecture: **Runtime Boundaries**.

Up until now, you have likely viewed Unity as a unified digital ecosystem where you write C# code, press "Play," and magic happens. But beneath that friendly, polished surface lies a massive, mechanical fault line. Unity is actually a split-brain creature. Its outer layer, where your gameplay scripts, custom AI, and UI systems live, is governed by the safe, managed **C# (.NET/Mono/IL2CPP) Runtime**. However, its deep, hyper-fast inner core, which handles raw 3D graphics rendering, audio mixing, matrix transformations, and physics impulses, is written entirely in raw, bare-metal, unmanaged **Native C++**.

When your game is running, these two worlds must talk to each other constantly. If an enemy breaks a physical barrier or an audio clip hits a specific playback marker deep within the C++ core, that event must instantly ring a alarm bell up in your C# script. **Lifecycle Event Subscriptions across Runtime Boundaries** is the study of how we build ultra-fast, zero-allocation, telepathic communication pipelines across this chasm without causing your game's frame rate to hitch, stutter, or drop dead.

---

#### 2. The Computer Science Lore: The Chasm, the Ambassador, and the Tollbooth

To appreciate how hard this is, we have to look back at the historical lore of computer science. In the early days of software engineering, programs were written in a single language. If it was C, it compiled straight to machine code, and every function could jump directly to any other function's memory address.

Then came the rise of **Virtual Machines** and **Managed Runtimes** (like Java and C#). These languages offered a "velvet prison": they wrapped your code in a safe layer that managed memory for you, checked for errors automatically, and prevented crashes. But they introduced a new dilemma: **How does a managed program interact with an unmanaged system component?**

Computer scientists invented a mechanism called **Interop** (short for Interoperability), specifically executed via **P/Invoke** (Platform Invoke) and **Marshalling**.

Imagine the Native C++ core as an ancient, highly disciplined warrior kingdom that speaks only raw binary dialects. The C# Managed Runtime is a modern, automated tech-city that speaks in complex object networks. Between them sits a physical border wall: the **Runtime Boundary**.

When a C# script wants to talk to a C++ engine routine, an "Ambassador" (the Marshaller) must step in. The Ambassador stops the code execution, translates the C# object into raw bits that C++ can understand, copies those bits across the border, and hands them over. This process is called **Data Marshalling**.

The lore's historical warning is clear: **Crossing the border is incredibly expensive.** It is a physical tollbooth. If your code crosses this border thousands of times a frame to listen for events, your CPU will spend all its time translating messages rather than running your game.

---

#### 3. The Original Problem: The Stalling Customs Office and Ghost Subscriptions

When a developer naively attempts to handle events across these boundaries, they fall face-first into two catastrophic architectural traps:

##### Trap A: The Boundary-Crossing Toll Booth Stalls the Frame Loop

Suppose a low-level C++ subsystem (like a custom fluid physics simulation running on background hardware) needs to notify 5,000 game entities in C# every time a liquid molecule collides with an object. If the C++ engine core halts its operations, opens up a standard interop pipeline, translates each collision data packet into a fresh C# heap object, and invokes a standard C# delegate event, the game will completely choke. The execution pipeline is forced into a series of constant micro-pauses as it synchronizes the unmanaged CPU registers with the managed virtual machine state.

##### Trap B: The "Ghost" Reference Memory Leak (Dangling Pointers)

C# objects are dynamic; the Garbage Collector (GC) loves to move them around or sweep them away when it thinks no one is looking. C++ memory is static and rigid; it stays exactly where it was placed until it is manually destroyed. If you pass a pointer (a memory address) of a C# method down into the C++ engine core so C++ can call it later, and then the C# Garbage Collector relocates that object in RAM to compact space, the C++ engine core will still hold the old, stale address. The next time C++ tries to fire that event, it will invoke a **dangling pointer**, firing into empty or corrupted memory, causing an instant, unhandled hard crash to the desktop.

---

#### 4. The Architectural Salvation: Static Function Pointers and Blittable Registries

To bypass the interop tollbooth entirely and secure absolute runtime stability, systems engineers build a **Sovereign Non-Allocating Callback Matrix**. Instead of passing heavy objects or dynamic delegates back and forth across the border, we leverage three cutting-edge architectural laws:

1. **Blittable Type Layouts:** We ensure that any event data packet passed across the border is made of "blittable" data types (like `int`, `float`, or `byte`). These types have an identical binary representation in both C++ and C#, meaning they require *zero translation* by the marshalling ambassador. They slide straight through border security.
2. **Native Function Pointers (`delegate* unmanaged`):** Instead of using standard, heavy C# event objects, we extract the pure, raw hardware memory address of a C# method using modern unmanaged function pointers. We mark these C# methods with special attributes like `[UnmanagedCallersOnly]`. This tells the compiler to freeze this execution address in place, making it perfectly readable by the C++ engine core as if it were a native C++ function.
3. **Double-Sided Index Registries:** Instead of passing object references, we pass a simple `int` ID (an Entity or Instance ID). C++ triggers the event by firing a raw function pointer and passing a simple number. C# receives that number and instantly uses it to look up the target entity in a pre-allocated array on the stack or local heap, achieving an $O(1)$ lookup with **Absolute Zero Garbage Generation**.

---

#### 5. Comprehensive Architectural Implementation

Let’s build a high-performance, production-grade simulation of this boundary. We will create a low-level Native Engine Event Core (simulating the C++ layer) and a Sovereign C# Runtime Boundary Bridge that handles lifecycle events (like deep-engine physics frames or initialization triggers) perfectly without generating a single byte of garbage or risking memory corruption.

##### ❌ The Naive Allocation-Heavy Boundary Approach (Performance Nightmare)

This represents how unoptimized systems handle callbacks—allocating delegates dynamically, creating new event arguments objects on the heap, and crossing the interop bridge with un-blittable data structures.

```csharp
using System;

// This simulates a heavy, messy data block that requires deep translation
public class NaiveEventData 
{
    public string EventName; // String is a pointer type, horrible for native interop!
    public int InstanceId;
    public float DeltaTime;
}

public class NaiveRuntimeBridge
{
    // A standard C# delegate creates a dynamic object wrapper on the heap
    public delegate void NaiveEventCallback(NaiveEventData data);
    private event NaiveEventCallback OnNativeUpdate;

    public void RegisterLegacyEvent(NaiveEventCallback callback)
    {
        // Every subscription creates dynamic allocations and binds object lifecycles across boundaries
        OnNativeUpdate += callback;
    }

    public void SimulateNativeEngineFiring(int instanceId, float dt)
    {
        // CRITICAL PERFORMANCE FLAW: Allocates a fresh object on the Heap EVERY single call!
        NaiveEventData frameData = new NaiveEventData(); 
        frameData.EventName = "NATIVE_PHYSICS_TICK"; // Allocates string memory
        frameData.InstanceId = instanceId;
        frameData.DeltaTime = dt;

        // Triggers the event, forcing the engine core to wait for virtual machine scheduling
        OnNativeUpdate?.Invoke(frameData);
    }
}

```

##### 👑 The Sovereign Boundary Architecture (Zero Allocation & Native Fast-Path)

Below is the highly optimized system. We use raw function pointers (`delegate* unmanaged`), structural blittable layouts, and static lookup arrays to achieve lightning-fast communication.

```csharp
using System;
using System.Runtime.InteropServices;
using System.Runtime.CompilerServices;

namespace SovereignEngine.Core
{
    // 1. Define a layout that is mathematically identical in both C++ and C# hardware layers
    [StructLayout(LayoutKind.Sequential)]
    public struct BlittableLifecycleEvent
    {
        public int EntityId;
        public int PhaseIndex;
        public float RawTimestamp;
    }

    // 2. The high-performance C# event receiver side
    public static class GameplaySystemRegistry
    {
        private static Action<BlittableLifecycleEvent>[] _systemsLookup = new Action<BlittableLifecycleEvent>[1000];

        public static void RegisterSystem(int entityId, Action<BlittableLifecycleEvent> systemLogic)
        {
            if (entityId < _systemsLookup.Length)
            {
                _systemsLookup[entityId] = systemLogic;
            }
        }

        // This method is compiled to act exactly like a native C++ function pointer!
        // It bypasses standard virtual machine tracking and can be invoked directly by native threads.
        [UnmanagedCallersOnly(CallConventions = new[] { typeof(CallConvCdecl) })]
        public static void OnNativeLifecycleTrigger(BlittableLifecycleEvent nativeEvent)
        {
            // Absolute Zero Allocation: We grab the entity ID instantly and execute local logic
            int id = nativeEvent.EntityId;
            if (id >= 0 && id < _systemsLookup.Length)
            {
                Action<BlittableLifecycleEvent> action = _systemsLookup[id];
                action?.Invoke(nativeEvent);
            }
        }
    }

    // 3. Simulating the deep C++ Native Engine Execution Core
    public unsafe class NativeEngineSimulator
    {
        // This is a raw hardware pointer slot that stores the address of our frozen C# function
        private delegate* unmanaged[Cdecl]<BlittableLifecycleEvent, void> _nativeCallbackPointer;

        // C++ registers the callback pointer directly into its micro-engine registry
        public void BindEngineCallback(IntPtr functionPointerAddress)
        {
            _nativeCallbackPointer = (delegate* unmanaged[Cdecl]<BlittableLifecycleEvent, void>)functionPointerAddress;
        }

        public void ExecuteHighFrequencyNativeLoop(int targetEntity, int currentPhase, float timestamp)
        {
            if (_nativeCallbackPointer == null) return;

            // Prepare data strictly on the hardware Stack registers (Zero Heap Overhead)
            BlittableLifecycleEvent hardwareEvent;
            hardwareEvent.EntityId = targetEntity;
            hardwareEvent.PhaseIndex = currentPhase;
            hardwareEvent.RawTimestamp = timestamp;

            // ULTRA FAST PATH: Invoke the pointer. The CPU jumps straight through the 
            // boundary barrier into the frozen C# method without checking with the Marshaller!
            _nativeCallbackPointer(hardwareEvent);
        }
    }
}

```

---

#### 6. Summary of the Architectural Shift

| Dimension | The Naive Allocation Boundary | The Sovereign Native-Fast Architecture |
| --- | --- | --- |
| **Allocation Matrix** | **Heavy Heap Bloat:** Instantiates new object configurations, data packages, and strings per event call. | **Absolute Flatline ($O(1)$):** Leverages stack-allocated structural data primitives. Zero garbage collector strain. |
| **Boundary Speed** | **High Translation Toll:** Requires the engine’s marshalling layer to verify object structures and data layouts. | **Instantaneous Jump:** Fires raw native machine address pointers via standard hardware execution pipelines. |
| **Memory Security** | **Fragile & Volatile:** High vulnerability to GC relocation stutters or corrupted pointer crashes. | **Immune & Frozen:** Methods are strictly locked using compile-time markers, securing permanent native safety. |
| **Threading Profile** | Main Thread bound. Attempting to invoke standard events from native backgrounds causes fatal runtime crashes. | Fully concurrent. Native physics or rendering worker threads can safely trigger callbacks instantly. |

### [Next: Chapter 15 Native Serialization](/Volume-III-Engine-Core-Runtime/Chapter-15-Native-Serialization/README.md)
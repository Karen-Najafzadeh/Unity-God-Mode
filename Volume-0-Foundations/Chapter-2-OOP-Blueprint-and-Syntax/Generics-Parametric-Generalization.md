# Generics: Parametric Generalization

In the **Unity God Mode** framework, **Generics** (`<T>`) are the ultimate tool for "DRY" (Don't Repeat Yourself) programming. They allow you to write logic once and apply it to *any data type*, without losing type safety.

---

## 1. The CS Lore: The Copy-Paste Nightmare & The Boxing Ring

### The Original Problem

Imagine you are building an inventory system or a data storage utility. You need a structure that can hold items.

* First, you need to store **integers** (like item IDs). So, you write an `IntStorage` class.
* Next, you need to store **strings** (like quest names). So, you copy-paste the exact same code, changing the types to make a `StringStorage` class.
* Then, you need to store custom components, weapons, or enemy data structures.

Suddenly, you have 10 different storage classes with identical logic. If you find a bug in how data is saved, you now have to manually fix it in 10 different places. This violates the sacred engineering rule of **DRY (Don't Repeat Yourself)**.

### The Dynamic "Fix" (and Why It Breaks)

Before generics existed, languages tried to solve this using a universal type. In C#, every single thing inherits from a master type called `object`. So, engineers thought: *"Great! I'll just make an `ObjectStorage` class that holds the type `object`. That way, it can hold anything!"*

It looks like a brilliant hack, but it introduces two severe engine-level fatal flaws:

1. **The Type-Safety Blindspot:** Because the storage class treats everything as a generic object, it has no idea what is actually inside it at compile time. You could accidentally push an enemy data struct into your UI gold counter array, and the compiler wouldn't warn you. The game would simply crash at runtime when a player opens their inventory.
2. **The Performance Tax (Boxing & Unboxing):** Value types (like `int`, `float`, `structs`) live on the lightning-fast **Stack** memory. Reference types (like `object`, classes) live on the managed **Heap**. When you force a Stack-based value type into an `object` variable, the engine has to wrap that data in a temporary reference bubble and throw it onto the Heap. This is called **Boxing**. When you want your data back, it has to rip it out of the bubble (**Unboxing**). This forces the CPU to do heavy pointer-chasing and triggers the **Garbage Collector (GC)** to clean up the temporary bubbles, tanking your game's framerate.

### The Ultimate Solution: Generics

Generics solve this by acting as a **blueprint code generator**. Instead of telling the compiler exactly what type of data your class holds, you leave a temporary placeholder (usually represented by the letter `<T>`, meaning "Type").

When you write the code, you write it once for `T`. When you initialize the code in your engine, you tell it exactly what type to substitute. The compiler then generates a dedicated, type-safe, perfectly optimized version of that class behind the scenes. **Zero boxing, zero copy-pasting, absolute type-safety.**

---

## 2. Structural C# Syntax: Building Your First Generic System

Let's look at how to declare a generic class. We use angle brackets `<T>` immediately after the class name to signal to C# that this is a generic blueprint.

```csharp
using UnityEngine;

// T is our placeholder variable for any type the architect chooses later
public class ArkaDataNode<T>
{
    private T dataValue;

    // Constructor that accepts our generic type
    public ArkaDataNode(T initialValue)
    {
        this.dataValue = initialValue;
    }

    public void UpdateData(T newValue)
    {
        dataValue = newValue;
        Debug.Log($"Node updated. Current value: {dataValue.ToString()}");
    }

    public T GetData()
    {
        return dataValue;
    }
}

```

### How You Instantiate It

Now, when you want to use this data node in your systems, you declare it while passing the target type inside the angle brackets. The engine treats these as completely distinct, high-performance types.

```csharp
public class GenericsTest : MonoBehaviour
{
    private void Start()
    {
        // Allocation 1: A node dedicated EXCLUSIVELY to high-speed integers
        ArkaDataNode<int> healthNode = new ArkaDataNode<int>(100);
        healthNode.UpdateData(85); // Pure value type speed. Zero boxing!

        // Allocation 2: A node dedicated EXCLUSIVELY to strings
        ArkaDataNode<string> activeQuestNode = new ArkaDataNode<string>("Locate Sector 7");
        
        // This will fail at compile time! Safety shield is active:
        // healthNode.UpdateData("Dead"); // The compiler stops you immediately!
    }
}

```

---

## 3. Generic Methods: Code Utility Without Class Restrictions

You don't have to make an entire class generic. You can apply generics directly to a single utility method. This is incredibly useful for custom physics queries, component finding tools, or debugging frameworks.

Here is an architectural pattern for an engine logger that swaps positions or processes array elements cleanly:

```csharp
public class EngineUtility : MonoBehaviour
{
    // A single generic method that can swap any two items in an array
    public static void SwapElements<T>(T[] array, int indexA, int indexB)
    {
        if (indexA < 0 || indexA >= array.Length || indexB < 0 || indexB >= array.Length)
        {
            return; // Out of bounds safety guard
        }

        T temporaryContainer = array[indexA];
        array[indexA] = array[indexB];
        array[indexB] = temporaryContainer;
    }
}

```

---

## 4. Generic Constraints: The Architect's Rules (`where`)

Right now, `<T>` can literally be *anything*. It could be a class, a primitive float, a lethal raw pointer, or a UI script. But as a systems architect, you often need to lay down strict rules for what types are allowed into your machine.

We do this using the `where` keyword. This tells the compiler: *"Only allow types that match this exact criteria."*

### Most Crucial Constraints for Unity Devs

* `where T : struct` $\rightarrow$ The type **must** be a value type (fast Stack memory allocation).
* `where T : class` $\rightarrow$ The type **must** be a reference type (Heap allocation).
* `where T : MonoBehaviour` $\rightarrow$ The type **must** be a component that can attach to Unity GameObjects.
* `where T : ISaveable` $\rightarrow$ The type **must** implement a specific interface contract.
* `where T : new()` $\rightarrow$ The type **must** possess a default public constructor so you can safely instantiate it inside the method using `new T()`.

### Real-World Production Example: The Component Fetcher Matrix

Here is a pattern you will see everywhere in production game loops—a script designed to cleanly spawn and register specialized system sub-modules without crashing:

```csharp
using UnityEngine;

public class ModuleArchitect : MonoBehaviour
{
    // Rules: T MUST be a MonoBehaviour, and it MUST have a blank constructor
    public T InitializeEngineSystem<T>(GameObject targetDrive) where T : MonoBehaviour, new()
    {
        T component = targetDrive.GetComponent<T>();

        if (component == null)
        {
            Debug.LogWarning($"System {typeof(T).Name} missing on {targetDrive.name}! Forcing installation...");
            component = targetDrive.AddComponent<T>();
        }

        return component;
    }
}

```

---

## 5. Architectural Comparison: The Tool Selection Matrix

| Pattern Strategy | Type Safety | Memory Footprint / GC | CPU Overhead | Use Case |
| --- | --- | --- | --- | --- |
| **Old School `object` Arrays** | ❌ Completely Blind | ⚠️ High (Triggers heavy Boxing allocations) | 🛑 High (Casting validations) | Avoid entirely in game design loops. |
| **Hardcoded Duplicate Classes** | Type-Safe | Low / Optimal | Zero | Tiny, hyper-isolated test scripts. |
| **C# Generics (`<T>`)** | 🛡️ Maximum Strict Validation | Absolute Best (Compiles down to raw specialized types) | Zero (Calculated at compile time) | Large-scale inventory systems, pooling engines, state machines, managers. |

---

## Architect's Summary Checklist

1. Use generics whenever you write structural logic that doesn't care about the *flavor* of data it's handling, only *how* it handles it.
2. Always apply strict `where` constraints to your generics to prevent your team or future-self from passing invalid classes into specialized systems.
3. Keep an eye out for standard built-in C# generic collections like `List<T>` and `Dictionary<TKey, TValue>`—they utilize these exact low-level systems under the hood to ensure your code runs at maximum frame rates.

Where should we take our engine architecture next?
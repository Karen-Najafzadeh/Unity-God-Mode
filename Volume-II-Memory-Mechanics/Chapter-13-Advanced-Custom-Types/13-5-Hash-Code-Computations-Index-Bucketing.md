<div align="center">

[<img src="https://upload.wikimedia.org/wikipedia/commons/b/b7/Lion_and_Sun_flag_%28emoji%29.svg" width="100" valign="middle"> به فارسی بخوانید](./FA/13-5-Hash-Code-Computations-Index-Bucketing-FA.md)

</div>




# Hash Code Computations and Index Bucketing

### 1. Introduction: The Infinite Warehouse and the Magical Sorting Hat

Imagine you are running a massive multiplayer online role-playing game (MMORPG) in Unity. Your game contains an inventory of hundreds of thousands of distinct items, or a database tracking the usernames of millions of global players.

When a player searches for an item in their vault—say, a legendary sword named `"ShadowSlayer_99"`—how does the computer find it?

If the computer stores items in a traditional list, it has to start at item #1, check if it's `"ShadowSlayer_99"`, move to item #2, check again, and keep scanning all the way to item **#500,000**. If the item doesn't exist, or is at the very end, the computer just wasted precious milliseconds hunting through the entire warehouse. In a fast-paced game, doing this every frame causes the game to stutter and freeze.

To solve this, computer scientists invented a combination of two brilliant architectural mechanisms: **Hash Code Computations** and **Index Bucketing**. Together, they form the foundation of a data structure known as a **Hash Table** (or a `Dictionary` in C#).

Instead of hunting through a massive list, the computer feeds the name `"ShadowSlayer_99"` into a mathematical machine called a **Hash Function**. This function acts like a "Magical Sorting Hat." It instantly turns that text string into a specific, predictable number (the **Hash Code**). Another system takes that number and maps it directly to a specific room or cabinet (the **Index Bucket**).

The next time you look for `"ShadowSlayer_99"`, you don't scan the warehouse. You pass the name back to the Sorting Hat, it gives you the exact cabinet number, and you walk straight to it in a single step.

---

### 2. The Computer Science Lore: The Post Office Blueprint and the Pigeonhole Principle

To understand where this comes from, we have to look back at the early days of mechanical sorting and postal networks.

#### The Lore of the Direct Address Table

In a perfect world, if you had an inventory of 100 items numbered 0 to 99, you could allocate exactly 100 memory slots in your computer's RAM. If you wanted item #45, you went to index slot 45. This is called a **Direct Address Table**. It is incredibly fast—taking $O(1)$ constant time, meaning it takes the exact same fraction of a microsecond to find an item whether you have 5 items or 5 million.

But what happens when the things you want to store aren't simple, sequential numbers? What if your keys are strings of text (like player names or item descriptions) or massive combinations of coordinate vectors?

A text string can be infinitely long. If you tried to pre-allocate a specific memory slot for every single possible combination of characters a player could ever type for a username, you would need more memory slots than there are atoms in the observable universe. Your computer's physical RAM would instantly burst into flames.

#### The Pigeonhole Principle and Collisions

This brings us to a foundational rule of mathematics called **The Pigeonhole Principle**. It states that if you have 10 pigeons but only 9 pigeonholes to put them in, at least one of those pigeonholes *must* contain more than one pigeon.

In computing, we have an infinite universe of possible data inputs (usernames, strings, items) but a finite, limited amount of physical memory buckets. The core challenge of Computer Science wasn't just turning text into numbers; it was figuring out how to compress an infinite universe of possibilities into a small, highly organized filing cabinet without the data overlapping and corrupting itself. This overlapping problem is called a **Collision**.

---

### 3. The Core Architecture: The Problem and The Solutions

Let's break down exactly how these two mechanisms work step-by-step to solve the infinite memory problem.

#### Step 1: Hash Code Computation (Compressing Identity)

The original problem is that a computer can only look up memory addresses using numbers, but humans use complex objects and text.

A **Hash Function** is a one-way mathematical pipeline. It takes an input of any size (a single character, a massive text file, or an entire game object) and processes its internal bytes to output a single, fixed-size 32-bit integer (the **Hash Code**).

In C#, every single object inherits a built-in function called `.GetHashCode()`.

A high-quality hash function must obey three strict rules:

1. **Deterministic:** If you give it the string `"Excalibur"`, it must return the exact same number every single time it is called during that program's run.
2. **Uniform Distribution:** Changing just one tiny letter (e.g., from `"Excalibur"` to `"excalibur"`) should result in a wildly different hash code. This spreads the items evenly across memory rather than clustering them together.
3. **Fast Evaluation:** The math must be simple enough for the CPU to compute in a few clock cycles.

#### Step 2: Index Bucketing (Fitting Into Reality)

Great! We turned `"ShadowSlayer_99"` into a hash code, let’s say the number `2,147,483,647`. But we can't create an array with over 2 billion slots just to store a few hundred items; that wastes massive amounts of RAM.

This is where **Index Bucketing** comes in. When you create a `Dictionary`, the computer allocates a small, manageable internal array of a specific size, let's say **10 slots** (indexed 0 to 9). These slots are our **Buckets**.

To translate our massive 2-billion-scale hash code into a bucket number between 0 and 9, we use a mathematical operation called the **Modulo Operator (%)**, which finds the remainder of a division.

$$\text{Bucket Index} = |\text{Hash Code}| \pmod{\text{Number of Buckets}}$$

If our hash code is `123456` and we have `10` buckets:


$$123456 \div 10 = 12345 \text{ with a remainder of } 6$$


The item is placed cleanly into **Bucket #6**.

#### Handling the Inevitable: Collision Resolution

Because of the Pigeonhole Principle, two completely different names will eventually end up with hash codes that point to the exact same bucket. If `"ShadowSlayer_99"` and `"DragonRider_12"` both map to Bucket #6, how does the system handle it?

There are two classic ways to solve this:

1. **Chaining (Linked Lists):** Each bucket isn't just a single slot; it's a small bucket that can hold a chain of items. If a collision occurs, the new item is linked behind the first item in that same bucket. When searching, the computer goes straight to Bucket #6, then scans only the tiny chain inside that bucket to find the exact match.
2. **Open Addressing (Linear Probing):** If Bucket #6 is taken, the computer looks at Bucket #7. If that's taken, it looks at Bucket #8, until it finds an empty slot.

---

### 4. Comprehensive Code Implementation

Let’s step away from Unity's high-level magic and build our very own customized, zero-allocation, high-performance Hash Table from scratch. This custom architecture will demonstrate exactly how a text string is hashed, compressed via modulo, and placed inside an index bucketing network using **Chaining** to handle collisions.

```csharp
using System;
using System.Collections.Generic;
using UnityEngine;

public class HashArchitectureDemo : MonoBehaviour
{
    void Start()
    {
        // 1. Initialize our custom high-performance storage vault with 5 buckets
        CustomDictionary itemVault = new CustomDictionary(5);

        Debug.Log("=== POPULATING THE ARCHITECTURAL VAULT ===");
        itemVault.Insert("ShadowSlayer_99", "Legendary Abyssal Greatsword +5");
        itemVault.Insert("DragonRider_12", "Mythic Wyvern Scale Chestplate");
        itemVault.Insert("Excalibur", "Holy Radiant Blade of Kings");
        itemVault.Insert("RustySpoon", "Common Trash Weapon");
        itemVault.Insert("PhoenixBow", "Ancient Firestrike Longbow");

        Debug.Log("\n=== RETRIEVING DATA FROM THE BUCKETS ===");
        itemVault.Search("Excalibur");
        itemVault.Search("ShadowSlayer_99");
        itemVault.Search("MegalodonTooth"); // Item that does not exist

        Debug.Log("\n=== VISUALIZING INTERNAL BUCKETS ===");
        itemVault.PrintStorageLayout();
    }
}

/// <summary>
/// A node representing a physical item stored inside a bucket chain.
/// </summary>
public class HashNode
{
    public string Key;         // The human-readable identifier (e.g., Player Name / Item ID)
    public string Value;       // The actual payload data (e.g., Item Stats / Description)
    public int ComputedHash;   // The raw hash code calculated for this key
    public HashNode Next;      // The link pointer to the next item in this bucket chain (Chaining)

    public HashNode(string key, string value, int computedHash)
    {
        Key = key;
        Value = value;
        ComputedHash = computedHash;
        Next = null;
    }
}

/// <summary>
/// Our custom engineered Hash Table showcasing Hash Code Computations and Index Bucketing.
/// </summary>
public class CustomDictionary
{
    private HashNode[] _buckets; // The core index array acting as our bucket list
    private int _bucketCount;    // Total size of our physical array filing cabinet

    public CustomDictionary(int totalBuckets)
    {
        _bucketCount = totalBuckets;
        _buckets = new HashNode[_bucketCount]; // Pre-allocate the fixed array vaults
    }

    /// <summary>
    /// Custom deterministic Hash Function (DJB2 Algorithm Variant).
    /// Turns any complex text string into a highly distributed 32-bit integer.
    /// </summary>
    private int ComputeDeterministicHash(string key)
    {
        unchecked // Allow arithmetic overflow safely to preserve performance
        {
            int hash = 5381; // Historical optimal prime starting seed
            for (int i = 0; i < key.Length; i++)
            {
                // Shift bits left by 5 and add the character's ASCII value
                hash = ((hash << 5) + hash) + key[i];
            }
            return hash;
        }
    }

    /// <summary>
    /// Inserts an item into our bucket architecture.
    /// </summary>
    public void Insert(string key, string value)
    {
        // Step 1: Compute the raw 32-bit identity hash code
        int rawHash = ComputeDeterministicHash(key);

        // Step 2: Compress the hash into a valid index bucket using Modulo math
        // We use Math.Abs to keep the index positive if the hash overflowed into a negative number
        int bucketIndex = Math.Abs(rawHash) % _bucketCount;

        Debug.Log($"[INSERT] Key: '{key}' -> Raw Hash: {rawHash} -> Mapped to Bucket Index: #{bucketIndex}");

        // Step 3: Handle structural insertion or collision chaining
        if (_buckets[bucketIndex] == null)
        {
            // The bucket cabinet is completely empty! Place the node down as the foundation.
            _buckets[bucketIndex] = new HashNode(key, value, rawHash);
        }
        else
        {
            // COLLISION DETECTED! The bucket is already occupied. 
            // We append the new item onto the head of the chain.
            Debug.LogWarning($"⚠️ [COLLISION] Bucket #{bucketIndex} is already occupied! Chaining '{key}' behind existing items.");
            
            HashNode newNode = new HashNode(key, value, rawHash);
            newNode.Next = _buckets[bucketIndex]; // Link the old chain behind our new node
            _buckets[bucketIndex] = newNode;      // Make this new node the main front entrance of the bucket
        }
    }

    /// <summary>
    /// Searches for an item directly via its bucket index, bypassing any full-array loops.
    /// </summary>
    public void Search(string key)
    {
        int rawHash = ComputeDeterministicHash(key);
        int bucketIndex = Math.Abs(rawHash) % _bucketCount;

        Debug.Log($"[LOOKUP] Hunting for '{key}'. Target Bucket Index determined instantly: #{bucketIndex}");

        HashNode currentElement = _buckets[bucketIndex];

        // Traverse only the narrow chain inside this specific isolated bucket cabinet
        while (currentElement != null)
        {
            if (currentElement.Key == key)
            {
                Debug.Log($"🎉 [FOUND] Success! Match discovered inside Bucket #{bucketIndex}. Payload: {currentElement.Value}");
                return;
            }
            currentElement = currentElement.Next; // Move down the link chain
        }

        Debug.LogError($"❌ [NOT FOUND] Key '{key}' does not exist inside Bucket #{bucketIndex}.");
    }

    /// <summary>
    /// Helper method to visually print out the contents of our warehouse cabinets.
    /// </summary>
    public void PrintStorageLayout()
    {
        for (int i = 0; i < _bucketCount; i++)
        {
            string bucketTrace = $"Bucket #{i}: ";
            HashNode node = _buckets[i];
            
            if (node == null)
            {
                bucketTrace += "[EMPTY FRAME]";
            }
            
            while (node != null)
            {
                bucketTrace += $"({node.Key} => {node.Value}) -> ";
                node = node.Next;
            }
            Debug.Log(bucketTrace);
        }
    }
}

```

---

### 5. Summary of the Architectural Shift

| Performance Dimension | Traditional Sequential List Layout | Hash Computation & Index Bucketing Architecture |
| --- | --- | --- |
| **Search Time Complexity** | $O(N)$ Linear Time: Must check every single item one-by-one from scratch. | $O(1)$ Constant Time: Computes index mathematically and jumps instantly straight to the target item. |
| **Lookup Mechanics** | Compares raw object values or string texts sequentially across memory. | Computes a lightweight 32-bit structural hash code and fits it into a fixed array size via modulo operations. |
| **Scaling Bottleneck** | As your game data scales to millions of items, lookups get slower and frame drops compound. | Performance remains lightning-fast regardless of size, provided your array size expands uniformly to limit internal collisions. |
| **Data Separation** | All data fragments share a single massive continuous block line. | Data is mathematically categorized and grouped into clean, isolated index lanes (**Buckets**). |


### [Unmanaged Memory Containers & Allocation Lifecycles](./13-6-Unmanaged-Memory-Containers-Allocation-Lifecycles.md)
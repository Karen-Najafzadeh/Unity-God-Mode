# Lists and Dictionaries: Managing Collections

In the **Unity God Mode** framework, **Lists** and **Dictionaries** are the primary "Containers" for managing multiple objects or pieces of data at once. While primitive types store individual values, these structures allow you to manage complex "Collections."

---

### 1. Lists: The Ordered Inventory
A **List** is a dynamic, ordered collection of items. Think of it like a grocery list where you can add items, remove items, and access them by their position (index).

#### The Problem: The Fixed Array
Before `List<T>`, we used Arrays (`int[]`). Arrays are fixed in size—if you have an array of 5 enemies and want to add a 6th, you have to create a *brand new, larger array* and copy all items over. It's incredibly inefficient.

#### The Solution: Dynamic Scaling
A `List` automatically resizes itself. You just `Add()` or `Remove()` items, and the engine manages the underlying memory.

#### Code Example
```csharp
using System.Collections.Generic; // REQUIRED for Lists
using UnityEngine;

public class Inventory : MonoBehaviour 
{
    public List<string> items = new List<string>();

    void Start() 
    {
        items.Add("Sword");
        items.Add("Shield");
        Debug.Log("First item: " + items[0]); // Accessing by index
    }
}
```

---

### 2. Dictionaries: The Fast Lookup
A **Dictionary** is a collection of Key-Value pairs. It’s like a phone book: you look up a *Name* (the Key) to find a *Phone Number* (the Value).

#### The Problem: Slow Searching
If you have a list of 1,000 players and need to find "Player_999", a `List` has to look at every item until it finds the right one. This is slow.

#### The Solution: O(1) Instant Lookup
A `Dictionary` uses a "Hash" algorithm to find the exact location of the value instantly, regardless of how large the collection is.

#### Code Example
```csharp
using System.Collections.Generic; // REQUIRED for Dictionaries
using UnityEngine;

public class Database : MonoBehaviour 
{
    // Key: String (Name), Value: Int (ID)
    public Dictionary<string, int> playerDatabase = new Dictionary<string, int>();

    void Start() 
    {
        playerDatabase.Add("Arka", 1);
        playerDatabase.Add("Kael", 2);
        
        Debug.Log("Arka's ID: " + playerDatabase["Arka"]);
    }
}
```

---

### Syntax Workshop: Lists and Dictionaries
This workshop practices adding, removing, and looking up data.

#### 1. The Exercise
Create `CollectionDemo.cs`.

```csharp
using System.Collections.Generic;
using UnityEngine;

public class CollectionDemo : MonoBehaviour 
{
    public List<string> partyMembers = new List<string>();
    public Dictionary<string, int> highScores = new Dictionary<string, int>();

    void Start() 
    {
        partyMembers.Add("Warrior");
        partyMembers.Add("Mage");
        Debug.Log("Party count: " + partyMembers.Count);

        highScores.Add("Arka", 1000);
        Debug.Log("Arka's score: " + highScores["Arka"]);
    }
}
```

#### 2. How to Verify
1.  **Attach:** Attach to a GameObject and Play.
2.  **Inspect:** The Console will log the list count and the dictionary value.

#### 3. Common Beginner Errors
*   **Dictionary KeyExistsException:** If you try to `Add()` a key that already exists, the Dictionary will crash. Use `TryAdd()` or check `ContainsKey()` first.
*   **List IndexOutOfRangeException:** Accessing `items[10]` when your list only has 3 items will crash the game. Always check `items.Count` before accessing an index!

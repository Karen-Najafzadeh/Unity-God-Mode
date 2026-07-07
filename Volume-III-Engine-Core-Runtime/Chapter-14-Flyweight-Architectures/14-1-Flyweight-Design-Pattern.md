<div align="center">

[ به فارسی بخوانید](./FA/14-1-Flyweight-Design-Pattern-FA.md)

</div>



# The Flyweight Design Pattern: ScriptableObjects as Unity’s Shared Blueprint

### 1. Introduction: The Art of the Shared Blueprint

Imagine you are building a vast battlefield of thousands of soldiers, weapons, enemies, and UI systems in Unity. If every entity carries its own complete copy of the same heavy configuration, your game will choke under duplicated data, redundant allocations, and brittle prefab inheritance.

The solution is not merely optimization. It is architectural sovereignty.

The Flyweight pattern teaches you to split an object into two realms:

1. **Intrinsic State** — the shared, stable blueprint that never changes per instance.
2. **Extrinsic State** — the unique, runtime context that changes from object to object.

In Unity, the most powerful native tool for this boundary is the **ScriptableObject**. A ScriptableObject is not just a data container; it is a shared asset, a project-level vault, a flyweight registry, and a clean way to decouple logic from scene objects. If MonoBehaviours are the bodies in the world, ScriptableObjects are the souls that remain eternal in the project database.

---

### 2. The Computer Science Lore: The Printing Press, Reimagined

Before computers, Johannes Gutenberg solved a similar problem. If a scribe wanted to print 1,000 books, copying every letter by hand would be absurd. Instead, he created reusable molds for each letter and arranged them into words, pages, and books.

The same principle applies to game architecture. A soldier’s base stats, weapon profile, enemy behavior rules, or item metadata should not be duplicated across every spawned instance. They should be forged once and referenced many times.

That is the flyweight idea in one sentence: keep the heavy, shared truth in one place, and let many lightweight objects point to it.

---

### 3. The Pattern in Code: A Bare-Bones Demonstration

Before diving deeper, let's see the core flyweight principle in pure C#:

#### The Naive Approach (MonoBehaviour)

If we naively make the data part of the MonoBehaviour:

```csharp

public class SoldierNaive : MonoBehaviour
{
    // These fields are duplicated for EVERY instance in the scene.
    // 10,000 soldiers = 10,000 copies of this data in memory.
    public string armorName = "Iron Plate";
    public float defenseValue = 50f;
    public float weight = 15f;
    public string material = "Steel";
    public string color = "Grey";
    
    public float currentHealth = 100f;
}
```

#### The Manual Flyweight Approach (Plain Data Class + MonoBehaviour)

```csharp
// 1. The INTRINSIC STATE: Shared data stored in a plain class
public class ArmorData
{
    public readonly string armorName;
    public readonly float defenseValue;
    public readonly float weight;
    public readonly string material;
    public readonly string color;

    public ArmorData(string name, float defense, float weight, string material, string color)
    {
        this.armorName = name;
        this.defenseValue = defense;
        this.weight = weight;
        this.material = material;
        this.color = color;
    }
}

// 2. The FLYWEIGHT FACTORY: Manages shared instances
public static class ArmorFactory
{
    private static System.Collections.Generic.Dictionary<string, ArmorData> _cache = new();

    public static ArmorData GetArmor(string name, float defense, float weight, string material, string color)
    {
        if (!_cache.ContainsKey(name))
            _cache[name] = new ArmorData(name, defense, weight, material, color);
        
        return _cache[name];
    }
}

// 3. The EXTRINSIC STATE: Lightweight usage in a MonoBehaviour
public class SoldierFlyweight : MonoBehaviour
{
    // Reference to the shared data (intrinsic)
    public ArmorData armorProfile; 
    
    // Instance-specific state (extrinsic)
    public float currentHealth = 100f;

    // Factory method to initialize (often called by an spawner script)
    public void Initialize(ArmorData data)
    {
        this.armorProfile = data;
    }
}
```

#### The Memory Impact

| Aspect | Naive | Flyweight |
|--------|-------|-----------|
| **Shared config copies** | 10,000 | 1 |
| **Unique state per soldier** | Still needed | Still needed |
| **Memory footprint** | $O(N)$ growth | Near constant |
| **Balance patch** | Edit 10,000 objects | Edit 1 blueprint |

This is the foundation. The object is not the source of truth. The blueprint is. Many lightweight references point to one shared authority. That is the entire pattern.


---

### 4. Why the Old Way Breaks: The MonoBehaviour Tax

A naive Unity architecture often puts everything on a MonoBehaviour attached to a prefab:

```csharp
using UnityEngine;

public class NaiveWeaponEntity : MonoBehaviour
{
    public string weaponName;
    public string description;
    public float baseDamage;
    public float attackSpeed;
    public byte[] highResTextureMatrix;
    public AudioClip swingSound;
    public GameObject impactParticlePrefab;

    public float currentDurability;
    public int currentItemLevel;
}
```

This looks harmless until you spawn hundreds or thousands of copies. Every instance now carries its own copy of the same configuration data. The more you clone, the more your memory profile balloons.

The hidden catastrophe is not only memory. It is also maintainability:

- Changing a balance value means editing many copies or many prefabs.
- Scene reloads can wipe runtime state unless you serialize it manually.
- Prefabs become bloated and fragile.
- Data becomes tightly welded to the visual object, making your architecture less reusable.

---

### 4. The Architectural Salvation: ScriptableObjects as the Shared Vault

A ScriptableObject lets you move the intrinsic data out of the scene object and into a project asset.

This is the Unity-native form of the Flyweight pattern.

Instead of storing the shared blueprint on each enemy, sword, or item instance, you create a single asset in your project and let every entity reference it.

The result is profound:

- One configuration asset can service thousands of runtime entities.
- Editing one asset updates the shared truth across the game.
- Instantiation becomes light, fast, and cheap.
- Your scene objects become thin runtime containers rather than data warehouses.

---

### 5. The Great Boundary: What Belongs on the Asset, and What Belongs on the Object

A Unity God must understand this rule clearly:

- Put shared, stable, repeated data on a ScriptableObject.
- Put unique per-object state on a MonoBehaviour or runtime component.

Good examples:

- Shared: weapon stats, enemy archetype data, level item definitions, event channels, UI configuration, reusable game variables.
- Unique: current health, current position, animation state, runtime cooldowns, local inventory count, scene-specific state.

This is the hidden law of the architecture: the asset is the truth, the component is the context.

---

### 6. The Core Implementation: Shared Data Asset + Lightweight Actor

#### The shared blueprint

```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "NewWeaponConfig", menuName = "SovereignEngine/Weapon Configuration")]
public class WeaponDataConfig : ScriptableObject
{
    [SerializeField] private string weaponName;
    [SerializeField] private float baseDamage;
    [SerializeField] private float attackSpeed;
    [SerializeField] private AudioClip swingSound;
    [SerializeField] private GameObject impactParticlePrefab;

    public string WeaponName => weaponName;
    public float BaseDamage => baseDamage;
    public float AttackSpeed => attackSpeed;
    public AudioClip SwingSound => swingSound;
    public GameObject ImpactParticlePrefab => impactParticlePrefab;
}
```

#### The lightweight runtime entity

```csharp
using UnityEngine;

public class WorldWeaponEntity : MonoBehaviour
{
    [SerializeField] private WeaponDataConfig configuration;

    public float currentDurability;
    public bool isEnchanted;

    public void ExecuteAttack()
    {
        Debug.Log($"Attacking with {configuration.WeaponName} dealing {configuration.BaseDamage} damage!");

        if (configuration.SwingSound != null)
        {
            AudioSource.PlayClipAtPoint(configuration.SwingSound, transform.position);
        }

        if (configuration.ImpactParticlePrefab != null)
        {
            Instantiate(configuration.ImpactParticlePrefab, transform.position, Quaternion.identity);
        }
    }
}
```

This is the flyweight architecture in its purest form: one shared config asset, many thin world objects pointing to it.

---

### 7. Hidden Secret: ScriptableObjects Are More Than Data Stores

Most developers think ScriptableObjects are just “shared variables.” That is only the surface.

They are actually three things at once:

1. **A data asset** — a serialized object stored in the project.
2. **A communication channel** — a central hub that many systems can subscribe to.
3. **A decoupling tool** — a way to make systems talk without directly referencing each other.

That means a ScriptableObject can become the foundation of:

- enemy archetype registries,
- inventory definitions,
- dialogue databases,
- global events,
- runtime state containers,
- gameplay balance tables,
- editor-driven configuration.

This is why they are so powerful in large Unity projects.

---

### 8. Jaw-Dropping Fact: One Asset Can Power an Entire Army

If you create a single enemy configuration asset and let 10,000 spawned units reference it, you are not just saving memory. You are changing the geometry of your architecture.

The old approach scales linearly with every instance. The flyweight approach stays near constant because the heavy shared data is not duplicated.

That is the real leap:

- Naive architecture: $O(N)$ memory growth per spawned instance.
- Flyweight architecture: near $O(1)$ shared blueprint cost.

A Unity God does not merely make things work. A Unity God makes them scale.

---

### 9. The Event Channel Pattern: Decoupling Without Singletons

One of the most dangerous habits in Unity is the overuse of singletons. They create hidden dependencies everywhere. A ScriptableObject can solve this more gracefully by acting as a global event bus.

```csharp
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "NewGameEvent", menuName = "SovereignEngine/Architecture/Game Event")]
public class SovereignGameEvent : ScriptableObject
{
    private readonly List<SovereignEventListener> listeners = new List<SovereignEventListener>();

    public void Raise()
    {
        for (int i = listeners.Count - 1; i >= 0; i--)
        {
            listeners[i].OnEventRaised();
        }
    }

    public void RegisterListener(SovereignEventListener listener)
    {
        if (!listeners.Contains(listener)) listeners.Add(listener);
    }

    public void UnregisterListener(SovereignEventListener listener)
    {
        if (listeners.Contains(listener)) listeners.Remove(listener);
    }
}
```

```csharp
using UnityEngine;
using UnityEngine.Events;

public class SovereignEventListener : MonoBehaviour
{
    [SerializeField] private SovereignGameEvent eventChannel;
    [SerializeField] private UnityEvent responseAction;

    private void OnEnable()
    {
        if (eventChannel != null) eventChannel.RegisterListener(this);
    }

    private void OnDisable()
    {
        if (eventChannel != null) eventChannel.UnregisterListener(this);
    }

    public void OnEventRaised()
    {
        responseAction?.Invoke();
    }
}
```

This is a jaw-dropping architectural shift. The player can trigger a game event without knowing who is listening. UI, sound, AI, and analytics can all react without tight coupling.

---

### 10. Hidden Secret: Shared Variables Are Powerful, but Dangerous if Misused

You can also use ScriptableObjects as shared runtime state containers:

```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "NewSharedFloat", menuName = "SovereignEngine/Variables/Shared Float")]
public class SharedFloatVariable : ScriptableObject
{
    [SerializeField] private float value;

    public float Value
    {
        get => value;
        set => this.value = value;
    }
}
```

This is useful for cross-system data like health, mana, difficulty, or mission state. But there is a hidden trap:

- If you make everything a shared variable, your game becomes a web of global state.
- Shared mutable data can create hard-to-debug coupling.
- ScriptableObjects are not magical save systems.

The discipline is this: use them for shared, intentionally global truths, not for every tiny piece of local state.

---

### 11. The Unified Pattern: Flyweight in One Glorious Diagram

A Unity God should think in this sequence:

1. Identify what data is truly shared.
2. Move that data into a ScriptableObject asset.
3. Keep the runtime object slim and contextual.
4. Let many objects reference the one shared asset.
5. Use the asset as a channel for communication and configuration.

That is the complete architecture.

---

### 12. Final Wisdom: The Unity God’s Rule

If you are building a serious project, never let your scene objects become data vaults.

Let them be:

- containers,
- controllers,
- interaction layers,
- runtime state holders.

Let your assets be:

- blueprints,
- registries,
- definitions,
- channels,
- shared truths.

That is the hidden secret of high-performance Unity architecture. The object is not the source of truth. The asset is.

And when you understand that, your game stops being a pile of duplicated objects and becomes a system of elegant, shared, scalable intelligence.



### [Next: Native C++ Allocations vs Managed Objects](./14-2-Native-C++-Allocations-vs-Managed-Objects.md)
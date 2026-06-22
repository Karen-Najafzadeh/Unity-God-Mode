# Generics: Parametric Generalization

In the **Unity God Mode** framework, **Generics** (`<T>`) are the ultimate tool for "DRY" (Don't Repeat Yourself) programming. They allow you to write logic once and apply it to *any data type*, without losing type safety.

---

### The CS Lore: The Universal Tool
Imagine you have a machine that sorts items. You don't want to build a "Sort Apples" machine, a "Sort Oranges" machine, and a "Sort Bananas" machine. You want to build *one* "Sort" machine that can handle *any fruit*. **Generics** are that machine. You define the "Sort" logic, and you tell the compiler: "This machine works with Type T." When you actually use it, you replace T with `Apple`, `Orange`, or `Banana`.

### The Original Problem: Type Safety vs. Flexibility
Before Generics, if you wanted a list of items, you had two bad options:
1.  **Strict Typing:** Create a `ListApple`, `ListOrange`, etc. (Impossible to maintain).
2.  **Weak Typing:** Use `List<object>`. This allows you to put anything in the list, but when you take an item *out*, the computer doesn't know what it is, requiring "Casting" (forcing it back to a type), which is slow and error-prone.

### The Solution: Generics
Generics allow you to define the *behavior* of the logic separately from the *data type* it operates on. You get the flexibility of `object` with the strictness of `Apple`.

---

### Syntax Workshop: Implementing Generics
This workshop shows how to create a generic container.

#### 1. The Exercise
Create a script `GenericDemo.cs`.

```csharp
using UnityEngine;

// <T> is our placeholder for a type
public class Container<T> 
{
    private T _content;

    public void Store(T item) { _content = item; }
    public T Retrieve() { return _content; }
}

public class GenericDemo : MonoBehaviour 
{
    void Start() 
    {
        // Now 'stringContainer' ONLY accepts strings!
        Container<string> stringContainer = new Container<string>();
        stringContainer.Store("Hello Generics");
        Debug.Log(stringContainer.Retrieve());
    }
}
```

#### 2. How to Verify
1.  **Attach:** Attach to a GameObject and Play.
2.  **Inspect:** The Console will log: `Hello Generics`.

#### 3. Common Beginner Errors
*   **Forgetting <T>:** When defining the class, you must include `<T>`. When *using* the class, you must specify the concrete type (e.g., `Container<string>`).
*   **Type Constraints:** Sometimes you want to restrict `T`. If you want to make sure `T` is always a `MonoBehaviour`, use `where T : MonoBehaviour` in the definition. Without this constraint, you can't access `transform` or other Unity features on `T`.

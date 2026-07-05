# Advanced Custom Types and Unmanaged Collections

Welcome to Chapter 13. This chapter bridges the gap between managed C# paradigms and bare-metal high-performance engineering in Unity. By mastering custom layouts, low-level bitwise operations, parametric safety, and unmanaged memory allocations, you will unlock the true execution speed of your hardware.

---

## Topics

### 1. [Bitwise Architecture & Binary Flags Systems](./13-1-Bitwise-Architecture-Binary-Flags-Systems.md)
* **Summary:** Dive into sub-atomic data packing. Learn how to replace expensive boolean arrays and heavy state classes with ultra-dense, zero-allocation binary mask systems (`[System.Flags]`) that the CPU can evaluate in a single clock cycle. This topic covers the core bitwise toolset: OR (`|`), AND (`&`), XOR (`^`), NOT (`~`), and Bit Shifting (`<<`, `>>`).

### 2. [Generic Metaprogramming & Parametric Generalization](./13-2-Generic-Metaprogramming-Parametric-Generalization.md)
* **Summary:** Master compile-time metaprogramming with Generics. Understand how C#'s runtime avoids the performance pitfalls of monomorphization (C++) and type erasure (Java) by precisely slicing native machine assembly for value types and pointer-optimized paths for reference types, ensuring 100% type safety with absolute zero boxing.

### 3. [Just-In-Time Compilation Profiles](./13-3-Just-In-Time-Compilation-Profiles.md)
* **Summary:** Understand the inner workings of JIT compilation. This topic details how the virtual machine translates intermediate language (IL) into native assembly at runtime, the performance impact of JIT compilation tiers, and how code patterns affect compilation performance in real-time.

### 4. [Covariance & Contravariance Variations](./13-4-Covariance-Contravariance-Variations.md)
* **Summary:** Demystify generic variance (`out` and `in` type parameters). Explore how it governs type safety, polymorphism, and compatibility within generic interfaces and delegates in Unity's architecture, and when to safely apply covariant or contravariant designs.

### 5. [Hash Code Computations & Index Bucketing](./13-5-Hash-Code-Computations-Index-Bucketing.md)
* **Summary:** Learn the mathematics behind efficient indexing. Explore how objects are uniquely hashed, how hash collisions are avoided, and how collections like dictionaries and hash sets use index bucketing to achieve constant-time $O(1)$ lookups.

### 6. [Unmanaged Memory Containers & Allocation Lifecycles](./13-6-Unmanaged-Memory-Containers-Allocation-Lifecycles.md)
* **Summary:** Step outside the safety of the Garbage Collector. Explore how to allocate, manage, and safely dispose of memory in unmanaged spaces (such as NativeContainers and custom buffers) using Unity's Burst compiler and Job system to bypass GC sweeps entirely and maximize hardware cache performance.

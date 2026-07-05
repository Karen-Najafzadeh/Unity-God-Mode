<div align="center">

[ به فارسی بخوانید](./README_FA.md)

</div>

Welcome to the **Unity God Mode** repository. This is not a collection of surface-level tutorials; it is a comprehensive technical odyssey designed to transform you from a "vibe coder" into a living Unity God. an engineer capable of building complex, production-grade systems from the molecular level up.

### The Prologue: Forging the Engine-Level Mindset



In the world of standard game development, most programmers are content to memorize APIs. They use `Vector3.MoveTowards` or `PlayerPrefs.SetInt` without ever questioning the mechanical "why" behind the function call. This repository exists to dismantle that black box. We do not just use the engine; we understand the silicon, the memory, and the mathematical laws that govern the virtual universe.

#### The CS Lore: From Human Thought to Machine Instructions
To understand "God Mode," you must first understand the **Computer Science Lore** of the execution environment. High-level C# code is written for human readability, but a microprocessor does not understand a "class" or a "method." It understands registers and binary instructions. Between your script and the hardware lies the **Common Language Runtime (CLR)**, a virtual machine that translates your "human-thoughts" into machine-executable reality. True mastery begins when you stop writing code for the compiler and start writing code for the hardware.

---

### The Curriculum Architecture

The journey is structured across eight distinct volumes, progressing from the foundational syntax of the C# language to the high-performance frontiers of Data-Oriented Design.

#### [Volume Zero: The Foundations of Syntax & Workflow](./Volume-0-Foundations/README.md)
Every master starts as a novice. Before we can manipulate the heap, we must master the syntax.
*   **The Original Problem:** Writing code that "just works" leads to unmaintainable, spaghetti-like logic.
*   **The Solution:** We begin with **Chapter 1: The Anatomy of a Program**, exploring namespaces, classes, and the "Component-Based Architecture" that makes Unity unique. You will learn how the **MonoBehaviour Lifecycle** (Awake, Start, Update) isn't just a set of magic methods, but a specific sequence of engine hooks that drive the simulation.

#### [Volume I: Mathematical Foundations & Physical Intuition](./Volume-I-Mathematical-Foundations/README.md)
Game engineering is the application of physics through the lens of linear algebra.
*   **The Lore:** We don't just "move things." We manipulate **Vector Spaces**.
*   **The Deep Dive:** We explore the **Dot Product** (Vector3.Dot) not as a math formula, but as a "Vision Engine" for AI detection and surface alignment. We master **Quaternions** to solve the dreaded **Gimbal Lock**—a phenomenon where three-dimensional rotation axes align and collapse, rendering your camera system useless.

#### [Volume II: Low-Level Memory Mechanics](./Volume-II-Memory-Mechanics/README.md)
Here, we enter the "GC Janitor" phase. You will learn to manage the **Stack** (fast, temporary, $O(1)$ allocation) versus the **Heap** (dynamic, fragmented, and dangerous).
*   **The Problem:** **Garbage Collector (GC) Spikes**. When you allocate too many objects, the engine must "stop the world" to clean up the mess, causing your game to stutter.
*   **The Solution:** Implementing **Object Pooling** and **Zero-Allocation** code patterns to ensure the hardware never has to stop to breathe.

#### [Volume III](./Volume-III-Engine-Core-Runtime/README.md) & [IV](./Volume-IV-Serialization-and-Cryptography/): [Data Architecture](./Volume-III-Engine-Core-Runtime/README.md) & [Persistence](./Volume-IV-Serialization-and-Cryptography/README.md)
Exploring the "nervous system" of the Unity engine, how it manages memory across the boundary of C# and C++, and how it handles the passage of time. alongside with the "memory" of your game—how to save progress, protect it from hackers, and ensure it works across different devices.


#### [Volume V](./Volume-V-Enterprise-Architecture/README.md) & [VI](./Volume-VI-Editor-Engineering/README.md): [Enterprise Patterns](./Volume-V-Enterprise-Architecture/README.md) & [Meta-Programming](./Volume-VI-Editor-Engineering/README.md)
We treat code as data. Through **Reflection** and **Automated Code Generation**, we eliminate "Magic Strings".
*   **The Original Problem:** Typing `PlayerPrefs.SetInt("PlayerScore", 10)` is prone to typos. If you misspell "PlayerScore," the code compiles but the game breaks at runtime.
*   **The Solution:** We use **StringBuilder** and **File I/O** to write scripts that *write other scripts*, generating type-safe APIs automatically based on your data definitions.

#### [Volume VII: The Engine-Programmer Tier (DOTS & Performance)](./Volume-VII-Performance-Engineering/README.md)
The final frontier. We move away from **Object-Oriented Programming** (which scatters data across RAM, causing "Cache Misses") and embrace **Data-Oriented Design (DOTS)**.
*   **Hardware Lore:** We optimize for the **CPU Cache**. By using the **Entity Component System (ECS)** and the **Burst Compiler**, we translate C# into ultra-optimized native assembly code that utilizes **SIMD (Single Instruction Multiple Data)**—allowing the processor to perform math on multiple vectors in a single clock cycle.

---

**Prepare for descent into the engine core.**

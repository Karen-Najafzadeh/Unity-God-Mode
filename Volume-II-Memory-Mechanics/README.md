<div align="center">

[ به فارسی بخوانید](./FA/README-FA.md)

</div>



# Volume II Memory Mechanics

Think of your computer's hardware as a hyper-fast, highly volatile manufacturing plant, and the Unity Engine as the factory supervisor. Volume II is all about Memory Mechanics, the art of structuring data so your hardware doesn't catch fire or stutter mid-game.

Here is the deep-dive architectural breakdown of Volume II.

---

### [Chapter 10: The Virtual Machine and Type System Allocations](./Chapter-10-Virtual-Machine-and-Type/README.md)

* **The CS Lore:** Early software was tied to specific hardware chips. Computer scientists solved this by inventing Virtual Machines, which act as software-based universal translators. They allow code to run seamlessly on a phone, console, or PC without rewriting it from scratch.
* **The Original Problem:** Computers use two internal workbenches to hold data. The Stack is an ultra-fast, organized desk with very limited space. The Heap is a massive, chaotic warehouse floor. If developers put everything on the fast desk, it overflows and crashes the game. If they put everything on the warehouse floor, searching for data wastes precious time and drops frame rates.
* **How it Solves the Problem:** The system automatically categorizes data based on its footprint. Small, simple numbers and true/false values are kept entirely on the fast local desk. Large, complex, or unpredictable game systems are stored in the warehouse, while a tiny placeholder index card pointing to its location is left on the desk.

### [Chapter 11: Memory Layout Optimization and Boxing Mechanics](./Chapter-11-Memory-Layout-and-Boxing/11-README.md)

* **The CS Lore:** To make programming easier, language designers created an architecture where every type of data can be treated as if it comes from one single, universal ancestor. This is called Type System Unification.
* **The Original Problem:** When you force a small data packet meant for the fast desk to hide inside a universal ancestor container, the system panics. It has to run out to the warehouse, manufacture a temporary cardboard shipping box, wrap the small data inside it, and track it. This process is called Boxing. Unwrapping it later requires customs checks. Doing this thousands of times a second creates severe micro-stutters in a video game.
* **How it Solves the Problem:** Instead of using universal containers that force data into boxes, developers use precise constraints. This tells the machine up front exactly what shape and size of raw data to expect, allowing the system to build optimized, direct processing pipelines that bypass the warehouse entirely.

### [Chapter 12: Automated Memory Management and Object Pooling](./Chapter-12-Automated-Memory-Management/README.md)

* **The CS Lore:** In older languages, programmers had to manually clean up every piece of data they threw away. Forgetting to do so would cause the computer to run out of RAM and crash. C# solved this by inventing an automated cleaner called the Garbage Collector.
* **The Original Problem:** The automated cleaner does not clean continuously because searching the warehouse takes time. Instead, it waits until trash builds up. When it finally wakes up, it forces the entire game to freeze in place while it sweeps through the system, creating a noticeable lag spike for the player.
* **How it Solves the Problem:** Instead of creating data and throwing it away to create trash, games use Object Pooling. Think of it as a lending library or a recycling drawer. When an item like a bullet or an enemy is done, it is simply hidden and tucked into a drawer. When a new one is needed, it is pulled back out and repurposed, preventing the automated cleaner from ever needing to trigger a freeze.

### [Chapter 13: Advanced Custom Types and Unmanaged Collections](./Chapter-13-Advanced-Custom-Types/README.md)

* **The CS Lore:** Unity is a hybrid engine. The gameplay logic you write operates in a safe, automated environment governed by C#. However, the core rendering engine and physical hardware instructions are built using raw, native C++ for extreme performance.
* **The Original Problem:** Every time the automated gameplay code needs to read data from the raw engine core, it must cross a translation boundary. This crossing acts like a slow toll bridge. Furthermore, standard arrays of data live in the regular warehouse, making them prone to the automatic cleaner's sudden lag spikes.
* **How it Solves the Problem:** Unity engineered Unmanaged Collections. These are specialized arrays that allocate blocks of memory directly on the native C++ side of the computer. Because the automated cleaner cannot see these blocks, they never cause lag spikes, allowing thousands of values to feed directly to the computer's physical processing threads instantly.
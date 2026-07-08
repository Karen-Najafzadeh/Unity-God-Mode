<div align="center">

[ نسخه فارسی جدید](./FA/README-FA.md)

</div>


# Vector Spaces and Linear Kinematics


In **Volume I, Chapter 5: Vector Spaces and Linear Kinematics**, we transition from the "grammar" of C# syntax into the fundamental laws of spatial reality. This chapter is designed to rebuild your engineering intuition by teaching you how a computer perceives and manipulates 3D space, moving you from simply "writing scripts" to acting as the architect of a physical simulation.

### [1. Scalars vs. Coordinate Vectors: The DNA of Space](/Volume-I-Mathematical-Foundations/Chapter-5-Vector-Spaces-and-Linear-Kinematics/5-1-Scalars-and-Coordinate-Vectors.md)
To understand vectors, we must first understand their simpler cousin: the **Scalar**.

*   **The CS Lore:** In the microprocessor's brain, a **Scalar** is a primitive value type (like an `int` or `float`) stored directly in a CPU register. A **Vector**, however, is a "packed array"—a collection of three floating-point numbers $(X, Y, Z)$ stored together so the hardware can perform "SIMD" (Single Instruction, Multiple Data) operations on them.
*   **The Original Problem:** A computer doesn't naturally understand "North" or "Forward." If you tell a computer a character is at "5," it doesn't know if that’s a location on a map or how fast the character is running.
*   **How it Solves the Problem:** We use **Coordinate Vectors** to separate "Nouns" from "Verbs" in space. 
    *   A **Position Vector** represents a specific point relative to the center of the universe $(0,0,0)$.
    *   A **Displacement Vector** represents a "Pure Direction"—it tells you how much to move, but not where you currently are.

### [2. Vector Mechanics: The Mathematics of Movement](/Volume-I-Mathematical-Foundations/Chapter-5-Vector-Spaces-and-Linear-Kinematics/5-2-Vector-Mechanics-Algebraic-Operations.md)
Once we have these vectors, we need to know how to "glue" them together using algebraic operations.

*   **Vector Addition:** When you add a Displacement Vector to a Position Vector, you calculate a new destination.
*   **Vector Subtraction (The AI Vision):** If you subtract the Guard’s position from the Player’s position, you get a "Steering Vector" that points directly from the Guard to the Player.

**Example: The AI Pursuit**
```csharp
// The mathematical formula for "Where do I look to find the player?"
// Target - Self = Direction
Vector3 vectorToPlayer = playerTransform.position - transform.position;
```

### [3. The Euclidean Distance Metric: Avoiding the "Math Tax"](/Volume-I-Mathematical-Foundations/Chapter-5-Vector-Spaces-and-Linear-Kinematics/5-3-Euclidean-Distance-Metrics.md)
Calculating how far away an enemy is might seem simple, but it carries a hidden "tax" on your computer's performance.

*   **The Original Problem:** The standard **Euclidean Distance** formula requires a **Square Root** calculation. In computer science, square roots are expensive because the CPU has to run a complex iterative process to find the answer.
*   **The "God Mode" Solution:** Instead of using `Vector3.magnitude`, we use `Vector3.sqrMagnitude`. This returns the distance *squared*. If you only need to know if an enemy is "close enough," comparing squared distances is an $O(1)$ hardware operation that is lightning-fast.

**Code Comparison:**
```csharp
// SLOW: Performs a square root calculation
if (Vector3.Distance(transform.position, player.position) < 5f) { ... }

// GOD MODE: Zero-allocation, high-speed comparison
float sqrDist = (player.position - transform.position).sqrMagnitude;
if (sqrDist < 25f) { // 25 is 5 squared. Faster for the CPU!
    Debug.Log("Player is within 5 meters.");
}
```

### [4. Vector Normalization: The "Pure Direction" Protocol](/Volume-I-Mathematical-Foundations/Chapter-5-Vector-Spaces-and-Linear-Kinematics/5-4-Vector-Normalization-Mechanics.md)
In game physics, you often want to know which way to look without caring how far away the target is.

*   **The Concept:** **Normalization** turns any vector into a **Unit Vector**—a vector with a length of exactly $1.0$.
*   **The Original Problem:** If a player moves diagonally (up and right at the same time), the raw math makes them move roughly $1.41$ times faster than if they move just "up." This is a classic bug in amateur games.
*   **The Solution:** By normalizing the movement vector, we ensure the player always moves at exactly $1.0$ unit per second, regardless of the direction they are facing.

### [5. Coordinate Spaces and Structural Transformations](/Volume-I-Mathematical-Foundations/Chapter-5-Vector-Spaces-and-Linear-Kinematics/5-5-Coordinate-Spaces-Structural-Transformations.md)
Finally, the chapter covers **Topologies**—how the engine organizes reality.

*   **The Lore:** Unity uses a **Left-Handed Coordinate System**. If you hold your left hand out, your thumb is $X$ (Right), your index finger is $Y$ (Up), and your middle finger is $Z$ (Forward).
*   **Hierarchy of Frames:** You will learn the difference between **Local Space** (where your hand is relative to your body) and **World Space** (where your hand is relative to the sun). Mastering these "Transformations" allows you to build complex objects like cars where the wheels stay attached while the vehicle spins.

### [6.Applied Kinematics & Constant Velocity Translation](./5-6-Applied-Kinematics-Constant-Velocity-Translation.md)
By the end of Chapter 5, you will be able to implement **Constant-Velocity Translation**, where objects move smoothly through space regardless of the game's frame rate. This sets the stage for **Chapter 6**, where we introduce **Trigonometry** to handle circles and rotations.

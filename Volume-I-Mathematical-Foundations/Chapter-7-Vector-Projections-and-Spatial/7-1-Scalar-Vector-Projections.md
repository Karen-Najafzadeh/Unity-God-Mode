# Scalar & Vector Projections (The Shadow Casters)

Welcome back to the architectural blueprint. Up until now, we’ve been building spaces, spinning them, and compounding them with matrices. Now, it’s time to focus on one of the most used spatial interrogation tools in game development: **Projections**.

In the real world, when you shine a flashlight on an object, it casts a flat shadow onto the wall behind it. In game math, **Projection** is that exact same process calculated with vectors. You take a vector flying through 3D space, drop a virtual flashlight above it, and flatten it onto another directional line.

There are two sides to this coin that you must master: **Scalar Projections** (the *length* of that shadow) and **Vector Projections** (the actual *directed shadow vector* itself). Let's tear them down.

---

## 1. The Core Concept: Dropping Perpendicular Shadows

To understand projections without getting lost in algebraic proofs, think of it as a spatial compression tool.

Imagine you have two vectors starting from the same origin point:

* Vector $\mathbf{b}$: A baseline direction stretched across the ground (like a landing strip).
* Vector $\mathbf{a}$: A target vector pointing up into the air (like an airplane taking off).

If you drop a perfectly straight line from the tip of vector $\mathbf{a}$ straight down onto vector $\mathbf{b}$ at a perfect $90^\circ$ right angle, you create a right-angled triangle.

* **Scalar Projection (The Magnitude):** This is a single float scalar number. It measures the exact length of the shadow that vector $\mathbf{a}$ casts onto the baseline direction of $\mathbf{b}$. It answers the question: *"How far along the direction of $\mathbf{b}$ does $\mathbf{a}$ actually reach?"*
* **Vector Projection (The Arrow):** This takes that scalar length and converts it back into a full 3D vector pointing in the exact direction of $\mathbf{b}$. It is the physical arrow representing the shadow itself.

---

## 2. The Mathematical Engine: Weaponizing the Dot Product

To calculate these projections at the silicon level, we don't use slow geometric ruler tools. We use the blindingly fast **Dot Product** ($\mathbf{a} \cdot \mathbf{b}$).

### A. The Scalar Projection Formula

To find just the length of the shadow, we take the dot product of vector $\mathbf{a}$ and multiply it by the **normalized direction** of $\mathbf{b}$ (written as $\hat{\mathbf{b}}$):

$$\text{scalar\_proj} = \mathbf{a} \cdot \hat{\mathbf{b}} = \frac{\mathbf{a} \cdot \mathbf{b}}{\Vert{}\mathbf{b}\Vert{}}$$

If $\mathbf{b}$ is already a normalized unit vector (length of 1), the math collapses into the ultimate optimization shortcut: the scalar projection is *just* the raw dot product $\mathbf{a} \cdot \mathbf{b}$!

### B. The Vector Projection Formula

To get the actual shadow vector, we take that scalar length we just found and multiply it by the normalized direction vector $\hat{\mathbf{b}}$ once again:

$$\text{proj}_{\mathbf{b}}(\mathbf{a}) = (\mathbf{a} \cdot \hat{\mathbf{b}}) \hat{\mathbf{b}} = \frac{\mathbf{a} \cdot \mathbf{b}}{\Vert{}\mathbf{b}\Vert{}^2} \mathbf{b}$$

### ⚠️ The God Mode Caution: Zero-Vector Hazards

In production physics engines, $\mathbf{b}$ can sometimes be a zero vector (e.g., a degenerate collision normal). Dividing by its magnitude will result in `NaN` (Not a Number), propagating silently through your transform calculations and breaking your game state.

Always sanitize your inputs for engine stability:

```csharp
// Robust projection
float lengthSq = Vector3.Dot(b, b);
if (lengthSq > float.Epsilon)
{
    Vector3 projection = (Vector3.Dot(a, b) / lengthSq) * b;
    // ...
}
else
{
    // Handle as zero vector or default
}
```

### 2.3 Practical Examples

#### Numerical Alignment Example
Imagine two vectors: $\mathbf{a} = (3, 4)$ and $\mathbf{b} = (5, 0)$.
The dot product is:
$$\mathbf{a} \cdot \mathbf{b} = (3 \times 5) + (4 \times 0) = 15$$
Since the result is a large positive number, we know these vectors are highly aligned and pointing in the same general direction. If we had $\mathbf{c} = (-5, 0)$, the dot product would be $\mathbf{a} \cdot \mathbf{c} = (3 \times -5) + (4 \times 0) = -15$, indicating they are pointing in opposing directions.

#### Programmatic Application: Field of View (FOV) Check
This is how you instantly determine if an enemy is in front of the player without expensive `Mathf.Acos` (inverse trig) calculations:

```csharp
public bool IsTargetInFOV(Transform player, Transform target, float fieldOfViewDegrees)
{
    Vector3 toTarget = (target.position - player.position).normalized;
    // Dot product between forward and toTarget
    float dot = Vector3.Dot(player.forward, toTarget);

    // Cosine of the angle: dot > cos(FOV / 2)
    // This is significantly faster than calculating the actual angle!
    return dot > Mathf.Cos(fieldOfViewDegrees * 0.5f * Mathf.Deg2Rad);
}
```

---

## 3. The Original Problem: Sliding Along Irregular Walls

Imagine you are building a physics system for a character controller, and the player runs diagonally straight into a solid concrete wall.

### The Broken Approach Without Projections

If you just stop all movement the moment the player touches the wall, the game will feel incredibly sticky, clunky, and broken. The player will freeze in place whenever they brush against a surface.

### The Projection Solution (The Sliding Vector)

To make movement feel silky smooth, you want the player to fluidly **slide** along the wall, converting their forward momentum into lateral movement parallel to the surface.

Using vector projection, you project the player's incoming velocity vector onto the wall's surface plane. This isolates the exact amount of velocity pushing *into* the wall (which you delete) and the exact amount of velocity running *parallel* to the wall (which you keep). This mathematical decomposition is called **Vector Rejection**, and it's how every major game engine handles clean collision sliding.

---

## 4. The CS Lore: Decomposing Forces in Shaders

In modern GPU graphics programming, scalar and vector projections are used millions of times per frame inside **Vertex and Fragment Shaders** to calculate advanced lighting and vertex manipulation.

### PBR (Physically Based Rendering) Light Splitting

When a light ray hits a rough surface, the shader needs to split that incoming light vector into two distinct structural components:

1. The **Specular Component** (the light bouncing cleanly off the surface into your eyes).
2. The **Diffuse Component** (the light penetrating into the micro-surface and scattering).

Shaders run rapid, low-level hardware dot product projections to instantly isolate the perpendicular alignment of the light vector relative to the vertex normal vector. Because modern GPUs have dedicated, single-cycle instructions for dot product math, this projection splitting costs virtually zero performance overhead, allowing games to compute complex material lighting in real-time.

---

## 5. Detailed Gameplay Examples

### Example A: The Racing Game Checkpoint (Track Progress)

You are building a racing game, and you need to know exactly how far along the track a car is to update the leaderboard UI, even if the driver is weaving wildly left and right across the asphalt.

* **The God Mode Method:** You create a baseline vector ($\mathbf{b}$) running down the exact center line of the track segment. You get the car's displacement vector ($\mathbf{a}$) from the start of the segment. By running a **Scalar Projection** of the car onto the track line, you extract a clean, single number showing exactly how many meters down the track the car has advanced, completely ignoring their sideways swaying.

```csharp
// Calculate progress along the track segment
Vector3 trackDirection = (segmentEnd.position - segmentStart.position).normalized;
Vector3 carDisplacement = car.position - segmentStart.position;

// Scalar projection: Dot product gives the magnitude of 'carDisplacement' along 'trackDirection'
float progressAlongTrack = Vector3.Dot(carDisplacement, trackDirection);

// Even if the car is 10 units to the side, 'progressAlongTrack' only cares about 
// distance relative to the track's forward direction.
```

### Example B: Gravity Alignment on Spherical Planets

You are building a space exploration game with small, spherical planets. When the player jumps, gravity should pull them straight down toward the center of the planet.

* **The God Mode Method:** You calculate the displacement vector from the planet's core to the player. That becomes your custom down-axis. To make the player walk forward naturally, you project their raw keyboard movement vector onto the tangent plane of the sphere using vector projection.

```csharp
// 1. Calculate gravity direction (center to player)
Vector3 gravityDown = (player.position - planetCore.position).normalized;

// 2. We want movement perpendicular to gravityDown (on the tangent plane)
// Vector Rejection: Movement - (Projection onto gravityDown)
Vector3 rawInput = transform.right * input.x + transform.forward * input.z;

// Isolate movement parallel to gravity
Vector3 movementIntoGravity = Vector3.Project(rawInput, gravityDown);

// Subtract it to get movement on the tangent plane
Vector3 alignedMovement = rawInput - movementIntoGravity;

// 'alignedMovement' is now guaranteed to be perpendicular to the surface normal,
// preventing the player from unintentionally walking "into" or "away" from the planet.
```

---

## 6. The Unity Code: Smooth Vector Flipping and Component Isolation

Unity's `Vector3` library actually includes built-in projection functions that handle this math cleanly. Here is how you use them to build a manual collision sliding pipeline.

```csharp
using UnityEngine;

public class ProjectionArchitect : MonoBehaviour
{
    [Header("Movement Configuration")]
    [SerializeField] private Vector3 rawInputVelocity = new Vector3(3f, 0f, 4f);

    void Update()
    {
        // Simulate a wall's surface normal vector (pointing straight out of a wall)
        Vector3 wallNormal = new Vector3(-1f, 0f, 0f).normalized; 
        
        // Visualize our raw intended velocity path (Yellow)
        Debug.DrawRay(transform.position, rawInputVelocity, Color.yellow);

        // ====================================================
        // 1. ISOLATE THE PENETRATION VECTOR (Vector Projection)
        // Find exactly how much force is pushing directly INTO the wall normal
        // ====================================================
        Vector3 penetrationVector = Vector3.Project(rawInputVelocity, wallNormal);
        
        // Visualize the destructive force vector (Red)
        Debug.DrawRay(transform.position, penetrationVector, Color.red);

        // ====================================================
        // 2. COMPUTE THE SLIDING VECTOR (Vector Rejection)
        // Subtract the penetration force from our raw velocity to get the parallel path
        // ====================================================
        Vector3 perfectSlidingVelocity = rawInputVelocity - penetrationVector;

        // Visualize the clean, optimized sliding velocity vector (Green)
        Debug.DrawRay(transform.position, perfectSlidingVelocity, Color.green);

        // ====================================================
        // 3. TRACK TRACKING PROGRESS (Scalar Projection)
        // Find the absolute scalar distance of our slide along a custom direction
        // ====================================================
        Vector3 forwardTrackDirection = new Vector3(0f, 0f, 1f);
        
        // Dot product shortcut: If the direction is normalized, Vector3.Dot returns the scalar projection length!
        float advanceDistance = Vector3.Dot(perfectSlidingVelocity, forwardTrackDirection);
    }
}

```

---

### [Next: Perpendicular Vector Generation and Orthogonality](./7-2-Perpendicular-Vector-Generation-Orthogonality.md)


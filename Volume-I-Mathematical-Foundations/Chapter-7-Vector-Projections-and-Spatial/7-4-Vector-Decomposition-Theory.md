# Vector Decomposition Theory (The Component Splitters)

---

[نسخه فارسی این مقاله را اینجا بخوانید](./FA/7-4-Vector-Decomposition-Theory-FA.md)



Welcome back to the architectural blueprint. When you are fighting complex physics bugs, writing custom physics engines, or handling high-performance character movement, a single vector is often too blunt of an instrument.

If a player dashes diagonally into an inclined ramp, their raw velocity vector contains a chaotic blend of three distinct physical desires: moving forward, sliding sideways, and fighting gravity. If you try to process that vector as a single, un-sliced entity, your player will jitter, stick, or fly off the ramp like a broken physics object.

Enter **Vector Decomposition Theory**. This is the art and science of taking a single vector flying through space and slicing it open into independent, perpendicular sub-vectors. By breaking a complex force down into clean component channels, you can modify, dampen, or amplify specific behaviors without corrupting the rest of the spatial motion. Let's look at how this works under the hood.

---

## 1. The Core Concept: Basis Vectors and the Orthogonal Canvas

Every time you read a `Vector3` position in Unity like $(3, 5, -2)$, you are already using a basic form of vector decomposition. You are looking at the vector split across the engine's global **Basis Vectors**:

$$\mathbf{v} = 3\hat{\mathbf{i}} + 5\hat{\mathbf{j}} - 2\hat{\mathbf{k}}$$

Where $\hat{\mathbf{i}}$, $\hat{\mathbf{j}}$, and $\hat{\mathbf{k}}$ are the standard unit directions for World $X$ (Right), World $Y$ (Up), and World $Z$ (Forward).

### The Pure Theory

Vector Decomposition states that **any vector $\mathbf{v}$ can be uniquely broken down into the sum of multiple component vectors, provided those component vectors point along linearly independent axes.**

$$\mathbf{v} = \mathbf{v}_1 + \mathbf{v}_2 + \mathbf{v}_3 + \dots$$

While you can technically decompose a vector across skewed, awkward angles, advanced game development relies heavily on **Orthogonal Decomposition**. By ensuring that your chosen axes meet at perfect $90^\circ$ angles, you decouple the components completely. What happens along Axis A has absolutely zero mathematical impact on Axis B.

---

## 2. The Mechanics: Projection and Rejection (The Slicing Machine)

To split a target vector $\mathbf{v}$ across a specific directional axis defined by a reference vector $\mathbf{u}$, you use a two-step mathematical machine consisting of **Vector Projection** and **Vector Rejection**.

### Step 1: Extract the Parallel Component (The Projection)

First, you project your target vector $\mathbf{v}$ cleanly down onto the reference vector $\mathbf{u}$. This isolates the exact amount of force acting *along* that specific line. We call this the parallel component ($\mathbf{v}_{\parallel}$):

$$\mathbf{v}_{\parallel} = \text{proj}_{\mathbf{u}}(\mathbf{v}) = \left( \frac{\mathbf{v} \cdot \mathbf{u}}{\Vert{}\mathbf{u}\Vert{}^2} \right) \mathbf{u}$$

### Step 2: Extract the Perpendicular Component (The Rejection)

Once you have the parallel component, finding the leftover force acting *perpendicular* to that axis (the rejection component, $\mathbf{v}_{\perp}$) is an absolute optimization freebie. You simply subtract the parallel shadow from the raw original vector:

$$\mathbf{v}_{\perp} = \mathbf{v} - \mathbf{v}_{\parallel}$$

By doing this, you have successfully decoupled the original vector into two pristine, orthogonal pieces:

$$\mathbf{v} = \mathbf{v}_{\parallel} + \mathbf{v}_{\perp}$$


 ### Numerical Example
 Consider a velocity vector $\mathbf{v} = (3, 4, 0)$ acting against a ramp defined by the directional axis $\mathbf{u} = (1, 1, 0)$.
 
 1.  **Project ($\mathbf{v}_{\parallel}$):**
     $\Vert\mathbf{u}\Vert^2 = 1^2 + 1^2 = 2$
     $\mathbf{v} \cdot \mathbf{u} = (3)(1) + (4)(1) + (0)(0) = 7$
     $\mathbf{v}_{\parallel} = (7 / 2) \cdot (1, 1, 0) = (3.5, 3.5, 0)$
 
 2.  **Reject ($\mathbf{v}_{\perp}$):**
     $\mathbf{v}_{\perp} = (3, 4, 0) - (3.5, 3.5, 0) = (-0.5, 0.5, 0) $
 
 The result is a parallel movement of $3.5$ along the ramp and a perpendicular force (rejection) of $-0.5$ pushing into/away from the
         surface.
 
 ### Unity Implementation
 ```csharp
 Vector3 v = new Vector3(3f, 4f, 0f);
 Vector3 u = new Vector3(1f, 1f, 0f); // Direction axis
 
 // Unity provides Vector3.Project(vector, onNormal)
 // Note: 'onNormal' expects a normalized vector for standard projection.
 Vector3 vParallel = Vector3.Project(v, u.normalized);
 Vector3 vPerpendicular = v - vParallel;
 ```
 

---

## 3. The Performance Trap: Re-Computing Normals vs. Cached Spaces

In a complex scene (like a vehicle suspension system tracking against uneven, procedurally generated terrain) the engine constantly needs to decompose forces relative to the ground's changing angles.

### The Bottleneck

If you manually run full dot products, vector divisions, and vector multiplications for every single tire collider against every jagged polygon normal on the main thread every frame, you run straight into a CPU serialization bottleneck.

### The Optimization Shortcut

Instead of constantly running the projection/rejection formulas from scratch, advanced architects use a spatial trick: **They convert the target vector into a specialized local coordinate matrix space.**

If you have a normalized surface coordinate space matrix (built out of the ground's Tangent, Bitangent, and Normal vectors), multiplying your world velocity vector by the transpose of that matrix instantly unpacks it into clean local components:

$$\mathbf{v}_{\text{local}} = M_{\text{TBN}}^T \cdot \mathbf{v}_{\text{world}}$$

Because the rows of an orthogonal matrix are perfectly perpendicular, this matrix multiplication completes the full 3D vector decomposition for all three axes simultaneously at the hardware level in a fraction of the clock cycles.

### Performance Heuristic: Dot vs. Matrix
A common mistake is using matrix multiplication for simple isolation. If you only need *one* component (e.g., the projection onto the normal), a simple dot product is significantly faster than constructing or multiplying by a transformation matrix. Reserve the full TBN matrix transformation for when you need to map a vector into *all three* axes of a new coordinate space simultaneously.

### A Note on Orthogonality Drifting
When performing continuous matrix transformations, floating-point precision errors will inevitably accumulate. Over time, your TBN basis vectors may lose their perfect $90^\circ$ orthogonality, causing your decomposed vectors to skew. In systems running these calculations every frame (like custom suspension), ensure you occasionally re-normalize and re-orthogonalize your basis vectors to prevent coordinate space degradation.

---

## 4. The CS Lore: Gram-Schmidt Vector Space Generation

When writing low-level procedural systems, like an automated camera system that needs to wrap around an asset while maintaining custom framing constraints, you often start with just a single arbitrary look-direction. To turn that single vector into a clean, fully functional 3D coordinate canvas, you use **Gram-Schmidt Orthogonalization**.

Gram-Schmidt is a classic piece of computer science lore. It is a mathematical conveyor belt that takes a collection of random, non-perpendicular vectors and systematically strips away their overlapping alignments until they form a pristine, orthogonal grid.

1. You take the first vector and set it as your base axis.
2. You take the second vector, project it onto the first, and subtract that projection out. The second vector instantly snaps to a perfect $90^\circ$ angle relative to the first.
3. You take the third vector, project it onto both the first and second axes, and subtract both projections out.

Suddenly, you have engineered a flawless, custom 3D vector space canvas out of absolute chaos.

### Unity/C# Implementation: Gram-Schmidt
```csharp
public static void GramSchmidt(Vector3 a, Vector3 b, Vector3 c, 
                               out Vector3 e1, out Vector3 e2, out Vector3 e3)
{
    // 1. Normalize the first vector
    e1 = a.normalized;

    // 2. Project b onto e1, subtract, and normalize
    Vector3 bParallel = Vector3.Project(b, e1);
    e2 = (b - bParallel).normalized;

    // 3. Project c onto e1 and e2, subtract, and normalize
    Vector3 cParallelE1 = Vector3.Project(c, e1);
    Vector3 cParallelE2 = Vector3.Project(c, e2);
    e3 = (c - cParallelE1 - cParallelE2).normalized;
}
```

---

## 5. Detailed Gameplay Examples

### Example A: The Racing Game Drifting Meter

You are building an arcade racing game, and you need to award the player style points based on how hard they are drifting horizontally through a sharp turn, while ignoring their forward engine speed.

* **The God Mode Method:** You read the car's absolute world velocity vector ($\mathbf{v}$). You query the car's forward chassis direction vector ($\mathbf{f}$). By running a vector decomposition, you extract $\mathbf{v}_{\parallel}$ (the forward speed) and $\mathbf{v}_{\perp}$ (the lateral sliding speed). The magnitude of $\mathbf{v}_{\perp}$ tells you exactly how fast the car is sliding sideways relative to where its tires are pointing, giving you a mathematically pure metric to feed straight into your drift score UI.

```csharp
// Inside your Car Controller
Vector3 velocity = rb.velocity;
Vector3 forwardDir = transform.forward;

// Decompose: Parallel (forward movement) and Perpendicular (lateral drift)
Vector3 vParallel = Vector3.Project(velocity, forwardDir);
Vector3 vLateral = velocity - vParallel;

float driftMagnitude = vLateral.magnitude;
// Now use driftMagnitude to drive your drift-score UI
```

### Example B: The Wind-Blown Glider (Aerodynamics)

You are building a hang-glider mechanic. When the player glides through a thermal updraft or a crosswind, the wind shouldn't just push the glider like a heavy box. The wings should convert a portion of that wind into upward lift and a portion into drag.

* **The God Mode Method:** You take the incoming wind force vector and decompose it relative to the glider's wing orientation plane. The component pushing perpendicular to the wing is converted straight into vertical **Lift**, while the component running parallel along the wing surface is processed as aerodynamic **Drag**. By splitting the wind vector apart, you can tune the physics of flight with absolute precision.

```csharp
// Inside your Glider Controller
Vector3 windVelocity = GetWindVelocity();
Vector3 wingNormal = transform.up; // Assume wing plane is aligned with up

// Project onto wing normal to get Lift direction
Vector3 liftForce = Vector3.Project(windVelocity, wingNormal);
// Rejection gives Drag force along the wing plane
Vector3 dragForce = windVelocity - liftForce;

// Apply forces with specific multipliers
rb.AddForce(liftForce * liftMultiplier, ForceMode.Force);
rb.AddForce(dragForce * dragMultiplier, ForceMode.Force);
```

---

## 6. The Unity Code: High-Performance Force Decomposer

Here is a clean, production-ready C# script demonstrating how to decompose an actor's incoming movement velocity across an arbitrary surface incline, completely isolating their climbing force from their sliding force.

```csharp
using UnityEngine;

public class VectorDecompositionArchitect : MonoBehaviour
{
    [Header("Movement Vectors")]
    [SerializeField] private Vector3 worldVelocity = new Vector3(5f, -2f, 3f);

    void Update()
    {
        // Simulate an inclined ground slope normal vector
        Vector3 slopeNormal = new Vector3(0.2f, 0.96f, 0.1f).normalized;

        // Visualize the raw incoming velocity path (Yellow)
        Debug.DrawRay(transform.position, worldVelocity, Color.yellow);

        // ====================================================
        // 1. ISOLATE THE PERPENDICULAR PENETRATION (Projection)
        // Find exactly how much force is pushing straight into the slope
        // ====================================================
        // Optimization: Since slopeNormal is normalized, we use the dot product shortcut
        float perpendicularMagnitude = Vector3.Dot(worldVelocity, slopeNormal);
        Vector3 velocityPerpendicular = slopeNormal * perpendicularMagnitude;

        // Visualize the perpendicular force component (Red)
        Debug.DrawRay(transform.position, velocityPerpendicular, Color.red);

        // ====================================================
        // 2. ISOLATE THE PARALLEL SLIDING VALUE (Rejection)
        // Subtract the perpendicular block to find the perfect tangential velocity
        // ====================================================
        Vector3 velocityParallel = worldVelocity - velocityPerpendicular;

        // Visualize the parallel force component running along the slope surface (Green)
        Debug.DrawRay(transform.position, velocityParallel, Color.green);
        
        // At this point, velocityParallel + velocityPerpendicular perfectly equals worldVelocity!
    }
}

```

---

### [Physics of Elastic Collisions Structural Reflections](./7-5-Physics-of-Elastic-Collisions-Structural-Reflections.md) 
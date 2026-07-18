# Physics of Elastic Collisions & Structural Reflections


---

[نسخه فارسی این مقاله را اینجا بخوانید](./FA/7-5-Physics-of-Elastic-Collisions-Structural-Reflections-FA.md)


Welcome back to the architectural blueprint. Up until now, we’ve used vector decomposition to split forces apart into clean, perpendicular channels. Now, it’s time to take those split vectors and smash them against solid boundaries.

Whether you are engineering a high-speed laser reflection, a bouncing grenade trajectory, or a custom low-overhead rigid-body physics solver, you must master the mechanics of **Elastic Collisions** and **Structural Reflections**.

If you try to implement reflections by simply multiplying velocities by $-1$, your physics objects will clip through geometry, lose energy on flat surfaces, or behave like glitchy black boxes. Let’s look at the deep mathematical mechanics and hardware shortcuts that govern structural reflections at the silicon level.

---

## 1. The Core Concept: The Law of Reflection

In pure kinematics, a reflection is a spatial operation that flips a vector across a boundary axis. To understand this in 3D game space, imagine a projectile hitting a flat, immovable wall.

[![Physics of Elastic Collisions](https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcSgLup3hGa7sFOpDoy3tI3pb8as8sbxPNN3kugWsBoZ9ugYzxReH7bCTHFfSALqboq7Emsm52tZH2nkOMU)](./7-5-Physics-of-Elastic-Collisions-Structural-Reflections.md)



Every reflection involves three structural components:

* **The Incident Vector ($\mathbf{I}$):** The incoming velocity arrow representing where the object *wants* to go.
* **The Normal Vector ($\mathbf{N}$):** The normalized surface vector pointing straight out of the wall face at a perfect $90^\circ$ angle.
* **The Reflected Vector ($\mathbf{R}$):** The outgoing velocity arrow after the impact.

The fundamental law of geometric reflection states that **the angle of incidence equals the angle of reflection**. To compute this without touchy, expensive trigonometric functions ($\sin$, $\cos$), we use the absolute king of graphics optimizations: **Vector Decomposition**.

---

## 2. The Mathematical Engine: Deriving the Reflection Formula

To calculate the outgoing path $\mathbf{R}$, we decompose the incoming vector $\mathbf{I}$ into two components relative to the wall normal $\mathbf{N}$:

1. A component **parallel** to the wall surface (which passes through completely unaffected).
2. A component **perpendicular** to the wall surface (which squashes straight into the wall normal).

$$\mathbf{I} = \mathbf{I}_{\parallel} + \mathbf{I}_{\perp}$$

When an elastic collision occurs, the wall exerts an equal and opposite normal force. The parallel velocity running along the wall stays identical, but the perpendicular penetration velocity is completely reversed:

$$\mathbf{R} = \mathbf{I}_{\parallel} - \mathbf{I}_{\perp}$$

Since we know from decomposition theory that the perpendicular shadow is $\mathbf{I}_{\perp} = (\mathbf{I} \cdot \mathbf{N})\mathbf{N}$ (assuming $\mathbf{N}$ is normalized), we can substitute it into our equation:

$$\mathbf{R} = (\mathbf{I} - (\mathbf{I} \cdot \mathbf{N})\mathbf{N}) - (\mathbf{I} \cdot \mathbf{N})\mathbf{N}$$

Collapsing those matching terms gives us the legendary, ultra-optimized **Standard Reflection Formula**:

$$\mathbf{R} = \mathbf{I} - 2(\mathbf{I} \cdot \mathbf{N})\mathbf{N}$$

---

## 3. The Real-World Factor: The Coefficient of Restitution ($e$)

The standard reflection formula assumes a *perfectly elastic* collision—meaning no energy is lost, and the object bounces back with $100\%$ of its incoming speed. In actual game design, perfectly elastic collisions look unnaturally floaty, like a glitchy arcade game.

To introduce physical realism, we introduce a scalar scalar parameter called the **Coefficient of Restitution ($e$)**.

```
e = 1.0  ===> Perfectly Elastic (Bounces back with full energy)
e = 0.5  ===> Partially Elastic (Loses half its perpendicular speed; generic bouncy ball)
e = 0.0  ===> Perfectly Inelastic (Loses all perpendicular speed; sticks to the wall completely)

```

By injecting this factor into our normal force channel, we get the **Impulse Reflection Formula**:

$$\mathbf{R} = \mathbf{I} - (1 + e)(\mathbf{I} \cdot \mathbf{N})\mathbf{N}$$

Notice that this parameter *only* dampens the force hitting directly into the wall. The sliding velocity running parallel to the wall remains fully intact, perfectly mirroring the real-world physics of friction and materials.

---

### A Note on Unity's Built-in `Vector3.Reflect`
Unity provides a built-in `Vector3.Reflect(incident, normal)` method. While convenient, this is a simple wrapper for the standard $R = I - 2(I \cdot N)N$ formula. It does **not** support restitution ($e$) or friction. In a high-performance custom physics system, you will almost always need to rebuild the formula manually to accommodate these energy-loss parameters.

---

## 4. Advanced Considerations: Friction, Performance, and Edge Cases

### Friction and Tangential Dampening
The standard reflection formula preserves 100% of the parallel velocity. However, real-world collisions lose energy tangentially due to friction. To simulate this, introduce a friction scalar $f$ (where $f=0$ is slippery, $f=1$ is sticky):

$$\mathbf{R} = (1 - f)\mathbf{I}_{\parallel} - e\mathbf{I}_{\perp}$$

By applying a friction coefficient to the tangential component, you can differentiate between bouncing off ice vs. rough concrete.

### Performance Heuristic: Surface Material Caching
If you are running hundreds of reflections per frame (e.g., bouncing complex debris), do not hard-code physics parameters. Instead, cache surface properties using `PhysicMaterial`. Retrieve the material's bounciness and friction values from the `RaycastHit.collider.sharedMaterial` to drive your restitution ($e$) and friction ($f$) parameters dynamically.

### Edge Case: The Corner Trap (Non-Convex Geometry)
Reflecting off a flat wall is mathematically robust. Reflecting off sharp concave corners (where two planes meet) is dangerous. If your collision detection is imprecise, you may resolve a hit on the wrong normal, causing the object to flip into the geometry. 

**God Mode Tip:** Always add a small "skin width" or epsilon-offset to the collision normal processing to ensure the object stays slightly outside the geometry, or perform a secondary "corner check" raycast if the hit is within a tight margin of a mesh vertex.

---

## 5. The Performance Trap: Tunneling and the Flash Glitch

When coding manual collision reflections on the CPU, developers frequently run into a terrifying bug called **Tunneling** (or the "Ghost Wall" glitch).

### The Disaster Scenario

If a projectile is moving incredibly fast (e.g., $100\text{ m/s}$), and your game is running at $60\text{ frames per second}$, the object travels roughly $1.6\text{ meters}$ in a single frame. If your wall is only $0.5\text{ meters}$ thick, the object can pass completely through the wall between frame updates.

When the next frame ticks, the engine detects that the object is now stuck *inside* the wall geometry. If you blindly apply the reflection formula while the object is buried past the boundary plane, the math will invert, catching the object in an infinite positional loop, or firing it backward deeper into the map's interior voids.

### The Architectural Fix

Advanced developers implement **Continuous Collision Detection (CCD)** using a parametric line sweep. Instead of checking the object's static position at Frame B, you construct a ray from Frame A to Frame B.

If that ray intersects a polygon, you extract the precise **Time of Impact ($t_{\text{hit}}$)**. You move the object forward exactly to that contact spot, execute your reflection formula, and then use the remaining frame time fraction ($1 - t_{\text{hit}}$) to finish processing the bounce path.

---

## 5. Detailed Gameplay Examples

### Example A: The Ricochet Laser Beam

You are building a tactical sci-fi shooter where players shoot high-tech energy rifles. The laser beams should bounce off metallic surfaces, allowing players to pull off advanced trick-shots around tight corners.

* **The God Mode Method:** When the player fires, you execute a world space `Physics.Raycast`. The hit structure returns the exact contact point and the geometric surface normal ($\mathbf{N}$). You grab the ray's incoming direction vector ($\mathbf{I}$), feed it into the standard reflection formula, and use that outgoing vector $\mathbf{R}$ to immediately fire a secondary raycast out from the hit position. Repeating this loop in a brief cycle allows you to draw multi-bounce laser paths instantly.

### Example B: The Pinball Bumper (Additive Impulse)

You are building a classic arcade pinball game. When the ball rolls into a glowing circular bumper, it shouldn't just bounce off passively—the bumper should actively *blast* the ball outward with explosive force.

* **The God Mode Method:** You use the reflection formula to find the baseline bouncing vector channel. However, instead of using a standard coefficient of restitution ($e \le 1$), you purposefully force $e = 2.5$. By setting the restitution value greater than $1$, the equation generates a massive, additive kinetic impulse. The bumper actively injects energy back into the physics system, throwing the ball across the board at high velocity.

---

## 6. The Unity Code: High-Performance Parametric Bounce Engine

Here is a clean, production-ready Unity C# script demonstrating how to calculate manual, frame-rate independent vector reflections with an adjustable coefficient of restitution and continuous trace correction.

```csharp
using UnityEngine;

public class StructuralReflectionEngine : MonoBehaviour
{
    [Header("Bumper Configuration")]
    [SerializeField] private Vector3 velocity = new Vector3(15f, -5f, 0f);
    [Range(0f, 2f)] [SerializeField] private float restitution = 0.8f;

    void Update()
    {
        float frameTime = Time.deltaTime;
        Vector3 currentPosition = transform.position;
        Vector3 intendedMovement = velocity * frameTime;

        // 1. EXECUTE PARAMETRIC CONTINUOUS TRACE (Prevent Tunneling)
        if (Physics.Raycast(currentPosition, intendedMovement.normalized, out RaycastHit hit, intendedMovement.magnitude))
        {
            // Move the object directly to the exact point of surface contact
            transform.position = hit.point;

            // 2. EXTRACT INCOMING DIRECTION
            Vector3 incidentVector = velocity;

            // 3. APPLY THE IMPULSE REFLECTION FORMULA
            // R = I - (1 + e) * (I . N) * N
            float dotProduct = Vector3.Dot(incidentVector, hit.normal);
            Vector3 reflectedVelocity = incidentVector - (1f + restitution) * dotProduct * hit.normal;

            // Update our persistent velocity field to use the new bounce vector
            velocity = reflectedVelocity;

            // Calculate leftover frame time fraction to complete the movement path
            float distanceTraveled = hit.distance;
            float totalIntendedDistance = intendedMovement.magnitude;
            float remainingFraction = 1f - (distanceTraveled / totalIntendedDistance);

            // Push the object out along its new path using the remaining time slice
            transform.position += velocity * (frameTime * remainingFraction);

            // Visualize the impact normal (Blue) and outgoing bounce path (Green)
            Debug.DrawRay(hit.point, hit.normal * 2f, Color.blue, 1f);
            Debug.DrawRay(hit.point, velocity, Color.green, 1f);
        }
        else
        {
            // No obstruction hit; move forward along standard linear trajectory
            transform.position += intendedMovement;
            Debug.DrawRay(currentPosition, velocity, Color.yellow);
        }
    }
}

```

---

### [Next: Chapter 8 Interpolation and Rotational](/Volume-I-Mathematical-Foundations/Chapter-8-Interpolation-and-Rotational/README.md)

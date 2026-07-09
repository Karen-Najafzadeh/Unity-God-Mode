


# Trigonometric Motion & Angular Projections
---

[نسخه فارسی این مقاله را اینجا بخوانید](./FA/6-1-Trigonometric-Motion-Angular-Projections-FA.md)


Welcome back to the architectural blueprint. Up until now, our digital universe has been rigidly linear. We’ve moved objects in straight paths forward, backward, left, and right. But the real world, and any game world worth its salt, isn't made entirely of straight grid lines. Nature curves. It waves, it spins, it oscillates, and it arcs.

To break free from the prison of straight lines and step into true "God Mode" over your engine, you must master **Trigonometric Motion** and **Angular Projections**. This is the art of using angles to project vectors onto curves, creating flawless circular paths, organic waves, and clean rotational mathematics.

### A Note on Angles: Degrees vs. Radians

Before we dive in, we must distinguish how we measure rotation:

*   **Degrees ($^\circ$):** An arbitrary unit where a full circle is divided into 360 equal parts. It is intuitive for human visualization but not naturally linked to the geometry of the circle itself.
*   **Radians (rad):** A natural unit based on the circle's geometry. One radian is the angle created when the arc length along the circumference is exactly equal to the circle's radius.

**The Relationship:**
A full circle is $360^\circ$ or $2\pi$ radians. Therefore:
$$\pi \text{ radians} = 180^\circ$$
To convert:
*   $\text{Radians} = \text{Degrees} \times \frac{\pi}{180}$
*   $\text{Degrees} = \text{Radians} \times \frac{180}{\pi}$

---

## 1. The Core Concept: The Unit Circle Playground

To understand angular projections, we return to a geometric masterpiece: the **Unit Circle**.

Imagine a unit circle (radius=1) centered at (0,0). A point $P$ at angle $\theta$ on the circle has coordinates $(\cos\theta, \sin\theta)$.

```
          +Y (Sine axis)
             ^
             |      P(cosθ, sinθ)
             |    *
             |  / |
             | /  | sinθ
             |/ θ |
  -----------+----+-----------> +X (Cosine axis)
             |    cosθ
```

*   **$\cos\theta$ (Cosine):** The length of the horizontal segment from the origin to the projection point $P$ on the X-axis.
*   **$\sin\theta$ (Sine):** The length of the vertical segment from the X-axis to the point $P$.

### The Geometry of Arcs: Arc Length ($s$)

The fundamental link between an angle $\theta$ and its distance along the circumference is the **Arc Length ($s$)**.

*   **The Formula:** $s = r\theta$ (where $\theta$ must be in radians and $r$ is the radius).

**Derivation (Proof):**
A full circle has a circumference $C = 2\pi r$ and corresponds to a full rotation of $2\pi$ radians. The ratio of the arc length $s$ to the total circumference $C$ is proportional to the ratio of the angle $\theta$ to the full circle angle $2\pi$:

$$\frac{s}{2\pi r} = \frac{\theta}{2\pi}$$

Multiplying both sides by $2\pi r$ yields:
$$s = r\theta$$

**GameDev Application:**
This formula is critical for smooth animation. If you want to move an object along a circular path at a constant *linear speed* ($v$), you can use arc length to calculate the necessary angular velocity ($\omega = d\theta/dt$):
$$v = \frac{ds}{dt} = r \frac{d\theta}{dt} = r\omega \implies \omega = \frac{v}{r}$$

### Extending to Reciprocal Functions (Sec, Csc, Tan, Cot)

Beyond the fundamental sine and cosine, we have four additional trigonometric functions derived from them.

**The Reciprocal Functions:**
*   **$\sec\theta$ (Secant):** The reciprocal of cosine; $\sec\theta = \frac{1}{\cos\theta}$.
*   **$\csc\theta$ (Cosecant):** The reciprocal of sine; $\csc\theta = \frac{1}{\sin\theta}$.

**The Tangent/Cotangent Functions:**
We can also define **Tangent** ($\tan$) and **Cotangent** ($\cot$) geometrically by observing where the ray at angle $\theta$ intersects lines tangent to the unit circle.

*   **$\tan\theta$ (Tangent):** Extend the radius at angle $\theta$ until it intersects the vertical line $x=1$. The height of this intersection point $T(1, \tan\theta)$ is $\tan\theta$.
*   **$\cot\theta$ (Cotangent):** Extend the radius at angle $\theta$ until it intersects the horizontal line $y=1$. The horizontal distance of this intersection point $C(\cot\theta, 1)$ from the Y-axis is $\cot\theta$.

```
           | y=1
    _______|______ C(cotθ, 1)
           |    /
           |  /
           |/θ
  ---------+---------->
          /|
         / |
        /  | x=1
       /   | T(1, tanθ)
```

By bundling these projections, you transform an abstract angular value into a clean, normalized direction or scalar in 2D space.


---

## 2. The Original Problem: The Jagged, Hardcoded Turn

Imagine you are building a classic top-down space shooter, and you want an alien ship to fly in a smooth, majestic loop-de-loop circle around the player.

### The Nightmare Without Trigonometry

Without angular projections, you are forced to hardcode linear checkpoints. You tell the ship: *"Move right for 2 seconds, then move up-right for 2 seconds, then move up for 2 seconds..."*

* **The Result:** The movement looks incredibly jagged, robotic, and unnatural.
* **The Maintenance Hell:** If you want to change how fast the alien spins, or make the circle wider, you have to manually recalculate every single one of those linear checkpoints by hand. Your codebase becomes a rigid cage.

---

## 3. How It Solves the Problem: The Continuous Spatial Wave

Trigonometry solves this by providing a continuous, fluid pipeline between **Time**, **Angles**, and **Vectors**.

Instead of hardcoding positions, you tell the engine: *"Take the current time, treat it as an endlessly increasing angle, and project that angle onto the Unit Circle."*

Because sine and cosine naturally oscillate in smooth, beautiful waves between `-1` and `1`, your alien ship moves with flawless, mathematically perfect organic curvature.

* Want to make the circle bigger? Multiply the resulting vector by a **Radius Scalar**.
* Want to make it spin faster? Multiply the time variable before passing it to the trig functions.

You control the entire simulation with just a couple of adjustable knobs.

---

## 4. The CS Lore: Look-Up Tables vs. Taylor Series Hardware

How does a microprocessor (which at its core can only perform basic addition and bit shifts) instantly calculate the complex curving value of a sine wave?

### The Old School Way: LUTs (Look-Up Tables)

In early gaming hardware (like the Sega Genesis or the original PlayStation), calculating a sine or cosine on the fly was far too computationally expensive. To bypass this, developers used a classic memory hack: a **Look-Up Table (LUT)**. They would pre-calculate the sine values for every whole angle from 0 to 360 degrees and store them in an array in the game's memory. When the code asked for `sin(45)`, the CPU didn't do math; it just grabbed the 45th index out of a pre-baked array. It was blindingly fast but sacrificed precision.

### The Modern Way: CORDIC & Taylor Series Hardware

Modern microprocessors and modern graphics cards handle trigonometry using hardware-level algorithms called **CORDIC** or polynomial approximations (**Taylor Series**). 

The Taylor series allows us to represent trigonometric functions as an infinite sum of powers, which is highly efficient for computational approximation:

$$\sin(x) = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \cdots$$

$$\cos(x) = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \cdots$$

> **Reminder: What is a Factorial (!)?**
> The factorial of a non-negative integer $n$, denoted by $n!$, is the product of all positive integers less than or equal to $n$.
> For example: $3! = 3 \times 2 \times 1 = 6$, and $5! = 5 \times 4 \times 3 \times 2 \times 1 = 120$.

### Taylor Series Numerical Example

Let's approximate $\sin(0.5)$ radians ($\approx 28.6^\circ$):

Using the first two terms:
$$\sin(0.5) \approx 0.5 - \frac{0.5^3}{3!} = 0.5 - \frac{0.125}{6} \approx 0.5 - 0.02083 = 0.47917$$

(The actual value is $\approx 0.47942$, showing the series converges rapidly.)

### Important Trigonometric Values (Lookup Table Reference)

While modern hardware computes these on the fly, understanding these key values is fundamental for mental mapping and engine optimization:

| Degrees | Radians | Sin | Cos | Tan | Cot |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | 0 | 0 | 1 | 0 | Undefined |
| 30 | $\pi/6$ | 0.5 | $\approx 0.866$ | $\approx 0.577$ | $\approx 1.732$ |
| 45 | $\pi/4$ | $\approx 0.707$ | $\approx 0.707$ | 1 | 1 |
| 60 | $\pi/3$ | $\approx 0.866$ | 0.5 | $\approx 1.732$ | $\approx 0.577$ |
| 90 | $\pi/2$ | 1 | 0 | Undefined | 0 |

#### Note on Calculating Tan and Cot
In practice, tangent and cotangent are derived directly from the fundamental sine and cosine projections:
*   **$\tan\theta = \frac{\sin\theta}{\cos\theta}$**
*   **$\cot\theta = \frac{\cos\theta}{\sin\theta} = \frac{1}{\tan\theta}$**

When $\cos\theta = 0$ (at $90^\circ$ and $270^\circ$), $\tan\theta$ is undefined (approaching infinity). When $\sin\theta = 0$ (at $0^\circ$ and $180^\circ$), $\cot\theta$ is undefined.

When you call `Mathf.Sin()` in Unity, the CPU runs the value through a rapid, highly optimized structural instruction directly inside the SIMD hardware pipeline. This computes floating-point precision curves for thousands of vertices or entities simultaneously without missing a single frame beat.

---

## 5. Detailed Gameplay Examples

Let's look at two classic game mechanics built entirely on angular projections.

### Example A: The Hovering Health Pick-Up (Oscillation)

You have a floating health potion hovering over the ground. If it just sits there statically, it looks dead. You want it to bob up and down gently in the air like a magical artifact.

* **The God Mode Trick:** You pass the current game time directly into a Sine function: $\text{Position}_Y = \sin(\text{Time})$. Because the output of sine smoothly climbs to 1, dips down to -1, and returns to 0 endlessly, your health potion bobs up and down with absolute grace.

### Example B: The Orbiting Shield Drone (Circular Projection)

You want a protective drone to orbit continuously around your main player character, acting as a physical shield against incoming lasers.

* **The God Mode Trick:** You keep track of a single scalar float variable called `_currentAngle`. Every frame, you increase this angle based on time. You then project this angle into a vector using $(\cos(\text{Angle}), 0, \sin(\text{Angle}))$. By adding this projected displacement vector directly to the player's world position, the shield drone locks into a perfect, custom-scaled orbital tracking pattern.

---

## 6. The Unity Code: Harmonic Waves and Orbitals

Here is a comprehensive Unity C# script that demonstrates how to implement both harmonic bouncing waves and full 3D orbital projections using pure math.

```csharp
using UnityEngine;

public class TrigonometricKinematics : MonoBehaviour
{
    [Header("Hover Settings (Sine Wave)")]
    [SerializeField] private bool enableHover = true;
    [SerializeField] private float hoverSpeed = 2.0f;     // Scalar: How fast it bobs
    [SerializeField] private float hoverAmplitude = 0.5f; // Scalar: How high it bobs

    [Header("Orbit Settings (Angular Projection)")]
    [SerializeField] private Transform orbitTarget;        // The central anchor (e.g., the player)
    [SerializeField] private float orbitRadius = 4.0f;     // Scalar: Distance from center
    [SerializeField] private float orbitSpeed = 3.0f;      // Scalar: Angular velocity

    private float _angleCounter = 0.0f;
    private Vector3 _startPosition;

    void Start()
    {
        // Store our initial address for the hover calculation
        _startPosition = transform.position;
    }

    void Update()
    {
        // ====================================================
        // 1. HARMONIC HOVER (Using a single projection wave)
        // ====================================================
        if (enableHover && orbitTarget == null)
        {
            // Time acts as our continuously increasing angular driver
            float currentWaveValue = Mathf.Sin(Time.time * hoverSpeed);

            // Scale the wave projection by our amplitude scalar
            float finalYOffset = currentWaveValue * hoverAmplitude;

            // Apply the offset back onto our baseline position structure
            transform.position = new Vector3(_startPosition.x, _startPosition.y + finalYOffset, _startPosition.z);
        }

        // ====================================================
        // 2. 3D ORBITAL PROJECTION (Using bundled Cos/Sin)
        // ====================================================
        if (orbitTarget != null)
        {
            // Endlessly step our angle forward based on independent time
            _angleCounter += orbitSpeed * Time.deltaTime;

            // Project our scalar angle into a packed directional coordinate system
            // We project onto the X and Z plane to orbit flat horizontally around the target
            float xOffset = Mathf.Cos(_angleCounter) * orbitRadius;
            float zOffset = Mathf.Sin(_angleCounter) * orbitRadius;

            // Construct our final displacement vector relative to the target's position address
            Vector3 orbitalDisplacement = new Vector3(xOffset, 0.0f, zOffset);
            
            // Apply the structural projection to our object
            transform.position = orbitTarget.position + orbitalDisplacement;
        }
    }
}

```

---


### [Next: Next: Inverse Trigonometric Processing](./6-2-Inverse-Trigonometric-Processing.md)


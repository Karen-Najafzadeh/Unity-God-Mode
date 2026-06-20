#!/usr/bin/env python3
"""
Generate the GitHub documentation book structure from the syllabus.
Creates volume folders, chapter folders, topic .md files, and README files with links.
"""

import os
import re
from pathlib import Path

# Define the complete structure from the syllabus
STRUCTURE = {
    "Volume-0-Foundations": {
        "description": "Foundations of Syntax, Compilation, and Development Workflow",
        "chapters": {
            "Chapter-1-Anatomy-of-a-Program": {
                "full_name": "The Anatomy of a Program and C# Structural Syntax",
                "topics": [
                    "Machine-Instructions-and-High-Level-Readability",
                    "Structure-of-C#-Script-Namespaces-Classes-Methods",
                    "Variables-Primitive-Data-Types-Type-Declarations",
                    "Control-Flow-Architecture-Conditional-Logic-Branching",
                    "Loop-Mechanics-Iterative-Execution-Structures",
                    "Method-Layouts-Parameter-Passing-Signatures-Return-Values",
                ]
            },
            "Chapter-2-OOP-Blueprint-and-Syntax": {
                "full_name": "The Object-Oriented Blueprint and Syntax Mechanics",
                "topics": [
                    "Concept-of-Objects-Fields-Properties-State-Representation",
                    "Access-Modifiers-Encapsulation-Code-Visibility-Scope",
                    "Constructor-Mechanics-Object-Lifecycle-Initialization",
                    "Inheritance-Topologies-Base-Classes-Polymorphic-Behavior",
                    "Method-Overriding-Virtual-Abstract-Execution-Contracts",
                    "Static-Class-Members-vs-Instance-Allocations",
                ]
            },
            "Chapter-3-Unity-Editor-Environment": {
                "full_name": "The Unity Editor Environment and Workspace Topology",
                "topics": [
                    "Multi-Panel-Interface-Layout-Context-Windows",
                    "Scene-View-Hierarchy-vs-Project-Asset-Frameworks",
                    "Inspector-Pipeline-Visualizing-Component-State",
                    "GameObjects-Component-Based-Design-Architecture",
                    "Prefab-Topologies-Reusable-Hierarchy-Instantiation",
                    "Console-Matrix-Debugging-Diagnostic-Logging-Layouts",
                ]
            },
            "Chapter-4-Core-Unity-Scripting": {
                "full_name": "Core Unity Scripting Syntax and Component Communication",
                "topics": [
                    "Lifecycle-of-an-Attached-MonoBehaviour-Component",
                    "Accessing-Components-Programmatically-via-Getters",
                    "Instantiating-Destroying-GameObjects-Real-Time",
                    "Transform-Component-Hierarchy-Parent-Child-Linkage-Syntax",
                    "Input-System-Baselines-Reading-Hardware-Events",
                    "Primitive-Component-Interaction-Protocols",
                ]
            },
        }
    },
    "Volume-I-Mathematical-Foundations": {
        "description": "Mathematical Foundations & Physical Intuition",
        "chapters": {
            "Chapter-5-Vector-Spaces-and-Linear-Kinematics": {
                "full_name": "Vector Spaces and Linear Kinematics",
                "topics": [
                    "Scalars-and-Coordinate-Vectors",
                    "Vector-Mechanics-Algebraic-Operations",
                    "Euclidean-Distance-Metrics",
                    "Vector-Normalization-Mechanics",
                    "Coordinate-Spaces-Structural-Transformations",
                    "Applied-Kinematics-Constant-Velocity-Translation",
                ]
            },
            "Chapter-6-Angular-Trigonometry-and-Matrix": {
                "full_name": "Angular Trigonometry and Matrix Transformations",
                "topics": [
                    "Trigonometric-Motion-Angular-Projections",
                    "Inverse-Trigonometric-Processing",
                    "Linear-Algebra-Foundations",
                    "Matrix-Operations-Determinants",
                    "Affine-Transformation-Matrices",
                    "Compounding-Positional-Rotational-Scaling-Matrices",
                ]
            },
            "Chapter-7-Vector-Projections-and-Spatial": {
                "full_name": "Vector Projections and Spatial Orientations",
                "topics": [
                    "Scalar-Vector-Projections",
                    "Perpendicular-Vector-Generation-Orthogonality",
                    "Surface-Normal-Analysis-Area-Interpretation",
                    "Vector-Decomposition-Theory",
                    "Physics-of-Elastic-Collisions-Structural-Reflections",
                ]
            },
            "Chapter-8-Interpolation-and-Rotational": {
                "full_name": "Interpolation Frameworks and Advanced Rotational Systems",
                "topics": [
                    "Linear-Interpolation-Matrices-Affine-Combinations",
                    "Kinematic-Smoothing-Critical-Damping",
                    "Gimbal-Lock-Phenomena",
                    "Hypercomplex-Numbers-4D-Vector-Spaces",
                    "Stable-Rotational-Computing-Geodesics",
                ]
            },
            "Chapter-9-Applied-Physics-and-Integration": {
                "full_name": "Applied Physics and Numerical Integration Methods",
                "topics": [
                    "Newtonian-Classical-Mechanics-Engines",
                    "Momentum-Conservation-Impulse-Vectors",
                    "Rotational-Rigid-Body-Dynamics-Inertia-Tensors",
                    "Explicit-Euler-Integration-Faults",
                    "Semi-Implicit-Euler-Integration-Pipelines",
                    "Verlet-Runge-Kutta-4th-Order-Solvers",
                    "Constraint-Solvers-Error-Propagation",
                ]
            },
        }
    },
    "Volume-II-Memory-Mechanics": {
        "description": "Low-Level Memory Mechanics & C# Runtime Architecture",
        "chapters": {
            "Chapter-10-Virtual-Machine-and-Type": {
                "full_name": "The Virtual Machine and Type System Allocations",
                "topics": [
                    "Microprocessor-Registers-System-Memory-Topologies",
                    "Virtual-Execution-Environments-Common-Language-Runtime",
                    "Stack-Memory-Architecture-Execution-Lifecycles",
                    "Heap-Memory-Architecture-Fragmentation-Hazards",
                    "Value-Types-vs-Reference-Types-Memory-Footprints",
                ]
            },
            "Chapter-11-Memory-Layout-and-Boxing": {
                "full_name": "Memory Layout Optimization and Boxing Mechanics",
                "topics": [
                    "Type-System-Unification-Object-Hierarchies",
                    "Allocation-Cost-of-Boxing-Operations",
                    "CPU-Penalty-of-Unboxing-Operations",
                    "Zero-Allocation-Data-Optimization-Formats",
                    "Value-Passing-Semantics-Stack-Restrictions",
                ]
            },
            "Chapter-12-Automated-Memory-Management": {
                "full_name": "Automated Memory Management and Object Pooling",
                "topics": [
                    "Garbage-Collector-Architecture",
                    "Generational-GC-Model-Object-Lifetime-Bands",
                    "Small-Object-Heap-vs-Large-Object-Heap-Metrics",
                    "Incremental-GC-Pipelines-Execution-Pauses",
                    "Object-Pooling-Structural-Pattern",
                ]
            },
            "Chapter-13-Advanced-Custom-Types": {
                "full_name": "Advanced Custom Types and Unmanaged Collections",
                "topics": [
                    "Bitwise-Architecture-Binary-Flags-Systems",
                    "Generic-Metaprogramming-Parametric-Generalization",
                    "Just-In-Time-Compilation-Profiles",
                    "Covariance-Contravariance-Variations",
                    "Hash-Code-Computations-Index-Bucketing",
                    "Unmanaged-Memory-Containers-Allocation-Lifecycles",
                ]
            },
        }
    },
    "Volume-III-Engine-Core-Runtime": {
        "description": "Engine Core Runtime & Data Execution Layers",
        "chapters": {
            "Chapter-14-Flyweight-Architectures": {
                "full_name": "Flyweight Architectures and Native Memory Models",
                "topics": [
                    "Flyweight-Design-Pattern",
                    "Native-C++-Allocations-vs-Managed-Objects",
                    "Memory-Optimization-via-Shared-Immutable-State",
                    "Lifecycle-Event-Subscriptions-Runtime-Boundaries",
                ]
            },
            "Chapter-15-Native-Serialization": {
                "full_name": "Native Serialization and High-Frequency Lifecycles",
                "topics": [
                    "Native-Serialization-Matrix-Document-Encoding",
                    "Engine-Initialization-Sequence",
                    "Discrete-Physics-Simulation-Timesteps-vs-Variable-Rendering",
                    "Broad-Phase-Narrow-Phase-Spatial-Queries",
                ]
            },
            "Chapter-16-Asynchronous-Systems": {
                "full_name": "Asynchronous Systems and Multithreading Foundations",
                "topics": [
                    "Cooperative-Concurrency-Intermediate-Language-State-Machines",
                    "Low-Level-Thread-Allocation-ThreadPool-Mechanics",
                    "Race-Conditions-Synchronization-Obstacles",
                    "Modern-Asynchronous-Execution-Pipelines",
                    "Thread-Safety-Contexts-Main-Thread-Dispatching",
                ]
            },
        }
    },
    "Volume-IV-Serialization-and-Cryptography": {
        "description": "Advanced Serialization, Cryptography, & Enterprise Storage",
        "chapters": {
            "Chapter-17-Serialization-Paradigms": {
                "full_name": "Serialization Paradigms and Binary Formats",
                "topics": [
                    "Data-State-Preservation-Transport-Translation",
                    "Polymorphic-Data-Storage-Constraints",
                    "Structured-Binary-Protocols-Byte-Packing-Algorithms",
                    "Schema-Evolution-Version-Compatibility",
                ]
            },
            "Chapter-18-File-System-Integration": {
                "full_name": "File System Integration and Application Sandboxing",
                "topics": [
                    "Synchronous-vs-Asynchronous-File-Stream-Architectures",
                    "Platform-Specific-Local-Storage-Sandboxes",
                    "Deployable-Asset-Storage-Contexts",
                ]
            },
            "Chapter-19-Cryptography-and-Anti-Cheat": {
                "full_name": "Cryptography, Obfuscation, and Anti-Cheat Infrastructures",
                "topics": [
                    "Symmetric-Key-Encryption-Profiles",
                    "Multi-Layered-Obfuscation-Matrices",
                    "Runtime-Memory-Interception-Tampering-Vulnerabilities",
                    "Bit-Shifted-Encrypted-Variable-Wrappers",
                    "Operating-System-Secure-Storage-Vaults",
                ]
            },
        }
    },
    "Volume-V-Enterprise-Architecture": {
        "description": "Enterprise Software Architecture & Design Patterns",
        "chapters": {
            "Chapter-20-Interface-Contracts": {
                "full_name": "Interface Contracts and Decoupling Strategies",
                "topics": [
                    "Interface-Abstraction-Software-Boundaries",
                    "Polymorphism-Driver-Isolation",
                    "Strategy-Design-Pattern",
                    "Runtime-Swapping-Functional-Providers",
                ]
            },
            "Chapter-21-Dependency-Processing": {
                "full_name": "Dependency Processing and Event-Driven Pipelines",
                "topics": [
                    "Singleton-Pattern-Risk-Metrics",
                    "Dependency-Injection-vs-Service-Locator-Frameworks",
                    "Constructor-Injection-Processing",
                    "Observer-Design-Pattern",
                    "Delegates-Actions-Formal-Event-Scopes",
                    "Memory-Retention-Lifecycle-Leak-Management",
                ]
            },
            "Chapter-22-Behavioral-Automation": {
                "full_name": "Behavioral Automation and Flow Management",
                "topics": [
                    "Finite-State-Machine-Architecture",
                    "Command-Design-Pattern",
                    "Undo-Redo-Execution-Queues",
                    "Thread-Safe-Lazy-Instantiation-Models",
                ]
            },
            "Chapter-23-Data-Migration": {
                "full_name": "Data Migration and Version Control Systems",
                "topics": [
                    "Data-Schema-Drift-Mitigation",
                    "Forward-Compatible-Structural-Headers",
                    "Chain-of-Responsibility-Design-Pattern",
                    "Multi-Version-Data-Adaptation-Regression-Safeguards",
                ]
            },
        }
    },
    "Volume-VI-Editor-Engineering": {
        "description": "Advanced Editor Engineering & Automated Source Generation",
        "chapters": {
            "Chapter-24-Development-Environment": {
                "full_name": "Development Environment Architecture and UI Frameworks",
                "topics": [
                    "Compilation-Assembly-Segregation-Rules",
                    "Preprocessor-Block-Compilation-Boundaries",
                    "System-Settings-Registry-Injection",
                    "Immediate-Mode-vs-Retained-Mode-UI-Architecture",
                    "XML-Based-Layouts-Document-Stylesheets",
                ]
            },
            "Chapter-25-Serialized-Property-Inspection": {
                "full_name": "Serialized Property Inspection and Asset Control Pipelines",
                "topics": [
                    "Data-Tree-Iteration-Serialization-Parsing",
                    "Asset-Database-Lifecycles-Automation-Engines",
                    "Programmatic-Resource-Selection-Database-Queries",
                ]
            },
            "Chapter-26-Meta-Programming": {
                "full_name": "Meta-Programming and Automated Code Generation",
                "topics": [
                    "Magic-String-Architectural-Vulnerability",
                    "Type-Safe-Wrapper-Generation-Automation",
                    "Compile-Time-API-Code-Reflection",
                ]
            },
        }
    },
    "Volume-VII-Performance-Engineering": {
        "description": "Engine-Level Performance Engineering, Hardware Optimization, & DOTS",
        "chapters": {
            "Chapter-27-Data-Oriented-Design": {
                "full_name": "Data-Oriented Design and Hardware Cache Topologies",
                "topics": [
                    "Object-Oriented-Encapsulation-vs-Data-Oriented-Optimization",
                    "CPU-Cache-Architecture-Cache-Miss-Costs",
                    "Spatial-Cache-Locality-Pointer-Chasing-Mitigation",
                    "Entity-Component-System-ECS-Model",
                    "Continuous-Memory-Allocation-Layouts-Archetype-Chunks",
                ]
            },
            "Chapter-28-Task-Schedulers": {
                "full_name": "Core Task Schedulers and Native Assembly Translation",
                "topics": [
                    "Context-Switching-Mitigation",
                    "Safety-Checked-Worker-Thread-Schedulers",
                    "Data-Race-Conditions-Thread-Modification-Tracking",
                    "Intermediate-Language-Native-Machine-Code-Translation",
                    "Single-Instruction-Multiple-Data-SIMD-Vectorization",
                    "Blittable-Data-Types-Hardware-Accelerated-Math-Primitives",
                ]
            },
            "Chapter-29-Performance-Diagnostics": {
                "full_name": "Performance Diagnostics, Memory Profiling, and Asset Pipelines",
                "topics": [
                    "String-Allocation-Optimizations-Hashing-Pre-Calculations",
                    "Zero-Allocation-Spatial-Detection-Arrays",
                    "Execution-Anomaly-Diagnostics",
                    "Unmanaged-Memory-Leak-Analysis",
                    "Resources-Ecosystem-Limitations",
                    "Asynchronous-Reference-Counting-Asset-Networks",
                    "Modular-Streamable-Asset-Package-Architectures",
                ]
            },
            "Chapter-30-Graphics-Pipelines": {
                "full_name": "Graphics Pipelines, Batching Engines, and Overdraw Mitigation",
                "topics": [
                    "CPU-Execution-Bounds-vs-GPU-Rasterization-Pipelining",
                    "Draw-Call-Management-State-Transmission-Overhead",
                    "Static-Dynamic-Scriptable-Render-Pipeline-Batching-Engines",
                    "GPU-Instancing-Architectures",
                    "Fill-Rate-Bottlenecks-Occlusion-Culling-Solutions",
                    "Texture-Block-Compression-Formats-Hardware-Compatibility",
                    "Texture-Cache-Optimization-Mipmapping-Pipelines",
                ]
            },
        }
    },
}


def slugify(text):
    """Convert text to slug format."""
    return text.strip()


def create_structure(base_path):
    """Create the entire directory and file structure."""
    base = Path(base_path)
    base.mkdir(parents=True, exist_ok=True)
    
    for volume_slug, volume_data in STRUCTURE.items():
        volume_path = base / volume_slug
        volume_path.mkdir(parents=True, exist_ok=True)
        
        print(f"Creating {volume_slug}...")
        
        for chapter_slug, chapter_data in volume_data["chapters"].items():
            chapter_path = volume_path / chapter_slug
            chapter_path.mkdir(parents=True, exist_ok=True)
            
            # Create topic files
            for topic_slug in chapter_data["topics"]:
                topic_file = chapter_path / f"{topic_slug}.md"
                if not topic_file.exists():
                    topic_file.write_text("")
                    
            # Create chapter README
            readme_path = chapter_path / "README.md"
            create_chapter_readme(readme_path, chapter_slug, chapter_data)
        
        # Create volume README
        readme_path = volume_path / "README.md"
        create_volume_readme(readme_path, volume_slug, volume_data)
    
    print("✓ Structure created successfully!")


def create_chapter_readme(filepath, chapter_slug, chapter_data):
    """Create chapter README with links to topics."""
    lines = [
        f"# {chapter_data['full_name']}",
        "",
        "## Topics",
        "",
    ]
    
    for topic_slug in chapter_data["topics"]:
        # Convert slug back to readable name
        readable_name = topic_slug.replace("-", " ")
        lines.append(f"- [{readable_name}](./{topic_slug}.md)")
    
    filepath.write_text("\n".join(lines) + "\n")


def create_volume_readme(filepath, volume_slug, volume_data):
    """Create volume README with links to chapters."""
    lines = [
        f"# {volume_slug.replace('-', ' ')}",
        "",
        f"*{volume_data['description']}*",
        "",
        "## Chapters",
        "",
    ]
    
    for chapter_slug, chapter_data in volume_data["chapters"].items():
        readable_chapter = chapter_data["full_name"]
        lines.append(f"- [{readable_chapter}](./{chapter_slug}/)")
    
    filepath.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    workspace_root = "/home/karen/Documents/Obsidian Vault/Unity God Mode"
    create_structure(workspace_root)

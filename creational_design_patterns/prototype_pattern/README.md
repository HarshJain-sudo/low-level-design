# Prototype Design Pattern

## Overview

The **Prototype Pattern** is a creational design pattern that allows you to
create new objects by copying existing ones (prototypes) rather than
constructing them from scratch. This is particularly useful when object
creation is expensive or when you want to create objects that are similar to
existing ones with minor modifications.

## Problem Statement

When creating multiple similar objects, the traditional approach requires
instantiating each object individually, which can be:

- **Time-consuming**: Heavy initialization (database calls, API requests,
  complex computations)
- **Resource-intensive**: Duplicate expensive operations for each object
- **Inefficient**: Repeating the same initialization logic multiple times

### Example Problem

```python
# Creating multiple users - each takes 1 second!
user1 = UserProfile("Alice", "Admin", ["read", "write", "delete"], 
                    {"theme": "dark"})
user2 = UserProfile("Bob", "Admin", ["read", "write", "delete"], 
                    {"theme": "dark"})
user3 = UserProfile("Charlie", "Admin", ["read", "write", "delete"], 
                    {"theme": "dark"})
# Total time: 3 seconds for 3 similar objects!
```

## Solution: Prototype Pattern

The Prototype pattern solves this by:

1. Creating a **prototype object** once (with the expensive initialization)
2. **Cloning** the prototype to create new instances
3. **Modifying** the cloned objects as needed

This way, expensive initialization happens only once, and subsequent objects
are created quickly through cloning.

## Implementation

### Structure

```
Prototype (Abstract Base Class)
    ├── clone() [abstract method]
    │
    ├── UserProfile (Concrete Prototype)
    │   └── clone() [returns deep copy]
    │
    └── AdminProfile (Concrete Prototype)
        └── clone() [returns deep copy]
```

### Key Components

1. **Prototype Interface**: Abstract base class defining the `clone()` method
2. **Concrete Prototypes**: Classes implementing the `clone()` method
3. **Client**: Code that uses prototypes to create new objects

### Code Example

```python
from abc import ABC, abstractmethod
import copy

class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass

class UserProfile(Prototype):
    def __init__(self, name, role, permissions, preferences):
        # Expensive initialization (simulated with time.sleep)
        self.name = name
        self.role = role
        self.permissions = permissions
        self.preferences = preferences

    def clone(self):
        return copy.deepcopy(self)  # Create a deep copy
```

### Usage

```python
# Step 1: Create prototype once (expensive operation)
prototype_user = UserProfile("PrototypeUser", "Member", ["read"], 
                             {"theme": "dark"})

# Step 2: Clone and customize (fast operation)
user1 = prototype_user.clone()
user1.name = "Alice"

user2 = prototype_user.clone()
user2.name = "Bob"
user2.preferences["theme"] = "light"
```

## Benefits

1. **Performance**: Avoids expensive object creation by cloning existing
   objects
2. **Flexibility**: Easy to create variations of existing objects
3. **Reduced Coupling**: Client code doesn't need to know about concrete
   classes
4. **Dynamic Configuration**: Prototypes can be configured at runtime

## When to Use

- Object creation is expensive (database queries, network calls, complex
  computations)
- You need multiple similar objects with minor differences
- Classes to instantiate are specified at runtime
- You want to avoid subclassing for object creation

## Deep Copy vs Shallow Copy

The implementation uses `copy.deepcopy()` to ensure:

- **Deep Copy**: Creates a completely independent copy, including nested
  objects
- **Shallow Copy**: Would only copy references, leading to shared mutable
  objects

### Example Difference

```python
# Deep Copy (used in solution)
user1 = prototype_user.clone()
user1.preferences["theme"] = "light"  # Doesn't affect prototype

# Shallow Copy (would cause issues)
user1 = copy.copy(prototype_user)
user1.preferences["theme"] = "light"  # Affects prototype too!
```

## Real-World Use Cases

1. **Game Development**: Cloning game objects (characters, weapons, items)
2. **Database Operations**: Cloning database connection configurations
3. **UI Components**: Creating similar UI elements with different properties
4. **Configuration Objects**: Cloning system configurations for different
   environments

## Running the Code

### Problem (Without Prototype Pattern)
```bash
python problem.py
```
- Creates 3 users, each taking 1 second
- Total time: ~3 seconds

### Solution (With Prototype Pattern)
```bash
python solution.py
```
- Creates 1 prototype (1 second)
- Clones 3 users (instant)
- Total time: ~1 second

## Key Takeaways

1. **Prototype Pattern** = Clone existing objects instead of creating new
   ones
2. Use when object creation is **expensive**
3. Use **deep copy** to ensure independent clones
4. Modify cloned objects to create variations
5. Significantly improves performance when creating multiple similar objects

## Related Patterns

- **Factory Pattern**: Creates objects without specifying exact classes
- **Builder Pattern**: Constructs complex objects step by step
- **Singleton Pattern**: Ensures only one instance exists

---

**Note**: This pattern is especially powerful when combined with a prototype
registry/manager that stores and retrieves prototypes by key, allowing for
even more flexible object creation.


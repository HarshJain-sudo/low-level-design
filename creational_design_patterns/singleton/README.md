# Singleton Design Pattern

## Overview

The **Singleton Pattern** is a creational design pattern that ensures a class
has only **one instance** and provides a global point of access to that
instance. This is useful when you need exactly one object to coordinate actions
across your application.

## Problem Statement

Sometimes, you need only **one instance** of a class throughout your entire
application. However, if you create objects normally, you might accidentally
create multiple instances, which can cause problems:

- **Inconsistent State**: Each instance has its own data, leading to confusion
- **Resource Waste**: Creating multiple instances when only one is needed
- **Unexpected Behavior**: Different parts of code using different instances

### Example Problem

Imagine a Logger class that should log all messages to one place:

```python
class Logger:
    def __init__(self):
        print("Creating new Logger instance...")
        self.log_messages = []

    def log(self, message):
        self.log_messages.append(message)
        print(f"LOG: {message}")

# Problem: Multiple instances created
logger1 = Logger()  # Creates instance 1
logger2 = Logger()  # Creates instance 2

logger1.log("User logged in")
logger2.log("User clicked button")

print(logger1.log_messages)  # Only has: ["User logged in"]
print(logger2.log_messages)  # Only has: ["User clicked button"]
```

**The Problem:**
- Two separate Logger instances are created
- Each instance has its own `log_messages` list
- Messages are split between instances
- You lose a complete log history
- Wastes memory with duplicate objects

## Solution: Singleton Pattern

The Singleton pattern solves this by:

1. **Preventing multiple instances**: Only allows one instance to be created
2. **Global access**: Provides a way to access that single instance from
   anywhere
3. **Lazy or Eager creation**: Creates the instance when needed or at startup

### How It Works

Instead of creating new instances every time, the Singleton pattern:
- Checks if an instance already exists
- If yes, returns the existing instance
- If no, creates one and stores it for future use

## Implementation Approaches

### 1. Lazy Singleton (Simple)

Creates the instance only when it's first requested.

```python
class LazySingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating instance lazily...")
            cls._instance = super(LazySingleton, cls).__new__(cls)
        return cls._instance

# Usage
s1 = LazySingleton()  # Creates instance
s2 = LazySingleton()  # Returns existing instance
print(s1 is s2)  # True - same object!
```

**Pros:**
- Simple and easy to understand
- Instance created only when needed
- Memory efficient

**Cons:**
- Not thread-safe (can create multiple instances in multi-threaded
  environments)

### 2. Eager Singleton

Creates the instance immediately when the class is loaded.

```python
class EagerSingleton:
    _instance = object.__new__(None.__class__)

    def __new__(cls):
        return cls._instance

# Usage
s1 = EagerSingleton()  # Returns pre-created instance
s2 = EagerSingleton()  # Returns same instance
print(s1 is s2)  # True
```

**Pros:**
- Thread-safe (instance exists before any thread can access it)
- Simple implementation

**Cons:**
- Instance created even if never used
- Wastes memory if instance is not needed

### 3. Synchronized Singleton (Thread-Safe)

Uses locks to ensure thread safety in multi-threaded environments.

```python
import threading

class SynchronizedSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:  # Only one thread can enter
            if cls._instance is None:
                print("Creating synchronized instance...")
                cls._instance = super(SynchronizedSingleton, cls).__new__(cls)
        return cls._instance
```

**Pros:**
- Thread-safe
- Instance created only when needed

**Cons:**
- Slightly slower due to locking overhead
- More complex than simple singleton

### 4. Double-Checked Singleton (Optimized Thread-Safe)

Checks twice to avoid unnecessary locking.

```python
import threading

class DoubleCheckedSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        # First check (fast, no lock)
        if cls._instance is None:
            with cls._lock:
                # Second check (inside lock)
                if cls._instance is None:
                    cls._instance = super(DoubleCheckedSingleton, cls).__new__(cls)
        return cls._instance
```

**Pros:**
- Thread-safe
- Better performance (avoids locking after first creation)
- Best of both worlds

**Cons:**
- More complex implementation

## Real-World Example: Logger with Singleton

```python
class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Logger, cls).__new__(cls)
                    cls._instance.log_messages = []
        return cls._instance

    def log(self, message):
        self.log_messages.append(message)
        print(f"LOG: {message}")

# Usage - all loggers are the same instance!
logger1 = Logger()
logger2 = Logger()

logger1.log("User logged in")
logger2.log("User clicked button")

print(logger1.log_messages)  
# Output: ["User logged in", "User clicked button"]
print(logger2.log_messages)  
# Output: ["User logged in", "User clicked button"]
# Same list! Same instance!
```

## Benefits

1. **Single Instance**: Guarantees only one instance exists
2. **Global Access**: Easy to access from anywhere in the code
3. **Resource Management**: Prevents unnecessary object creation
4. **Consistent State**: All code uses the same instance and data
5. **Memory Efficient**: Saves memory by reusing one instance

## When to Use

- **Configuration Objects**: Database connections, app settings
- **Logging**: Single logger instance for entire application
- **Caching**: Single cache manager
- **Thread Pools**: Single thread pool manager
- **Device Drivers**: Single driver instance for hardware
- **Registry Settings**: Single registry access point

## When NOT to Use

- **Avoid for regular classes**: Not every class needs to be a singleton
- **Testing difficulties**: Hard to test because of global state
- **Hidden dependencies**: Makes dependencies less clear
- **Thread safety concerns**: Simple singleton is not thread-safe

## Key Takeaways

1. **Singleton Pattern** = Only one instance of a class can exist
2. Use when you need **one shared instance** across the application
3. **Lazy Singleton**: Simple but not thread-safe
4. **Synchronized Singleton**: Thread-safe but slower
5. **Double-Checked Singleton**: Thread-safe and optimized
6. All instances point to the **same object** in memory

## Common Mistakes

### Mistake 1: Not Using `__new__`
```python
# Wrong - doesn't prevent multiple instances
class BadSingleton:
    _instance = None
    
    def __init__(self):
        if BadSingleton._instance is None:
            BadSingleton._instance = self
```

### Mistake 2: Not Thread-Safe
```python
# Wrong - can create multiple instances in threads
class BadSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:  # Race condition here!
            cls._instance = super().__new__(cls)
        return cls._instance
```

## Running the Code

### Problem (Without Singleton)
```bash
python problem.py
```
- Creates multiple Logger instances
- Each has separate log messages
- Inconsistent logging

### Solution (With Singleton)
```bash
python lazy_singleton.py          # Simple singleton
python eager_singleton.py          # Eager singleton
python synchronized_singleton.py   # Thread-safe singleton
python double_checked_singleton.py # Optimized thread-safe
```
- Creates only one instance
- All references point to same object
- Consistent state across application

## Related Patterns

- **Factory Pattern**: Creates objects without specifying exact classes
- **Prototype Pattern**: Clones existing objects
- **Builder Pattern**: Constructs complex objects step by step

---

**Remember**: Singleton is powerful but use it wisely. Overusing singletons
can make your code harder to test and maintain. Use it only when you truly
need exactly one instance of a class.


# Strategy Design Pattern

## Overview

The **Strategy Pattern** is a behavioral design pattern that lets you define a
family of algorithms, encapsulate each one, and make them interchangeable. It
allows you to select an algorithm at runtime rather than hard-coding it. The
pattern lets the algorithm vary independently from the clients that use it.

## Problem Statement

When you have multiple ways to perform a task, the direct approach often uses
if-else or switch statements. This creates several problems:

- **Violates Open/Closed Principle**: Must modify class to add new behaviors
- **Multiple Responsibilities**: Class handles multiple algorithms
- **Hard to Test**: Can't test algorithms independently
- **Code Duplication**: Similar logic scattered across classes
- **Tight Coupling**: Behavior is tightly coupled to the class

### Example Problem

Imagine a Vehicle class that can drive in different ways:

```python
class Vehicle:
    def __init__(self, type):
        self.type = type

    def drive(self):
        if self.type == "car":
            print("Driving on the road 🛣️")
        elif self.type == "offroad":
            print("Driving off-road 🏞️")
        elif self.type == "airplane":
            print("Flying in the air ✈️")
        else:
            print("Unknown vehicle type")

# Usage
v1 = Vehicle("car")
v2 = Vehicle("airplane")
v1.drive()
v2.drive()
```

**The Problems:**
- **Adding New Behavior**: Must modify Vehicle class (violates Open/Closed)
- **Too Many Responsibilities**: Vehicle class handles all drive behaviors
- **Hard to Test**: Can't test each drive behavior separately
- **Not Flexible**: Can't change behavior at runtime
- **Code Duplication**: If other classes need similar logic, code is duplicated

## Solution: Strategy Pattern

The Strategy pattern solves this by:

1. **Encapsulating Algorithms**: Each algorithm becomes a separate strategy
   class
2. **Interchangeable Strategies**: All strategies implement the same interface
3. **Runtime Selection**: Choose strategy at runtime
4. **Separation of Concerns**: Vehicle class doesn't know algorithm details
5. **Easy to Extend**: Add new strategies without modifying existing code

### How It Works

Instead of if-else statements in the class:
- Create a **Strategy Interface** (abstract class)
- Implement **Concrete Strategies** for each algorithm
- The main class **uses** a strategy (composition)
- Can **change strategies** at runtime

## Implementation

### Structure

```
DriveStrategy (Strategy Interface)
    ├── drive() [abstract method]
    │
    ├── RoadDriveStrategy (Concrete Strategy)
    ├── OffRoadDriveStrategy (Concrete Strategy)
    ├── AirDriveStrategy (Concrete Strategy)
    └── WaterDriveStrategy (Concrete Strategy)

Vehicle (Context)
    └── Uses DriveStrategy
```

### Code Implementation

```python
from abc import ABC, abstractmethod

# Step 1: Strategy Interface
class DriveStrategy(ABC):
    @abstractmethod
    def drive(self):
        pass

# Step 2: Concrete Strategies
class RoadDriveStrategy(DriveStrategy):
    def drive(self):
        print("Driving on the road 🛣️")

class OffRoadDriveStrategy(DriveStrategy):
    def drive(self):
        print("Driving off-road 🏞️")

class AirDriveStrategy(DriveStrategy):
    def drive(self):
        print("Flying in the air ✈️")

class WaterDriveStrategy(DriveStrategy):
    def drive(self):
        print("Sailing on water 🚤")

# Step 3: Context Class (Vehicle)
class Vehicle:
    def __init__(self, name, strategy: DriveStrategy):
        self.name = name
        self._drive_strategy = strategy  # Composition

    def drive(self):
        print(f"{self.name}:", end=" ")
        self._drive_strategy.drive()  # Delegate to strategy

    def set_drive_strategy(self, new_strategy: DriveStrategy):
        self._drive_strategy = new_strategy  # Change at runtime

# Usage
car = Vehicle("Car", RoadDriveStrategy())
jeep = Vehicle("Jeep", OffRoadDriveStrategy())
plane = Vehicle("Plane", AirDriveStrategy())

car.drive()    # Car: Driving on the road 🛣️
jeep.drive()   # Jeep: Driving off-road 🏞️
plane.drive()  # Plane: Flying in the air ✈️
```

## Key Features

### 1. Runtime Strategy Change

You can change the strategy at runtime:

```python
jeep = Vehicle("Jeep", OffRoadDriveStrategy())
jeep.drive()  # Driving off-road

# Change behavior dynamically!
jeep.set_drive_strategy(AirDriveStrategy())
jeep.drive()  # Flying in the air ✈️
```

### 2. Easy to Extend

Add new strategies without modifying existing code:

```python
# Add new strategy - no changes to Vehicle class!
class SpaceDriveStrategy(DriveStrategy):
    def drive(self):
        print("Flying in space 🚀")

# Use it immediately
rocket = Vehicle("Rocket", SpaceDriveStrategy())
rocket.drive()
```

### 3. Separation of Concerns

- **Vehicle class**: Knows it has a drive behavior, but not how
- **Strategy classes**: Know how to drive, but not about vehicles
- **Client code**: Chooses which strategy to use

### 4. Testable

Each strategy can be tested independently:

```python
# Test strategies separately
def test_road_strategy():
    strategy = RoadDriveStrategy()
    strategy.drive()  # Easy to test

def test_air_strategy():
    strategy = AirDriveStrategy()
    strategy.drive()  # Easy to test
```

## Benefits

1. **Open/Closed Principle**: Open for extension, closed for modification
2. **Single Responsibility**: Each strategy has one job
3. **Runtime Flexibility**: Change behavior at runtime
4. **Easy to Test**: Test strategies independently
5. **Code Reusability**: Strategies can be reused in other classes
6. **Eliminates Conditionals**: No more if-else chains
7. **Loose Coupling**: Context doesn't depend on concrete strategies

## When to Use

- **Multiple Algorithms**: You have multiple ways to do the same thing
- **Runtime Selection**: Need to choose algorithm at runtime
- **Avoid Conditionals**: Want to eliminate if-else/switch statements
- **Algorithm Variations**: Algorithms vary independently
- **Extensibility**: Need to add new algorithms frequently
- **Testability**: Want to test algorithms separately

## Real-World Use Cases

### 1. Payment Processing

```python
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paying ${amount} with Credit Card")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paying ${amount} with PayPal")

class CryptoPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paying ${amount} with Cryptocurrency")

class ShoppingCart:
    def __init__(self, payment_strategy: PaymentStrategy):
        self.payment_strategy = payment_strategy

    def checkout(self, amount):
        self.payment_strategy.pay(amount)

# Usage
cart = ShoppingCart(CreditCardPayment())
cart.checkout(100)  # Paying $100 with Credit Card
```

### 2. Sorting Algorithms

```python
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data):
        pass

class QuickSort(SortStrategy):
    def sort(self, data):
        # Quick sort implementation
        return sorted(data)

class MergeSort(SortStrategy):
    def sort(self, data):
        # Merge sort implementation
        return sorted(data)

class DataProcessor:
    def __init__(self, sort_strategy: SortStrategy):
        self.sort_strategy = sort_strategy

    def process(self, data):
        return self.sort_strategy.sort(data)
```

### 3. Compression Algorithms

```python
class CompressionStrategy(ABC):
    @abstractmethod
    def compress(self, data):
        pass

class ZipCompression(CompressionStrategy):
    def compress(self, data):
        # ZIP compression
        pass

class RarCompression(CompressionStrategy):
    def compress(self, data):
        # RAR compression
        pass

class FileManager:
    def __init__(self, compression_strategy: CompressionStrategy):
        self.compression_strategy = compression_strategy

    def save(self, data):
        return self.compression_strategy.compress(data)
```

### 4. Navigation Algorithms

```python
class NavigationStrategy(ABC):
    @abstractmethod
    def calculate_route(self, start, end):
        pass

class FastestRoute(NavigationStrategy):
    def calculate_route(self, start, end):
        # Calculate fastest route
        pass

class ShortestRoute(NavigationStrategy):
    def calculate_route(self, start, end):
        # Calculate shortest route
        pass

class ScenicRoute(NavigationStrategy):
    def calculate_route(self, start, end):
        # Calculate scenic route
        pass
```

## Strategy vs Other Patterns

### Strategy vs State Pattern

| Strategy | State |
|----------|-------|
| Algorithms are independent | States are related |
| Client chooses strategy | State changes automatically |
| No state transitions | Has state transitions |
| All strategies available | Only current state available |

### Strategy vs Template Method

| Strategy | Template Method |
|----------|-----------------|
| Composition (has-a) | Inheritance (is-a) |
| Complete algorithm | Algorithm skeleton |
| Runtime selection | Compile-time selection |
| More flexible | Less flexible |

## Key Components

1. **Strategy Interface**: Defines the contract for all strategies
2. **Concrete Strategies**: Implement specific algorithms
3. **Context Class**: Uses a strategy (composition)
4. **Client**: Creates and uses strategies

## Key Takeaways

1. **Strategy Pattern** = Encapsulate algorithms and make them
   interchangeable
2. **Composition over Inheritance**: Use composition (has-a) not inheritance
3. **Runtime Selection**: Choose algorithm at runtime
4. **Open/Closed Principle**: Add new strategies without modifying code
5. **Eliminates Conditionals**: No more if-else chains
6. **Testable**: Each strategy can be tested independently

## Common Mistakes

### Mistake 1: Strategy Knowing About Context
```python
# Wrong - strategy knows about context
class BadStrategy:
    def drive(self, vehicle):
        if vehicle.type == "car":
            # Strategy shouldn't know about vehicle details
```

### Mistake 2: Context Creating Strategies
```python
# Wrong - context creates strategies
class Vehicle:
    def drive(self):
        if self.type == "car":
            strategy = RoadDriveStrategy()  # Context shouldn't create
```

### Mistake 3: Too Many Small Strategies
```python
# Wrong - over-engineering
class Strategy1: pass  # Too simple, not worth a class
class Strategy2: pass
class Strategy3: pass
# Sometimes a simple if-else is fine!
```

## Best Practices

1. **Keep Strategies Simple**: Each strategy should do one thing well
2. **Strategy Interface**: Use abstract base class for type safety
3. **Dependency Injection**: Pass strategy to context, don't create inside
4. **Document Strategies**: Make it clear when to use which strategy
5. **Consider Default Strategy**: Provide a default strategy if needed

## Running the Code

### Problem (Without Strategy)
```bash
python without_strategy.py
```
- If-else statements in Vehicle class
- Hard to extend
- Violates Open/Closed Principle
- Multiple responsibilities

### Solution (With Strategy)
```bash
python with_strategy.py
```
- Clean separation of concerns
- Easy to extend
- Runtime strategy change
- Follows SOLID principles

## Related Patterns

- **State Pattern**: Similar structure but for state management
- **Template Method**: Defines algorithm skeleton
- **Command Pattern**: Encapsulates requests as objects
- **Factory Pattern**: Creates strategy objects

---

**Remember**: Use Strategy pattern when you have multiple ways to do something
and want to choose the method at runtime. It's perfect for eliminating long
if-else chains and making your code more flexible and maintainable!


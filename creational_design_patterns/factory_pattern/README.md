# Factory Design Pattern

## Overview

The **Factory Pattern** is a creational design pattern that provides a way to
create objects without specifying the exact class of object that will be
created. Instead of directly creating objects using constructors, you use a
factory method or factory class to create objects based on some input or
condition.

## Problem Statement

When creating objects, you often need to decide which class to instantiate
based on runtime conditions. The direct approach has several problems:

- **Tight Coupling**: Client code depends on concrete classes
- **Hard to Maintain**: Adding new types requires changing client code
- **Violates Open/Closed Principle**: Code must be modified to extend
- **Complex Conditional Logic**: If-else chains scattered throughout code

### Example Problem

Imagine you need to create different types of vehicles based on user input:

```python
class Car:
    def drive(self):
        print("Driving a Car")

class Bike:
    def drive(self):
        print("Riding a Bike")

class Truck:
    def drive(self):
        print("Driving a Truck")

# Problem: Client code directly creates objects
vehicle_type = input("Enter vehicle (car/bike/truck): ").lower()

if vehicle_type == "car":
    vehicle = Car()
elif vehicle_type == "bike":
    vehicle = Bike()
elif vehicle_type == "truck":
    vehicle = Truck()
else:
    raise ValueError("Invalid vehicle type")

vehicle.drive()
```

**The Problems:**
- Client code knows about all concrete classes (Car, Bike, Truck)
- Adding a new vehicle type requires changing client code
- If-else logic is repeated everywhere vehicles are created
- Hard to test and maintain
- Violates Single Responsibility Principle

## Solution: Factory Pattern

The Factory pattern solves this by:

1. **Centralizing Object Creation**: All object creation logic in one place
2. **Hiding Implementation Details**: Client doesn't know which class is
   instantiated
3. **Easy to Extend**: Add new types without changing client code
4. **Loose Coupling**: Client depends on interfaces, not concrete classes

## Three Types of Factory Patterns

### 1. Simple Factory (Static Factory)

The simplest form where a factory class has a static method to create objects.

#### Structure

```
VehicleFactory (Factory Class)
    └── get_vehicle(type) → Returns Vehicle object
```

#### Implementation

```python
class VehicleFactory:
    @staticmethod
    def get_vehicle(vehicle_type):
        if vehicle_type == "car":
            return Car()
        elif vehicle_type == "bike":
            return Bike()
        elif vehicle_type == "truck":
            return Truck()
        else:
            raise ValueError("Invalid vehicle type")

# Client code - much cleaner!
vehicle_type = input("Enter vehicle (car/bike/truck): ").lower()
vehicle = VehicleFactory.get_vehicle(vehicle_type)
vehicle.drive()
```

**Pros:**
- Simple and easy to understand
- Centralizes object creation
- Client code is cleaner

**Cons:**
- Still uses if-else (can be improved)
- Not as flexible as Factory Method
- Adding new types requires modifying factory

**When to Use:**
- Small number of object types
- Simple creation logic
- Quick solution for object creation

### 2. Factory Method Pattern

Uses inheritance and abstract classes. Each concrete factory creates one type
of product.

#### Structure

```
Vehicle (Abstract Product)
    ├── Car (Concrete Product)
    └── Bike (Concrete Product)

VehicleFactory (Abstract Creator)
    ├── CarFactory (Concrete Creator)
    └── BikeFactory (Concrete Creator)
```

#### Implementation

```python
from abc import ABC, abstractmethod

# Step 1: Product Interface
class Vehicle(ABC):
    @abstractmethod
    def drive(self):
        pass

# Step 2: Concrete Products
class Car(Vehicle):
    def drive(self):
        print("Driving a Car")

class Bike(Vehicle):
    def drive(self):
        print("Riding a Bike")

# Step 3: Creator Interface (Factory)
class VehicleFactory(ABC):
    @abstractmethod
    def create_vehicle(self):
        pass

# Step 4: Concrete Factories
class CarFactory(VehicleFactory):
    def create_vehicle(self):
        return Car()

class BikeFactory(VehicleFactory):
    def create_vehicle(self):
        return Bike()

# Client code
factory = CarFactory()
vehicle = factory.create_vehicle()
vehicle.drive()
```

**Pros:**
- Follows Open/Closed Principle
- Easy to add new products and factories
- No if-else chains
- Each factory has single responsibility

**Cons:**
- More classes to maintain
- Can be overkill for simple scenarios

**When to Use:**
- You don't know exact types at compile time
- You want to extend with new types easily
- Different factories might have different creation logic

### 3. Abstract Factory Pattern

Creates families of related objects. Each factory can create multiple related
products.

#### Structure

```
Abstract Products:
    ├── Car (Abstract)
    └── Bike (Abstract)

Concrete Products:
    ├── ElectricCar, PetrolCar
    └── ElectricBike, PetrolBike

Abstract Factory:
    └── VehicleFactory (creates Car + Bike)

Concrete Factories:
    ├── ElectricVehicleFactory
    └── PetrolVehicleFactory
```

#### Implementation

```python
from abc import ABC, abstractmethod

# Step 1: Abstract Products
class Car(ABC):
    @abstractmethod
    def drive(self):
        pass

class Bike(ABC):
    @abstractmethod
    def ride(self):
        pass

# Step 2: Concrete Products (Electric Family)
class ElectricCar(Car):
    def drive(self):
        print("Driving Electric Car")

class ElectricBike(Bike):
    def ride(self):
        print("Riding Electric Bike")

# Step 3: Concrete Products (Petrol Family)
class PetrolCar(Car):
    def drive(self):
        print("Driving Petrol Car")

class PetrolBike(Bike):
    def ride(self):
        print("Riding Petrol Bike")

# Step 4: Abstract Factory
class VehicleFactory(ABC):
    @abstractmethod
    def create_car(self):
        pass

    @abstractmethod
    def create_bike(self):
        pass

# Step 5: Concrete Factories
class ElectricVehicleFactory(VehicleFactory):
    def create_car(self):
        return ElectricCar()

    def create_bike(self):
        return ElectricBike()

class PetrolVehicleFactory(VehicleFactory):
    def create_car(self):
        return PetrolCar()

    def create_bike(self):
        return PetrolBike()

# Client code
def create_vehicles(factory: VehicleFactory):
    car = factory.create_car()
    bike = factory.create_bike()
    car.drive()
    bike.ride()

# Use electric factory
create_vehicles(ElectricVehicleFactory())
# Output: Driving Electric Car
#         Riding Electric Bike
```

**Pros:**
- Ensures products from same family work together
- Easy to switch between product families
- Isolates concrete classes from client

**Cons:**
- Complex - many classes and interfaces
- Hard to extend with new product types

**When to Use:**
- You need families of related objects
- Products must be used together
- You want to provide multiple product variants

## Comparison Table

| Feature | Simple Factory | Factory Method | Abstract Factory |
|---------|---------------|----------------|------------------|
| **Complexity** | Low | Medium | High |
| **Flexibility** | Low | Medium | High |
| **Number of Products** | Multiple | One per factory | Multiple related |
| **If-Else Logic** | Yes | No | No |
| **Extensibility** | Medium | High | Medium |
| **Use Case** | Simple scenarios | Single product types | Product families |

## Real-World Use Cases

### Simple Factory
- Database connection creation (MySQL, PostgreSQL, SQLite)
- Logger creation (FileLogger, ConsoleLogger)
- Payment gateway selection

### Factory Method
- UI framework components (Button, TextField for different themes)
- Document creation (PDF, Word, Excel)
- Notification systems (Email, SMS, Push)

### Abstract Factory
- Cross-platform UI (Windows, Mac, Linux components)
- Theme systems (Dark theme, Light theme components)
- Database abstraction (MySQL, PostgreSQL with different operations)

## Benefits

1. **Loose Coupling**: Client doesn't depend on concrete classes
2. **Single Responsibility**: Object creation logic in one place
3. **Open/Closed Principle**: Easy to extend without modifying existing code
4. **Code Reusability**: Factory logic can be reused
5. **Easier Testing**: Can mock factories easily
6. **Centralized Control**: All creation logic in one place

## Key Takeaways

1. **Simple Factory**: One factory class with static method - good for simple
   cases
2. **Factory Method**: Abstract factory + concrete factories - good for
   extensibility
3. **Abstract Factory**: Creates families of related objects - good for
   product families
4. **All patterns** hide object creation from client code
5. **Choose based on complexity**: Start simple, upgrade if needed

## Common Mistakes

### Mistake 1: Using Factory for Simple Cases
```python
# Don't use factory for simple cases
class SimpleFactory:
    @staticmethod
    def create_string():
        return "Hello"  # Just use: "Hello"
```

### Mistake 2: Factory Knowing Too Much
```python
# Bad - factory has business logic
class BadFactory:
    def create_vehicle(self, type, user_role, budget):
        if user_role == "admin" and budget > 100000:
            # Too much logic in factory!
```

### Mistake 3: Not Using Interfaces
```python
# Bad - returns concrete types
def get_vehicle(type):
    if type == "car":
        return Car()  # Client depends on Car class
```

## Running the Code

### Problem (Without Factory)
```bash
python problem.py
```
- Client code directly creates objects
- Tight coupling with concrete classes
- Hard to maintain and extend

### Solutions (With Factory Patterns)
```bash
python simple_factory.py      # Simple factory pattern
python factory_method.py      # Factory method pattern
python abstract_factory.py    # Abstract factory pattern
```
- Clean client code
- Loose coupling
- Easy to extend

## Related Patterns

- **Builder Pattern**: Constructs complex objects step by step
- **Prototype Pattern**: Clones existing objects
- **Singleton Pattern**: Ensures only one instance exists

## Pattern Selection Guide

**Use Simple Factory when:**
- You have a small, fixed set of object types
- Creation logic is straightforward
- You want a quick solution

**Use Factory Method when:**
- You need to create one type of product
- You want easy extensibility
- Different factories might have different logic

**Use Abstract Factory when:**
- You need families of related objects
- Products must work together
- You want to switch between product families

---

**Remember**: Start with the simplest pattern that solves your problem. You
can always refactor to a more complex pattern if needed. Don't over-engineer!


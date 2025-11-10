# Decorator Design Pattern

## Overview

The **Decorator Pattern** is a structural design pattern that allows you to
attach new behaviors to objects by placing them inside wrapper objects that
contain these behaviors. It provides a flexible alternative to subclassing for
extending functionality. The pattern lets you add features to objects
dynamically at runtime.

## Problem Statement

When you need to add features to objects, inheritance often leads to problems:

- **Class Explosion**: Need a new class for every combination of features
- **Rigid Structure**: Can't add features at runtime
- **Violates Open/Closed Principle**: Must modify code to add new features
- **Tight Coupling**: Features are tightly coupled to classes
- **Combinatorial Explosion**: Too many subclasses for different combinations

### Example Problem

Imagine a Coffee class where you want to add different toppings (milk, sugar,
cream):

```python
class Coffee:
    def cost(self):
        return 50

class MilkCoffee(Coffee):
    def cost(self):
        return super().cost() + 10

class MilkSugarCoffee(MilkCoffee):
    def cost(self):
        return super().cost() + 5

class MilkSugarCreamCoffee(MilkSugarCoffee):
    def cost(self):
        return super().cost() + 15

# Usage
coffee = MilkSugarCreamCoffee()
print("Total cost:", coffee.cost())
```

**The Problems:**
- **Class Explosion**: Need classes for:
  - MilkCoffee, SugarCoffee, CreamCoffee
  - MilkSugarCoffee, MilkCreamCoffee, SugarCreamCoffee
  - MilkSugarCreamCoffee, etc.
- **Can't Mix Features**: Can't add features at runtime
- **Hard to Maintain**: Adding new topping requires many new classes
- **Not Flexible**: Can't have coffee with just sugar, or just cream
- **Combinatorial Explosion**: 3 toppings = 7 classes, 4 toppings = 15
  classes!

## Solution: Decorator Pattern

The Decorator pattern solves this by:

1. **Composition over Inheritance**: Uses composition instead of inheritance
2. **Dynamic Behavior**: Add features at runtime
3. **Flexible Combinations**: Mix and match features easily
4. **Single Responsibility**: Each decorator adds one feature
5. **No Class Explosion**: One decorator class per feature

### How It Works

Instead of creating subclasses:
- Create a **Base Component** interface
- Create **Concrete Component** (the object to decorate)
- Create **Decorator** base class that wraps the component
- Create **Concrete Decorators** that add specific features
- **Wrap objects** with decorators to add features dynamically

## Implementation

### Structure

```
Coffee (Component Interface)
    ├── cost()
    └── description()

SimpleCoffee (Concrete Component)
    └── Implements Coffee

CoffeeDecorator (Base Decorator)
    └── Wraps Coffee component

MilkDecorator (Concrete Decorator)
SugarDecorator (Concrete Decorator)
CreamDecorator (Concrete Decorator)
    └── All extend CoffeeDecorator
```

### Code Implementation

```python
from abc import ABC, abstractmethod

# Step 1: Component Interface
class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def description(self):
        pass

# Step 2: Concrete Component
class SimpleCoffee(Coffee):
    def cost(self):
        return 50

    def description(self):
        return "Simple Coffee"

# Step 3: Base Decorator
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee  # Wraps the component

    def cost(self):
        return self._coffee.cost()  # Delegate to wrapped object

    def description(self):
        return self._coffee.description()

# Step 4: Concrete Decorators
class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 10  # Add milk cost

    def description(self):
        return self._coffee.description() + ", Milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 5  # Add sugar cost

    def description(self):
        return self._coffee.description() + ", Sugar"

class CreamDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 15  # Add cream cost

    def description(self):
        return self._coffee.description() + ", Cream"

# Usage - build coffee dynamically!
coffee = SimpleCoffee()
print(f"{coffee.description()} → ₹{coffee.cost()}")
# Output: Simple Coffee → ₹50

# Add milk
coffee = MilkDecorator(coffee)
print(f"{coffee.description()} → ₹{coffee.cost()}")
# Output: Simple Coffee, Milk → ₹60

# Add sugar
coffee = SugarDecorator(coffee)
print(f"{coffee.description()} → ₹{coffee.cost()}")
# Output: Simple Coffee, Milk, Sugar → ₹65

# Add cream
coffee = CreamDecorator(coffee)
print(f"{coffee.description()} → ₹{coffee.cost()}")
# Output: Simple Coffee, Milk, Sugar, Cream → ₹80
```

## Key Features

### 1. Dynamic Composition

Add features at runtime:

```python
coffee = SimpleCoffee()

# Add features as needed
if customer_wants_milk:
    coffee = MilkDecorator(coffee)
if customer_wants_sugar:
    coffee = SugarDecorator(coffee)
if customer_wants_cream:
    coffee = CreamDecorator(coffee)
```

### 2. Flexible Combinations

Mix and match any combination:

```python
# Just sugar
coffee1 = SugarDecorator(SimpleCoffee())

# Milk and cream (no sugar)
coffee2 = CreamDecorator(MilkDecorator(SimpleCoffee()))

# All three
coffee3 = CreamDecorator(SugarDecorator(MilkDecorator(SimpleCoffee())))
```

### 3. Order Matters

Decorators can be applied in any order:

```python
# Different order, same result
coffee1 = SugarDecorator(MilkDecorator(SimpleCoffee()))
coffee2 = MilkDecorator(SugarDecorator(SimpleCoffee()))
# Both: Simple Coffee, Milk, Sugar → ₹65
```

### 4. No Class Explosion

With 3 toppings, you only need 3 decorator classes (not 7 subclasses):

```python
# Only 3 decorator classes needed:
# - MilkDecorator
# - SugarDecorator
# - CreamDecorator

# Can create any combination:
# - Just milk
# - Just sugar
# - Just cream
# - Milk + Sugar
# - Milk + Cream
# - Sugar + Cream
# - All three
```

## Benefits

1. **Flexibility**: Add features dynamically at runtime
2. **No Class Explosion**: One decorator per feature, not per combination
3. **Single Responsibility**: Each decorator adds one feature
4. **Open/Closed Principle**: Add decorators without modifying existing code
5. **Composition over Inheritance**: More flexible than inheritance
6. **Mix and Match**: Combine features in any way
7. **Reusable**: Decorators can be reused with different components

## When to Use

- **Dynamic Features**: Need to add features at runtime
- **Many Combinations**: Too many feature combinations for subclasses
- **Extending Functionality**: Want to extend objects without subclassing
- **Wrapping Objects**: Need to wrap objects with additional behavior
- **Feature Mixing**: Need to mix and match features flexibly
- **Avoiding Inheritance**: Want to avoid class explosion

## Real-World Use Cases

### 1. Text Formatting

```python
class Text(ABC):
    @abstractmethod
    def render(self):
        pass

class PlainText(Text):
    def __init__(self, content):
        self.content = content

    def render(self):
        return self.content

class TextDecorator(Text):
    def __init__(self, text: Text):
        self._text = text

    def render(self):
        return self._text.render()

class BoldDecorator(TextDecorator):
    def render(self):
        return f"<b>{self._text.render()}</b>"

class ItalicDecorator(TextDecorator):
    def render(self):
        return f"<i>{self._text.render()}</i>"

class UnderlineDecorator(TextDecorator):
    def render(self):
        return f"<u>{self._text.render()}</u>"

# Usage
text = PlainText("Hello World")
text = BoldDecorator(text)
text = ItalicDecorator(text)
print(text.render())  # <i><b>Hello World</b></i>
```

### 2. File I/O with Compression and Encryption

```python
class DataSource(ABC):
    @abstractmethod
    def write(self, data):
        pass

    @abstractmethod
    def read(self):
        pass

class FileDataSource(DataSource):
    def write(self, data):
        # Write to file
        pass

    def read(self):
        # Read from file
        pass

class DataSourceDecorator(DataSource):
    def __init__(self, source: DataSource):
        self._source = source

class CompressionDecorator(DataSourceDecorator):
    def write(self, data):
        compressed = compress(data)
        self._source.write(compressed)

    def read(self):
        data = self._source.read()
        return decompress(data)

class EncryptionDecorator(DataSourceDecorator):
    def write(self, data):
        encrypted = encrypt(data)
        self._source.write(encrypted)

    def read(self):
        data = self._source.read()
        return decrypt(data)

# Usage - combine compression and encryption
source = FileDataSource()
source = CompressionDecorator(source)
source = EncryptionDecorator(source)
source.write("sensitive data")
```

### 3. Web Request Middleware

```python
class RequestHandler(ABC):
    @abstractmethod
    def handle(self, request):
        pass

class BaseHandler(RequestHandler):
    def handle(self, request):
        return "Response"

class HandlerDecorator(RequestHandler):
    def __init__(self, handler: RequestHandler):
        self._handler = handler

class LoggingDecorator(HandlerDecorator):
    def handle(self, request):
        print(f"Logging: {request}")
        return self._handler.handle(request)

class AuthenticationDecorator(HandlerDecorator):
    def handle(self, request):
        if not self.is_authenticated(request):
            return "Unauthorized"
        return self._handler.handle(request)

class RateLimitingDecorator(HandlerDecorator):
    def handle(self, request):
        if self.is_rate_limited(request):
            return "Rate limit exceeded"
        return self._handler.handle(request)

# Usage - stack decorators
handler = BaseHandler()
handler = LoggingDecorator(handler)
handler = AuthenticationDecorator(handler)
handler = RateLimitingDecorator(handler)
response = handler.handle(request)
```

### 4. Pizza Toppings

```python
class Pizza(ABC):
    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def description(self):
        pass

class MargheritaPizza(Pizza):
    def cost(self):
        return 200

    def description(self):
        return "Margherita Pizza"

class PizzaDecorator(Pizza):
    def __init__(self, pizza: Pizza):
        self._pizza = pizza

class CheeseDecorator(PizzaDecorator):
    def cost(self):
        return self._pizza.cost() + 30

    def description(self):
        return self._pizza.description() + ", Extra Cheese"

class PepperoniDecorator(PizzaDecorator):
    def cost(self):
        return self._pizza.cost() + 50

    def description(self):
        return self._pizza.description() + ", Pepperoni"

class MushroomDecorator(PizzaDecorator):
    def cost(self):
        return self._pizza.cost() + 40

    def description(self):
        return self._pizza.description() + ", Mushrooms"
```

## Decorator vs Other Patterns

### Decorator vs Inheritance

| Decorator | Inheritance |
|-----------|-------------|
| Composition | Inheritance |
| Runtime | Compile-time |
| Flexible | Rigid |
| No class explosion | Class explosion |
| Dynamic | Static |

### Decorator vs Adapter

| Decorator | Adapter |
|-----------|---------|
| Adds behavior | Changes interface |
| Same interface | Different interface |
| Wraps same type | Wraps different type |
| Enhances | Converts |

### Decorator vs Strategy

| Decorator | Strategy |
|-----------|----------|
| Adds features | Changes algorithm |
| Stackable | Replaceable |
| Composition | Composition |
| Multiple decorators | One strategy |

## Key Components

1. **Component Interface**: Defines operations that can be decorated
2. **Concrete Component**: The object being decorated
3. **Base Decorator**: Wraps component and implements same interface
4. **Concrete Decorators**: Add specific features/behaviors
5. **Client**: Uses decorated objects

## Key Takeaways

1. **Decorator Pattern** = Add features to objects dynamically
2. **Composition over Inheritance** = Wrap objects instead of subclassing
3. **Runtime Flexibility** = Add features at runtime
4. **No Class Explosion** = One decorator per feature, not per combination
5. **Stackable** = Can stack multiple decorators
6. **Same Interface** = Decorators implement same interface as component

## Common Mistakes

### Mistake 1: Decorator Not Implementing Full Interface
```python
# Wrong - decorator missing methods
class BadDecorator:
    def cost(self):
        return self._coffee.cost() + 10
    # Missing description() method!
```

### Mistake 2: Modifying Original Object
```python
# Wrong - modifying original
class BadDecorator:
    def __init__(self, coffee):
        coffee.cost = lambda: coffee.cost() + 10  # Modifies original!
```

### Mistake 3: Not Delegating to Wrapped Object
```python
# Wrong - doesn't delegate
class BadDecorator:
    def cost(self):
        return 10  # Should add to wrapped object's cost!
```

## Best Practices

1. **Implement Full Interface**: Decorators must implement all component
   methods
2. **Delegate First**: Always delegate to wrapped object, then add behavior
3. **Transparent**: Decorators should be transparent (same interface)
4. **Order Matters**: Consider if decorator order should matter
5. **Document Behavior**: Make it clear what each decorator does
6. **Keep Simple**: Each decorator should add one clear feature

## Running the Code

### Problem (Without Decorator)
```bash
python without_decorator.py
```
- Class explosion
- Need new class for each combination
- Can't add features at runtime
- Hard to maintain

### Solution (With Decorator)
```bash
python with_decoracator.py
```
- No class explosion
- Add features dynamically
- Flexible combinations
- Easy to extend

## Related Patterns

- **Adapter Pattern**: Changes interface of an object
- **Proxy Pattern**: Controls access to an object
- **Chain of Responsibility**: Passes requests along a chain
- **Composite Pattern**: Composes objects into tree structures

---

**Remember**: Use Decorator pattern when you need to add features to objects
dynamically and want to avoid class explosion. It's perfect for scenarios
where you have many possible feature combinations and want flexibility at
runtime!


# Builder Design Pattern

## Overview

The **Builder Pattern** is a creational design pattern that lets you construct
complex objects step by step. Instead of creating objects with a long list of
parameters, the Builder pattern allows you to build objects using a fluent,
readable interface. This makes object construction more flexible and easier to
understand.

## Problem Statement

When creating objects with many parameters, the traditional approach has
several problems:

- **Long Parameter Lists**: Constructor with many parameters is hard to read
- **Parameter Confusion**: Easy to mix up parameter order
- **Optional Parameters**: Hard to handle optional fields
- **Telescoping Constructor**: Multiple constructors for different
  combinations
- **Immutable Objects**: Can't build immutable objects step by step

### Example Problem

Imagine building a Computer object with many components:

```python
class Computer:
    def __init__(self, cpu, ram, storage, gpu, os):
        self.cpu = cpu
        self.ram = ram
        self.storage = storage
        self.gpu = gpu
        self.os = os

# Problem: Long parameter list, hard to read
computer1 = Computer("i7", "16GB", "1TB SSD", "NVIDIA RTX 4060", "Windows 11")

# Problem: What if GPU is optional? Need to pass None
computer2 = Computer("i5", "8GB", "512GB SSD", None, "Ubuntu Linux")

# Problem: Easy to mix up parameter order
computer3 = Computer("16GB", "i7", "Windows 11", "1TB SSD", "NVIDIA RTX 4060")
# Oops! Wrong order - but no error, just wrong values!
```

**The Problems:**
- **Hard to Read**: Which parameter is which?
- **Error-Prone**: Easy to swap parameters
- **Optional Parameters**: Must pass `None` for optional fields
- **Not Flexible**: Can't build objects step by step
- **Hard to Maintain**: Adding new parameters breaks existing code

## Solution: Builder Pattern

The Builder pattern solves this by:

1. **Step-by-Step Construction**: Build objects one property at a time
2. **Fluent Interface**: Chain method calls for readability
3. **Optional Parameters**: Only set what you need
4. **Clear Intent**: Method names make it obvious what you're setting
5. **Flexible Building**: Can create different configurations easily

### How It Works

Instead of passing all parameters to constructor:
- Create a **Builder** class
- Use methods to set each property
- Methods return `self` for method chaining
- Call `build()` to get the final object

## Implementation

### Structure

```
Computer (Product)
    └── Simple constructor

ComputerBuilder (Builder)
    ├── set_cpu()
    ├── set_ram()
    ├── set_storage()
    ├── set_gpu()
    ├── set_os()
    └── build() → Returns Computer

Director (Optional)
    ├── build_gaming_pc() → Uses builder
    └── build_office_pc() → Uses builder
```

### Basic Builder Implementation

```python
class Computer:
    def __init__(self):
        # Simple constructor - no parameters
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None
        self.os = None

    def show(self):
        print(f"CPU: {self.cpu}, RAM: {self.ram}, "
              f"Storage: {self.storage}, GPU: {self.gpu}, OS: {self.os}")

class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()

    def set_cpu(self, cpu):
        self.computer.cpu = cpu
        return self  # Return self for chaining

    def set_ram(self, ram):
        self.computer.ram = ram
        return self

    def set_storage(self, storage):
        self.computer.storage = storage
        return self

    def set_gpu(self, gpu):
        self.computer.gpu = gpu
        return self

    def set_os(self, os):
        self.computer.os = os
        return self

    def build(self):
        return self.computer

# Usage - much clearer!
builder = ComputerBuilder()
computer = (builder
            .set_cpu("i7")
            .set_ram("16GB")
            .set_storage("1TB SSD")
            .set_gpu("NVIDIA RTX 4060")
            .set_os("Windows 11")
            .build())

computer.show()
```

### With Director (Optional)

The Director class defines common building sequences:

```python
class Director:
    def __init__(self, builder):
        self.builder = builder

    def build_gaming_pc(self):
        return (self.builder
                .set_cpu("Ryzen 9")
                .set_ram("32GB")
                .set_storage("2TB SSD")
                .set_gpu("NVIDIA RTX 4080")
                .set_os("Windows 11")
                .build())

    def build_office_pc(self):
        return (self.builder
                .set_cpu("Intel i5")
                .set_ram("16GB")
                .set_storage("512GB SSD")
                .set_os("Ubuntu Linux")
                .build())

# Usage with Director
builder = ComputerBuilder()
director = Director(builder)

gaming_pc = director.build_gaming_pc()
office_pc = director.build_office_pc()
```

## Key Features

### 1. Fluent Interface (Method Chaining)

Methods return `self` to allow chaining:

```python
# Instead of:
builder.set_cpu("i7")
builder.set_ram("16GB")
builder.set_storage("1TB SSD")
computer = builder.build()

# You can write:
computer = (builder
            .set_cpu("i7")
            .set_ram("16GB")
            .set_storage("1TB SSD")
            .build())
```

### 2. Optional Parameters

Only set what you need:

```python
# GPU is optional - just don't set it!
office_pc = (builder
             .set_cpu("i5")
             .set_ram("8GB")
             .set_storage("512GB SSD")
             .set_os("Ubuntu")
             .build())
# No need to pass None for GPU!
```

### 3. Clear and Readable

Method names make it obvious:

```python
# Clear what each value means
computer = (builder
            .set_cpu("i7")           # Obviously CPU
            .set_ram("16GB")         # Obviously RAM
            .set_storage("1TB SSD")  # Obviously storage
            .build())
```

### 4. Flexible Construction

Build different configurations easily:

```python
# Gaming PC
gaming = (builder
          .set_cpu("Ryzen 9")
          .set_ram("32GB")
          .set_gpu("RTX 4080")
          .build())

# Office PC
office = (builder
          .set_cpu("i5")
          .set_ram("8GB")
          .build())

# Server
server = (builder
          .set_cpu("Xeon")
          .set_ram("64GB")
          .set_storage("10TB HDD")
          .build())
```

## Benefits

1. **Readability**: Code is self-documenting
2. **Flexibility**: Easy to create different configurations
3. **Optional Parameters**: Handle optional fields naturally
4. **No Parameter Confusion**: Can't mix up parameter order
5. **Step-by-Step Building**: Build complex objects gradually
6. **Reusable Builders**: Can reuse builder for similar objects
7. **Validation**: Can add validation in `build()` method

## When to Use

- **Many Parameters**: Object has 4+ constructor parameters
- **Optional Parameters**: Many optional fields
- **Complex Objects**: Objects with many parts/components
- **Different Configurations**: Need to create objects in various ways
- **Immutable Objects**: Want to build immutable objects step by step
- **Readability**: Want clear, self-documenting code

## Real-World Use Cases

1. **SQL Query Builders**: Building complex SQL queries step by step
   ```python
   query = (QueryBuilder()
            .select("name", "email")
            .from_table("users")
            .where("age > 18")
            .order_by("name")
            .build())
   ```

2. **HTTP Request Builders**: Building HTTP requests
   ```python
   request = (RequestBuilder()
              .method("POST")
              .url("https://api.example.com/users")
              .header("Content-Type", "application/json")
              .body({"name": "John"})
              .build())
   ```

3. **Configuration Objects**: Building application configurations
   ```python
   config = (ConfigBuilder()
             .database("postgresql")
             .host("localhost")
             .port(5432)
             .username("admin")
             .build())
   ```

4. **UI Component Builders**: Building complex UI components
   ```python
   button = (ButtonBuilder()
             .text("Click Me")
             .color("blue")
             .size("large")
             .on_click(handle_click)
             .build())
   ```

## Builder vs Other Patterns

### Builder vs Factory

| Builder | Factory |
|---------|---------|
| Builds objects step by step | Creates objects in one call |
| Many parameters | Few or no parameters |
| Flexible construction | Fixed creation process |
| Method chaining | Single method call |

### Builder vs Constructor

| Builder | Constructor |
|---------|-------------|
| Step-by-step | All at once |
| Readable | Hard to read with many params |
| Optional params easy | Must pass None |
| Can't mix up order | Easy to mix up order |

## Advanced: Validation in Builder

You can add validation in the `build()` method:

```python
class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()

    def set_cpu(self, cpu):
        self.computer.cpu = cpu
        return self

    def build(self):
        # Validate before building
        if not self.computer.cpu:
            raise ValueError("CPU is required!")
        if not self.computer.ram:
            raise ValueError("RAM is required!")
        return self.computer
```

## Key Takeaways

1. **Builder Pattern** = Build complex objects step by step
2. **Fluent Interface** = Methods return `self` for chaining
3. **Optional Parameters** = Only set what you need
4. **Director** = Optional class for common build sequences
5. **Readable Code** = Self-documenting method names
6. **Flexible** = Easy to create different configurations

## Common Mistakes

### Mistake 1: Not Returning Self
```python
# Wrong - can't chain methods
def set_cpu(self, cpu):
    self.computer.cpu = cpu
    # Missing: return self
```

### Mistake 2: Building Without Validation
```python
# Wrong - no validation
def build(self):
    return self.computer  # Might be incomplete!
```

### Mistake 3: Reusing Builder Without Reset
```python
# Wrong - builder retains old values
builder = ComputerBuilder()
pc1 = builder.set_cpu("i7").build()
pc2 = builder.set_cpu("i5").build()  # Still has i7!
```

**Solution**: Create new builder or reset in `build()`:
```python
def build(self):
    computer = self.computer
    self.computer = Computer()  # Reset for next build
    return computer
```

## Running the Code

### Problem (Without Builder)
```bash
python problem.py
```
- Long parameter lists
- Hard to read
- Easy to make mistakes
- Optional parameters require None

### Solution (With Builder)
```bash
python solution.py
```
- Clear, readable code
- Method chaining
- Optional parameters handled naturally
- Director for common configurations

## Related Patterns

- **Factory Pattern**: Creates objects without specifying exact classes
- **Prototype Pattern**: Clones existing objects
- **Singleton Pattern**: Ensures only one instance exists

---

**Remember**: Use Builder when you have objects with many parameters or
optional fields. It makes your code much more readable and maintainable. The
fluent interface makes the code read like natural language!


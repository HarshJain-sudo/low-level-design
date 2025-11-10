# Observer Design Pattern

## Overview

The **Observer Pattern** is a behavioral design pattern that defines a
one-to-many dependency between objects. When one object (the subject) changes
its state, all dependent objects (observers) are automatically notified and
updated. This pattern is also known as the **Publish-Subscribe** pattern.

## Problem Statement

When you have objects that need to be notified when another object changes,
the direct approach creates several problems:

- **Tight Coupling**: Subject directly knows about all observers
- **Violates Open/Closed Principle**: Must modify subject to add new
  observers
- **Hard to Maintain**: Adding/removing observers requires code changes
- **Not Scalable**: Subject must manually notify each observer
- **No Dynamic Subscription**: Can't add/remove observers at runtime

### Example Problem

Imagine a Weather Station that needs to update multiple displays when
temperature changes:

```python
class WeatherStation:
    def __init__(self):
        self.temperature = 0
        self.mobile_display = None
        self.desktop_display = None

    def set_displays(self, mobile, desktop):
        self.mobile_display = mobile
        self.desktop_display = desktop

    def set_temperature(self, temp):
        print(f"Weather Station: Temperature updated to {temp}°C")
        self.temperature = temp
        if self.mobile_display:
            self.mobile_display.update(temp)
        if self.desktop_display:
            self.desktop_display.update(temp)

class MobileDisplay:
    def update(self, temperature):
        print(f"Mobile Display: Updated temperature = {temperature}°C")

class DesktopDisplay:
    def update(self, temperature):
        print(f"Desktop Display: Updated temperature = {temperature}°C")

# Usage
station = WeatherStation()
station.set_displays(MobileDisplay(), DesktopDisplay())
station.set_temperature(30)
```

**The Problems:**
- **Adding New Display**: Must modify WeatherStation class (violates
  Open/Closed)
- **Tight Coupling**: WeatherStation knows about MobileDisplay and
  DesktopDisplay
- **Manual Notification**: Must manually call each display's update method
- **Not Flexible**: Can't add/remove displays at runtime
- **Hard to Scale**: Adding 10 displays means 10 if statements!

## Solution: Observer Pattern

The Observer pattern solves this by:

1. **Loose Coupling**: Subject doesn't know concrete observer classes
2. **Dynamic Subscription**: Add/remove observers at runtime
3. **Automatic Notification**: Subject notifies all observers automatically
4. **Open/Closed Principle**: Add new observers without modifying subject
5. **One-to-Many**: One subject can have many observers

### How It Works

- **Subject**: Maintains a list of observers and notifies them of changes
- **Observer Interface**: Defines the update method all observers implement
- **Concrete Observers**: Implement the update method to react to changes
- **Subscription**: Observers register/unregister themselves with subject

## Implementation

### Structure

```
Subject (Abstract)
    ├── add_observer()
    ├── remove_observer()
    └── notify_observers()

WeatherStation (Concrete Subject)
    └── Implements Subject interface

Observer (Abstract)
    └── update()

MobileDisplay (Concrete Observer)
DesktopDisplay (Concrete Observer)
WebDashboard (Concrete Observer)
    └── All implement Observer interface
```

### Code Implementation

```python
from abc import ABC, abstractmethod

# Step 1: Observer Interface
class Observer(ABC):
    @abstractmethod
    def update(self, temperature):
        pass

# Step 2: Subject Interface
class Subject(ABC):
    @abstractmethod
    def add_observer(self, observer: Observer):
        pass

    @abstractmethod
    def remove_observer(self, observer: Observer):
        pass

    @abstractmethod
    def notify_observers(self):
        pass

# Step 3: Concrete Subject
class WeatherStation(Subject):
    def __init__(self):
        self._observers = []  # List of observers
        self._temperature = 0

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def set_temperature(self, temperature):
        print(f"Weather Station: Temperature updated to {temperature}°C")
        self._temperature = temperature
        self.notify_observers()  # Notify all observers

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self._temperature)

# Step 4: Concrete Observers
class MobileDisplay(Observer):
    def update(self, temperature):
        print(f"📱 Mobile Display: Temperature is now {temperature}°C")

class DesktopDisplay(Observer):
    def update(self, temperature):
        print(f"💻 Desktop Display: Temperature is now {temperature}°C")

class WebDashboard(Observer):
    def update(self, temperature):
        print(f"🌐 Web Dashboard: Temperature is now {temperature}°C")

# Step 5: Client Code
station = WeatherStation()

# Create and subscribe observers
mobile = MobileDisplay()
desktop = DesktopDisplay()
web = WebDashboard()

station.add_observer(mobile)
station.add_observer(desktop)
station.add_observer(web)

# Change temperature - all observers notified automatically!
station.set_temperature(28)
station.set_temperature(31)

# Remove observer at runtime
station.remove_observer(desktop)
station.set_temperature(35)  # Only mobile and web notified
```

## Key Features

### 1. Dynamic Subscription

Add or remove observers at runtime:

```python
station = WeatherStation()
mobile = MobileDisplay()
desktop = DesktopDisplay()

# Subscribe
station.add_observer(mobile)
station.add_observer(desktop)

# Unsubscribe
station.remove_observer(mobile)

# Add new observer later
web = WebDashboard()
station.add_observer(web)
```

### 2. Automatic Notification

Subject automatically notifies all observers:

```python
station.set_temperature(30)
# Automatically calls:
# - mobile.update(30)
# - desktop.update(30)
# - web.update(30)
```

### 3. Loose Coupling

Subject doesn't know about concrete observer classes:

```python
# Subject only knows about Observer interface
def add_observer(self, observer: Observer):  # Any Observer works!
    self._observers.append(observer)
```

### 4. Easy to Extend

Add new observers without modifying subject:

```python
# Add new observer - no changes to WeatherStation!
class TVDisplay(Observer):
    def update(self, temperature):
        print(f"📺 TV Display: {temperature}°C")

tv = TVDisplay()
station.add_observer(tv)  # Works immediately!
```

## Benefits

1. **Loose Coupling**: Subject and observers are loosely coupled
2. **Dynamic Relationships**: Add/remove observers at runtime
3. **Open/Closed Principle**: Add observers without modifying subject
4. **Automatic Updates**: Observers updated automatically
5. **One-to-Many**: One subject can notify many observers
6. **Reusable**: Observer classes can be reused
7. **Testable**: Easy to test subject and observers separately

## When to Use

- **Event Handling**: When events need to notify multiple handlers
- **Model-View Architecture**: Model (subject) updates views (observers)
- **Notification Systems**: Notify multiple components of changes
- **Real-time Updates**: When multiple objects need real-time updates
- **Decoupling**: When you want to decouple sender and receivers
- **Broadcast Communication**: One-to-many communication needed

## Real-World Use Cases

### 1. Stock Price Updates

```python
class StockMarket(Subject):
    def __init__(self):
        self._observers = []
        self._price = 0

    def add_observer(self, observer):
        self._observers.append(observer)

    def set_price(self, price):
        self._price = price
        self.notify_observers()

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self._price)

class Trader(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, price):
        print(f"{self.name}: Stock price is now ${price}")

# Usage
market = StockMarket()
trader1 = Trader("Alice")
trader2 = Trader("Bob")

market.add_observer(trader1)
market.add_observer(trader2)
market.set_price(150)  # Both traders notified
```

### 2. News Publisher

```python
class NewsPublisher(Subject):
    def __init__(self):
        self._observers = []
        self._news = ""

    def add_observer(self, observer):
        self._observers.append(observer)

    def publish_news(self, news):
        self._news = news
        self.notify_observers()

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self._news)

class EmailSubscriber(Observer):
    def update(self, news):
        print(f"📧 Email: {news}")

class SMSSubscriber(Observer):
    def update(self, news):
        print(f"📱 SMS: {news}")

class PushSubscriber(Observer):
    def update(self, news):
        print(f"🔔 Push: {news}")
```

### 3. UI Event Handling

```python
class Button(Subject):
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def click(self):
        print("Button clicked!")
        self.notify_observers()

    def notify_observers(self):
        for observer in self._observers:
            observer.update()

class LogHandler(Observer):
    def update(self):
        print("Log: Button was clicked")

class EmailHandler(Observer):
    def update(self):
        print("Email: Button click notification sent")

# Usage
button = Button()
button.add_observer(LogHandler())
button.add_observer(EmailHandler())
button.click()  # Both handlers notified
```

### 4. Model-View-Controller (MVC)

```python
# Model (Subject)
class DataModel(Subject):
    def __init__(self):
        self._observers = []
        self._data = {}

    def add_observer(self, observer):
        self._observers.append(observer)

    def update_data(self, key, value):
        self._data[key] = value
        self.notify_observers()

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self._data)

# View (Observer)
class ChartView(Observer):
    def update(self, data):
        print(f"Chart updated with: {data}")

class TableView(Observer):
    def update(self, data):
        print(f"Table updated with: {data}")
```

## Observer vs Other Patterns

### Observer vs Mediator

| Observer | Mediator |
|----------|----------|
| One-to-many | Many-to-many |
| Subject notifies observers | Mediator coordinates objects |
| Loose coupling | Centralized communication |
| Push updates | Pull updates |

### Observer vs Publish-Subscribe

| Observer | Pub-Sub |
|----------|---------|
| Direct reference | Message broker |
| Synchronous | Can be asynchronous |
| Subject knows observers | Publisher doesn't know subscribers |
| Simpler | More complex |

## Push vs Pull Model

### Push Model (Current Implementation)

Subject sends all data to observers:

```python
def notify_observers(self):
    for observer in self._observers:
        observer.update(self._temperature)  # Pushes temperature
```

**Pros:** Simple, observers get data directly
**Cons:** Observers get data they might not need

### Pull Model

Observers pull data they need:

```python
def notify_observers(self):
    for observer in self._observers:
        observer.update()  # Observer pulls data it needs

class MobileDisplay(Observer):
    def update(self):
        temp = self.subject.get_temperature()  # Pull what it needs
        print(f"Temperature: {temp}°C")
```

**Pros:** Observers get only what they need
**Cons:** More complex, observers need reference to subject

## Key Components

1. **Subject Interface**: Defines methods to manage observers
2. **Concrete Subject**: Maintains observer list and notifies them
3. **Observer Interface**: Defines update method
4. **Concrete Observers**: Implement update to react to changes
5. **Client**: Creates subject and observers, manages subscriptions

## Key Takeaways

1. **Observer Pattern** = One subject notifies many observers
2. **Loose Coupling** = Subject doesn't know concrete observer classes
3. **Dynamic Subscription** = Add/remove observers at runtime
4. **Automatic Notification** = Subject notifies all observers
5. **Open/Closed Principle** = Add observers without modifying subject
6. **One-to-Many** = One subject, many observers

## Common Mistakes

### Mistake 1: Subject Creating Observers
```python
# Wrong - subject shouldn't create observers
class WeatherStation:
    def __init__(self):
        self.mobile = MobileDisplay()  # Subject creates observer
```

### Mistake 2: Observers Knowing About Each Other
```python
# Wrong - observers shouldn't know about each other
class MobileDisplay:
    def update(self, temp):
        self.desktop.update(temp)  # Observer updates another observer
```

### Mistake 3: Notifying During Iteration
```python
# Wrong - modifying list during iteration
def notify_observers(self):
    for observer in self._observers:
        observer.update()  # If observer removes itself, error!
```

**Solution:** Create a copy of the list:
```python
def notify_observers(self):
    for observer in list(self._observers):  # Copy the list
        observer.update()
```

## Best Practices

1. **Use Interfaces**: Define Observer and Subject interfaces
2. **Manage Subscriptions**: Provide add/remove observer methods
3. **Handle Errors**: Don't let one observer's error break others
4. **Consider Order**: Decide if observer notification order matters
5. **Memory Management**: Remove observers when no longer needed
6. **Thread Safety**: Consider thread safety for multi-threaded apps

## Running the Code

### Problem (Without Observer)
```bash
python without_observer.py
```
- Tight coupling between subject and observers
- Must modify subject to add observers
- Manual notification
- Not scalable

### Solution (With Observer)
```bash
python with_observer.py
```
- Loose coupling
- Dynamic subscription
- Automatic notification
- Easy to extend

## Related Patterns

- **Mediator Pattern**: Coordinates communication between objects
- **Command Pattern**: Encapsulates requests as objects
- **Chain of Responsibility**: Passes requests along a chain

---

**Remember**: Use Observer pattern when you need one object to notify many
other objects about changes. It's perfect for event handling, MVC
architecture, and any scenario where you need loose coupling between a subject
and its dependents!


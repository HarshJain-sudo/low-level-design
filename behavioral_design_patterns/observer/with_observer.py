from abc import ABC, abstractmethod

# Step 1️⃣: Observer Interface
class Observer(ABC):
    @abstractmethod
    def update(self, temperature):
        pass


# Step 2️⃣: Subject Interface
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


# Step 3️⃣: Concrete Subject (WeatherStation)
class WeatherStation(Subject):
    def __init__(self):
        self._observers = []
        self._temperature = 0

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def set_temperature(self, temperature):
        print(f"\nWeather Station: Temperature updated to {temperature}°C 🌡️")
        self._temperature = temperature
        self.notify_observers()

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self._temperature)


# Step 4️⃣: Concrete Observers
class MobileDisplay(Observer):
    def update(self, temperature):
        print(f"📱 Mobile Display: Temperature is now {temperature}°C")

class DesktopDisplay(Observer):
    def update(self, temperature):
        print(f"💻 Desktop Display: Temperature is now {temperature}°C")

class WebDashboard(Observer):
    def update(self, temperature):
        print(f"🌐 Web Dashboard: Temperature is now {temperature}°C")


# Step 5️⃣: Client Code
if __name__ == "__main__":
    # Create subject
    station = WeatherStation()

    # Create observers
    mobile = MobileDisplay()
    desktop = DesktopDisplay()
    web = WebDashboard()

    # Subscribe them
    station.add_observer(mobile)
    station.add_observer(desktop)
    station.add_observer(web)

    # Change temperature
    station.set_temperature(28)
    station.set_temperature(31)

    # Remove one observer
    station.remove_observer(desktop)
    station.set_temperature(35)

from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def description(self):
        pass

class SimpleCoffee(Coffee):
    def cost(self):
        return 50

    def description(self):
        return "Simple Coffee"

class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost()

    def description(self):
        return self._coffee.description()


class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 10

    def description(self):
        return self._coffee.description() + ", Milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 5

    def description(self):
        return self._coffee.description() + ", Sugar"

class CreamDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 15

    def description(self):
        return self._coffee.description() + ", Cream"


if __name__ == "__main__":
    coffee = SimpleCoffee()
    print(f"{coffee.description()} → ₹{coffee.cost()}")

    # Add milk
    coffee = MilkDecorator(coffee)
    print(f"{coffee.description()} → ₹{coffee.cost()}")

    # Add sugar
    coffee = SugarDecorator(coffee)
    print(f"{coffee.description()} → ₹{coffee.cost()}")

    # Add cream
    coffee = CreamDecorator(coffee)
    print(f"{coffee.description()} → ₹{coffee.cost()}")

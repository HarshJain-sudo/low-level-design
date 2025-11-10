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


# Client
coffee = MilkSugarCreamCoffee()
print("Total cost:", coffee.cost())


"""
Every new combination = a new subclass 😩
Explosion of classes (MilkCoffee, SugarCoffee, CreamCoffee, etc.)
Hard to manage or extend.
"""

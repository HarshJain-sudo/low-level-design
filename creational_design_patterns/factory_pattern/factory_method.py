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


# Step 5: Client code
def get_factory(vehicle_type):
    if vehicle_type == "car":
        return CarFactory()
    elif vehicle_type == "bike":
        return BikeFactory()
    else:
        raise ValueError("Unknown vehicle type")


# Client
factory = get_factory("bike")
vehicle = factory.create_vehicle()
vehicle.drive()

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


# Step 2: Concrete Products (Electric)
class ElectricCar(Car):
    def drive(self):
        print("Driving Electric Car")

class ElectricBike(Bike):
    def ride(self):
        print("Riding Electric Bike")


# Step 3: Concrete Products (Petrol)
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


# Step 6: Client code
def create_vehicles(factory: VehicleFactory):
    car = factory.create_car()
    bike = factory.create_bike()
    car.drive()
    bike.ride()


# Test both factories
print("Electric Factory:")
create_vehicles(ElectricVehicleFactory())

print("\nPetrol Factory:")
create_vehicles(PetrolVehicleFactory())

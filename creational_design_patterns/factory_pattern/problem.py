class Car:
    @staticmethod
    def drive():
        print("Driving a Car")

class Bike:
    @staticmethod
    def drive():
        print("Riding a Bike")

class Truck:
    @staticmethod
    def drive():
        print("Driving a Truck")


# Client code (problematic)
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

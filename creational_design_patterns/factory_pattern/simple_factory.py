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


# Factory class
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


# Client code
vehicle_type = input("Enter vehicle (car/bike/truck): ").lower()
vehicle = VehicleFactory.get_vehicle(vehicle_type)
vehicle.drive()

from abc import ABC, abstractmethod

class DriveStrategy(ABC):
    @abstractmethod
    def drive(self):
        pass

class RoadDriveStrategy(DriveStrategy):
    def drive(self):
        print("Driving on the road 🛣️")

class OffRoadDriveStrategy(DriveStrategy):
    def drive(self):
        print("Driving off-road 🏞️")

class AirDriveStrategy(DriveStrategy):
    def drive(self):
        print("Flying in the air ✈️")

class WaterDriveStrategy(DriveStrategy):
    def drive(self):
        print("Sailing on water 🚤")


class Vehicle:
    def __init__(self, name, strategy: DriveStrategy):
        self.name = name
        self._drive_strategy = strategy

    def drive(self):
        print(f"{self.name}:", end=" ")
        self._drive_strategy.drive()

    def set_drive_strategy(self, new_strategy: DriveStrategy):
        self._drive_strategy = new_strategy


if __name__ == "__main__":
    car = Vehicle("Car", RoadDriveStrategy())
    jeep = Vehicle("Jeep", OffRoadDriveStrategy())
    plane = Vehicle("Plane", AirDriveStrategy())

    car.drive()
    jeep.drive()
    plane.drive()

    # Change behavior dynamically at runtime!
    print("\nChanging Jeep's behavior to AirDrive 🚀")
    jeep.set_drive_strategy(AirDriveStrategy())
    jeep.drive()

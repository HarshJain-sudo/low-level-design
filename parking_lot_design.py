import abc
import datetime
import typing
import uuid
from enum import Enum

class VehicleSize(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class Vehicle:
    def __init__(self, size: VehicleSize, licence_number: str):
        self.size = size
        self.licence_number = licence_number

    def get_vehicle_size(self):
        return self.size

    def get_licence_number(self):
        return self.licence_number

class MotorCycle(Vehicle):
    def __init__(self, licence_number: str):
        super().__init__(
            size=VehicleSize.SMALL, licence_number=licence_number)

class Car(Vehicle):
    def __init__(self, licence_number: str):
        super().__init__(
            size=VehicleSize.MEDIUM, licence_number=licence_number)

class Truck(Vehicle):
    def __init__(self, licence_number: str):
        super().__init__(
            size=VehicleSize.LARGE, licence_number=licence_number)

class ParkingSlot:
    def __init__(self, vehicle_size: VehicleSize):
        self.parking_slot_id = str(uuid.uuid4())
        self.vehicle_size = vehicle_size
        self.is_occupied = False
        self.vehicle = None

    def park_vehicle(self, vehicle: Vehicle):
        self.vehicle = vehicle
        self.is_occupied = True

    def remove_vehicle(self):
        self.vehicle = None
        self.is_occupied = False

class ParkingFloor:
    def __init__(self, floor_num: int):
        self.floor_num = floor_num
        self.slots: typing.List[ParkingSlot] = []

    def add_parking_slot(self, slot: ParkingSlot):
        self.slots.append(slot)

    def get_available_slot(self, vehicle_size: VehicleSize):
        for slot in self.slots:
            if not slot.is_occupied and slot.vehicle_size == vehicle_size:
                return slot
        return None


class Ticket:
    def __init__(self, licence_number: str, issued_time: datetime.datetime):
        self.ticket_id = str(uuid.uuid4())
        self.licence_number = licence_number
        self.issued_time = issued_time
        self.leave_datetime = None

    def close_ticket(self):
        self.leave_datetime = datetime.datetime.now()


class FeeStrategy(abc.ABC):
    @abc.abstractmethod
    def calculate_fee(self, ticket: Ticket) -> float:
        pass


class HourlyFeeStrategy(FeeStrategy):
    def calculate_fee(self, ticket: Ticket) -> float:
        hours = (ticket.leave_datetime - ticket.issued_time).total_seconds() / 3600
        return round(hours * 20, 2)


class FlatFeeStrategy(FeeStrategy):
    def calculate_fee(self, ticket: Ticket) -> float:
        return 50


class ProgressiveFeeStrategy(FeeStrategy):
    def calculate_fee(self, ticket: Ticket) -> float:
        hours = (ticket.leave_datetime - ticket.issued_time).total_seconds() / 3600
        if hours <= 2:
            return 30
        elif hours <= 5:
            return 60
        else:
            return 100

class ParkingLot:
    def __init__(self, name: str):
        self.name = name
        self.floors: typing.List[ParkingFloor] = []

    def add_floor(self, floor: ParkingFloor):
        self.floors.append(floor)

    def find_slot_for_vehicle(self, vehicle_size: VehicleSize):
        for floor in self.floors:
            slot = floor.get_available_slot(vehicle_size)
            if slot:
                return slot
        return None

class ParkingManager:
    def __init__(self, parking_lot: ParkingLot, fee_strategy: FeeStrategy):
        self.parking_lot = parking_lot
        self.fee_strategy = fee_strategy
        self.active_tickets: typing.Dict[str, Ticket] = {}

    def park_vehicle(self, vehicle: Vehicle) -> Ticket:
        slot = self.parking_lot.find_slot_for_vehicle(vehicle.size)
        if not slot:
            print(f"No available slot for vehicle size {vehicle.size}")
            return None

        slot.park_vehicle(vehicle)
        ticket = Ticket(vehicle.licence_number, datetime.datetime.now())
        self.active_tickets[ticket.ticket_id] = ticket
        print(f"Vehicle {vehicle.licence_number} parked at slot {slot.parking_slot_id}")
        return ticket

    def unpark_vehicle(self, ticket_id: str):
        if ticket_id not in self.active_tickets:
            print("Invalid ticket ID.")
            return None

        ticket = self.active_tickets[ticket_id]
        ticket.close_ticket()
        fee = self.fee_strategy.calculate_fee(ticket)

        # free up slot
        for floor in self.parking_lot.floors:
            for slot in floor.slots:
                if slot.vehicle and slot.vehicle.licence_number == ticket.licence_number:
                    slot.remove_vehicle()

        print(f"Vehicle {ticket.licence_number} left. Fee: ₹{fee}")
        del self.active_tickets[ticket_id]
        return fee



if __name__ == "__main__":
    lot = ParkingLot("Parking 1")
    floor1 = ParkingFloor(1)
    floor2 = ParkingFloor(2)

    for _ in range(2):
        floor1.add_parking_slot(ParkingSlot(VehicleSize.SMALL))
        floor1.add_parking_slot(ParkingSlot(VehicleSize.MEDIUM))
    for _ in range(2):
        floor2.add_parking_slot(ParkingSlot(VehicleSize.LARGE))

    lot.add_floor(floor1)
    lot.add_floor(floor2)

    manager = ParkingManager(lot, ProgressiveFeeStrategy())

    # Park vehicles
    car = Car("TS09AB1234")
    truck = Truck("AP11XY9999")

    car_ticket = manager.park_vehicle(car)
    truck_ticket = manager.park_vehicle(truck)

    import time
    time.sleep(2)

    # Unpark
    manager.unpark_vehicle(car_ticket.ticket_id)
    manager.unpark_vehicle(truck_ticket.ticket_id)

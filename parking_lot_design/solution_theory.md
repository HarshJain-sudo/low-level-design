# Parking Lot Design - Solution Theory: Bottom-Up Approach

## What is Bottom-Up Approach?
----------------------------
Bottom-Up approach means starting with the smallest, most basic components
and building up to more complex systems. We identify the fundamental building
blocks first, then combine them to create higher-level functionality.

## Step-by-Step Approach for Parking Lot:
---------------------------------------

### STEP 1: Identify Core Primitives (Lowest Level)
------------------------------------------------
Start with the most basic, indivisible components:

1. **VehicleSize (Enum)**
   - Purpose: Represents the size categories of vehicles
   - Why first: It's a fundamental classification that everything else depends
     on
   - Values: SMALL, MEDIUM, LARGE
   - Used by: Vehicle, ParkingSlot

2. **DateTime (Built-in)**
   - Purpose: Track time for ticket issuance and fee calculation
   - Why early: Needed for ticket management and fee calculation
   - Used by: Ticket, FeeStrategy

### STEP 2: Build Basic Entities (Next Level)
------------------------------------------
Combine primitives to create basic entities:

3. **Vehicle (Base Class)**
   - Purpose: Represents a vehicle that needs parking
   - Depends on: VehicleSize
   - Properties: size, licence_number
   - Methods: get_vehicle_size(), get_licence_number()
   - Subclasses: MotorCycle, Car, Truck (specific vehicle types)

4. **ParkingSlot**
   - Purpose: Represents a single parking space
   - Depends on: VehicleSize, Vehicle
   - Properties: parking_slot_id, vehicle_size, is_occupied, vehicle
   - Methods:
     * park_vehicle(vehicle) - Assigns vehicle to slot
     * remove_vehicle() - Frees the slot
   - Why early: It's the atomic unit of parking

### STEP 3: Build Composite Structures
-------------------------------------
Combine basic entities to create larger structures:

5. **ParkingFloor**
   - Purpose: Represents a floor containing multiple parking slots
   - Depends on: ParkingSlot, VehicleSize
   - Properties: floor_num, slots (list of ParkingSlot)
   - Methods:
     * add_parking_slot(slot) - Adds slot to floor
     * get_available_slot(vehicle_size) - Finds available slot for vehicle
   - Why composite: Groups slots together logically

6. **Ticket**
   - Purpose: Represents a parking ticket issued to a vehicle
   - Depends on: DateTime
   - Properties: ticket_id, licence_number, issued_time, leave_datetime
   - Methods: close_ticket() - Records exit time
   - Why separate: Tracks parking session independently

### STEP 4: Build Business Logic Components
----------------------------------------
Add components that contain business rules:

7. **FeeStrategy (Strategy Pattern)**
   - Purpose: Calculate parking fees using different algorithms
   - Depends on: Ticket
   - Why separate: Different fee calculation methods (hourly, flat, progressive)
   - Components:
     * FeeStrategy (abstract interface)
     * HourlyFeeStrategy - Charges based on hours parked
     * FlatFeeStrategy - Fixed fee regardless of time
     * ProgressiveFeeStrategy - Tiered pricing based on duration
   - Why Strategy Pattern: Allows switching fee calculation methods easily

### STEP 5: Build Aggregate Structures
------------------------------------
Combine structures to create complete systems:

8. **ParkingLot**
   - Purpose: Represents the entire parking facility
   - Depends on: ParkingFloor
   - Properties: name, floors (list of ParkingFloor)
   - Methods:
     * add_floor(floor) - Adds floor to parking lot
     * find_slot_for_vehicle(vehicle_size) - Searches all floors for
       available slot
   - Why aggregate: Combines multiple floors into one facility

### STEP 6: Build Manager/Controller Layer
------------------------------------------
Create the top-level orchestrator:

9. **ParkingManager**
   - Purpose: Orchestrates parking operations and manages tickets
   - Depends on: ParkingLot, FeeStrategy, Vehicle, Ticket
   - Properties: parking_lot, fee_strategy, active_tickets (dictionary)
   - Methods:
     * park_vehicle(vehicle) - Parks vehicle and issues ticket
     * unpark_vehicle(ticket_id) - Removes vehicle and calculates fee
   - Why manager: Coordinates between parking lot, tickets, and fee
     calculation

## Bottom-Up Building Order:
-------------------------
**Level 1 (Primitives):**
  VehicleSize (Enum) → DateTime (Built-in)

**Level 2 (Basic Entities):**
  Vehicle (uses VehicleSize)
  ParkingSlot (uses VehicleSize, Vehicle)

**Level 3 (Composite Structures):**
  ParkingFloor (uses ParkingSlot, VehicleSize)
  Ticket (uses DateTime)

**Level 4 (Business Logic):**
  FeeStrategy (uses Ticket)
  - HourlyFeeStrategy
  - FlatFeeStrategy
  - ProgressiveFeeStrategy

**Level 5 (Aggregate Structures):**
  ParkingLot (uses ParkingFloor)

**Level 6 (Orchestration):**
  ParkingManager (uses ParkingLot, FeeStrategy, Vehicle, Ticket)

**Level 7 (Usage/Interface):**
  Main function (uses ParkingManager)

## Dependency Flow:
------------------
```
VehicleSize (Enum)
    ↓
Vehicle → ParkingSlot
    ↓         ↓
    └─────────┘
         ↓
    ParkingFloor
         ↓
    ParkingLot
         ↓
    ParkingManager ← FeeStrategy ← Ticket
```

## Benefits of Bottom-Up Approach:
-------------------------------
1. **Clear Dependencies**: Each level depends only on lower levels
2. **Testable**: Can test each component independently
   - Test Vehicle creation
   - Test ParkingSlot operations
   - Test ParkingFloor slot finding
   - Test FeeStrategy calculations
   - Test ParkingManager operations
3. **Reusable**: Lower-level components can be reused
   - Vehicle can be used in other contexts
   - FeeStrategy can be applied to different parking systems
4. **Maintainable**: Changes in one level don't affect others
   - Change fee calculation? Only modify FeeStrategy
   - Add new vehicle type? Only extend Vehicle class
5. **Understandable**: Build complexity gradually
   - Start simple, add complexity layer by layer

## Key Design Principles Applied:
------------------------------
1. **Single Responsibility**: Each class has one clear purpose
   - Vehicle: Represents a vehicle
   - ParkingSlot: Manages one parking space
   - ParkingFloor: Manages slots on one floor
   - FeeStrategy: Calculates fees
   - ParkingManager: Orchestrates operations

2. **Strategy Pattern**: Fee calculation is pluggable
   - Can switch between different fee strategies
   - Easy to add new fee calculation methods

3. **Composition over Inheritance**: 
   - ParkingLot contains ParkingFloors
   - ParkingFloor contains ParkingSlots
   - ParkingManager uses ParkingLot and FeeStrategy

4. **Separation of Concerns**: 
   - Data structures (Vehicle, Slot, Floor, Lot)
   - Business logic (FeeStrategy)
   - Orchestration (ParkingManager)

5. **Encapsulation**: 
   - Internal state is protected
   - Methods provide controlled access

## Testing Strategy (Bottom-Up):
-----------------------------
1. **Test VehicleSize enum** (simplest)
2. **Test Vehicle classes** (MotorCycle, Car, Truck)
3. **Test ParkingSlot** with Vehicle
4. **Test ParkingFloor** with multiple slots
5. **Test Ticket** creation and closing
6. **Test FeeStrategy** implementations independently
7. **Test ParkingLot** with multiple floors
8. **Test ParkingManager** with all components
9. **Integration test** with Main function

## Real-World Extensions (Future):
--------------------------------
This bottom-up approach makes it easy to extend:

- **Level 1 Extension**: Add new VehicleSize (e.g., EXTRA_LARGE)
- **Level 2 Extension**: Add new Vehicle types (e.g., Bus, RV)
- **Level 3 Extension**: Add features to ParkingFloor (e.g., reserved slots)
- **Level 4 Extension**: Add new FeeStrategy (e.g., PeakHourStrategy)
- **Level 5 Extension**: Add features to ParkingLot (e.g., multiple entrances)
- **Level 6 Extension**: Add features to ParkingManager (e.g., payment
  processing)

Each extension only affects the relevant level and above, not the levels
below.

## Summary:
---------
The bottom-up approach ensures:
- ✅ Each component is built on solid foundations
- ✅ Dependencies flow in one direction (downward)
- ✅ Components can be tested independently
- ✅ System is easy to understand and maintain
- ✅ Extensions don't break existing functionality

This approach makes the parking lot system robust, maintainable, and
extensible.


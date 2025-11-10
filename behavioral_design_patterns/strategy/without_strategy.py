class Vehicle:
    def __init__(self, type):
        self.type = type

    def drive(self):
        if self.type == "car":
            print("Driving on the road 🛣️")
        elif self.type == "offroad":
            print("Driving off-road 🏞️")
        elif self.type == "airplane":
            print("Flying in the air ✈️")
        else:
            print("Unknown vehicle type")


# Client code
v1 = Vehicle("car")
v2 = Vehicle("airplane")

v1.drive()
v2.drive()

 # Problems:
# Adding a new vehicle type (e.g., boat) means editing the class — violates Open/Closed Principle.
# Vehicle class has too many responsibilities.
# Hard to maintain, test, and extend.
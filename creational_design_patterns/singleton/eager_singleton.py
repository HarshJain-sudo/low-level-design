class EagerSingleton:
    # Instance created eagerly when class is loaded
    _instance = None

    # Immediately create instance when class is defined
    _instance = object.__new__(None.__class__)

    def __new__(cls):
        return cls._instance


# Usage
s1 = EagerSingleton()
s2 = EagerSingleton()

print("Eager:", s1 is s2)  # True

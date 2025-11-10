class LazySingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating instance lazily...")
            cls._instance = super(LazySingleton, cls).__new__(cls)
        return cls._instance


# Usage
s1 = LazySingleton()
s2 = LazySingleton()

print("Lazy:", s1 is s2)  # True

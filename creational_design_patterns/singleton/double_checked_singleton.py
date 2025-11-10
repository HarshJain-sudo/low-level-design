import threading

class DoubleCheckedSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        # First check (no locking)
        if cls._instance is None:
            with cls._lock:
                # Second check (inside lock)
                if cls._instance is None:
                    print("Creating double-checked instance...")
                    cls._instance = super(DoubleCheckedSingleton, cls).__new__(cls)
        return cls._instance


# Usage
def create_instance():
    obj = DoubleCheckedSingleton()
    print(f"Instance ID: {id(obj)}")

threads = [threading.Thread(target=create_instance) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

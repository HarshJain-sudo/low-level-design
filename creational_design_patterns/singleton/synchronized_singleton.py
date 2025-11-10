import threading

class SynchronizedSingleton:
    _instance = None
    _lock = threading.Lock()  # synchronization lock

    def __new__(cls):
        with cls._lock:  # only one thread can enter this block
            if cls._instance is None:
                print("Creating synchronized instance...")
                cls._instance = super(SynchronizedSingleton, cls).__new__(cls)
        return cls._instance


# Usage
def create_instance():
    obj = SynchronizedSingleton()
    print(f"Instance ID: {id(obj)}")

# Run multiple threads
threads = [threading.Thread(target=create_instance) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

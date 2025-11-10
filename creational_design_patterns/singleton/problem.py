class Logger:
    def __init__(self):
        print("Creating new Logger instance...")
        self.log_messages = []

    def log(self, message):
        self.log_messages.append(message)
        print(f"LOG: {message}")

# Multiple instances of Logger
logger1 = Logger()
logger2 = Logger()

logger1.log("User logged in")
logger2.log("User clicked button")

print(logger1.log_messages)
print(logger2.log_messages)

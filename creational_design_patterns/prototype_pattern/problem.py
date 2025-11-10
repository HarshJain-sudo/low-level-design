import time

class UserProfile:
    def __init__(self, name, role, permissions, preferences):
        print("Creating user profile... (takes time)")
        time.sleep(1)  # simulate heavy initialization (database calls, API requests)
        self.name = name
        self.role = role
        self.permissions = permissions
        self.preferences = preferences

    def show(self):
        print(f"Name: {self.name}")
        print(f"Role: {self.role}")
        print(f"Permissions: {self.permissions}")
        print(f"Preferences: {self.preferences}")


# Let's create multiple users
user1 = UserProfile("Alice", "Admin", ["read", "write", "delete"], {"theme": "dark"})
user2 = UserProfile("Bob", "Admin", ["read", "write", "delete"], {"theme": "dark"})
user3 = UserProfile("Charlie", "Admin", ["read", "write", "delete"], {"theme": "dark"})

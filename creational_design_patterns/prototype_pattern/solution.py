import copy
import time
from abc import ABC, abstractmethod

class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass


class UserProfile(Prototype):
    def __init__(self, name, role, permissions, preferences):
        print("Creating user profile... (takes time)")
        time.sleep(1)  # simulate heavy setup
        self.name = name
        self.role = role
        self.permissions = permissions
        self.preferences = preferences

    def clone(self):
        return copy.deepcopy(self)

    def show(self):
        print(f"Name: {self.name}")
        print(f"Role: {self.role}")
        print(f"Permissions: {self.permissions}")
        print(f"Preferences: {self.preferences}")


class AdminProfile(Prototype):
    def __init__(self, name, access_level):
        print("Creating admin profile... (heavy initialization)")
        time.sleep(1)
        self.name = name
        self.access_level = access_level

    def clone(self):
        return copy.deepcopy(self)

    def show(self):
        print(f"Admin: {self.name} | Access Level: {self.access_level}")


if __name__ == "__main__":
    # Create prototype objects
    prototype_user = UserProfile("PrototypeUser", "Member", ["read"], {"theme": "dark"})
    prototype_admin = AdminProfile("SuperAdmin", "Full")

    # Clone and modify user profiles
    user1 = prototype_user.clone()
    user1.name = "Alice"

    user2 = prototype_user.clone()
    user2.name = "Bob"
    user2.preferences["theme"] = "light"

    # Clone admin profile
    admin1 = prototype_admin.clone()
    admin1.name = "Admin_Alice"

    # Display all
    print("\n--- Cloned Profiles ---")
    user1.show()
    user2.show()
    admin1.show()

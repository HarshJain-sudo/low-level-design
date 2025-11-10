class Computer:
    def __init__(self, cpu, ram, storage, gpu, os):
        self.cpu = cpu
        self.ram = ram
        self.storage = storage
        self.gpu = gpu
        self.os = os

    def show(self):
        print(f"Computer -> CPU: {self.cpu}, RAM: {self.ram}, Storage: {self.storage}, GPU: {self.gpu}, OS: {self.os}")


# Building an object manually (messy)
computer1 = Computer("i7", "16GB", "1TB SSD", "NVIDIA RTX 4060", "Windows 11")
computer2 = Computer("i5", "8GB", "512GB SSD", None, "Ubuntu Linux")

computer1.show()
computer2.show()

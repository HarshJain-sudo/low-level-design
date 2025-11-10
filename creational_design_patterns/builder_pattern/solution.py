class Computer:
    def __init__(self):
        self.cpu = self.ram = self.storage = self.gpu = self.os = None

    def show(self):
        print(f"Computer -> CPU: {self.cpu}, RAM: {self.ram}, Storage: {self.storage}, GPU: {self.gpu}, OS: {self.os}")


class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()

    def set_cpu(self, cpu): self.computer.cpu = cpu; return self
    def set_ram(self, ram): self.computer.ram = ram; return self
    def set_storage(self, storage): self.computer.storage = storage; return self
    def set_gpu(self, gpu): self.computer.gpu = gpu; return self
    def set_os(self, os): self.computer.os = os; return self
    def build(self): return self.computer


# Director — controls the sequence of building steps
class Director:
    def __init__(self, builder):
        self.builder = builder

    def build_gaming_pc(self):
        return (self.builder
                .set_cpu("Ryzen 9")
                .set_ram("32GB")
                .set_storage("2TB SSD")
                .set_gpu("NVIDIA RTX 4080")
                .set_os("Windows 11")
                .build())

    def build_office_pc(self):
        return (self.builder
                .set_cpu("Intel i5")
                .set_ram("16GB")
                .set_storage("512GB SSD")
                .set_os("Ubuntu Linux")
                .build())


# Client
builder = ComputerBuilder()
director = Director(builder)

gaming_pc = director.build_gaming_pc()
office_pc = director.build_office_pc()

gaming_pc.show()
office_pc.show()

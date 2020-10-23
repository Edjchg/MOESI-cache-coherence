class Instruction:
    def __init__(self):
        self.processor_number = 0
        self.operation = ""
        self.operation_number = 0  # 0 -> write / 1 -> read / 2 -> calc
        self.address_bin = 0
        self.data = 0

    def get_processor_number(self):
        return self.processor_number

    def set_processor_number(self, number):
        self.processor_number = number

    def get_operation(self):
        return self.operation

    def set_operation(self, operation):
        self.operation = operation
        if operation == "write":
            self.operation_number = 2
        elif operation == "read":
            self.operation_number = 0
        else:
            self.operation_number = 1

    def get_operation_number(self):
        return self.operation_number

    def get_address_bin(self):
        # self.address_bin = bin(self.address_bin)
        # return self.address_bin[2:6]
        return self.address_bin

    def set_address_bin(self, address):
        self.address_bin = bin(address)

    def set_data(self, data):
        self.data = hex(data)

    def get_data(self):
        return self.data

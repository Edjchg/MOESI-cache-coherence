class Block:
    def __init__(self):
        self.number = 0
        self.state = "I"
        self.memory_address = 0
        self.data = 0
        self.tag = 0
        self.data_I = 0

    def get_number(self):
        return self.number

    def set_number(self, number):
        self.number = number

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def get_memory_address(self):
        return self.memory_address

    def set_memory_address(self, memory_address):
        self.memory_address = memory_address

    def set_data(self, data):
        self.data = data
        #self.data_I = hex(data)

    def get_data(self):
        return self.data

    def set_tag(self, tag):
        # self.tag = self.get_memory_address()[2:4]
        self.tag = tag

    def get_tag(self):
        return self.tag

    def get_data_I(self):
        return self.data_I
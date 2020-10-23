from snooper import Snooper
import random
import time
import numpy as np
from instruction import Instruction
from cache import Cache


class CPU:
    def __init__(self):
        self.cache = Cache()
        self.snooper = Snooper()
        self.instructions = []
        self.number = 0
        self.actual_instruction = Instruction()

    def get_block(self, index):
        cache = self.get_cache_blocks(index)
        word = str(index) + "-" + cache.get_state() + "-" + str(cache.get_memory_address()) + "-" + str(cache.get_data())
        return word

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    def set_cache(self, cache):
        self.cache = cache

    def get_cache(self):
        return self.cache

    def set_snooper(self, snooper):
        self.snooper = snooper

    def get_snooper(self):
        return self.snooper

    def set_instructions(self, instructions):
        self.instructions = instructions

    def get_instructions(self):
        return self.instructions

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def insert_instruction(self, operation, address, data, index):
        instruction = Instruction()
        instruction.set_operation(operation)
        instruction.set_address_bin(address)
        instruction.set_data(data)
        self.instructions.insert(index, instruction)

    def get_cache_blocks(self, index):
        return self.get_cache().get_blocks()[index]

    def start_thread(self):
        while 1:
            print(self.get_number())
            time.sleep(2)

    def get_instruction_formated(self):
        instruction = self.get_actual_instruction()
        if instruction.get_operation() == "calc":
            instr = "P" + str(self.get_number())+ " :" + "calc"
        elif instruction.get_operation() == "read":
            instr = "P" + str(self.get_number()) + " :" + "read " + str(instruction.get_address_bin())
        elif instruction.get_operation() == "write":
            instr = "P" + str(self.get_number()) + " :" + "write " + str(instruction.get_address_bin()) + " ; " + str(instruction.get_data())
        return instr
    def instructions_generate(self):
        instruction_type = ["write", "read", "calc"]
        index = 0
        read = 0
        calc = 0
        write = 0
        while index < 100:
            operation = np.random.normal(2)
            operation = int(np.round(operation))
            if operation > 2 or operation < 0:
                pass
            else:
                # If operation is 0, it means that is a write.
                if operation == 0:
                    flag = True
                    while flag:
                        address = np.random.poisson(8)
                        if 0 <= address < 16:
                            write_instruction = Instruction()
                            write_instruction.set_processor_number(self.get_number())
                            write_instruction.set_operation(instruction_type[0])
                            write_instruction.set_address_bin(address)
                            write_instruction.set_data(random.randint(0, 65535))
                            self.add_instruction(write_instruction)
                            flag = False
                            write += 1
                        else:
                            pass
                # If operation is 1, it means that is a read
                elif operation == 1:
                    flag = True
                    while flag:
                        address = np.random.poisson(8)
                        if 0 <= address < 16:
                            read_instruction = Instruction()
                            read_instruction.set_processor_number(self.get_number())
                            read_instruction.set_operation(instruction_type[1])
                            read_instruction.set_address_bin(address)
                            read_instruction.set_data(0)
                            self.add_instruction(read_instruction)
                            flag = False
                            read += 1
                        else:
                            pass
                elif operation == 2:
                    calc_instruction = Instruction()
                    calc_instruction.set_processor_number(self.get_number())
                    calc_instruction.set_operation(instruction_type[2])
                    calc_instruction.set_address_bin(0)
                    calc_instruction.set_data(0)
                    self.add_instruction(calc_instruction)
                    calc += 1
                index += 1
        print("Calc:" + str(calc))
        print("Read:" + str(read))
        print("Write:" + str(write))

    def set_actual_instruction(self, instruction):
        self.actual_instruction = instruction

    def get_actual_instruction(self):
        return self.actual_instruction

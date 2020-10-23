from block import Block
class Cache:
    # Cache is a set of objects called Blocks or cache lines
    def __init__(self):
        self.blocks = []
        self.sets = []

    def get_blocks(self):
        return self.blocks

    def set_blocks(self, block):
        self.blocks = block

    def add_block(self, block):
        self.blocks.append(block)

    def set_sets(self, sets):
        self.sets = sets

    def get_sets(self):
        return self.sets

    def cache_constructor(self):
        block0 = Block()
        block0.set_number(0)
        block0.set_state("I")
        block0.set_memory_address(0)
        block0.set_data(0)
        block0.set_tag(0)

        block1 = Block()
        block1.set_number(1)
        block1.set_state("I")
        block1.set_memory_address(0)
        block1.set_data(0)
        block1.set_tag(0)

        block2 = Block()
        block2.set_number(2)
        block2.set_state("I")
        block2.set_memory_address(0)
        block2.set_data(0)
        block2.set_tag(0)

        block3 = Block()
        block3.set_number(3)
        block3.set_state("I")
        block3.set_memory_address(0)
        block3.set_data(0)
        block3.set_tag(0)

        set0 = [block0, block1]
        set1 = [block2, block3]

        self.set_sets([set0, set1])
        self.set_blocks([block0, block1, block2, block3])

    def print_blocks(self):
        index = 0
        while index < 4:
            print(str(self.get_blocks()[index].get_number()) + "-" + self.get_blocks()[index].get_state() + "-" + str(self.get_blocks()[index].get_memory_address())+ "-" + str(self.get_blocks()[index].get_data()))
            index += 1
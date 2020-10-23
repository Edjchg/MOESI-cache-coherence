class MainMem:
    def __init__(self):
        self.blocks = []

    def set_blocks(self, blocks):
        self.blocks = blocks

    def get_blocks(self):
        return self.blocks

    def add_block(self, block):
        self.blocks.append(block)

    def construction(self):
        index = 0
        while index < 16:
            self.add_block(0)
            index += 1
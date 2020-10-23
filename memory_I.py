from tkinter import *


class Memory_I:
    def __init__(self, canvas, x0, y0, x1, y1):
        self.canvas = canvas
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.blocks = []  # debe ser una lista de objetos bloques

    def set_canvas(self, canvas):
        self.canvas = canvas

    def get_canvas(self):
        return self.canvas

    def set_x0(self, x0):
        self.x0 = x0

    def get_x0(self):
        return self.x0

    def set_y0(self, y0):
        self.y0 = y0

    def get_y0(self):
        return self.y0

    def set_x1(self, x1):
        self.x1 = x1

    def get_x1(self):
        return self.x1

    def set_y1(self, y1):
        self.y1 = y1

    def get_y1(self):
        return self.y1

    def set_blocks(self, blocks):
        self.blocks = blocks

    def get_blocks(self):
        return self.blocks

    def update_mem(self, main_memory):
        blocks = self.get_blocks()
        index = 0
        while index < 16:
            number = 58 - 2 * len(str(main_memory[index]))
            word = blank_string(number)
            word = str(main_memory[index]) + word
            blocks[index].config(text=word)
            index += 1


    def paint_mem(self):
        canvas = self.get_canvas()
        x0 = self.get_x0()
        y0 = self.get_y0()
        x1 = self.get_x1()
        y1 = self.get_y1()
        lb_mem = Label(text="Memoria").place(x=x0, y=y0)
        memory = canvas.create_rectangle(x0, y0, x1, y1, outline="#5c73c4", fill="#5c73c4")
        x0 += 10
        y0 += 30

        data = "asd"
        number = 58 - 2 * len(data)
        print(len(data))
        palabra = blank_string(number)
        print(len(palabra))
        print(data + palabra)
        # First column
        block1 = Label(text=data + palabra)
        block1.place(x=x0, y=y0)
        y0 += 30
        palabra = blank_string(58)
        block2 = Label(text=palabra)
        block2.place(x=x0, y=y0)
        y0 += 30
        block3 = Label(text=palabra)
        block3.place(x=x0, y=y0)
        y0 += 30
        block4 = Label(text=palabra)
        block4.place(x=x0, y=y0)

        # Second column
        y0 = self.get_y0() + 30
        x0 += 200
        block5 = Label(text=palabra)
        block5.place(x=x0, y=y0)
        y0 += 30
        palabra = blank_string(58)
        block6 = Label(text=palabra)
        block6.place(x=x0, y=y0)
        y0 += 30
        block7 = Label(text=palabra)
        block7.place(x=x0, y=y0)
        y0 += 30
        block8 = Label(text=palabra)
        block8.place(x=x0, y=y0)

        # Third column

        y0 = self.get_y0() + 30
        x0 += 200
        block9 = Label(text=palabra)
        block9.place(x=x0, y=y0)
        y0 += 30
        palabra = blank_string(58)
        block10 = Label(text=palabra)
        block10.place(x=x0, y=y0)
        y0 += 30
        block11 = Label(text=palabra)
        block11.place(x=x0, y=y0)
        y0 += 30
        block12 = Label(text=palabra)
        block12.place(x=x0, y=y0)

        # Fourth column

        y0 = self.get_y0() + 30
        x0 += 200
        block13 = Label(text=palabra)
        block13.place(x=x0, y=y0)
        y0 += 30
        palabra = blank_string(58)
        block14 = Label(text=palabra)
        block14.place(x=x0, y=y0)
        y0 += 30
        block15 = Label(text=palabra)
        block15.place(x=x0, y=y0)
        y0 += 30
        block16 = Label(text=palabra)
        block16.place(x=x0, y=y0)

        blocks = [block1, block2, block3, block4, block5, block6, block7, block8, block9, block10, block11, block12, block13, block14, block15, block16]
        self.set_blocks(blocks)

        #self.set_blocks()
def blank_string(lenght):
    index = 0
    word = ""
    while index < lenght:
        word += " "
        index += 1
    return word



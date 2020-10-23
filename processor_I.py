from tkinter import *
import time


class Processor_I:
    def __init__(self, canvas, number, x0, y0, x1, y1):
        self.canvas = canvas
        self.number = number
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

        self.block1 = None
        self.block2 = None
        self.block3 = None
        self.block4 = None

    def get_block1(self):
        return self.block1

    def set_block1(self, block):
        self.block1 = block

    def get_block2(self):
        return self.block2

    def set_block2(self, block):
        self.block2 = block

    def get_block3(self):
        return self.block3

    def set_block3(self, block):
        self.block3 = block

    def get_block4(self):
        return self.block4

    def set_block4(self, block):
        self.block4 = block

    def update_block(self, data, index):
        number = 58 - 2 * len(data)
        word = blank_string(number)
        word = data+word
        if index == 0:
            self.get_block1().config(text=word)
        elif index == 1:
            self.get_block2().config(text=word)
        elif index == 2:
            self.get_block3().config(text=word)
        elif index == 3:
            self.get_block4().config(text=word)

    def get_canvas(self):
        return self.canvas

    def set_canvas(self, canvas):
        self.canvas = canvas

    def get_number(self):
        return self.number

    def set_number(self, number):
        self.number = number

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

    def paint_processor(self):
        canvas = self.get_canvas()
        x0 = self.get_x0()
        y0 = self.get_y0()
        x1 = self.get_x1()
        y1 = self.get_y1()
        procesador = canvas.create_rectangle(x0, y0, x1, y1, outline="#3de388", fill="#3de388")

        lb_procesador = Label(text="Procesador " + str(self.get_number()))
        lb_procesador.place(x=x0, y=y0)
        x0 += 10
        y0 += 30
        cache_1_1 = Label(text="0-I-0-0")
        cache_1_1.place(x=x0, y=y0)
        cache_1_1.config(width=25)
        self.set_block1(cache_1_1)

        y0 += 30
        cache_1_2 = Label(text="1-I-0-0")
        cache_1_2.place(x=x0, y=y0)
        cache_1_2.config(width=25)
        self.set_block2(cache_1_2)

        y0 += 30
        cache_1_3 = Label(text="2-I-0-0")
        cache_1_3.place(x=x0, y=y0)
        cache_1_3.config(width=25)
        self.set_block3(cache_1_3)

        y0 += 30
        cache_1_4 = Label(text="3-I-0-0")
        cache_1_4.place(x=x0, y=y0)

        cache_1_4.config(width=25)
        self.set_block4(cache_1_4)


def blank_string(lenght):
    index = 0
    word = ""
    while index < lenght:
        word += " "
        index += 1
    return word

from tkinter import *


class Bus_I:
    def __init__(self, canvas, x0, y0, x1, y1):
        self.canvas = canvas
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

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

    def paint_bus(self):
        canvas = self.get_canvas()
        x0 = self.get_x0()
        y0 = self.get_y0()
        x1 = self.get_x1()
        y1 = self.get_y1()
        lb_bus = Label(text="Bus").place(x=x0, y=y0)
        bus = canvas.create_rectangle(x0, y0, x1, y1, outline="#cc5d49", fill="#cc5d49")

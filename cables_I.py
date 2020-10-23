class Connection:
    def __init__(self, canvas):
        self.canvas = canvas

    def set_canvas(self, canvas):
        self.canvas = canvas

    def get_canvas(self):
        return self.canvas

    def print_proc_bus(self):
        canvas = self.get_canvas()
        # procesador 1
        line1 = canvas.create_line(110, 160, 110, 250)
        #self.set_proc1(line1)

        # Procesador 2

        canvas.create_line(320, 160, 320, 250)

        # Procesador 3

        canvas.create_line(530, 160, 530, 250)

        # procesador 4
        canvas.create_line(740, 160, 740, 250)

        # Linea que los une
        canvas.create_line(110, 250, 740, 250)

        # union con bus
        canvas.create_line(425, 250, 425, 300)
import threading
import time
from tkinter import *
# --Logic imports----
from processor import CPU
from cache import Cache
from snooper import Snooper
from bus import Bus
# --Interface imports----
from processor_I import Processor_I
from memory_I import Memory_I
from cables_I import Connection
from bus_I import Bus_I

# -------Some variables---------
processor0 = None
processor1 = None
processor2 = None
processor3 = None
cache0 = None
cache1 = None
cache2 = None
cache3 = None
snooper0 = None
snooper1 = None
snooper2 = None
snooper3 = None
main_bus = None
index = 0
clk = True
cycles = 0
cycles1 = 0
entry = 0
stop = False

# --------Interface variables---------
window = None
canvas = None
processor1_I = None
processor2_I = None
processor3_I = None
processor4_I = None
memory_I = None
cycle_cuantity = None
instr_1 = None
instr_2 = None
instr_3 = None
instr_4 = None


def interface_init():
    global processor1_I, processor2_I, processor3_I, processor4_I, memory_I, canvas
    global instr_1, instr_2, instr_3, instr_4
    processor1_I = Processor_I(canvas, 1, 10, 10, 210, 160)
    processor1_I.paint_processor()

    processor2_I = Processor_I(canvas, 2, 220, 10, 420, 160)
    processor2_I.paint_processor()

    processor3_I = Processor_I(canvas, 3, 430, 10, 630, 160)
    processor3_I.paint_processor()

    processor4_I = Processor_I(canvas, 4, 640, 10, 840, 160)
    processor4_I.paint_processor()

    interconnection = Connection(canvas)
    interconnection.print_proc_bus()

    bus_I = Bus_I(canvas, 220, 300, 640, 400)
    bus_I.paint_bus()

    canvas.create_line(425, 400, 425, 500)

    memory_I = Memory_I(canvas, 10, 500, 810, 650)
    memory_I.paint_mem()

    label_proc = Label(text="Instrucción Actual en cada procesador")
    label_proc.place(x=820, y=500)
    block = canvas.create_rectangle(820, 500, 1250, 590, outline="#86898a", fill="#86898a")

    instr_1 = Label(text="                                                          ")
    instr_1.place(x=830, y=530)

    instr_2 = Label(text="                                                          ")
    instr_2.place(x=830, y=560)

    instr_3 = Label(text="                                                          ")
    instr_3.place(x=1040, y=530)

    instr_4 = Label(text="                                                          ")
    instr_4.place(x=1040, y=560)

    update_mem()


def organization_init():
    global processor0, processor1, processor2, processor3
    global cache0, cache1, cache2, cache3
    global snooper0, snooper1, snooper2, snooper3
    global main_bus, instr_1, instr_2, instr_3, instr_4

    # Making the instance of the first processor:
    processor0 = CPU()
    # Generating its instructions:
    processor0.instructions_generate()
    # Assign internally the processor number:
    processor0.set_number(0)

    # Making the instance of the first processor cache
    cache0 = Cache()
    # Filling this cache with invalid blocks
    cache0.cache_constructor()
    # Assign this cache to processor 0:
    processor0.set_cache(cache0)

    # Making the instance of the snooper for first processor
    snooper0 = Snooper()
    # Assign to snopper0 the cache0
    snooper0.set_cache(cache0)
    # Assign to snooper0 the processor0
    snooper0.set_cpu(processor0)
    #########################################################

    # Making the instance of the second processor:
    processor1 = CPU()
    # Generating its instructions:
    processor1.instructions_generate()
    # Assign internally the processor number:
    processor1.set_number(1)

    # Making the instance of the second processor cache
    cache1 = Cache()
    # Filling this cache with invalid blocks
    cache1.cache_constructor()
    # Assign this cache to processor 1:
    processor1.set_cache(cache1)

    # Making the instance of the snooper for the second processor
    snooper1 = Snooper()
    # Assign to snooper1 the cache1
    snooper1.set_cache(cache1)
    # Assig to snooper1 the processor1
    snooper1.set_cpu(processor1)
    #######################################################

    # Making the instance of the third processor:
    processor2 = CPU()
    # Generating its instructions:
    processor2.instructions_generate()
    # Assign internally the processor number:
    processor2.set_number(2)

    # Making the instance of the third processor cache
    cache2 = Cache()
    # Filling this cache with invalid blocks
    cache2.cache_constructor()
    # Assign this cache to processor 2:
    processor2.set_cache(cache2)

    # Making the instance of the snooper for the third processor
    snooper2 = Snooper()
    # Assign to snooper2 the cache2
    snooper2.set_cache(cache2)
    # Assign to snooper2 the processor2
    snooper2.set_cpu(processor2)
    #######################################################

    # Making the instance of the fourth processor:
    processor3 = CPU()
    # Generating its instructions:
    processor3.instructions_generate()
    # Assign internally the processor number:
    processor3.set_number(3)

    # Making the instance of the fourth processor cache
    cache3 = Cache()
    # Filling this cache with invalid blocks
    cache3.cache_constructor()
    # Assign this cache to processor 3:
    processor3.set_cache(cache3)

    # Making the instance of the snooper for the fourth processor
    snooper3 = Snooper()
    # Assign to snooper3 the cache3
    snooper3.set_cache(cache3)
    # Assign to snopper3 the processor3
    snooper3.set_cpu(processor3)
    ###########################################################

    # Making the instance of the main bus:
    main_bus = Bus()
    # Creating the main memory from bus
    main_bus.bus_constructor()

    # Assign to snooper0 the main bus
    snooper0.set_bus(main_bus)
    # Assign to snooper1 the main bus
    snooper1.set_bus(main_bus)
    # Assign to snooper2 the main bus
    snooper2.set_bus(main_bus)
    # Assign to snooper3 the main bus
    snooper3.set_bus(main_bus)

    # Assign to the bus the set of snoopers:
    snoopers = [snooper0, snooper1, snooper2, snooper3]
    main_bus.set_snoopers(snoopers)


def processor0_thread():
    global index
    global processor0
    while 1:
        if clk:
            break
        else:
            pass
    instruction = processor0.get_instructions()[index]
    processor0.set_actual_instruction(instruction)
    snooper0.MOESI_FSM()
    update_P1()
    print(str(index) + "from processor 0")


def processor1_thread():
    global index
    global processor1
    while 1:
        if clk:
            break
        else:
            pass
    instruction = processor1.get_instructions()[index]
    processor1.set_actual_instruction(instruction)
    snooper1.MOESI_FSM()
    update_P2()
    print(str(index) + "from processor 1")


def processor2_thread():
    global index
    global processor2
    while 1:
        if clk:
            break
        else:
            pass
    instruction = processor2.get_instructions()[index]
    processor2.set_actual_instruction(instruction)
    snooper2.MOESI_FSM()
    update_P3()


def processor3_thread():
    global index
    global processor3
    while 1:
        if clk:
            break
        else:
            pass
    instruction = processor3.get_instructions()[index]
    processor3.set_actual_instruction(instruction)
    snooper3.MOESI_FSM()
    update_P4()


def update_P1():
    global instr_1
    data = processor0.get_block(0)
    processor1_I.update_block(data, 0)

    data = processor0.get_block(1)
    processor1_I.update_block(data, 1)

    data = processor0.get_block(2)
    processor1_I.update_block(data, 2)

    data = processor0.get_block(3)
    processor1_I.update_block(data, 3)

    instr1 = processor0.get_instruction_formated()
    number = 58 - len(instr1) * 2
    word = blank_string(number)
    instr_1.config(text=instr1 + word)


def update_P2():
    data = processor1.get_block(0)
    processor2_I.update_block(data, 0)

    data = processor1.get_block(1)
    processor2_I.update_block(data, 1)

    data = processor1.get_block(2)
    processor2_I.update_block(data, 2)

    data = processor1.get_block(3)
    processor2_I.update_block(data, 3)

    instr2 = processor1.get_instruction_formated()
    number = 58 - len(instr2) * 2
    word = blank_string(number)
    instr_2.config(text=instr2 + word)


def update_P3():
    data = processor2.get_block(0)
    processor3_I.update_block(data, 0)

    data = processor2.get_block(1)
    processor3_I.update_block(data, 1)

    data = processor2.get_block(2)
    processor3_I.update_block(data, 2)

    data = processor2.get_block(3)
    processor3_I.update_block(data, 3)

    instr3 = processor2.get_instruction_formated()
    number = 58 - len(instr3) * 2
    word = blank_string(number)
    instr_3.config(text=instr3 + word)


def update_P4():
    data = processor3.get_block(0)
    processor4_I.update_block(data, 0)

    data = processor3.get_block(1)
    processor4_I.update_block(data, 1)

    data = processor3.get_block(2)
    processor4_I.update_block(data, 2)

    data = processor3.get_block(3)
    processor4_I.update_block(data, 3)

    instr4 = processor3.get_instruction_formated()
    number = 58 - len(instr4) * 2
    word = blank_string(number)
    instr_4.config(text=instr4 + word)


def update_mem():
    global memory_I, main_bus
    memory_I.update_mem(main_bus.get_main_memory())


def engine1():
    global index, clk, cycles, stop

    while 1:
        if index > 99 or stop:
            return 0
        else:
            while 1:
                clk = True
                p1 = threading.Thread(target=processor0_thread)
                p1.start()

                p1 = threading.Thread(target=processor1_thread)
                p1.start()

                p2 = threading.Thread(target=processor2_thread)
                p2.start()

                p3 = threading.Thread(target=processor3_thread)
                p3.start()

                main_bus.bus_processing_requests()
                print("--------Memory--------")
                main_bus.print_mem()
                print("----------------------")
                print("------Cache 0---------")
                snooper0.print_cache()
                print("----------------------")
                print("------Cache 1---------")
                snooper1.print_cache()
                print("----------------------")
                print("------Cache 2---------")
                snooper2.print_cache()
                print("----------------------")
                print("------Cache 3---------")
                snooper3.print_cache()
                print("----------------------")

                print(index)
                index += 1
                # update_I()
                update_mem()
                # clock_counter.config(text="CLK:" + str(index))
                time.sleep(3)

                clk = False
                break


def engine2():
    global index, clk, cycles,cycles1,  stop

    while 1:
        if cycles1 >= cycles or stop:
            stop1()
            break
            #return 0
        else:
            while 1:
                clk = True
                p1 = threading.Thread(target=processor0_thread)
                p1.start()

                p1 = threading.Thread(target=processor1_thread)
                p1.start()

                p2 = threading.Thread(target=processor2_thread)
                p2.start()

                p3 = threading.Thread(target=processor3_thread)
                p3.start()

                main_bus.bus_processing_requests()
                print("--------Memory--------")
                main_bus.print_mem()
                print("----------------------")
                print("------Cache 0---------")
                snooper0.print_cache()
                print("----------------------")
                print("------Cache 1---------")
                snooper1.print_cache()
                print("----------------------")
                print("------Cache 2---------")
                snooper2.print_cache()
                print("----------------------")
                print("------Cache 3---------")
                snooper3.print_cache()
                print("----------------------")

                print(index)
                index += 1
                # update_I()
                update_mem()
                # clock_counter.config(text="CLK:" + str(cycles))
                time.sleep(3)

                clk = False
                break


def engine3():
    global index, clk, cycles
    if index < 99:
        clk = True
        p1 = threading.Thread(target=processor0_thread)
        p1.start()

        p1 = threading.Thread(target=processor1_thread)
        p1.start()

        p2 = threading.Thread(target=processor2_thread)
        p2.start()

        p3 = threading.Thread(target=processor3_thread)
        p3.start()

        main_bus.bus_processing_requests()
        print("--------Memory--------")
        main_bus.print_mem()
        print("----------------------")
        print("------Cache 0---------")
        snooper0.print_cache()
        print("----------------------")
        print("------Cache 1---------")
        snooper1.print_cache()
        print("----------------------")
        print("------Cache 2---------")
        snooper2.print_cache()
        print("----------------------")
        print("------Cache 3---------")
        snooper3.print_cache()
        print("----------------------")

        print(index)
        index += 1
        # update_I()
        update_mem()
        clock_counter.config(text="CLK:" + str(index))
        # time.sleep(3)

        clk = False
    else:
        return 0


def create_main_thread():
    global stop
    stop = False
    process = threading.Thread(target=engine1)
    process.start()

    clk = threading.Thread(target=cycles_counter)
    clk.start()


def set_cycles():
    global cycles, entry, stop
    stop = False
    cycles = entry.get()
    process = threading.Thread(target=engine2)
    process.start()

    clk = threading.Thread(target=cycles_counter)
    clk.start()


def blank_string(lenght):
    index1 = 0
    word = ""
    while index1 < lenght:
        word += " "
        index1 += 1
    return word


def insert_instructions():
    processor0.insert_instruction(operation1.get(), int(address1.get()), data1.get(), index)
    processor1.insert_instruction(operation2.get(), int(address2.get()), data2.get(), index)
    processor2.insert_instruction(operation3.get(), address3.get(), data3.get(), index)
    processor3.insert_instruction(operation4.get(), address4.get(), data4.get(), index)


def stop1():
    global stop
    stop = True


def cycles_counter():
    global cycles1, clock_counter, stop
    while 1:
        if not stop:
            cycles1 += 1
            clock_counter.config(text="CLK:" + str(cycles1))
            time.sleep(1)
        else:
            break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    window = Tk()
    window.title("Organización Multiprocesadores (MOESI)")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight() - 100
    window.geometry(str(screen_width) + "x" + str(screen_height))
    canvas = Canvas(window)
    canvas.pack(fill=BOTH, expand=1)

    organization_init()
    interface_init()
    play_automatic_Mode = Button(canvas, text="Ejecución continua", command=create_main_thread)
    play_automatic_Mode.place(x=850, y=10)
    entry = IntVar()
    cycle_cuantity = Entry(canvas, textvariable=entry)
    cycle_cuantity.place(x=1000, y=12)
    play_cycles = Button(canvas, text="Ejecución por ciclos", command=set_cycles)
    play_cycles.place(x=1000, y=40)
    next_step = Button(canvas, text="Siguiente paso", command=engine3)
    next_step.place(x=1150, y=10)
    pause = Button(canvas, text="Pausa", command=stop1)
    pause.place(x=1040, y=100)

    add_instructions = Label(text="---------------------Agregar instrucciones en caso de pausa------------------")
    add_instructions.place(x=850, y=150)

    Label(text="P0:").place(x=850, y=180)
    operation1 = StringVar()
    pOperation0 = Entry(canvas, textvariable=operation1)
    pOperation0.place(x=870, y=180)

    address1 = IntVar()
    pAdress0 = Entry(canvas, textvariable=address1)
    pAdress0.place(x=1000, y=180)

    data1 = IntVar()
    pData0 = Entry(canvas, textvariable=data1)
    pData0.place(x=1130, y=180)
    ##############################################################
    Label(text="P1:").place(x=850, y=210)
    operation2 = StringVar()
    pOperation1 = Entry(canvas, textvariable=operation2)
    pOperation1.place(x=870, y=210)

    address2 = IntVar()
    pAdress1 = Entry(canvas, textvariable=address2)
    pAdress1.place(x=1000, y=210)

    data2 = IntVar()
    pData1 = Entry(canvas, textvariable=data2)
    pData1.place(x=1130, y=210)
    ##############################################################
    Label(text="P2:").place(x=850, y=240)
    operation3 = StringVar()
    pOperation2 = Entry(canvas, textvariable=operation3)
    pOperation2.place(x=870, y=240)

    address3 = IntVar()
    pAdress2 = Entry(canvas, textvariable=address3)
    pAdress2.place(x=1000, y=240)

    data3 = IntVar()
    pData2 = Entry(canvas, textvariable=data3)
    pData2.place(x=1130, y=240)
    ##############################################################
    Label(text="P3:").place(x=850, y=270)
    operation4 = StringVar()
    pOperation3 = Entry(canvas, textvariable=operation4)
    pOperation3.place(x=870, y=270)

    address4 = IntVar()
    pAdress3 = Entry(canvas, textvariable=address4)
    pAdress3.place(x=1000, y=270)

    data4 = IntVar()
    pData3 = Entry(canvas, textvariable=data4)
    pData3.place(x=1130, y=270)

    get_instructions = Button(canvas, text="Agregar instrucciones", command=insert_instructions)
    get_instructions.place(x=1000, y=300)

    clock_counter = Label(text="CLK:" + str(cycles1))
    clock_counter.place(x=1250, y=10)

    window.mainloop()

import time


class Bus:
    def __init__(self):
        self.snoopers = []
        self.main_memory = []

    def print_mem(self):
        index = 0
        mem = self.get_main_memory()
        while index < 16:
            print(mem[index])
            index += 1

    def add_to_main_memory(self, data):
        self.main_memory.append(data)

    def bus_constructor(self):
        index = 0
        while index < 16:
            self.add_to_main_memory(0)
            index += 1

    def get_snoopers(self):
        return self.snoopers

    def set_snoopers(self, snoopers):
        self.snoopers = snoopers

    def get_main_memory(self):
        return self.main_memory

    def set_data_to_main_memory(self, data, address):
        address = int(address, 2)
        self.get_main_memory()[address] = data

    def get_data_from_memory(self, address):
        address = int(address, 2)
        return self.get_main_memory()[address]

    def look_for_block_copies(self, snoop_number, set_to_look, bit, tag):
        snoopers = self.get_snoopers()
        max_ = len(snoopers)
        index = 0
        while index < max_:
            if snoop_number == index:
                pass
            elif snoopers[index].get_cache().get_sets()[set_to_look][bit].get_tag() == tag:
                flag = True
                #break
                return True
            else:
                flag = False
            index += 1
        return flag

    def get_state_from_certain_block(self, snooper, set_to_look, bit):
        return self.snoopers[snooper].get_cache().get_sets()[set_to_look][bit].get_state()

    def set_state_from_certain_block(self, state, snooper, set_to_look, bit):
        self.snoopers[snooper].get_cache().get_sets()[set_to_look][bit].set_state(state)

    def get_data_from_cache(self, snoop_number, set_to_look, bit, address):
        snoopers = self.get_snoopers()
        max_ = len(snoopers)
        index = 0
        while index < max_:
            if snoop_number == index:
                pass
            elif snoopers[index].get_cache().get_sets()[set_to_look][bit].get_memory_address() == address:
                return snoopers[index].get_cache().get_sets()[set_to_look][bit].get_data()
            else:
                pass
            index += 1

    def bus_processing_requests(self):
        snoopers = self.get_snoopers()
        max_ = len(snoopers)
        index = 0
        while index < max_:
            # Si el snooper actual pone una lectura BusRd en el bus, lo que le sucede a los demás bloques esta aca:
            if snoopers[index].get_BusRd():
                address = snoopers[index].get_address()
                # Se pregunta si hay copias
                # if not snoopers[index].get_shared_block_status():
                if not self.look_for_block_copies(index,
                                                  get_set_to_look(address),
                                                  get_bit(address),
                                                  get_tag(address)) and snoopers[index].get_state() == "I":
                    # Si no hay copias entonces se va a memoria.
                    data = self.get_data_from_memory(address)

                    snoopers[index].set_new_block(address, data, "E")
                    snoopers[index].set_read_miss_flag(False)
                    snoopers[index].set_BusRd(False)
                    time.sleep(2)
                else:
                    index2 = 0
                    while index2 < max_:
                        if index2 == index:
                            pass
                        # Se pregunta por las copias
                        elif self.look_for_block_copies(index2, get_set_to_look(address), get_bit(address),
                                                        get_tag(address)):
                            # Si este snooper tiene la copia y esta en estado E pasa a estado S
                            if self.get_state_from_certain_block(index2, get_set_to_look(address),
                                                                 get_bit(address)) == "E":
                                data = self.get_data_from_cache(index, get_set_to_look(address), get_bit(address),
                                                                address)
                                # El bloque que puso el request es puesto en S
                                snoopers[index].set_new_block(address, data, "S")
                                # Si el bloque que dio el dato esta en E pasa a S
                                self.set_state_from_certain_block("S", index2, get_set_to_look(address),
                                                                  get_bit(address))
                                break
                            # Si este snooper tiene la copia y esta en estado S, pasa a estado
                            elif self.get_state_from_certain_block(index2, get_set_to_look(address),
                                                                   get_bit(address)) == "M":
                                data = self.get_data_from_cache(index, get_set_to_look(address), get_bit(address),
                                                                address)
                                # El bloque que puso el request es puesto en S
                                snoopers[index].set_new_block(address, data, "S")
                                # Si el bloque que dio el dato esta en estado M pasa a O
                                self.set_state_from_certain_block("O", index2, get_set_to_look(address),
                                                                  get_bit(address))
                                break
                            # Si este snooper tiene la copia y esta en estado O, sigue estando en estado O.
                            elif self.get_state_from_certain_block(index2, get_set_to_look(address),
                                                                   get_bit(address)) == "O":
                                data = self.get_data_from_cache(index, get_set_to_look(address), get_bit(address),
                                                                address)
                                # El bloque que puso el request es puesto en S
                                snoopers[index].set_new_block(address, data, "S")
                                # Si el bloque que dio el dato esta en estado O pasa a O
                                break
                            elif self.get_state_from_certain_block(index2, get_set_to_look(address),
                                                                   get_bit(address)) == "S":
                                data = self.get_data_from_cache(index2, get_set_to_look(address), get_bit(address),
                                                                address)
                                # El bloque que puso el request es puesto en S
                                snoopers[index].set_new_block(address, data, "S")
                                # Si el bloque que dio el dato esta en estado S pasa a S
                                break
                        index2 += 1
            # Si el snooper actual pone una solicitud de BusRdX, lo que le pasa a las copias es:
            elif snoopers[index].get_BusRdX():
                index3 = 0
                address = snoopers[index].get_address()
                # Si hay otras copias del dato que se quiere modificar entonces:

                while index3 < max_:

                    if index3 == index:
                        pass
                    elif self.look_for_block_copies(index3, get_set_to_look(address), get_bit(address),
                                                    get_tag(address)):
                        # Si otro snooper posee una copia del snooper que cambio el dato y esta en estado invalido:
                        if snoopers[index3].get_block_state(get_set_to_look(address), get_bit(address)) == "I":
                            # Lo deja en estado Invalido y no le cambia nada.
                            # data = snoopers[index].instruction_data()
                            # self.set_data_to_main_memory(data, address)
                            pass
                        # Si otro snooper posee una copia del snooper que cambio el dato y esta en estado Exclusive:
                        elif snoopers[index3].get_block_state(get_set_to_look(address), get_bit(address)) == "E":
                            # El snooper que tiene el bloque en exclusivo pasaría a Invalid
                            self.set_state_from_certain_block("I", index3, get_set_to_look(address), get_bit(address))
                            # Tomando la data de la instruccion que tiene el snooper que puso el mensaje de BusRdX,
                            # para escribirla en memoria:
                            data = snoopers[index].instruction_data()
                            # Y ahora se actualiza el dato en memoria
                            time.sleep(2)
                            self.set_data_to_main_memory(data, address)
                        elif snoopers[index3].get_block_state(get_set_to_look(address), get_bit(address)) == "M":
                            # El snooper que tiene el bloque en modified pasaría a Invalid
                            self.set_state_from_certain_block("I", index3, get_set_to_look(address), get_bit(address))
                            # Tomando la data de la instruccion que tiene el snooper que puso el mensaje de BusRdX,
                            # para escribirla en memoria:
                            data = snoopers[index].instruction_data()
                            # Y ahora se actualiza el dato en memoria
                            time.sleep(2)
                            self.set_data_to_main_memory(data, address)
                        elif snoopers[index3].get_block_state(get_set_to_look(address), get_bit(address)) == "O":
                            # El snooper que tiene el bloque en owned pasaría a Invalid
                            self.set_state_from_certain_block("I", index3, get_set_to_look(address), get_bit(address))
                            # Tomando la data de la instruccion que tiene el snooper que puso el mensaje de BusRdX,
                            # para escribirla en memoria:
                            data = snoopers[index].instruction_data()
                            # Y ahora se actualiza el dato en memoria
                            self.set_data_to_main_memory(data, address)
                        elif snoopers[index3].get_block_state(get_set_to_look(address), get_bit(address)) == "S":
                            # El snooper que tiene el bloque en shared pasaría a Invalid
                            self.set_state_from_certain_block("I", index3, get_set_to_look(address), get_bit(address))
                            # No actualiza la data a memoria.
                    index3 += 1
            elif snoopers[index].get_BusUpgrd():
                index4 = 0
                address = snoopers[index].get_address()
                while index4 < max_:
                    if index4 == index:
                        pass
                    elif self.look_for_block_copies(index4, get_set_to_look(address), get_bit(address),
                                                    get_tag(address)):
                        if snoopers[index4].get_block_state(get_set_to_look(address), get_bit(address)) == "I":
                            # Lo deja en estado Invalido y no le cambia nada.
                            pass
                        elif snoopers[index4].get_block_state(get_set_to_look(address), get_bit(address)) == "O":
                            # El snooper que tiene el bloque en owned pasaría a Invalid
                            self.set_state_from_certain_block("I", index4, get_set_to_look(address), get_bit(address))
                            # No actualiza la data a memoria.
                        elif snoopers[index4].get_block_state(get_set_to_look(address), get_bit(address)) == "S":
                            # El snooper que tiene el bloque en owned pasaría a Invalid
                            self.set_state_from_certain_block("I", index4, get_set_to_look(address), get_bit(address))
                    index4 += 1
            snoopers[index].set_read_miss_flag(False)
            snoopers[index].set_BusRd(False)
            snoopers[index].set_BusUpgrd(False)
            snoopers[index].set_BusRdX(False)
            index += 1


def get_bit(address):
    bit = 0
    address_dec = int(address, 2)
    if address_dec == 0 or address_dec == 1:
        bit = 0
    elif address_dec == 2 or address_dec == 3:
        bit = 1
    elif 4 <= address_dec <= 7:
        bit = int(address[3:4], 2)
    elif 7 < address_dec < 16:
        bit = int(address[4:5], 2)
    return bit


def get_set_to_look(address):
    set_ = 1
    address_dec = int(address, 2)
    if address_dec == 0:
        set_ = 0
    elif address_dec == 1:
        set_ = 1
    elif address_dec == 2 or address_dec == 3:
        set_ = int(address[3:4], 2)
    elif 4 <= address_dec <= 7:
        set_ = int(address[4:5], 2)
    elif 7 < address_dec < 16:
        set_ = int(address[5:6], 2)
    return set_


def get_tag(address):
    tag = 0
    address_dec = int(address, 2)
    if address_dec == 1 or address_dec == 0:
        pass
    elif address_dec == 2 or address_dec == 3:
        tag = 1
    elif 4 <= address_dec <= 7:
        tag = int(address[2:4], 2)
    elif 7 < address_dec < 16:
        tag = int(address[2:5], 2)

    return tag

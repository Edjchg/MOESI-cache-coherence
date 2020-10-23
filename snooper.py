class Snooper:
    def __init__(self):
        self.status = ""  # esta variable es para saber si hay una instr de escritura o lectura.
        self.cpu = None  # este es el cpu al que pertenece
        self.cache = None  # es la cache que tiene que observar
        self.bus = None  # es el bus de interconexion
        self.PrRd = False  # si el procesador desea leer
        self.PrWrt = False  # si el procesador desea escribir
        self.BusUpgrd = False  # si el bus desea actaulizar algun bloque
        self.BusRdX = False  # si el bus desea actualizar
        self.BusRd = False  # si el bus desea leer.
        self.shared_block_status = False
        self.state = "I"
        self.read_miss_flag = False

    def print_cache(self):
        cache_blocks = self.get_cache().get_blocks()
        index = 0
        while index < 4:
            print(cache_blocks[index].get_state() + str(cache_blocks[index].get_data()))
            index += 1

    def get_read_miss_flag(self):
        return self.read_miss_flag

    def set_read_miss_flag(self, status):
        self.read_miss_flag = status

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_new_block(self, address, data, state):
        set_too_look = get_set_to_look(address)
        bit = get_bit(address)
        tag = get_tag(address)
        self.get_cache().get_sets()[set_too_look][bit].set_tag(tag)
        self.get_cache().get_sets()[set_too_look][bit].set_state(state)
        self.get_cache().get_sets()[set_too_look][bit].set_data(data)
        self.get_cache().get_sets()[set_too_look][bit].set_memory_address(address)

    def get_shared_block_status(self):
        return self.shared_block_status

    def set_shared_block_status(self, status):
        self.shared_block_status = status

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_cpu(self):
        return self.cpu

    def set_cpu(self, cpu):
        self.cpu = cpu

    def get_cache(self):
        return self.cache

    def set_cache(self, cache):
        self.cache = cache

    def get_bus(self):
        return self.bus

    def set_bus(self, bus):
        self.bus = bus

    def get_PrRd(self):
        return self.PrRd

    def set_PrRd(self, status):
        self.PrRd = status

    def get_PrWrt(self):
        return self.PrWrt

    def set_PrWrt(self, status):
        self.PrWrt = status

    def get_BusUpgrd(self):
        return self.BusUpgrd

    def set_BusUpgrd(self, status):
        self.BusUpgrd = status

    def get_BusRdX(self):
        return self.BusRdX

    def set_BusRdX(self, status):
        self.BusRdX = status

    def get_BusRd(self):
        return self.BusRd

    def set_BusRd(self, status):
        self.BusRd = status

    def instruction_read(self):
        # Veo la operacion que hace el procesador
        status = self.get_cpu().get_actual_instruction().get_operation()
        return status

    def instruction_data(self):
        # Tomo la data de la isntruccion que escribe.
        data = self.get_cpu().get_actual_instruction().get_data()
        return data

    def get_address(self):
        # Retorna el address de donde quiere leer o escribir
        return self.get_cpu().get_actual_instruction().get_address_bin()

    def get_block_state(self, set_to_look, bit):
        # Retorna el estado del bloque que se esté consultando
        return self.get_cache().get_sets()[set_to_look][bit].get_state()

    def get_snooper_number(self):
        return self.get_cpu().get_number()

    def read_miss(self, set_to_look, bit, tag):
        block = self.get_cache().get_sets()[set_to_look][bit]
        if block.get_tag() == tag:
            return True
        else:
            return False

    def write_miss(self, set_to_look, bit, tag):
        block = self.get_cache().get_sets()[set_to_look][bit]
        if block.get_tag() == tag:
            return True
        else:
            return False

    def MOESI_FSM(self):
        # Pregunto si el procesador desea leer:
        if self.instruction_read() == "read":

            self.set_BusRd(True)
            # Levanto la bandera de que el procesador desea leer:
            self.set_PrRd(True)
            # Verificando cada estado, en conjunto con la necesidad del procesador de leer información:
            # Consulto por el address donde se va a leer:
            address = self.get_address()
            print(address)
            set_to_look = get_set_to_look(address)
            bit = get_bit(address)
            tag = get_tag(address)
            cache_block_state = self.get_block_state(set_to_look, bit)
            # Pregunto si el bloque esta en invalido o hay un miss:
            if cache_block_state == "I" and self.read_miss(set_to_look, bit, tag):
                print("Si es un read miss")
                self.set_read_miss_flag(True)
                self.set_state("I")
                # Seteo que el caso especial tratado en el bus es el de miss o Invalido
                # Pregunto al bus si hay copias:
                if self.get_bus().look_for_block_copies(self.get_snooper_number(), set_to_look, bit, tag):
                    # Levanto la bandera de que hay copias:
                    self.set_shared_block_status(True)
                    print("Si hay copias")
                    print(address)
                    # Levanto la bandera de que se debe poner el request de BusRd

                    #self.get_cache().get_sets()[set_to_look][bit].set_state("S")

                else:
                    # Si no hay copias:
                    # Levanto la bandera de que no hay copias:
                    self.set_shared_block_status(False)
                    print("No hay copias")
                    # Levanto la bandera de que se debe poner el request de BusRd
                    #self.get_cache().get_sets()[set_to_look][bit].set_state("E")
                    self.set_state("I")
            elif cache_block_state == "M":
                # Si no hay caché miss, y estaba en estado modificado entonces el procesador sí puede leer el dato.
                # Por lo tanto el bloque no pasa de estado y no genera nada en el bus.

                pass
            elif cache_block_state == "E":
                # Si no hay un caché miss y el bloque está en estado E, el procesador sí puede leer el dato.
                # Por lo tanto el bloque no pasa de estado y no genera nada en el bus.
                pass
            elif cache_block_state == "O":
                # Si no hay un caché miss y el bloque está en estado O, el procesador sí puede leer el dato.
                # Por lo tanto el bloque no pasa de estado y no genera nada en el bus.
                pass
            elif cache_block_state == "S":
                # Si no hay un caché miss y el bloque esta en el estado S, el procesador sí puede leer el dato.
                # Por lo tanto el bloque no pasa de estado y no genera nada en el bus.
                pass
            else:
                self.set_read_miss_flag(False)

            ################################Seguir con el resto de estados.
        # Pregunto si la instruccion es un write:
        elif self.instruction_read() == "write":
            address = self.get_address()
            set_to_look = get_set_to_look(address)
            bit = get_bit(address)
            tag = get_tag(address)
            cache_block_state = self.get_block_state(set_to_look, bit)
            if cache_block_state == "I" or self.write_miss(set_to_look, bit, tag):
                # Seteo la bandera de que el procesador desea escribir.
                self.set_PrWrt(True)
                # Levanto bandera de que el procesador desea escribir e intenta hacer que el bus actualice.
                self.set_BusRdX(True)
                self.get_cache().get_sets()[set_to_look][bit].set_data(self.instruction_data())
                self.get_cache().get_sets()[set_to_look][bit].set_tag(tag)
                self.get_cache().get_sets()[set_to_look][bit].set_memory_address(address)
                self.get_cache().get_sets()[set_to_look][bit].set_state("M")
                self.set_state("M")
            elif cache_block_state == "M":
                # Como el procesador quiere escribir, y no hay un write miss, entonces se queda en este estado
                # y escribe el dato.
                # Por lo tanto no genera nada en el bus.
                self.get_cache().get_sets()[set_to_look][bit].set_data(self.instruction_data())
                self.get_cache().get_sets()[set_to_look][bit].set_tag(tag)
                self.get_cache().get_sets()[set_to_look][bit].set_memory_address(address)
                self.get_cache().get_sets()[set_to_look][bit].set_state("M")
            elif cache_block_state == "E":
                # Como el procesador quiere escribir, y no hay un write miss, entonces se queda en el estado M
                # y escribe el dato
                # Por lo tanto no genera nada en el bus.
                self.get_cache().get_sets()[set_to_look][bit].set_data(self.instruction_data())
                self.get_cache().get_sets()[set_to_look][bit].set_tag(tag)
                self.get_cache().get_sets()[set_to_look][bit].set_memory_address(address)
                self.get_cache().get_sets()[set_to_look][bit].set_state("M")
            elif cache_block_state == "O":
                # Como el procesador quiere escribir, y no hay un write miss, entonces se queda en el estado M
                # y escribe el dato.
                # Por lo tanto debe actualizar
                self.get_cache().get_sets()[set_to_look][bit].set_data(self.instruction_data())
                self.get_cache().get_sets()[set_to_look][bit].set_tag(tag)
                self.get_cache().get_sets()[set_to_look][bit].set_memory_address(address)
                self.get_cache().get_sets()[set_to_look][bit].set_state("M")
                self.set_BusUpgrd(True)
            elif cache_block_state == "S":
                self.get_cache().get_sets()[set_to_look][bit].set_data(self.instruction_data())
                self.get_cache().get_sets()[set_to_look][bit].set_tag(tag)
                self.get_cache().get_sets()[set_to_look][bit].set_memory_address(address)
                self.get_cache().get_sets()[set_to_look][bit].set_state("M")
                self.set_BusUpgrd(True)
        elif self.instruction_read() == "calc":
            self.set_BusRd(False)
            self.set_BusUpgrd(False)
            self.set_BusRdX(False)
            self.set_read_miss_flag(False)








# Address siempre lo trato como binario


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

import utils
import board
import analogio
import digitalio


class Potentiostat:
    """
    Provides an interface to IO Rodeo's Rodeostat FeatherWing potentiostat. 

        pstat = Potentiostat()

    Optionally the current_range and number averages per measurement can be given 
    as arguments. 
        
        pstat = Potentiostat(current_range='100uA', num_avg=10)

    The counter electrode can be connected/disconnected with the "connected" property.

        pstat.connected = True 

        or

        pstat.connected = False

    The set-point is available via the "voltage" property To set the set-point voltage

        pstat.voltage = new_voltage_value

    Alternatively you can read the current set-point value as follows.

        setpt_voltage = pstat.voltage

    To get the current in/out of the working electrode you can read the current property. 

        current = pstat.current

    Additional properties are

        current_range:   set/get current range setting 
        averaging:       set/get the number of averaging values
        tia_voltage:     get the transimpedance amplifier voltage
        ref_voltage:     get the reference electrode voltage

    """

    CURRENT_RANGE_TO_TIA_RESISTOR = {
            '1uA'    : 1650000.0,
            '10uA'   : 165000.0, 
            '100uA'  : 16500.0,
            '1000uA' : 1650.0,
            }
    TIA_RESISTOR_TO_CURRENT_RANGE = {v:k for (k,v) in CURRENT_RANGE_TO_TIA_RESISTOR.items()}

    def __init__(self, current_range='100uA', num_avg=15):

        self.current_range = current_range
        self.num_avg = num_avg 

        # Hardware connections 
        self.setp_aout = analogio.AnalogOut(board.A0)
        self.setp_aout_saved_value = 0.0
        self.tia_ain = analogio.AnalogIn(board.A2)
        self.ref_ain = analogio.AnalogIn(board.A4)
        self.ctr_elect_switch = digitalio.DigitalInOut(board.D13)
        self.ctr_elect_switch.direction = digitalio.Direction.OUTPUT

        # Transimpedance amplifier resistor value
        self.tia_resistor_ohm = self.CURRENT_RANGE_TO_TIA_RESISTOR[current_range]

        # System voltage (vpow) and virtual ground voltage (vgnd) 
        self.vpow = self.tia_ain.reference_voltage  
        self.vgnd = 0.5*self.vpow                   

        # Set initial state
        self.offset = 0.0
        self.connected = False 
        self.voltage = 0.0

    @property
    def current_range(self):
        return self.TIA_RESISTOR_TO_CURRENT_RANGE[self.tia_resistor_ohm]

    @current_range.setter
    def current_range(self, value):
        self.tia_resistor_ohm = self.CURRENT_RANGE_TO_TIA_RESISTOR[value]

    @property
    def averaging(self):
        return self.num_avg

    @averaging.setter
    def averaging(self, num):
        self.num_avg = num 

    @property
    def connected(self):
        return not self.ctr_elect_switch.value

    @connected.setter
    def connected(self,value):
        if value:
            self.ctr_elect_switch.value = False
        else:
            self.ctr_elect_switch.value = True 

    @property
    def voltage(self):
        return self.setp_aout_saved_value

    @voltage.setter
    def voltage(self,value):
        value_shifted = self.vgnd + value + self.offset
        value_uint16 = utils.volt_to_uint16(value_shifted,self.vpow)
        self.setp_aout.value = value_uint16
        self.setp_aout_saved_value = value

    @property
    def current(self):
        value = self.tia_voltage/self.tia_resistor_ohm
        return value

    @property
    def tia_voltage(self):
        return self.read_ain_avg(self.tia_ain, self.num_avg)

    @property
    def ref_voltage(self):
        return self.read_ain_avg(self.ref_ain, self.num_avg)

    def read_ain(self,ain):
        value_uint16 = ain.value
        value_shifted = utils.uint16_to_volt(value_uint16,self.vpow)
        value = value_shifted - self.vgnd
        return value

    def read_ain_avg(self,ain,num):
        value = 0.0
        for i in range(num):
            value += self.read_ain(ain)
        return value/float(num)





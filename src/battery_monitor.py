import board
import analogio
import ulab.numpy as np
import constants
import utils
import lowpass_filter


class BatteryMonitor:
    """
    Implements a simple battery monitor for the PyBadge. 

        monitor = BatteryMonitor()

    Reads the lipo battery voltage from analog input A6 every time the 
    update method is called. 

        monitor.update()

    This method should be called periodically with an regular time step
    equal to constants.LOOP_DT. 

    The battery voltage is available in both raw 

        monitor.voltage_raw 

    and lowpass filtered
    
        monitor.voltage_lowpass

    versions. The lowpass filtered version is useful for displays of the
    battery voltage as it doesn't jump around as much as the raw value. 

    """
    VOLT_NUM_INIT = 5 
    FREQ_CUTOFF = 0.02

    def __init__(self):
        self.battery_ain = analogio.AnalogIn(board.A6)
        self.vpow = self.battery_ain.reference_voltage  
        self.lowpass = None

    def update(self):
        # Initialize lowpass filter
        if self.lowpass is None:
            # First reading tends to be low for some reason. Throw a couple away 
            # points rather than initialize lowpass filter to low value.
            for i in range(self.VOLT_NUM_INIT):
                dummy = self.voltage_raw

            #Create lowpass filter 
            self.lowpass = lowpass_filter.LowpassFilter(
                    freq_cutoff = self.FREQ_CUTOFF, 
                    value = self.voltage_raw,  
                    dt = constants.LOOP_DT
                    )
        else:
            # Update filter on new reading
            self.lowpass.update(self.voltage_raw)

    @property
    def voltage_lowpass(self):
        if self.lowpass is None:
            return 0.0
        else:
            return self.lowpass.value

    @property
    def voltage_raw(self):
       return 2.0*utils.uint16_to_volt(self.battery_ain.value, self.vpow)



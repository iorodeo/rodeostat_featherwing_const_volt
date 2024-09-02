import time
import utils
import constants
from data_logger import DataLogger
from potentiostat import Potentiostat
from button_monitor import ButtonMonitor
from battery_monitor import BatteryMonitor
from const_volt_display import ConstVoltDisplay
from temperature_sensor import TemperatureSensor

class ConstVoltApp:
    """
    Implements a constant voltage voltammetry example app for the Rodeostat
    Feather & PyBadge. 

    By default, when no buttons are pressed during startup the flash storage
    will be read-write for circuitpython and read-only for the host PC (if
    present).  This can be changed by pressing any button (except reset) during
    startup during powerup of after a hard reset. In which case the flash
    storage will be read-only for circuitpython and read-write for the host PC
    (if present). 

    See constants.py for the values of the various constants. 


    BUTTON_START: (currently the start button on the pybadge) 

        Connects electrode and starts acquisition. If the false drive is
        read-write, which is the default, then data is written to a file in the
        DATA_FILES_DIR directory on the PyBadge. The data files are named
        DATA_FILE_PREFIX[N].txt where [N] in the number of the data file being
        created. 

    BUTTON_STOP  (current the select button on the pybadge)

        Stops the acquisition of data and closes any open files.

    BUTTON_SETPT_INCR (currently the up arrow key on the pybadge)

        Increases the set-point voltage by SETPT_VOLT_STEP. 

    BUTTON_SETPT_DECR (currently the down arrow key on the pybadge)

        Decreases the set-point voltage by SETPT_VOLT_STEP 

    BUTTON_CLEAR_FILES (currently button A on the pybadge)

        Clears/erases all data files on the device. 
 
    """

    def __init__(self):
        self.running = False
        self.t_start = 0.0
        self.read_only = utils.is_read_only()
        self.setpt_voltage = constants.DEFAULT_SETPT_VOLT 
        self.pstat = Potentiostat(constants.CURRENT_RANGE)
        self.pstat.connected = False
        self.button_monitor = ButtonMonitor()
        self.battery_monitor = BatteryMonitor()
        self.data_logger = DataLogger(self.read_only)
        self.temperature_sensor = TemperatureSensor()

        self.display = ConstVoltDisplay()
        self.display.set_running(False)
        self.display.set_time(0.0)
        self.display.set_volt(self.setpt_voltage)
        self.display.set_curr(0.0)
        self.button_to_action = {
                constants.BUTTON_START       : self.on_button_start, 
                constants.BUTTON_STOP        : self.on_button_stop, 
                constants.BUTTON_SETPT_INCR  : self.on_button_setpt_incr, 
                constants.BUTTON_SETPT_DECR  : self.on_button_setpt_decr, 
                constants.BUTTON_CLEAR_FILES : self.on_button_clear_files, 
                }

    def handle_button_press(self):
        button = self.button_monitor.events
        if button is None:
            return
        try:
            self.button_to_action[button]()
        except KeyError:
            pass

    def on_button_start(self): 
        self.pstat.connected = True
        self.pstat.voltage = self.setpt_voltage
        self.t_start = time.monotonic()
        self.running = True
        self.data_logger.start()
        self.display.set_running(True)

    def on_button_stop(self):
        self.pstat.connected = False
        self.pstat.voltage = 0.0
        self.running = False
        self.data_logger.stop()
        self.display.set_running(False)

    def on_button_setpt_incr(self):
        self.setpt_voltage += constants.SETPT_VOLT_STEP
        self.setpt_voltage = min(self.setpt_voltage, constants.SETPT_VOLT_MAXVAL)

    def on_button_setpt_decr(self):
        self.setpt_voltage -= constants.SETPT_VOLT_STEP
        self.setpt_voltage = max(self.setpt_voltage, constants.SETPT_VOLT_MINVAL)

    def on_button_clear_files(self):
        if not self.running:
            self.file_count = 0
            self.data_logger.reset()

    def run(self):
        while True:
            self.handle_button_press()
            
            self.battery_monitor.update()
            self.temperature_sensor.update()

            self.display.set_volt(self.setpt_voltage)
            self.display.set_mode(self.read_only)
            self.display.set_file(self.data_logger.data_file_name)
            self.display.set_vbat(self.battery_monitor.voltage_lowpass)
            self.display.set_temp(self.temperature_sensor.value)

            if self.running:
                t = time.monotonic() - self.t_start
                self.pstat.voltage = self.setpt_voltage
                curr_ua = utils.convert_a_to_ua(self.pstat.current)
                self.display.set_time(t)
                self.display.set_curr(curr_ua)
                data = {
                        't'    : t, 
                        'volt' : self.setpt_voltage, 
                        'curr' : curr_ua, 
                        'temp' : self.temperature_sensor.value, 
                        }
                self.data_logger.update(data)
            else:
                self.display.set_time(0.0)
                self.display.set_curr(None)




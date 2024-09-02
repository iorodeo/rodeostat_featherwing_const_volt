import time
import board
import utils
import constants
import adafruit_ds18x20
from adafruit_onewire.bus import OneWireBus


class TemperatureSensor:

    READY_MARGIN = 1.2

    def __init__(self):
        self.value = None 
        self.have_sensor = False

        if constants.TEMP_SENSOR_ENABLED:
            # Scan bus to get onewire device. We assume tempature
            # sensor is the only device on the bus
            self.bus = OneWireBus(board.D2)
            device_list = self.bus.scan()
            try:
                # Assume sensor is only device on the bus - use first devie.
                self.sensor = adafruit_ds18x20.DS18X20(self.bus, device_list[0]) 
            except (IndexError, ValueError):
                pass
            else:
                self.have_sensor = True
                self.sensor.resolution = constants.TEMP_SENSOR_RESOLUTION
                self.conversion_delay = self.sensor.start_temperature_read()
                self.t_ready = self.next_t_ready()

    def next_t_ready(self):
        return self.READY_MARGIN*self.conversion_delay + time.monotonic()

    @utils.with_temp_sensor
    def update(self):
        if time.monotonic() > self.t_ready: 
            self.value = self.sensor.read_temperature()
            self.sensor.start_temperature_read()
            self.t_ready = self.next_t_ready()

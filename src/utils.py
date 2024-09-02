import constants

UINT16_MAX_VALUE = 2**16 - 1

# Utility functions
# -----------------------------------------------------------------------

def volt_to_uint16(v,vref):
    vint = int(UINT16_MAX_VALUE*float(v)/float(vref))
    return clamp(vint, 0, UINT16_MAX_VALUE)

def uint16_to_volt(n,vref):
    return vref*float(n)/float(UINT16_MAX_VALUE)

def clamp(value, min_value, max_value):
    value_clamped = min(max_value, value)
    value_clamped = max(0,value_clamped)
    return value_clamped

def convert_a_to_ua(val):
    return val*1.0e6

def is_read_only():
    """
    Reads boot_out.txt file to see if flash drive is mounted read-only or 
    read-write. Note, this has to be written to boot_out.py in boot.py. 
    """
    read_only = False
    with open('boot_out.txt') as f:
        for line in f.readlines():
            if 'read-only' in line:
                read_only = True
    return read_only

# Decorators
# ------------------------------------------------------------------------

def if_read_write(func):
    """ 
    Class method decorator, modifies method so that method is only called if
    the class's read_only property is False  
    """
    def wrap(self, *args, **kwargs):
        if self.read_only:
            return None
        else:
            return func(self, *args, **kwargs)
    return wrap

def with_temp_sensor(func):
    """ 
    Class method decorator, modifies method so that method is only called if
    the temperature sensor is enabled, the is found on the onewire bus, i.e., 
    self.have_sensor==True.
    """
    def wrap(self, *args, **kwargs):
        if constants.TEMP_SENSOR_ENABLED and self.have_sensor: 
            return func(self, *args, **kwargs)
        else:
            return None
    return wrap


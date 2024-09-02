# Voltage and current 
CURRENT_RANGE = '100uA'
DEFAULT_SETPT_VOLT = 0.5
SETPT_VOLT_STEP    = 0.05
SETPT_VOLT_MAXVAL  = 1.6
SETPT_VOLT_MINVAL  = -1.6

# Temperature sensor
TEMP_SENSOR_ENABLED = False 
TEMP_SENSOR_RESOLUTION = 12 # 9, 10, 11 or 12 
TEMP_SENSOR_SCHEDULE = [
        ( 5.0, 10.0),  # window #1 (t_start, t_stop)
        (20.0, 30.0),  # window #2 (t_start, t_stop) 
        ]              # ... etc

# Data logging
DATA_FILES_DIR = 'data_files'
DATA_FILE_PREFIX = 'data'
TEMP_FILE_PREFIX = 'temp'
TEMP_IN_DATA_FILE = False 

# Button assignments
BUTTON_STOP = 3
BUTTON_START = 2
BUTTON_SETPT_INCR = 6
BUTTON_SETPT_DECR = 5
BUTTON_CLEAR_FILES = 1
BUTTON_MOUNT_READONLY = 7

# Display settings
RUNNING_STR = 'RUNNING'
STOPPED_STR = 'STOPPED'
STATE_STR = 'STATE'
TIME_STR = 'TIME'
VOLT_STR = 'VSET'
CURR_STR = 'IWRK'
TEMP_STR = 'TEMP'
VBAT_STR = 'VBAT'
MODE_STR = 'MODE'
FILE_STR = 'FILE'
NONE_STR = 'NONE'
READ_ONLY_STR = 'READ-ONLY'
READ_WRITE_STR = 'READ-WRITE'

# Display font and colors
FONT_FILE = 'Hack-Bold-10.pcf'
TEXT_COLOR = 'orange'
BACKGROUND_COLOR = 'black'

# Display positioning
LABELS_XPOS = 4
LABELS_YPOS_START = 0
if TEMP_SENSOR_ENABLED:
    LABELS_YPOS_STEP = 16 
else:
    LABELS_YPOS_STEP = 18 



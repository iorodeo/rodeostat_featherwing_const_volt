import os
import utils
import constants
from running_average import RunningAverage


class DataLogger:
    """
    Implements a simple data logger which writes data to files in the
    constants.DATA_FILES_DIR directory.  This directory is created if it
    doesn't exist.  

    data_logger = DataLogger()

    The files will have prefix constants.DATA_FILE_PREFIX and are numbered
    in the order created, e.g. 

        {DATA_FILE_PREFIX}1.txt
        {DATA_FILE_PREFIX}2.txt
        {DATA_FILE_PREFIX}3.txt
        ...
        etc

    Logging is started with the "start" method

        data_logger.start()

    and stopped with the "stop" method

        data_logger.stop()

    On creation the data logger will look for files in the constants.DATA_FILES_DIR 
    directory and use the number of files present to initialize the current file_count.

    The files in the constants.DATA_FILES_DIR directory and be deleted using 
    the "reset" method. This will also reset the file_count to zero.

    """

    def __init__(self, read_only):
        self.read_only = read_only
        self.data_fid = None
        self.temp_fid = None
        self.data_file_name = None 
        self.data_file_path = None
        self.temp_file_name = None
        self.temp_file_path = None
        self.file_count = 0
        self.create_data_dir()
        self.init_file_count()
        self.temp_averages = [RunningAverage() for _ in constants.TEMP_SENSOR_SCHEDULE]

    def __del__(self):
        os.sync()
        if self.data_fid is not None:
            self.data_fid.close()
        if self.temp_fid is not None:
            self.temp_fid.close()

    @utils.if_read_write
    def init_file_count(self):
        """ Checks for existing data files and sets file_count. """
        self.file_count = 0
        for item in os.listdir(constants.DATA_FILES_DIR):
            if constants.DATA_FILE_PREFIX in item:
                self.incr_file()

    @utils.if_read_write
    def start(self):
        """ Increments file count and starts data logging """
        self.incr_file()
        self.data_fid = open(self.data_file_path, 'w')
        if constants.TEMP_SENSOR_ENABLED and constants.TEMP_SENSOR_SCHEDULE:
            self.temp_fid = open(self.temp_file_path, 'w')
            for average in self.temp_averages:
                average.reset()

    @utils.if_read_write
    def stop(self):
        """ Stops data logging """
        if self.data_fid is not None:
            self.data_fid.close()
            self.data_fid = None
        if self.temp_fid is not None:
            self.temp_fid.close()
            self.temp_fid = None
        os.sync()

    @utils.if_read_write
    def reset(self):
        """ Erases existing data files and resets file count """ 
        if self.data_fid is not None or self.temp_fid is not None:
            self.stop()
        for file_name in os.listdir(constants.DATA_FILES_DIR):
            os.unlink(f'{constants.DATA_FILES_DIR}/{file_name}')
        self.file_count = 0
        self.data_file_name = constants.NONE_STR 
        self.temp_file_name = constants.NONE_STR
        os.sync()

    @utils.if_read_write
    def write_data(self, msg):
        if self.data_fid is not None:
            self.data_fid.write(f'{msg}\n')

    @utils.if_read_write
    def write_temp(self,msg):
        if constants.TEMP_SENSOR_ENABLED:
            if self.temp_fid is not None:
                self.temp_fid.write(f'{msg}\n')

    def incr_file(self):
        self.file_count += 1
        self.data_file_name = f'{constants.DATA_FILE_PREFIX}{self.file_count}.txt'
        self.data_file_path = f'{constants.DATA_FILES_DIR}/{self.data_file_name}'
        self.temp_file_name = f'{constants.TEMP_FILE_PREFIX}{self.file_count}.txt'
        self.temp_file_path = f'{constants.DATA_FILES_DIR}/{self.temp_file_name}'

    @utils.if_read_write
    def create_data_dir(self):
        if not constants.DATA_FILES_DIR in os.listdir():
            os.mkdir(constants.DATA_FILES_DIR)

    @utils.if_read_write
    def update(self, data):
        t    = data['t']
        volt = data['volt']
        curr = data['curr']
        temp = data['temp']
        if constants.TEMP_IN_DATA_FILE and temp is not None:
            self.write_data(f'{t:1.2f} {volt:1.2f} {curr:1.2f} {temp:1.2f}')
        else:
            self.write_data(f'{t:1.2f} {volt:1.2f} {curr:1.2f}')
        if constants.TEMP_SENSOR_ENABLED:
            for index, window in enumerate(constants.TEMP_SENSOR_SCHEDULE):
                t0, t1 = window
                if t >= t0 and t <= t1 and temp is not None: 
                    self.temp_averages[index].update(temp)
                    temp_average = self.temp_averages[index].value
                    self.write_temp(f'{t:1.2f} {temp:1.2f} {temp_average:1.2f}')


import os
import utils
import constants

def if_read_write(func):
    """ 
    Decorator, modifies method so that method is only called if the class's
    read_only property is False  
    """
    def wrap(self, *args, **kwargs):
        if self.read_only:
            return None
        else:
            return func(self, *args, **kwargs)
    return wrap


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
        self.fid = None
        self.file_name = None 
        self.file_path = None
        self.file_count = 0
        self.create_data_dir()
        self.init_file_count()

    def __del__(self):
        if self.fid is not None:
            os.sync()
            self.fid.close()

    @if_read_write
    def init_file_count(self):
        """ Checks for existing data files and sets file_count. """
        self.file_count = 0
        for item in os.listdir(constants.DATA_FILES_DIR):
            self.incr_file()

    @if_read_write
    def start(self):
        """ Increments file count and starts data logging """
        self.incr_file()
        self.fid = open(self.file_path, 'w')

    @if_read_write
    def stop(self):
        """ Stops data logging """
        if self.fid is not None:
            self.fid.close()
            self.fid = None
            os.sync()
            print(os.statvfs('/'))

    @if_read_write
    def reset(self):
        """ Erases existing data files and resets file count """ 
        if self.fid is not None:
            self.stop()
        for file_name in os.listdir(constants.DATA_FILES_DIR):
            os.unlink(f'{constants.DATA_FILES_DIR}/{file_name}')
        self.file_count = 0
        self.file_name = constants.NONE_STR 
        os.sync()

    @if_read_write
    def write(self, data):
        if self.fid is not None:
            self.fid.write(f'{data}\n')

    @if_read_write
    def incr_file(self):
        self.file_count += 1
        self.file_name = f'{constants.DATA_FILE_PREFIX}{self.file_count}.txt'
        self.file_path = f'{constants.DATA_FILES_DIR}/{self.file_name}'

    @if_read_write
    def create_data_dir(self):
        if not constants.DATA_FILES_DIR in os.listdir():
            os.mkdir(constants.DATA_FILES_DIR)


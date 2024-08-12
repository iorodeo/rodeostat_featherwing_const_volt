import time
import board
import displayio
import constants
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes import circle
from colors import color_to_rgb
from colors import color_to_index
from colors import num_color

class ConstVoltDisplay:

    """
    Implements the display for the constant voltage example app. 
    """

    def __init__(self):
        board.DISPLAY.brightness = 1.0
        font = bitmap_font.load_font(constants.FONT_FILE)
        
        self.palette = displayio.Palette(num_color)
        for i, self.palette_tuple in enumerate(color_to_rgb.items()):
            self.palette[i] = self.palette_tuple[1]   
        
        # Create self.bitmap and tile grid for display
        self.bitmap = displayio.Bitmap(
                board.DISPLAY.width, 
                board.DISPLAY.height, 
                num_color
                )
        self.bitmap.fill(color_to_index[constants.BACKGROUND_COLOR])
        self.tile_grid = displayio.TileGrid(self.bitmap,pixel_shader=self.palette)

        # Create runnning label 
        xpos = constants.LABELS_XPOS 
        ypos = constants.LABELS_YPOS_START 
        ystep = constants.LABELS_YPOS_STEP 
        self.running_label = label.Label(
                font, 
                text = constants.STOPPED_STR,  
                color = color_to_rgb[constants.TEXT_COLOR], 
                scale = 1,
                anchor_point = (0.0, 0.0),
                )
        self.running_label.anchored_position = xpos, ypos 
        ypos += ystep

        # Create time label 
        self.time_label = label.Label(
                font, 
                text = f'{constants.TIME_STR} 0.0',  
                color = color_to_rgb[constants.TEXT_COLOR], 
                scale = 1,
                anchor_point = (0.0, 0.0),
                )
        self.time_label.anchored_position = xpos, ypos 
        ypos += ystep

        # Create voltage label 
        self.volt_label = label.Label(
                font, 
                text = f'{constants.VOLT_STR} 0.0',  
                color = color_to_rgb[constants.TEXT_COLOR], 
                scale = 1,
                anchor_point = (0.0, 0.0),
                )
        self.volt_label.anchored_position = xpos, ypos 
        ypos += ystep

        # Create current label 
        self.curr_label = label.Label(
                font, 
                text = f'{constants.CURR_STR} 0.0',  
                color = color_to_rgb[constants.TEXT_COLOR], 
                scale = 1,
                anchor_point = (0.0, 0.0),
                )
        self.curr_label.anchored_position = xpos, ypos 
        ypos += ystep

        # Create battery voltage label
        self.vbat_label = label.Label(
                font, 
                text = f'{constants.VBAT_STR}   0', 
                color = color_to_rgb[constants.TEXT_COLOR],
                scale = 1, 
                anchor_point = (0.0, 0.0),
                )
        self.vbat_label.anchored_position = xpos, ypos 
        ypos += ystep

        # Create number of mode label
        self.mode_label = label.Label(
                font, 
                text = f'{constants.MODE_STR}', 
                color = color_to_rgb[constants.TEXT_COLOR],
                scale = 1, 
                anchor_point = (0.0, 0.0),
                )
        self.mode_label.anchored_position = xpos, ypos 
        ypos += ystep
        
        # Create number of file label
        self.file_label = label.Label(
                font, 
                text = f'{constants.FILE_STR}   none', 
                color = color_to_rgb[constants.TEXT_COLOR],
                scale = 1, 
                anchor_point = (0.0, 0.0),
                )
        self.file_label.anchored_position = xpos, ypos 
        
        # Create display group
        self.group = displayio.Group()
        self.group.append(self.tile_grid)
        self.group.append(self.running_label)
        self.group.append(self.time_label)
        self.group.append(self.volt_label)
        self.group.append(self.curr_label)
        self.group.append(self.vbat_label)
        self.group.append(self.mode_label)
        self.group.append(self.file_label)
        board.DISPLAY.root_group = self.group

    def set_running(self, value):
        if value:
            text = f'{constants.STATE_STR}   {constants.RUNNING_STR}'
        else:
            text = f'{constants.STATE_STR}   {constants.STOPPED_STR}'
        self.running_label.text = text
    def set_time(self, t):
        self.time_label.text = f'{constants.TIME_STR} {t:7.2f}s'

    def set_volt(self, volt):
        if volt is not None:
            text = f'{constants.VOLT_STR} {volt:7.2f}V'
        else:
            text = f'{constants.VOLT_STR}    {constants.NONE_STR}'
        self.volt_label.text = text

    def set_curr(self, curr):
        if curr is not None:
            text = f'{constants.CURR_STR}  {curr:7.2f}uA'
        else:
            text = f'{constants.CURR_STR}    {constants.NONE_STR}'
        self.curr_label.text = text

    def set_vbat(self, volt):
        if volt is not None:
            text = f'{constants.VBAT_STR} {volt:7.2f}V'
        else:
            text = f'{constants.VBAT_STR}    {constants.NONE_STR}'
        self.vbat_label.text = text

    def set_mode(self, readonly):
        if readonly:
            text = f'{constants.MODE_STR}    {constants.READ_ONLY_STR}'
        else:
            text = f'{constants.MODE_STR}    {constants.READ_WRITE_STR}'
        self.mode_label.text = text

    def set_file(self, name):
        if name is None:
            text = f'{constants.FILE_STR}    {constants.NONE_STR}'
        else:
            text = f'{constants.FILE_STR}    {name}'
        self.file_label.text = text





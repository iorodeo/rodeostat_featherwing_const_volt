import board
import keypad

class ButtonMonitor:

    """
    A button monitor or the PyBadge.  Only monitors for released events. 

        button_monitor = ButtonMonitor()

    Check for events using the events method. 

        event = button_monitor.event()

    The returned value, event, will be the the number of the key pressed and
    released to generate the event. 

    """

    def __init__(self):
        self.pad = keypad.ShiftRegisterKeys( 
                clock=board.BUTTON_CLOCK, 
                data=board.BUTTON_OUT, 
                latch=board.BUTTON_LATCH, 
                key_count=8, 
                value_when_pressed=True,
                )

    @property
    def events(self):
        key = None
        event = self.pad.events.get()
        if event is not None:  
            if event.released:
                key = event.key_number
        return key


""" 
boot.py

Run on startup after powerup of after a hard reset.  Run before code.py. This
file can be used to set the device configuration. 

Currently setup to remount the flash drive as read-only for circuitpython if any
key is pressed during startup. 
"""
import time
import board
import keypad
import storage

# Setup keypad for button entry
pad = keypad.ShiftRegisterKeys( 
        clock=board.BUTTON_CLOCK, 
        data=board.BUTTON_OUT, 
        latch=board.BUTTON_LATCH, 
        key_count=8, 
        value_when_pressed=True,
        )

read_only = False
startup_dt = 3.0
t0 = time.monotonic()

# Window where user can press a button to set whether or not 
# flash storage is mounted read-write (default) or read-only
# for circuitpython
print('Flash config window')
while time.monotonic() < t0 + startup_dt:
    event = pad.events.get()
    if (event is not None) and event.released: 
        read_only = True
        break
print('Flash config window done')

# Write information to boot_out.txt so that it can be used by
# utils.is_read_only
if read_only:
    print('flash read-only')
else:
    print('flash read-write')

# Actually remount the flash storage  
storage.remount("/", readonly=read_only)

# De-initialize the pad so we can use it later
pad.deinit()
del pad

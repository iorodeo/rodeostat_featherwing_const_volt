# rodeostat_featherwing_const_volt

Example firmware which implements a constant voltage voltammetry example app
for the Rodeostat Feather and PyBadge. 

The function of the PyBadge buttons are shown in the figure below. 


![button functions](/images/button_functions.png)

* **Start Button**: connects electrode and starts acquisition. 

* **Stop Button**: stops acquisition and closes any open files.

* **Increase Voltage Button**: increases the set-point voltage. 

* **Decrease Voltage Button**: decreases the set-point voltage.  

* **Clear Files Button**: erases all data files. 

By default, when no buttons are pressed during startup the flash storage
will be read-write for circuitpython and read-only for the host PC (if
present).  This can be changed by pressing any button (except reset) during
startup during powerup of after a hard reset. In which case the flash
storage will be read-only for circuitpython and read-write for the host PC
(if present). 

When the flash storage is read-write data files will be written to a directory
named "data_files" on the PyBadge. The data files are named sequentially i.e.,
data1.txt, data2.txt, ... etc. 


## Firmware Installation

The firmware has been tested on CircuitPython 9.1.1. 


Instructions for installing CircuitPython on the PyBadge can be found  
[here](https://learn.adafruit.com/adafruit-pybadge/installing-circuitpython) 
and [here](https://circuitpython.org/board/pybadge/).

The dependencies for the firmware can be installed using the
[circup](https://github.com/adafruit/circup) utilty which can be installed on
your development PC using pip.  

To install the dependencies using circup run the following  

```bash
circup install -r requirements.txt


```
from inside the projects top-level directory.  


To install constant voltage voltammetry firmware on the to PyBadge you can use
one of the two the provided upload scripts:  upload.bash and upload.ps1 for
bash and powershell respectively.  

To upload the firmware using the upload.bash script simply run 

``` bash
./upload.bash


```
from a bash shell within the projects "src" directry. 

To install the firmware using the powershell script, upload.ps1 run the .ps1
script   

```powershell
upload.ps1

```

from a powerhsell withing the project's "src" directory. 



import ulab.numpy as np

class LowpassFilter:
    """
    Implements a simple 1st order lowpass filter. Assumes a fixed time 
    step. 

        filter = LowpassFilter()

    Optionally the cutoff frequency, initial value and time step can be
    specified. 

    The update method should be called periodically and the time step
    specified.

        filter.update(new_value)

    """

    def __init__(self, freq_cutoff=1.0, value=0.0, dt=1.0):
        self.dt = dt
        self.value = value
        self.freq_cutoff = freq_cutoff

    @property
    def freq_cutoff(self):
        return self._alpha/((1.0-self._alpha)*2.0*np.pi*self.dt)

    @freq_cutoff.setter
    def freq_cutoff(self, freq):
        self._alpha = (2.0*np.pi*self.dt*freq)/(2.0*np.pi*self.dt*freq+1)

    def update(self, new_value):
        self.value = self._alpha*new_value + (1.0-self._alpha)*self.value

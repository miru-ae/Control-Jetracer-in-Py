import ipywidgets.widgets as widgets
from IPython.display import display
import traitlets
import sys
controller = widgets.Controller(index=0)

display(controller)

from jetracer.nvidia_racecar import NvidiaRacecar
import traitlets

car = NvidiaRacecar()

car.throttle_gain = 0.2
car.steering_offset = 0.18
car.steering = 0.0

left_link = traitlets.dlink((controller.axes[0], 'value'), (car, 'steering'), transform = lambda x: -x)
right_link = traitlets.dlink((controller.axes[5], 'value'), (car, 'throttle'), transform = lambda x: -x)

from gpiozero import Button
from signal import pause
from RPiFunctions import start_rec
from RPiFunctions import stop_rec

button = Button(12)
button_stop = Button(20)

button.when_pressed = start_rec(False)
button_stop.when_pressed = stop_rec

pause()

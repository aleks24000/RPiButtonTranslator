from gpiozero import Button
from signal import pause
from RPiFunctions import start_rec
from RPiFunctions import stop_rec
from RPiFunctions import upload_file

button = Button(12)
button_stop = Button(20)
button_upload = Button(26)

button.when_pressed = start_rec(False)
button_stop.when_pressed = stop_rec(False)
button_upload.when_pressed = upload_file()

pause()

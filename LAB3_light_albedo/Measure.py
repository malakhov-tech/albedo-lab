from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview()
sleep(5)
camera.capture('/home/b03-401/pictures/nakal_red.png')
camera.stop_preview()
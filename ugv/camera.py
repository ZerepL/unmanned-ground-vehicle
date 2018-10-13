# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.2)

def tirafoto():
	camera.capture(rawCapture, format="bgr")
	return rawCapture.array

def salvarFoto():
	camera.start_preview()
	time.sleep(20)
	camera.capture("foto.jpg", resize=(320,240)) 
	camera.stop_preview()




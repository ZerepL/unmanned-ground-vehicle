'''Modulo responsavel pela camera'''
import time
from picamera.array import PiRGBArray
from picamera import PiCamera


CAMERA = PiCamera()
CAMERA.resolution = (640, 480)
CAMERA.framerate = 32
RAWCAPTURE = PiRGBArray(CAMERA, size=(640, 480))
time.sleep(0.2)


def tira_foto():
    '''Tira e retorna uma unica foto em formato brg'''
    CAMERA.capture(RAWCAPTURE, format="bgr")
    image = RAWCAPTURE.array
    RAWCAPTURE.truncate(0)
    return image


def salvar_foto():
    '''Funcao para salvar imagens direto na memoria do rasp
    Usado para criar representacoes de simbolos padroes no sistema interno'''
    CAMERA.start_preview()
    time.sleep(20)
    CAMERA.capture("foto.jpg", resize=(1080, 720))
    CAMERA.stop_preview()

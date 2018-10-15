import RPi.GPIO as io
import time

io.setwarnings(False)

io.setmode (io.BOARD)
io.setup(38,io.OUT)
io.setup(37,io.OUT)
io.setup(36,io.OUT)
io.setup(35,io.OUT)

pwmIn1 = io.PWM(38, 100)
pwmIn2 = io.PWM(37, 100)
pwmIn3 = io.PWM(36, 100)
pwmIn4 = io.PWM(35, 100)
pwmIn1.start(0)
pwmIn2.start(0)
pwmIn3.start(0)
pwmIn4.start(0)

def virar(direcao):
    if direcao == "esquerda":
        io.output(38,1)
        io.output(37,0)
        io.output(35,0)
        io.output(36,1)
        time.sleep(1)
        io.output(38,0)
        io.output(36,0)
        io.cleanup()

    elif direcao == "direita":
        io.output(38,0)
        io.output(37,1)
        io.output(35,1)
        io.output(36,0)
        time.sleep(1)
        io.output(37,0)
        io.output(36,0)
        io.cleanup()

    elif direcao == "frente":
        io.output(38,1)
        io.output(37,0)
        io.output(35,1)
        io.output(36,0)
        time.sleep(1)
        io.output(37,0)
        io.output(36,0)
        io.cleanup()

    elif direcao == "chegou":
        io.output(38,0)
        io.output(37,0)
        io.output(35,0)
        io.output(36,0)
        time.sleep(1)
        io.output(37,0)
        io.output(36,0)
        io.cleanup()

    else:
        io.cleanup()

def lerlinhas():
    for x in range(0,100):
        pwmIn1.ChangeDutyCycle(x)
        time.sleep(0.05)

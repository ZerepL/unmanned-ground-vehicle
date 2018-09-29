import RPi.GPIO as io
import time

io.setmode (io.BOARD)
io.setup(38,io.OUT)
io.setup(37,io.OUT)
io.setup(36,io.OUT)
io.setup(35,io.OUT)

def virar(direcao):
    if direcao == "left":
        io.output(38,1)
        io.output(37,0)
        io.output(35,0)
        io.output(36,1)
        time.sleep(1)
        io.output(38,0)
        io.output(36,0)
        io.cleanup()

    elif direcao == "right":
        io.output(38,0)
        io.output(37,1)
        io.output(35,1)
        io.output(36,0)
        time.sleep(1)
        io.output(37,0)
        io.output(36,0)
        io.cleanup()

    else:
        io.cleanup()

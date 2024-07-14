import pyfirmata

#To run without arduino connected
connected = True
try:
    comport = 'COM4'
    board = pyfirmata.Arduino(comport)
except:
    connected = False
    print("BOARD NOT CONNECTED!!\nCheck connection and try changing port number\nRunning without Arduino connected")

if connected:
    cathodeSegments = [
        [1, 1, 1, 1, 1, 1, 0],  # 0
        [0, 1, 1, 0, 0, 0, 0],  # 1
        [1, 1, 0, 1, 1, 0, 1],  # 2
        [1, 1, 1, 1, 0, 0, 1],  # 3
        [0, 1, 1, 0, 0, 1, 1],  # 4
        [1, 0, 1, 1, 0, 1, 1],  # 5
        [1, 0, 1, 1, 1, 1, 1],  # 6
        [1, 1, 1, 0, 0, 0, 0],  # 7
        [1, 1, 1, 1, 1, 1, 1],  # 8
        [1, 1, 1, 1, 0, 1, 1]   # 9
    ]


    pins = []

    for i in range(7, 14):
        pin = board.get_pin('d:{}:o'.format(i))
        pin.mode = pyfirmata.OUTPUT
        pins.append(pin)

def led(raised):
    if(connected):
        raisedBounded = min(9,raised)
        if (raised==-1):
            for i in range(7):
                pins[i].write(0)
        else:        
            for i in range(7):
                pins[i].write(cathodeSegments[raisedBounded][i])

def endProgram():
    led(-1)
    if connected:
        board.exit()
        

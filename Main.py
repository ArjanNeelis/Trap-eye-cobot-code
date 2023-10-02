from DRCF import *
import pyfirmata
from pyfirmata import util
import time

# ---- Set up communication with Arduino ----
board = pyfirmata.Arduino('COM4')
board.digital[2].mode = pyfirmata.OUTPUT    # Vacuum pump
board.digital[3].mode = pyfirmata.OUTPUT    # Screwdriver
board.digital[4].mode = pyfirmata.OUTPUT    # Linear actuator
board.digital[5].mode = pyfirmata.OUTPUT    # Trapezium servo
board.digital[6].mode = pyfirmata.OUTPUT    # Clamp servo
board.digital[7].mode = pyfirmata.INPUT     # Magnet switch
board.digital[8].mode = pyfirmata.INPUT     # Trapezium switch
board.digital[9].mode = pyfirmata.INPUT     # Trap-eye switch
board.digital[10].mode = pyfirmata.INPUT   # Start button
# board.digital[22].mode = pyfirmata.OUTPUT   # status LED green
# board.digital[24].mode = pyfirmata.OUTPUT   # status LED yellow
# board.digital[26].mode = pyfirmata.OUTPUT   # status LED red
# board.digital[28].mode = pyfirmata.OUTPUT   # status LED blue

it = util.Iterator(board)
it.start()

board.digital[7].enable_reporting()
board.digital[8].enable_reporting()
board.digital[9].enable_reporting()
board.digital[10].enable_reporting()

# ---- Coordinates for pick and place magnets ----
approach_magnet_1 = posx(200, -400, 350, 0, 180, 90)        # Above magnet storage
approach_magnet_2 = posx(200, -400, 100, 0, 150, 90)        # Angled above magnet
approach_magnet_3 = posx(100, -500, 350, 0, 180, 90)        # Above magnet place 1
approach_magnet_4 = posx(100, -590, 350, 0, 180, 90)        # Above magnet place 2
pick_magnet = posx(240, -400, 60, 0, 150, 90)               # Pick up position
place_position_1 = posx(100, -500, 280, 0, 180, 90)         # Place position 1st magnet
place_position_2 = posx(100, -590, 280, 0, 180, 90)         # Place position 2nd magnet

# ---- Coordinates for pick and place trapezium ----
approach_trapezium_1 = posx(200, -400, 350, 0, 180, 90)     # Above trapezium storage
approach_trapezium_2 = posx(200, -400, 100, 0, 150, 90)     # Go up at an angle
approach_trapezium_3 = posx(107.5, -545, 350, 0, 180, 90)   # Above trapezium place
pick_trapezium = posx(240, -600, 60, 0, 150, 90)            # Pick up position
place_trapezium = posx(107.5, -545, 280, 0, 180, 90)        # Place position trapezium

# ---- Coordinates for pick and place screw ----
approach_screw_1 = posx(100, -400, 350, 0, 180, 90)         # Start position
approach_screw_1j = posj(104.04, -7.73, -95.47, 180.0, 76.80, 14.04)
approach_screw_2 = posj(86.14, -13.48, -110.15, 267.86, 93.21, -213.69)  # Rotated tool
approach_screw_3 = posx(200, -300, 350, 180, -90, 90)       # Above screw feeder
approach_screw_4 = posx(125, -400, 230, 0, 180, 90)         # Move around TRAP-EYE
approach_screw_5 = posx(125, -655, 230, 0, 180, 90)         # Line up with screw hole
pick_screw = posx(200, -300, 300, 0, 90, -90)               # Pick up position
place_screw = posx(90, -655, 260, 0, 180, 90)               # Place position trapezium

# ---- Speed and acceleration parameter ----
v = 100
a = 100

# ---- timers for stuff ----
suck_time = 1       # Number of seconds to wait after (de)activating the vacuumpump
screw_time = 1       # Number of seconds to wait after (de)activating the screwdriver

# ---- Start with all variables False ----
magnets_placed = False
trapezium_placed = False
screw_placed = False
start = False
button_state = False
prev_button_state = False


def place_magnet_1():
    movel(approach_magnet_1, v=v, a=a)
    movel(approach_magnet_2, v=v, a=a)
    movel(pick_magnet, v=v, a=a)
    board.digital[2].write(1)               # Activate suction cup
    wait(suck_time)
    movel(approach_magnet_2, v=v, a=a)
    movel(approach_magnet_1, v=v, a=a)
    movel(approach_magnet_3, v=v, a=a)
    movel(place_magnet_1, v=v, a=a)
    board.digital[2].write(0)               # Deactivate suction cup
    wait(suck_time)
    movel(approach_magnet_3, v=v, a=a)


def place_magnet_2():
    movel(approach_magnet_1, v=v, a=a)
    movel(approach_magnet_2, v=v, a=a)
    movel(pick_magnet, v=v, a=a)
    board.digital[2].write(1)               # Activate suction cup
    wait(suck_time)
    movel(approach_magnet_2, v=v, a=a)
    movel(approach_magnet_1, v=v, a=a)
    movel(approach_magnet_4, v=v, a=a)
    movel(place_magnet_2, v=v, a=a)
    board.digital[2].write(0)               # Deactivate suction cup
    wait(suck_time)
    movel(approach_magnet_4, v=v, a=a)


def place_trapezium_1():
    movel(approach_trapezium_1, v=v, a=a)
    movel(approach_trapezium_2, v=v, a=a)
    movel(pick_trapezium, v=v, a=a)
    board.digital[2].write(1)               # Activate suction cup
    wait(suck_time)
    movel(approach_trapezium_2, v=v, a=a)
    movel(approach_trapezium_1, v=v, a=a)
    movel(approach_trapezium_3, v=v, a=a)
    movel(place_trapezium, v=v, a=a)
    board.digital[2].write(0)               # Deactivate suction cup
    wait(suck_time)
    movel(approach_trapezium_3, v=v, a=a)


def place_screw_1():
    movel(approach_screw_1, v=v, a=a)
    movej(approach_screw_2, v=v, a=a)
    movel(approach_screw_3, v=v, a=a)
    board.digital[3].write(1)               # Activate screwdriver
    movel(pick_screw, v=v, a=a)
    board.digital[2].write(0)               # Deactivate screwdriver
    movel(approach_screw_3, v=v, a=a)
    movel(approach_screw_1j, v=v, a=a)
    movel(approach_screw_4, v=v, a=a)
    movel(approach_screw_5, v=v, a=a)
    board.digital[2].write(1)               # Activate screwdriver
    movel(place_screw, v=v, a=a)
    # Maybe play with force control to feel is the screw is all the way in
    # The screwdriver does not have a slip clutch
    board.digital[2].write(0)               # Deactivate screwdriver
    movel(approach_screw_5, v=v, a=a)
    movel(approach_screw_4, v=v, a=a)


def calibration():
    movej(posj(0.0, 0.0, 0.0, 0.0, 0.0, 0.0), v=40, a=100)      # Home position needed for accuracy calibration
    movej(posj(116.57, -12.5, -89.73, 180.0, 77.76, 26.57), v=40, a=100)    # First position as joint value


# ---- Main code ----
# board.digital[24].write(1)
calibration()
# board.digital[24].write(0)

while not start:
    button_state = board.digital[10].read()
    if button_state != prev_button_state:
        if button_state:
            print('Button pressed')
            start = True
        else:
            pass
    print('Waiting for button press', sep=' ', end='', flush=True)
    wait(0.1)
    print(sep=' ', end='\r')
    prev_button_state = button_state

while start:
    magnet_switch = board.digital[6].read()
    trapezium_switch = board.digital[7].read()
    trap_eye_switch = board.digital[8].read()
    start_button = board.digital[9].read()
    print('Inputs read')
    time.sleep(0.1)

    if magnet_switch and not magnets_placed:
        print('Placing magnet 1...')
        place_magnet_1()
        print('Magnet 1 placed')
        print('Placing magnet 2...')
        place_magnet_2()
        print('Magnet 2 placed')
        magnets_placed = True
    elif trapezium_switch and magnets_placed and not trapezium_placed:
        print('Placing trapezium...')
        place_trapezium_1()
        print('Trapezium placed')
        trapezium_placed = True
    elif magnets_placed and trapezium_placed and not screw_placed:
        print('Placing screw...')
        place_screw_1()
        print('Screw placed')
        screw_placed = True
    elif magnets_placed and trapezium_placed and screw_placed:
        magnets_placed = False
        trapezium_placed = False
        screw_placed = False
        start = False
    else:
        if not magnets_placed and not magnet_switch:
            print('Magnet storage empty')
        elif not trapezium_placed and not trapezium_switch:
            print('Trapezium storage empty')
        else:
            print('Unexpected Error')

from DRCF import *
import pyfirmata
from pyfirmata import util
import time

board = pyfirmata.Arduino('COM4')
board.digital[3].mode = pyfirmata.OUTPUT
board.digital[4].mode = pyfirmata.OUTPUT
board.digital[5].mode = pyfirmata.OUTPUT
board.digital[6].mode = pyfirmata.INPUT
board.digital[7].mode = pyfirmata.INPUT
board.digital[8].mode = pyfirmata.INPUT
board.digital[9].mode = pyfirmata.INPUT
board.digital[10].mode = pyfirmata.OUTPUT
board.digital[11].mode = pyfirmata.OUTPUT
board.digital[12].mode = pyfirmata.OUTPUT

it = util.Iterator(board)
it.start()

board.digital[6].enable_reporting()
board.digital[7].enable_reporting()
board.digital[8].enable_reporting()
board.digital[9].enable_reporting()

# ---- Settings for I/O ----
suction_cup = 1     # Vacuum pump connected to digital_output 1
suck_time = 1       # Number of seconds to wait after (de)activating the vacuumpump
screwdriver = 2        # Screwdriver motor connected to digital_output 2
# screw_time = 1       # Number of seconds to wait after (de)activating the screwdriver

# ---- Coordinates for pick and place magnets ----
approach_magnet_1 = posx(200, -400, 350, 0, 180, 90)        # Above magnet storage
approach_magnet_2 = posx(200, -400, 100, 0, 150, 90)        # Angled above magnet
approach_magnet_3 = posx(100, -500, 350, 0, 180, 90)        # Above magnet place 1
approach_magnet_4 = posx(100, -590, 350, 0, 180, 90)        # Above magnet place 2
pick_magnet = posx(240, -400, 60, 0, 150, 90)               # Pick up position
place_position_1 = posx(100, -500, 280, 0, 180, 90)         # Place position 1st magnet
place_position_2 = posx(100, -590, 280, 0, 180, 90)         # Place position 2nd magnet

# ---- Coordinates for pick and place trapezium----
approach_trapezium_1 = posx(200, -400, 350, 0, 180, 90)     # Above trapezium storage
approach_trapezium_2 = posx(200, -400, 100, 0, 150, 90)     # Go up at an angle
approach_trapezium_3 = posx(107.5, -545, 350, 0, 180, 90)   # Above trapezium place
pick_trapezium = posx(240, -600, 60, 0, 150, 90)            # Pick up position
place_trapezium = posx(107.5, -545, 280, 0, 180, 90)    # Place position trapezium

# ---- Coordinates for pick and place screw ----
approach_screw_1 = posx(100, -400, 350, 0, 180, 90)  # Start position
approach_screw_1j = posj(104.04, -7.73, -95.47, 180.0, 76.80, 14.04)
approach_screw_2 = posj(86.14, -13.48, -110.15, 267.86, 93.21, -213.69)  # Rotated tool
approach_screw_3 = posx(200, -300, 350, 180, -90, 90)   # Above screw feeder
approach_screw_4 = posx(125, -400, 230, 0, 180, 90)     # Move around TRAP-EYE
approach_screw_5 = posx(125, -655, 230, 0, 180, 90)     # Line up with screw hole
pick_screw = posx(200, -300, 300, 0, 90, -90)   # Pick up position
place_screw = posx(90, -655, 260, 0, 180, 90)   # Place position trapezium

# ---- Speed and acceleration parameter ----
v = 100
a = 100


def place_magnet_1():
    movel(approach_magnet_1, v=v, a=a)
    movel(approach_magnet_2, v=v, a=a)
    movel(pick_magnet, v=v, a=a)
    set_digital_output(suction_cup, ON)                   # Activate suction cup
    wait(suck_time)
    movel(approach_magnet_2, v=v, a=a)
    movel(approach_magnet_1, v=v, a=a)
    movel(approach_magnet_3, v=v, a=a)
    movel(place_magnet_1, v=v, a=a)
    set_digital_output(suction_cup, OFF)                  # Deactivate suction cup
    wait(suck_time)
    movel(approach_magnet_3, v=v, a=a)


def place_magnet_2():
    movel(approach_magnet_1, v=v, a=a)
    movel(approach_magnet_2, v=v, a=a)
    movel(pick_magnet, v=v, a=a)
    set_digital_output(suction_cup, ON)                   # Activate suction cup
    wait(suck_time)
    movel(approach_magnet_2, v=v, a=a)
    movel(approach_magnet_1, v=v, a=a)
    movel(approach_magnet_4, v=v, a=a)
    movel(place_magnet_2, v=v, a=a)
    set_digital_output(suction_cup, OFF)                  # Deactivate suction cup
    wait(suck_time)
    movel(approach_magnet_4, v=v, a=a)


def place_trapezium_1():
    movel(approach_trapezium_1, v=v, a=a)
    movel(approach_trapezium_2, v=v, a=a)
    movel(pick_trapezium, v=v, a=a)
    set_digital_output(suction_cup, ON)  # Activate suction cup
    wait(suck_time)
    movel(approach_trapezium_2, v=v, a=a)
    movel(approach_trapezium_1, v=v, a=a)
    movel(approach_trapezium_3, v=v, a=a)
    movel(place_trapezium, v=v, a=a)
    set_digital_output(suction_cup, OFF)  # Deactivate suction cup
    wait(suck_time)
    movel(approach_trapezium_3, v=v, a=a)


def place_screw_1():
    movel(approach_screw_1, v=v, a=a)
    movej(approach_screw_2, v=v, a=a)
    movel(approach_screw_3, v=v, a=a)
    set_digital_output(screwdriver, ON)  # Activate screwdriver
    movel(pick_screw, v=v, a=a)
    set_digital_output(screwdriver, OFF)  # Deactivate screwdriver
    movel(approach_screw_3, v=v, a=a)
    movel(approach_screw_1j, v=v, a=a)
    movel(approach_screw_4, v=v, a=a)
    movel(approach_screw_5, v=v, a=a)
    set_digital_output(screwdriver, ON)  # Activate screwdriver
    movel(place_screw, v=v, a=a)
    set_digital_output(screwdriver, OFF)  # Deactivate screwdriver
    movel(approach_screw_5, v=v, a=a)
    movel(approach_screw_4, v=v, a=a)


def calibration():
    movej(posj(0.0, 0.0, 0.0, 0.0, 0.0, 0.0), v=40, a=100)      # Home position needed for accuracy calibration
    movej(posj(116.57, -12.5, -89.73, 180.0, 77.76, 26.57), v=40, a=100)        # First position as joint values


# ---- Main code ----
while True:
    magnet_switch = board.digital[6].read()
    trapezium_switch = board.digital[7].read()
    trap_eye_switch = board.digital[8].read()
    start_button = board.digital[9].read()
    print('Inputs read')
    time.sleep(0.1)

    magnets_placed = False
    trapezium_placed = False
    screw_placed = False

    if magnet_switch and not magnets_placed:
        place_magnet_1()
        place_magnet_2()
        magnets_placed = True
    elif trapezium_switch and magnets_placed and not trapezium_placed:
        place_trapezium_1()
        trapezium_placed = True
    elif magnets_placed and trapezium_placed and not screw_placed:
        place_screw_1()
        screw_placed = True
    elif magnets_placed and trapezium_placed and screw_placed:
        magnets_placed = False
        trapezium_placed = False
        screw_placed = False
    else:
        print('Error')
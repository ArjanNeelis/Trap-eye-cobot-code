from DRCF import *

# Code for picking&placing trapezium
# Settings for suction cup
suction_cup = 1                              # Vacuum pump connected to digital_output 1
suck_time = 1                                # Number of seconds to wait after (de)activating the vacuumpump
# Coordinates for pick and place
approach_trapezium_1 = posx(200, -400, 350, 0, 180, 90)     # Above trapezium storage
approach_trapezium_2 = posx(200, -400, 100, 0, 150, 90)     # Go up at an angle
approach_trapezium_3 = posx(107.5, -545, 350, 0, 180, 90)     # Above trapezium place
pick_trapezium = posx(240, -600, 60, 0, 150, 90)        # Pick up position
place_trapezium_pos = posx(107.5, -545, 280, 0, 180, 90)       # Place position trapezium
# Speed and acceleration parameter
v = 100
a = 100


def calibration():
    movej(posj(0.0, 0.0, 0.0, 0.0, 0.0, 0.0), v=40, a=100)      # Home position needed for accuracy calibration
    movej(posj(116.57, -12.5, -89.73, 180.0, 77.76, 26.57), v=40, a=100)        # First position as joint values


def place_trapezium():
    movel(approach_trapezium_1, v=v, a=a)
    movel(approach_trapezium_2, v=v, a=a)
    movel(pick_trapezium, v=v, a=a)
    set_digital_output(suction_cup, ON)  # Activate suctioncup
    wait(suck_time)
    movel(approach_trapezium_2, v=v, a=a)
    movel(approach_trapezium_1, v=v, a=a)
    movel(approach_trapezium_3, v=v, a=a)
    movel(place_trapezium_pos, v=v, a=a)
    set_digital_output(suction_cup, OFF)  # Deactivate suctioncup
    wait(suck_time)
    movel(approach_trapezium_3, v=v, a=a)
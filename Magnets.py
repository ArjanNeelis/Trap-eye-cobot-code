from DRCF import *

# Code for picking&placing magnets
# Settings for suction cup
suction_cup = 1     # Vacuum pump connected to digital_output 1
suck_time = 1       # Number of seconds to wait after (de)activating the vacuumpump
# Coordinates for pick and place
approach_magnet_1 = posx(200, -400, 350, 0, 180, 90)        # Above magnet storage
approach_magnet_2 = posx(200, -400, 100, 0, 150, 90)        # Angled above magnet
approach_magnet_3 = posx(100, -500, 350, 0, 180, 90)        # Above magnet place 1
approach_magnet_4 = posx(100, -590, 350, 0, 180, 90)        # Above magnet place 2
pick_magnet = posx(240, -400, 60, 0, 150, 90)       # Pick up position
place_position_1 = posx(100, -500, 280, 0, 180, 90)     # Place position 1st magnet
place_position_2 = posx(100, -590, 280, 0, 180, 90)     # Place position 2nd magnet
# Speed and acceleration parameter
v = 100
a = 100


def place_magnet_1():
    movel(approach_magnet_1, v=v, a=a)
    movel(approach_magnet_2, v=v, a=a)
    movel(pick_magnet, v=v, a=a)
    set_digital_output(suction_cup, ON)                   # Activate suctioncup
    wait(suck_time)
    movel(approach_magnet_2, v=v, a=a)
    movel(approach_magnet_1, v=v, a=a)
    movel(approach_magnet_3, v=v, a=a)
    movel(place_magnet_1, v=v, a=a)
    set_digital_output(suction_cup, OFF)                  # Deactivate suctioncup
    wait(suck_time)
    movel(approach_magnet_3, v=v, a=a)


def place_magnet_2():
    movel(approach_magnet_1, v=v, a=a)
    movel(approach_magnet_2, v=v, a=a)
    movel(pick_magnet, v=v, a=a)
    set_digital_output(suction_cup, ON)                   # Activate suctioncup
    wait(suck_time)
    movel(approach_magnet_2, v=v, a=a)
    movel(approach_magnet_1, v=v, a=a)
    movel(approach_magnet_4, v=v, a=a)
    movel(place_magnet_2, v=v, a=a)
    set_digital_output(suction_cup, OFF)                  # Deactivate suctioncup
    wait(suck_time)
    movel(approach_magnet_4, v=v, a=a)


def calibration():
    movej(posj(0.0, 0.0, 0.0, 0.0, 0.0, 0.0), v=40, a=100)      # Home position needed for accuracy calibration
    movej(posj(116.57, -12.5, -89.73, 180.0, 77.76, 26.57), v=40, a=100)        # First position as joint values


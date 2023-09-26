from DRCF import *

# Code for picking&placing magnets
# Settings for suctioncup
suction_cup = 1     # Vacuumpump connected to digital_output 1
suck_time = 1       # Number of seconds to wait after (de)activating the vacuumpump
# Coordinates for pick and place
approach_magnet_1 = posx(100, -400, 350, 30, -180, 115)     # Above magnet storage
approach_magnet_2 = posx(100, -500, 350, 30, -180, 115)     # Above magnet place 1
approach_magnet_3 = posx(100, -590, 350, 30, -180, 115)     # Above magnet place 2
pick_magnet = posx(100, -400, 60, 30, -180, 115)            # Pick up position
place_position_1 = posx(100, -500, 280, 30, -180, 115)      # Place position 1st magnet
place_position_2 = posx(100, -590, 280, 30, -180, 115)      # Place position 2nd magnet


def place_magnet_1():
    movel(approach_magnet_1, v=100, a=100)
    movel(pick_magnet, v=100, a=100)
    set_digital_output(suction_cup, ON)                   # Activate suctioncup
    wait(suck_time)
    movel(approach_magnet_1, v=100, a=100)
    movel(approach_magnet_2, v=100, a=100)
    movel(place_magnet_1, v=100, a=100)
    set_digital_output(suction_cup, OFF)                  # Deactivate suctioncup
    wait(suck_time)
    movel(approach_magnet_2, v=100, a=100)


def place_magnet_2():
    movel(approach_magnet_1, v=100, a=100)
    movel(pick_magnet, v=100, a=100)
    set_digital_output(suction_cup, ON)                   # Activate suctioncup
    wait(suck_time)
    movel(approach_magnet_1, v=100, a=100)
    movel(approach_magnet_3, v=100, a=100)
    movel(place_magnet_2, v=100, a=100)
    set_digital_output(suction_cup, OFF)                  # Deactivate suctioncup
    wait(suck_time)
    movel(approach_magnet_3, v=100, a=100)


if get_digital_input(1) == 1:
    place_magnet_1()
    place_magnet_2()

from DRCF import *

# Code for picking&placing trapezium
# Settings for suctioncup
suction_cup = 1                              # Vacuumpump connected to digital_output 1
suck_time = 1                                # Number of seconds to wait after (de)activating the vacuumpump
# Coordinates for pick and place
approach_trapezium_1 = posx(100, -400, 350, 30, -180, 115)  # Above trapezium storage
approach_trapezium_2 = posx(50, -400, 110, 75, -180, 115)   # Go up at an angle
approach_trapezium_3 = posx(107.5, -545, 350, 30, -180, 115)  # Above trapezium place
pick_trapezium = posx(100, -400, 60, 75, -180, 115)        # Pick up position
place_trapezium = posx(100, -545, 280, 30, -180, 115)     # Place position 1st magnet

movel(approach_trapezium_1)
movel(approach_trapezium_2)
movel(pick_trapezium)
set_digital_output(suction_cup, ON)  # Activate suctioncup
wait(suck_time)
movel(approach_trapezium_2)
movel(approach_trapezium_1)
movel(approach_trapezium_3)
movel(place_trapezium)
set_digital_output(suction_cup, OFF)  # Activate suctioncup
wait(suck_time)
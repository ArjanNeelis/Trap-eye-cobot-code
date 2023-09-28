from DRCF import *

# Code for picking&placing screw
# Settings for screwdriver
screwdriver = 2        # Screwdriver motor connected to digital_output 2
screw_time = 1       # Number of seconds to wait after (de)activating the screwdriver
# Coordinates for pick and place
approach_screw_1 = posx(100, -400, 350, 0, 180, 90)     # Start position
approach_screw_1j = (104.04, -7.73, -95.47, 180.0, 76.80, 14.04)
approach_screw_2 = posj(86.14, -13.48, -110.15, 267.86, 93.21, -213.69)      # Rotated tool
approach_screw_3 = posx(200, -300, 350, 180, -90, 90)       # Above screw feeder
approach_screw_4 = posx(125, -400, 230, 0, 180, 90)     # Move around TRAP-EYE
approach_screw_5 = posx(125, -655, 230, 0, 180, 90)     # Line up with screw hole
pick_screw = posx(200, -300, 300, 0, 90, -90)       # Pick up position
place_screw = posx(90, -655, 260, 0, 180, 90)       # Place position trapezium
# Speed and acceleration parameter
v = 100
a = 100

# --- Main code --- #
movej(posj(0.0, 0.0, 0.0, 0.0, 0.0, 0.0), v=40, a=100)
movej(posj(104.04, -7.73, -95.47, 180.0, 76.80, 14.04), v=40, a=100)

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
wait(screw_time)
set_digital_output(screwdriver, OFF)  # Deactivate screwdriver
movel(approach_screw_5, v=v, a=a)
movel(approach_screw_4, v=v, a=a)

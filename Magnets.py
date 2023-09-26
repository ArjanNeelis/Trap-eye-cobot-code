from DRCF import *

### Code for picking&placing magnets
### Settings for suctioncup
suctioncup = 1                              # Vacuumpump connected to digital_output 1
sucktime = 1                                # Number of seconds to wait after (de)activating the vacuumpump
### Coordinates for pick and place
approach1 = posx(100,-400,350,30,-180,115)  # Above magnet storage
approach2 = posx(100,-500,350,30,-180,115)  # Above magnet place 1
approach3 = posx(100,-590,350,30,-180,115)  # Above magnet place 2
pick = posx(100,-400,60,30,-180,115)        # Pick up position
place1 = posx(100,-500,280,30,-180,115)     # Place position 1st magnet
place2 = posx(100,-590,280,30,-180,115)     # Place position 2nd magnet

movel(approach1, v = 100, a = 100)
movel(pick, v = 100, a = 100)
set_digital_output(suctioncup, ON)                   # Activate suctioncup
wait(sucktime)
movel(approach1, v = 100, a = 100)
movel(approach2, v = 100, a = 100)
movel(place1, v = 100, a = 100)
set_digital_output(suctioncup, OFF)                  # Deactivate suctioncup
wait(sucktime)
movel(approach2, v = 100, a = 100)
movel(approach1, v = 100, a = 100)
movel(pick, v = 100, a = 100)
set_digital_output(suctioncup, ON)                   # Activate suctioncup
wait(sucktime)
movel(approach1, v = 100, a = 100)
movel(approach3, v = 100, a = 100)
movel(place2, v = 100, a = 100)
set_digital_output(suctioncup, OFF)                  # Deactivate suctioncup
wait(sucktime)
movel(approach3, v = 100, a = 100)
#movel(approach1, v = 100, a = 100)

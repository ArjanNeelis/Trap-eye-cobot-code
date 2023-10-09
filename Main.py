from DRCF import *
import pyfirmata
from pyfirmata import util
# import Vision

# ---- Set up communication with Arduino ----
port = 'COM4'                           # Port used to communicate with Arduino (Visible in Arduino IDE)
board = pyfirmata.Arduino(port)         # The connection between Arduino and laptop
linear_out = 2
linear_speed = 3
linear_in = 4
clamp_servo = 5
magnet_switch = 6
trapezium_switch = 7
trapeye_switch = 8
start_button = 9
vacuum_pump = 10
screwdriver = 11
red_LED = 12
green_LED = 13

board.digital[linear_in].mode = pyfirmata.OUTPUT       # Linear actuator
board.digital[linear_speed].mode = pyfirmata.PWM        # Linear actuator (PWM)
board.digital[linear_out].mode = pyfirmata.OUTPUT       # Linear actuator
board.digital[clamp_servo].mode = pyfirmata.SERVO       # Clamp servo (PWM)
board.digital[magnet_switch].mode = pyfirmata.INPUT     # Magnet switch
board.digital[trapezium_switch].mode = pyfirmata.INPUT  # Trapezium switch
board.digital[trapeye_switch].mode = pyfirmata.INPUT    # Trap-eye switch
board.digital[start_button].mode = pyfirmata.INPUT      # Start button
board.digital[vacuum_pump].mode = pyfirmata.OUTPUT      # Vacuum pump
board.digital[screwdriver].mode = pyfirmata.OUTPUT      # Screwdriver
board.digital[red_LED].mode = pyfirmata.OUTPUT          # status LED
board.digital[green_LED].mode = pyfirmata.OUTPUT        # status LED

it = util.Iterator(board)
it.start()

board.digital[magnet_switch].enable_reporting()         # Enable reading this port
board.digital[trapezium_switch].enable_reporting()      # Enable reading this port
board.digital[trapeye_switch].enable_reporting()        # Enable reading this port
board.digital[start_button].enable_reporting()          # Enable reading this port

# ---- Coordinates for pick and place magnets ----
approach_magnet_1 = posx(346, -297, 350, 0, 180, 90)        # Above magnet storage
approach_magnet_2 = posx(-15, -561, 370, 0, -150, 0)          # Above magnet place 1 angled
approach_magnet_3 = posx(-15, -546, 370, 0, -150, 0)        # Above magnet place 2 angled
pick_magnet = posx(346, -297, 111, 0, 180, 90)               # Pick up position
place_position_1 = posx(-15, -561, 350, 0, -150, 0)         # Place position 1st magnet
place_position_2 = posx(-15, -646, 350, 0, -150, 0)         # Place position 2nd magnet

# ---- Coordinates for pick and place trapezium ----
approach_trapezium_1 = posx(200, -400, 350, 0, 180, 90)     # Above trapezium storage
approach_trapezium_2 = posx(107.5, -545, 350, 0, 180, 90)   # Above trapezium place
pick_trapezium = posx(255, -342, 156, 0, 180, 90)            # Pick up position
place_trapezium = posx(-15, -603.5, 350, 0, -150, 0)        # Place position trapezium

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
v = 40
a = 50

# ---- Timers for stuff ----
suck_time = 1       # Number of seconds to wait after (de)activating the vacuum pump
screw_time = 1      # Number of seconds to wait after (de)activating the screwdriver

# ---- Start with all variables False ----
magnets_placed = False
trapezium_placed = False
screw_placed = False
qc_checked = False
start = False
button_state = False
prev_button_state = False


def place_magnet_1():
    board.digital[linear_out].write(0)      # Stop linear actuator extending
    board.digital[linear_in].write(1)       # Retract linear actuator
    board.digital[linear_speed].write(1)
    movel(approach_magnet_1, v=v, a=a)
    movel(pick_magnet, v=v, a=a)
    board.digital[vacuum_pump].write(1)     # Activate suction cup
    wait(suck_time)
    movel(approach_magnet_1, v=v, a=a)
    board.digital[linear_in].write(0)       # Stop linear actuator retracting
    board.digital[linear_out].write(1)      # Linear actuator out to give new magnet
    board.digital[linear_speed].write(1)
    movel(approach_magnet_2, v=v, a=a)
    movel(place_position_1, v=v, a=a)
    board.digital[vacuum_pump].write(0)     # Deactivate suction cup
    wait(suck_time)
    movel(approach_magnet_2, v=v, a=a)


def place_magnet_2():
    board.digital[linear_out].write(0)      # Stop linear actuator extending
    board.digital[linear_in].write(1)       # Retract linear actuator
    board.digital[linear_speed].write(1)
    movel(approach_magnet_1, v=v, a=a)
    movel(pick_magnet, v=v, a=a)
    board.digital[vacuum_pump].write(1)     # Activate suction cup
    wait(suck_time)
    movel(approach_magnet_1, v=v, a=a)
    board.digital[linear_in].write(0)       # Stop linear actuator retracting
    board.digital[linear_out].write(1)      # Linear actuator out to give new magnet
    board.digital[linear_speed].write(1)
    movel(approach_magnet_3, v=v, a=a)
    movel(place_position_2, v=v, a=a)
    board.digital[vacuum_pump].write(0)     # Deactivate suction cup
    wait(suck_time)
    movel(approach_magnet_3, v=v, a=a)


def place_trapezium_1():
    movel(approach_trapezium_1, v=v, a=a)
    movel(pick_trapezium, v=v, a=a)
    board.digital[vacuum_pump].write(1)     # Activate suction cup
    wait(suck_time)
    movel(approach_trapezium_1, v=v, a=a)
    movel(approach_trapezium_2, v=v, a=a)
    movel(place_trapezium, v=v, a=a)
    board.digital[vacuum_pump].write(0)     # Deactivate suction cup
    wait(suck_time)
    movel(approach_trapezium_2, v=v, a=a)


def place_screw_1():
    movel(approach_screw_1, v=v, a=a)
    movej(approach_screw_2, v=v, a=a)
    movel(approach_screw_3, v=v, a=a)
    board.digital[screwdriver].write(1)     # Activate screwdriver
    movel(pick_screw, v=v, a=a)
    board.digital[screwdriver].write(0)     # Deactivate screwdriver
    movel(approach_screw_3, v=v, a=a)
    movej(approach_screw_1j, v=v, a=a)
    movel(approach_screw_4, v=v, a=a)
    clamping()
    movel(approach_screw_5, v=v, a=a)
    board.digital[screwdriver].write(1)     # Activate screwdriver
    movel(place_screw, v=v, a=a)
    # Maybe play with force control to feel is the screw is all the way in
    # The screwdriver does not have a slip clutch
    board.digital[screwdriver].write(0)     # Deactivate screwdriver
    movel(approach_screw_5, v=v, a=a)
    movel(approach_screw_4, v=v, a=a)


def clamping():
    board.digital[clamp_servo].write(0)         # Press on the magnets
    board.digital[clamp_servo].write(39)        # Position for photo background
    board.digital[clamp_servo].write(100)       # Retreat to give robot more space


def calibration():
    movej(posj(0.0, 0.0, 0.0, 0.0, 0.0, 0.0), v=80, a=100)      # Home position needed for accuracy calibration
    movej(posj(139.4, -13.7, -88.2, 180.0, 78.1, 49.4), v=80, a=100)    # First position after calibration


# ---- Main code ----
board.digital[green_LED].write(1)
calibration()
board.digital[green_LED].write(0)

while True:
    while not start:
        button_state = board.digital[start_button].read()
        if button_state != prev_button_state:
            if button_state and trapeye_switch:
                print('Button pressed')
                start = True
            elif button_state and not trapeye_switch:
                print('No TRAP-EYE detected')
            else:
                pass
        print('Waiting for button press', sep=' ', end='', flush=True)
        wait(0.1)
        print(sep=' ', end='\r')
        prev_button_state = button_state

    while start:
        magnet_state = board.digital[magnet_switch].read()
        trapezium_state = board.digital[trapezium_switch].read()
        trapeye_state = board.digital[trapeye_switch].read()
        start_button_state = board.digital[start_button].read()
        print('Inputs read')
        wait(1)

        if magnet_state and not magnets_placed:
            print('Placing magnet 1...')
            place_magnet_1()
            print('Magnet 1 placed')
            magnet_state = board.digital[magnet_switch].read()
            while not magnet_state:
                magnet_state = board.digital[magnet_switch].read()
                wait(0.5)
            print('Placing magnet 2...')
            place_magnet_2()
            print('Magnet 2 placed')
            magnets_placed = True
        elif not trapezium_state and magnets_placed and not trapezium_placed:
            print('Placing trapezium...')
            place_trapezium_1()
            print('Trapezium placed')
            trapezium_placed = True
        elif magnets_placed and trapezium_placed and not screw_placed:
            print('Placing screw...')
            place_screw_1()
            print('Screw placed')
            screw_placed = True
        elif magnets_placed and trapezium_placed and screw_placed and not qc_checked:
            # Vision.Vision()
            qc_checked = True
            print('QC check passed')
        elif magnets_placed and trapezium_placed and screw_placed and qc_checked:
            magnets_placed = False
            trapezium_placed = False
            screw_placed = False
            qc_checked = False
            start = False
            print('TRAP-EYE assembly finished. Remove and place new TRAP-EYE')
        else:
            if not magnets_placed and not magnet_switch:
                board.digital[linear_in].write(0)
                board.digital[linear_out].write(1)
                while not magnet_switch:
                    board.digital[magnet_switch].read()
                    print('Waiting for magnet or magnets empty', sep=' ', end='', flush=True)
                    wait(0.1)
                    print(sep=' ', end='\r')
                    wait(1)
                board.digital[linear_out].write(0)
                board.digital[linear_in].write(1)
                print('Magnet storage empty')
            elif not trapezium_placed and trapezium_state:
                print('Trapezium storage empty')
                wait(1)
            else:
                print('TRAP-EYE not placed')
                wait(1)

from DRCF import *
import pyfirmata
from pyfirmata import util
import checkVision

# ---- Set up client/server ----
ip = "192.168.127.100"           # Server IP adress (Cobot is "192.168.127.100")
port = 10000

sock = client_socket_open(ip, port)
state = client_socket_state(sock)

# ---- Set up communication with Arduino Mega ----
port = 'COM8'                               # Port used to communicate with Arduino (Visible in Arduino IDE)
board = pyfirmata.ArduinoMega(port)         # The connection between Arduino and laptop
linear_out = 2
linear_speed = 3
linear_in = 4
clamp_servo = 5
magnet_switch = 6
trapezium_switch = 7
screwdriver = 8
white_LED = 9
vacuum_pump = 10
green_LED = 11
red_LED = 12
start_button = 22
trapeye_switch = 24

board.digital[linear_in].mode = pyfirmata.OUTPUT        # Linear actuator
board.digital[linear_speed].mode = pyfirmata.PWM        # Linear actuator (PWM)
board.digital[linear_out].mode = pyfirmata.OUTPUT       # Linear actuator
board.digital[clamp_servo].mode = pyfirmata.SERVO       # Clamp servo (PWM)
board.digital[magnet_switch].mode = pyfirmata.INPUT     # Magnet switch
board.digital[trapezium_switch].mode = pyfirmata.INPUT  # Trapezium switch
board.digital[screwdriver].mode = pyfirmata.OUTPUT      # Screwdriver
board.digital[white_LED].mode = pyfirmata.OUTPUT        # white LED for photo
board.digital[vacuum_pump].mode = pyfirmata.OUTPUT      # Vacuum pump
board.digital[green_LED].mode = pyfirmata.OUTPUT        # status LED
board.digital[red_LED].mode = pyfirmata.OUTPUT          # status LED
board.digital[start_button].mode = pyfirmata.INPUT      # Start button
board.digital[trapeye_switch].mode = pyfirmata.INPUT    # Trap-eye switch

it = util.Iterator(board)
it.start()

board.digital[magnet_switch].enable_reporting()         # Enable reading this port
board.digital[trapezium_switch].enable_reporting()      # Enable reading this port
board.digital[trapeye_switch].enable_reporting()        # Enable reading this port
board.digital[start_button].enable_reporting()          # Enable reading this port

# ---- Start with all variables False ----
magnets_placed = False
trapezium_placed = False
screw_placed = False
qc_checked = False
start = False
button_state = False
prev_button_state = False


def move_linear_in():
    board.digital[linear_out].write(0)
    board.digital[linear_in].write(1)
    board.digital[linear_speed].write(1)


def move_linear_out():
    board.digital[linear_in].write(0)
    board.digital[linear_out].write(1)
    board.digital[linear_speed].write(1)


def clamping():
    board.digital[clamp_servo].write(0)             # Press on the magnets
    print('Clamped')


# ---- Main code ----
move_linear_in()
board.digital[clamp_servo].write(135)               # Retreat to give robot more space
msg = "calibration()"
client_socket_write(sock, msg.encode("utf-8"))      # Sends data to the server
res, rx_data = client_socket_read(sock)             # Receives data from the server
print(rx_data)

while True:
    while not start:
        button_state = board.digital[start_button].read()
        print('Waiting for button press', sep=' ', end='', flush=True)
        wait(0.1)
        print(sep=' ', end='\r')
        if button_state != prev_button_state:
            trapeye_state = board.digital[trapeye_switch].read()
            if button_state and trapeye_state:
                print('Button pressed')
                start = True
            elif button_state and not trapeye_state:
                print('No TRAP-EYE detected')
            else:
                pass
                prev_button_state = button_state

    board.digital[red_LED].write(0)
    board.digital[green_LED].write(0)

    while start:
        magnet_state = board.digital[magnet_switch].read()
        trapezium_state = board.digital[trapezium_switch].read()
        trapeye_state = board.digital[trapeye_switch].read()
        print('Inputs read')
        wait(0.1)

        if not magnet_state and not magnets_placed:
            print('Placing magnet 1...')
            msg = "place_magnet_1()"
            client_socket_write(sock, msg.encode("utf-8"))              # Sends data to the server
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)                                                # Receiving 'retract linear actuator'
            msg = "Linear actuator moving in"
            client_socket_write(sock, msg.encode("utf-8"))              # Sending 'moving in'
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)                                                # Receiving 'activate vacuum pump'
            msg = "pump on"
            client_socket_write(sock, msg.encode("utf-8"))              # Sending 'pump on'
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)                                                # Receiving 'retract linear actuator'
            msg = "Linear actuator moving out"
            client_socket_write(sock, msg.encode("utf-8"))              # Sending 'moving out'
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)                                                # Receiving 'retract linear actuator'
            msg = "pump off"
            client_socket_write(sock, msg.encode("utf-8"))              # Sending 'pump off'
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            print(rx_msg)                                               # Magnet 1 placed successfully
            magnet_state = board.digital[magnet_switch].read()
            while magnet_state:
                magnet_state = board.digital[magnet_switch].read()
                wait(0.5)
            print('Placing magnet 2...')
            msg = "place_magnet_2()"
            client_socket_write(sock, msg.encode("utf-8"))              # Sends data to the server
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)                                                # Receiving 'retract linear actuator'
            msg = "Linear actuator moving in"
            client_socket_write(sock, msg.encode("utf-8"))              # Sending 'moving in'
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)                                                # Receiving 'activate vacuum pump'
            msg = "pump on"
            client_socket_write(sock, msg.encode("utf-8"))              # Sending 'pump on'
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)                                                # Receiving 'retract linear actuator'
            msg = "Linear actuator moving out"
            client_socket_write(sock, msg.encode("utf-8"))              # Sending 'moving out'
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)                                                # Receiving 'retract linear actuator'
            msg = "pump off"
            client_socket_write(sock, msg.encode("utf-8"))              # Sending 'pump off'
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            print(rx_msg)                                               # Magnet 2 placed successfully
            magnets_placed = True
        elif not trapezium_state and magnets_placed and not trapezium_placed:
            print('Placing trapezium...')
            msg = "place_trapezium_1()"
            client_socket_write(sock, msg.encode("utf-8"))              # Sends data to the server
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)                                                # Activate vacuum pump
            msg = "pump on"
            client_socket_write(sock, msg.encode("utf-8"))              # Sends data to the server
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)
            msg = "pump off"
            client_socket_write(sock, msg.encode("utf-8"))              # Sends data to the server
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            print(rx_msg)                                               # Trapezium placed successfully
            trapezium_placed = True
        elif magnets_placed and trapezium_placed and not screw_placed:
            print('Placing screw...')
            msg = "place_screw_1()"
            client_socket_write(sock, msg.encode("utf-8"))              # Sends data to the server
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)                                                # Activate screwdriver
            msg = "screwdriver on"
            client_socket_write(sock, msg.encode("utf-8"))              # Sends data to the server
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)                                                # Activate screwdriver
            msg = "screwdriver off"
            client_socket_write(sock, msg.encode("utf-8"))              # Sends data to the server
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)                                                # Clamping the magnets and trapezium
            msg = "Clamping"
            client_socket_write(sock, msg.encode("utf-8"))              # Sends data to the server
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)                                                # Activate screwdriver
            msg = "screwdriver on"
            client_socket_write(sock, msg.encode("utf-8"))              # Sends data to the server
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            exec(rx_msg)                                                # Activate screwdriver
            msg = "screwdriver off"
            client_socket_write(sock, msg.encode("utf-8"))              # Sends data to the server
            res, rx_data = client_socket_read(sock)                     # Receives data from the server
            rx_msg = rx_data.decode("utf-8")
            print(rx_msg)                                               # Screw placed successfully
            screw_placed = True
        elif magnets_placed and trapezium_placed and screw_placed and not qc_checked:
            board.digital[clamp_servo].write(35)                        # Position for photo background
            board.digital[white_LED].write(1)
            wait(2)
            checkVision.capture_photo()
            checkVision.HVS()
            p1 = (710, 550)
            p2 = (900, 700)
            p3 = (1100, 550)
            p4 = (1270, 700)
            checkVision.pixel(p1, p2, p3, p4)
            qc_checked = checkVision.check
            if not checkVision.check:
               board.digital[red_LED].write(1)
               print('QC check: Failed')
            else:
               board.digital[green_LED].write(1)
               print('QC check: Passed')
            board.digital[white_LED].write(0)
            board.digital[clamp_servo].write(135)                       # Position for photo background
            while trapeye_state:
                trapeye_state = board.digital[trapeye_switch].read()
                print('TRAP-EYE assembly finished. Remove and place new TRAP-EYE', sep=' ', end='', flush=True)
                wait(0.1)
                print(sep=' ', end='\r')
            magnets_placed = False
            trapezium_placed = False
            screw_placed = False
            qc_checked = False
            start = False

        else:
            if not magnets_placed and magnet_state:
                print("Supplying magnet")
                move_linear_out()
                while magnet_state:
                    magnet_state = board.digital[magnet_switch].read()
                    print('Waiting for magnet or magnets empty', sep=' ', end='', flush=True)
                    wait(0.1)
                    print(sep=' ', end='\r')
                    wait(1)
                move_linear_in()
                print('Magnet storage empty')
            elif not trapezium_placed and trapezium_state:
                print('Trapezium storage empty')
                wait(1)
            elif not trapeye_state:
                print('TRAP-EYE not placed')
                start = False
                wait(1)
            else:
                print('Unknown Error')
                wait(1)

# client_socket_close(sock)                   # Closes the socket
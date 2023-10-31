from DRCF import *

port = 10000

sock = server_socket_open(port)
state = server_socket_state(sock)

# ---- Coordinates for pick and place magnets ----
approach_magnet_1 = posx(349, -303, 400, 0, 180, 90)            # Above magnet storage
approach_magnet_2 = posx(-13, -559, 400, 0, -150, 0)            # Above magnet place 1 angled
approach_magnet_3 = posx(-14, -646, 400, 0, -150, 0)            # Above magnet place 2 angled
approach_magnet_4 = posx(349, -137, 400, 0, 180, 90)            # Move away at an angle
pick_magnet = posx(349, -303, 116, 0, 180, 90)                  # Pick up position
place_position_1a = posx(-13, -559.5, 351, 0, -150, 0)          # Place position 1st magnet
place_position_1b = posx(-13, -558.5, 351, 0, -150, 0)          # Place position 1st magnet
place_position_2a = posx(-14.5, -645, 352, 0, -150, 0)          # Place position 2nd magnet
place_position_2b = posx(-14.5, -646, 352, 0, -150, 0)          # Place position 2nd magnet

# ---- Coordinates for pick and place trapezium ----
approach_trapezium_1 = posx(247, -338, 400, 0, 180, 90)             # Above trapezium storage
approach_trapezium_2 = posx(-5.5, -603.5, 400, 0, -150, 0)          # Above trapezium place
pick_trapezium = posx(247, -338, 152.5, 0, 180, 90)                 # Pick up position
place_trapezium = posx(-5.5, -603.5, 351, 0, -150, 0)               # Place position trapezium

# ---- Coordinates for pick and place screw ----
global screw
screw = 239.5                                                               # Always start with picking screw 1
approach_screw_1 = posj(104.04, -7.73, -95.47, 180.0, 76.80, 14.04)         # Start position
approach_screw_2 = posj(86.14, -13.48, -110.15, 267.86, 93.21, -213.69)     # Rotated tool
approach_screw_4 = posx(-230, -400, 244, 0, 180, 90)                        # Move around TRAP-EYE
approach_screw_5 = posx(-230, -688, 244, 0, 180, 90)                  # Move around TRAP-EYE
approach_screw_6 = posx(-190, -688, 244, 0, 180, 90)                  # Line up with screw hole
place_screw = posx(-175, -688, 244, 0, 180, 90)                       # Place position trapezium

# ---- Speed and acceleration parameter ----
v = 600
a = 300

# ---- timers for stuff ----
suck_time = 2       # Number of seconds to wait after (de)activating the vacuum pump
screw_time = 1      # Number of seconds to wait after (de)activating the screwdriver


def place_magnet_1():
    msg = "move_linear_in()"                                # Retract linear actuator
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    movel(approach_magnet_1, v=v, a=a)
    movel(pick_magnet, v=v, a=a)
    msg = "board.digital[vacuum_pump].write(1)"             # Activate suction cup
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    wait(suck_time)
    movel(approach_magnet_4, v=v, a=a)
    movel(approach_magnet_2, v=v, a=a)
    msg = "move_linear_out()"                               # Extend linear actuator
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    movel(place_position_1a, v=100, a=50)
    movel(place_position_1b, v=100, a=50)
    msg = "board.digital[vacuum_pump].write(0)"             # Deactivate suction cup
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    wait(3)
    movel(approach_magnet_2, v=v, a=a)


def place_magnet_2():
    msg = "move_linear_in()"                                # Retract linear actuator
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    movel(approach_magnet_1, v=v, a=a)
    movel(pick_magnet, v=v, a=a)
    msg = "board.digital[vacuum_pump].write(1)"             # Activate suction cup
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    wait(suck_time)
    movel(approach_magnet_4, v=v, a=a)
    movel(approach_magnet_3, v=v, a=a)
    msg = "move_linear_out()"                               # Extend linear actuator
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    movel(place_position_2a, v=100, a=50)
    movel(place_position_2b, v=100, a=50)
    msg = "board.digital[vacuum_pump].write(0)"             # Deactivate suction cup
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    wait(suck_time)
    movel(approach_magnet_3, v=v, a=a)


def place_trapezium_1():
    movel(approach_trapezium_1, v=v, a=a)
    movel(pick_trapezium, v=v, a=a)
    msg = "board.digital[vacuum_pump].write(1)"             # Activate suction cup
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    wait(suck_time)
    movel(approach_trapezium_1, v=v, a=a)
    movel(approach_trapezium_2, v=v, a=a)
    movel(place_trapezium, v=100, a=50)
    msg = "board.digital[vacuum_pump].write(0)"             # Deactivate suction cup
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    wait(suck_time)
    movel(approach_trapezium_2, v=v, a=a)


def place_screw_1():
    movej(approach_screw_1, v=v, a=a)
    movej(approach_screw_2, v=v, a=a)
    movel(approach_screw_3, v=v, a=a)
    movel(pick_screw_1, v=v, a=a)
    msg = "board.digital[screwdriver].write(1)"             # Activate screwdriver
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    movel(pick_screw_2, v=5, a=a)
    msg = "board.digital[screwdriver].write(0)"             # Deactivate screwdriver
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    movel(approach_screw_3, v=v, a=a)
    movej(approach_screw_1, v=v, a=a)                  # Fixed speed to not lose screw
    movel(approach_screw_4, v=v, a=a)
    movel(approach_screw_5, v=v, a=a)
    msg = "clamping()"
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    movel(approach_screw_6, v=v, a=a)
    msg = "board.digital[screwdriver].write(1)"             # Activate screwdriver
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    movel(place_screw, v=7.5, a=a)
    wait(screw_time)                                        # Make sure the screw is tight with slip clutch
    msg = "board.digital[screwdriver].write(0)"             # Deactivate screwdriver
    server_socket_write(sock, msg.encode("utf-8"))
    res, rx_data = server_socket_read(sock)                 # Expecting 'received message'
    rx_msg = rx_data.decode("utf-8")
    print(rx_msg)
    movel(approach_screw_5, v=v, a=a)
    movel(approach_screw_4, v=v, a=a)
    movej(approach_screw_1, v=200, a=100)


def calibration():
    pass
    # movej(posj(0.0, 0.0, 0.0, 0.0, 0.0, 0.0), v=v, a=a)               # Home position needed for accuracy calibration
    # movej(posj(139.4, -13.7, -88.2, 180.0, 78.1, 49.4), v=v, a=a)     # First position after calibration


# ---- Main code ----
while True:
    # ---- Inside loop to update screw variable ----
    approach_screw_3 = posx(screw, -266.5, 350, 180, -90, 90)       # Above screw feeder
    pick_screw_1 = posx(screw, -266.5, 225, 180, -90, 90)           # Pick up position
    pick_screw_2 = posx(screw, -266.5, 220, 180, -90, 90)           # Pick up position
    # ----------------------------------------------
    res, rx_data = server_socket_read(sock)     # Receives data from the server
    command = rx_data.decode("utf-8")
    if command == "place_magnet_1()":
        exec(command)
        wait(0.1)
        msg = "Magnet 1 placed successfully"
        server_socket_write(sock, msg.encode("utf-8"))
    elif command == "place_magnet_2()":
        exec(command)
        wait(0.1)
        msg = "Magnet 2 placed successfully"
        server_socket_write(sock, msg.encode("utf-8"))
    elif command == "place_trapezium_1()":
        exec(command)
        wait(0.1)
        msg = "Trapezium placed successfully"
        server_socket_write(sock, msg.encode("utf-8"))
    elif command == "place_screw_1()":
        exec(command)
        wait(0.1)
        screw += 10
        if screw == 309.5:
            screw = 239.5
        msg = "Screw placed successfully"
        server_socket_write(sock, msg.encode("utf-8"))
    elif command == "calibration()":
        exec(command)
        wait(0.1)
        msg = "Calibration successful"
        server_socket_write(sock, msg.encode("utf-8"))
    wait(0.1)
    # server_socket_close(sock)                   # Closes the socket
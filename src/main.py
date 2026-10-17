# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       AustinC                                                      #
# 	Created:      14/05/2026, 15:03:53                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #
#Aviel Code Changing On Aviel branch Test
# Library imports
from vex import *

brain = Brain()
controller = Controller()

# The drivetrain uses one motor on each side.
left_rear = Motor(Ports.PORT3)
right_rear = Motor(Ports.PORT4)

claw_roll_motor = Motor(Ports.PORT11)
claw_pitch_motor = Motor(Ports.PORT12)
claw_solenoid = DigitalOut(brain.three_wire_port.a)

lift_motor_left = Motor(Ports.PORT20)
# right motor is reverse due to the motors facing opposite directions on the lift
lift_motor_right = Motor(Ports.PORT19)

def close_claw():
    claw_solenoid.set(True)

def open_claw():
    claw_solenoid.set(False)



def move_forward(speed, degrees):
    left_rear.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT, wait=False)
    right_rear.spin_for(REVERSE, degrees, DEGREES, speed, PERCENT)


def move_backward(speed, degrees):
    left_rear.spin_for(REVERSE, degrees, DEGREES, speed, PERCENT, wait=False)
    right_rear.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT)

def turn_left(speed, degrees):
    left_rear.spin_for(REVERSE, degrees, DEGREES, speed, PERCENT, wait=False)
    right_rear.spin_for(REVERSE, degrees, DEGREES, speed, PERCENT)

def turn_right(speed, degrees):
    left_rear.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT, wait=False)
    right_rear.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT)

def lift_up(speed, degrees):
    lift_motor_left.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT, wait=False)
    lift_motor_right.spin_for(REVERSE, degrees, DEGREES, speed, PERCENT)

def lift_down(speed, degrees):
    lift_motor_left.spin_for(REVERSE, degrees, DEGREES, speed, PERCENT)
    lift_motor_right.spin_for(FORWARD, degrees, DEGREES, speed, PERCENT)







def control_claw_pitch(pitch_joystick_active):
    claw_pitch_speed = controller.axis2.position()
    print(lift_motor_left.position(DEGREES))
    if abs(claw_pitch_speed) <= 20:
        # Inside deadzone, stop motor
        claw_pitch_speed = 0
    else:
        # Outside deadzone. Enable joystick
        pitch_joystick_active = True

    if pitch_joystick_active:
        # Joystick is enabled, set motor speed based on joystick position
        if claw_pitch_speed == 0:
            claw_pitch_motor.stop(HOLD)
        elif controller.buttonY.pressed:
            claw_pitch_motor.spin(FORWARD, claw_pitch_speed * 1, PERCENT)

        else:
            claw_pitch_motor.spin(FORWARD, claw_pitch_speed * 0.35, PERCENT)

    return pitch_joystick_active

def control_claw_roll(roll_joystick_active):
    claw_roll_speed = controller.axis1.position()
    if abs(claw_roll_speed) <= 20:
        # Inside deadzone, stop motor
        claw_roll_speed = 0
    else:
        # Outside deadzone. Enable joystick
        roll_joystick_active = True

    if roll_joystick_active:
        # Joystick is enabled, set motor speed based on joystick position
        if claw_roll_speed == 0:
            claw_roll_motor.stop(HOLD)
        else:
            if claw_roll_motor.position(DEGREES) < -180 and claw_roll_speed < 0:
                claw_roll_motor.stop(HOLD)
            elif claw_roll_motor.position(DEGREES) > 180 and claw_roll_speed > 0:
                claw_roll_motor.stop(HOLD)
            else:
                claw_roll_motor.spin(FORWARD, claw_roll_speed / 5, PERCENT)

    if controller.buttonX.pressing():
        # Disable joystick until outside of deadzone
        roll_joystick_active = False
        claw_roll_motor.set_velocity(50, PERCENT)
        claw_roll_motor.spin_to_position(0, DEGREES, wait=False)
    if controller.buttonLeft.pressing():
            roll_joystick_active = False
            claw_roll_motor.set_velocity(50, PERCENT)
            claw_roll_motor.spin_to_position(-90, DEGREES, wait=False)
    if controller.buttonRight.pressing():
            roll_joystick_active = False
            claw_roll_motor.set_velocity(50, PERCENT)
            claw_roll_motor.spin_to_position(90, DEGREES, wait=False)

    

    return roll_joystick_active


def move_lift_and_pitch_to_position(pitch_joystick_active):

    if controller.buttonUp.pressing():
        # Disable joystick until outside of deadzone
        pitch_joystick_active = False
        lift_motor_left.set_velocity(100, PERCENT)
        lift_motor_left.spin_to_position(40, DEGREES, wait=False)
        lift_motor_right.spin_to_position(40, DEGREES, wait=False)
        claw_pitch_motor.spin_to_position(360, DEGREES, wait=False)

    if controller.buttonDown.pressing():
        # Disable joystick until outside of deadzone
        pitch_joystick_active = False
        lift_motor_left.set_velocity(75, PERCENT)
        lift_motor_left.spin_to_position(534, DEGREES, wait=False)
        lift_motor_right.spin_to_position(534, DEGREES, wait=False)
        claw_pitch_motor.spin_to_position(720, DEGREES, wait=False)

    return pitch_joystick_active
def move_claw_roll(claw_roll_position, claw_roll_speed):
    claw_roll_motor.set_velocity(claw_roll_speed, VelocityUnits.DPS)
    claw_roll_motor.spin_to_position(claw_roll_position, DEGREES, wait=False)
    

def drive_code():
    forward_speed = controller.axis3.position()
    turn_speed = controller.axis4.position()

    print(controller.axis3.position())

    left_speed = forward_speed + turn_speed
    right_speed = forward_speed - turn_speed

    maximum_speed = max(abs(left_speed), abs(right_speed), 100)
    left_speed = left_speed / maximum_speed * 100
    right_speed = right_speed / maximum_speed * 100

    if abs(left_speed) <= 5:
        left_speed = 0
    if abs(right_speed) <= 5:
        right_speed = 0

    if lift_motor_left.position(DEGREES) > 500:
        crawl_multiplier = 0.20
    elif controller.buttonB.pressing():
        crawl_multiplier = 0.30
    else:
        crawl_multiplier = 1.0

    left_speed *= crawl_multiplier
    right_speed *= crawl_multiplier

    if left_speed == 0:
        left_rear.stop(BRAKE)
    elif left_speed > 0:
        left_rear.spin(FORWARD, left_speed, PERCENT)
    else:
        left_rear.spin(REVERSE, -left_speed, PERCENT)

    if right_speed == 0:
        right_rear.stop(BRAKE)
    elif right_speed > 0:
        right_rear.spin(REVERSE, right_speed, PERCENT)
    else:
        right_rear.spin(FORWARD, -right_speed, PERCENT)

# This function is used durng the autonomous period.
# The lift and drivetrain can be programmed here later.
def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here
    close_claw()
    move_forward(20, 250)
    lift_up(50, 700)
    claw_pitch_motor.spin_to_position(360, DEGREES, wait=True)
    open_claw()
    
# This function is used while the driver controls the robot.
def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    close_claw()

    claw_roll_position = 0
    claw_roll_speed = 180

    pitch_joystick_active = True
    roll_joystick_active = True
    brain.timer.reset()
    last_update_time = brain.timer.time(SECONDS)
    while True:
        this_update_time = brain.timer.time(SECONDS)
        delta_time = this_update_time - last_update_time
        last_update_time = this_update_time

        drive_code()
        if controller.buttonR2.pressing():
            lift_motor_left.spin(FORWARD, 80, PERCENT, wait=False)
            lift_motor_right.spin(REVERSE, 80, PERCENT)
        elif controller.buttonL2.pressing():
            lift_motor_left.spin(REVERSE, 80, PERCENT, wait=False)
            lift_motor_right.spin(FORWARD, 80, PERCENT)
        else:
            lift_motor_left.stop(HOLD)
            lift_motor_right.stop(HOLD)

        pitch_joystick_active = control_claw_pitch(pitch_joystick_active)
        roll_joystick_active = control_claw_roll(roll_joystick_active)

        pitch_joystick_active = move_lift_and_pitch_to_position(pitch_joystick_active)

        if controller.buttonL1.pressing():
            close_claw()

        if controller.buttonR1.pressing():
            open_claw()

        wait(100, MSEC)

# Create the VEX competition instance so the system can call the correct mode.
comp = Competition(user_control, autonomous)

# Clear the screen when the program starts.
brain.screen.clear_screen()

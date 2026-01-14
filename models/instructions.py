from enum import Enum

from models.robot import Robot, positions
from models.field import Field, fieldState

# instructions are functions
# def instruction(field: Field, robot: Robot):

def redCycle(field: Field, robot: Robot):
    while True:
        if field.state == fieldState.RED_ACTIVE or field.state == fieldState.TRANS or field.state == fieldState.AUTO: # if red is active or all is active
            if field.redFuel == 0:
                while robot.fuel > 0:
                    robot.shoot(field)
                while robot.position != positions.NEUTRAL:
                    robot.moveTo(field, positions.NEUTRAL) # go to neutral
                while robot.fuel < robot.capacity:
                    robot.intake(field) # intake in neutral
                while robot.position != positions.RED:
                    robot.moveTo(field, positions.RED) # go to red
            else:
                robot.moveTo(field, positions.RED)
                while robot.fuel > 0:
                    robot.shoot(field)
                while field.redFuel > 0:
                    robot.intake(field)
                    robot.shoot(field) # while there is balls in the blue field, and blue is active, shoot them

        elif field.state == fieldState.BLUE_ACTIVE: # SHUTTLING
            robot.moveTo(field, positions.NEUTRAL)
            robot.intake(field)
            robot.shuttle(field, positions.RED)
def blueCycle(field: Field, robot: Robot):
    while True:
        if field.state == fieldState.BLUE_ACTIVE or field.state == fieldState.TRANS or field.state == fieldState.AUTO or field.state == fieldState.END: # if red is active or all is active
            if field.blueFuel == 0:
                while robot.fuel > 0:
                    robot.shoot(field)
                while robot.position != positions.NEUTRAL:
                    robot.moveTo(field, positions.NEUTRAL) # go to neutral
                while robot.fuel < robot.capacity:
                    robot.intake(field) # intake in neutral
                while robot.position != positions.BLUE:
                    robot.moveTo(field, positions.BLUE) # go to blue
            else:
                robot.moveTo(field, positions.BLUE)
                while robot.fuel > 0:
                    robot.shoot(field)
                while field.redFuel > 0:
                    robot.intake(field)
                    robot.shoot(field) # while there is balls in the blue field, and blue is active, shoot them

        elif field.state == fieldState.RED_ACTIVE: # SHUTTLING
            robot.moveTo(field, positions.NEUTRAL)
            robot.intake(field)
            robot.shuttle(field, positions.BLUE)

def shuttleRed(field: Field, robot: Robot):
    while True:
        robot.moveTo(field, positions.NEUTRAL)
        robot.intake(field)
        robot.shuttle(field, positions.RED)

def shuttleBlue(field: Field, robot: Robot):
    while True:
        robot.moveTo(field, positions.NEUTRAL)
        robot.intake(field)
        robot.shuttle(field, positions.BLUE)

def shootBlue(field: Field, robot: Robot):
    while True:
        robot.moveTo(field, positions.BLUE)
        if field.state != fieldState.RED_ACTIVE:
            robot.intake(field)
            robot.shoot(field)

def shootRed(field: Field, robot: Robot):
    while True:
        robot.moveTo(field, positions.RED)
        if field.state != fieldState.BLUE_ACTIVE:
            robot.intake(field)
            robot.shoot(field)

def test(field: Field, robot: Robot):
    while True:
        robot.moveTo(field, positions.NEUTRAL)
        robot.moveTo(field, positions.RED)

def debug(field: Field, robot: Robot):
    while True:
        print("field state: " + str(field.state) + "\n red score: " + str(field.redScore) + "\n blue score: " + str(field.blueScore) + "\n - BALLS IN THE NEUTRAL ZONE - " + str(field.neutralFuel))
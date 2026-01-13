from enum import Enum

from models.robot import Robot, positions
from models.field import Field, fieldState

# instructions are functions
# def instruction(field: Field, robot: Robot):

def redCycle(field: Field, robot: Robot):
    while True:
        if field.state in [fieldState.RED_ACTIVE, fieldState.TRANS, fieldState.AUTO, fieldState.END]:
            while robot.fuel > 0:
                robot.shoot(field)
            while robot.position != positions.NEUTRAL:
                robot.moveTo(field, positions.NEUTRAL)
            while robot.fuel < robot.capacity:
                robot.intake(field)
            while robot.position != positions.RED:
                robot.moveTo(field, positions.RED)
        elif field.state == fieldState.BLUE_ACTIVE:
            while robot.fuel < robot.capacity:
                while robot.position != positions.NEUTRAL:
                    robot.moveTo(field, positions.NEUTRAL)
                while robot.fuel < robot.capacity:
                    robot.intake(field)
                while robot.position != positions.RED:
                    robot.moveTo(field, positions.RED)

def blueCycle(field: Field, robot: Robot):
    while True:
        if field.state == fieldState.BLUE_ACTIVE or field.state == fieldState.TRANS: # LGBTQ field
            while robot.fuel > 0:
                robot.shoot(field)
            while robot.position != positions.NEUTRAL:
                robot.moveTo(field, positions.NEUTRAL)
            while robot.fuel < robot.capacity:
                robot.intake(field)
            while robot.position != positions.BLUE:
                robot.moveTo(field, positions.BLUE)
        elif field.state == fieldState.RED_ACTIVE:
            while robot.fuel < robot.capacity:
                while robot.position != positions.NEUTRAL:
                    robot.moveTo(field, positions.NEUTRAL)
                while robot.fuel < robot.capacity:
                    robot.intake(field)
                while robot.position != positions.BLUE:
                    robot.moveTo(field, positions.BLUE)



def debug(field: Field, robot: Robot):
    while True:
        print("field state: " + str(field.state) + "\n red score: " + str(field.redScore) + "\n blue score: " + str(field.blueScore) + "\n - BALLS IN THE NEUTRAL ZONE - " + str(field.neutralFuel))
from enum import Enum

from models.robot import Robot, positions
from models.field import Field, fieldState

# instructions are functions
# def instruction(field: Field, robot: Robot):

def testInstruction(field: Field, robot: Robot, timestamp):
    if field.state == fieldState.BLUE_ACTIVE:
        robot.moveTo(positions.NEUTRAL, timestamp)
        robot.intake(field, timestamp)
    if field.state == fieldState.RED_ACTIVE:
        robot.moveTo(positions.RED, timestamp)
        robot.shoot(field, timestamp)
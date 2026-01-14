from enum import Enum
from models.robot import action, Instruction
from models.field import Field, fieldState

redCycle = Instruction('redCycle')
redCycle.activeHub([
    action.MOVE_HOME,
    action.INTAKE,
    action.SCORE
])
redCycle.inactiveHub([
    action.MOVE_NEUTRAL,
    action.PASS
])
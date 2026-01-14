from enum import Enum
from models.robot import action, Instruction
from models.field import Field, fieldState

cycle = Instruction() # go to neutral, intake, go home, score, and shuttle while inactive
cycle.activeHub([
    action.MOVE_NEUTRAL,
    action.INTAKE,
    action.MOVE_HOME,
    action.SCORE
])
cycle.inactiveHub([
    action.MOVE_NEUTRAL,
    action.PASS # shuttling to deprive other team
])

shuttle = Instruction() # bots eat balls like a fatty and put it in their zone
shuttle.activeHub([
    action.MOVE_NEUTRAL,
    action.PASS # shuttling to deprive other team
])
shuttle.inactiveHub([
    action.MOVE_NEUTRAL,
    action.PASS # shuttling to deprive other team
])

shoot = Instruction() # bots will always shoot during active
shoot.activeHub([
    action.MOVE_NEUTRAL,
    action.SCORE,
])
shoot.inactiveHub([
    action.MOVE_NEUTRAL,
    action.PASS # shuttling to deprive other team
])

test = Instruction()
test.activeHub([
    action.MOVE_NEUTRAL,
    action.PASS
])
test.inactiveHub([
    action.MOVE_NEUTRAL,
    action.PASS
])
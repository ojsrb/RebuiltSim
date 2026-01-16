from enum import Enum
from models.robot import action, Instruction
from models.field import Field, fieldState

# cycle between alliance area and neutral zone while hub actve, shuttle fuel into alliance zone when hub inactive.
cycle = Instruction() # go to neutral, intake, go home, score, and shuttle while inactive
cycle.activeHub([
    action.MOVE_HOME,
    action.INTAKE,
    action.SCORE,
    action.MOVE_NEUTRAL,
    action.INTAKE,
    action.MOVE_HOME,
    action.SCORE
])
cycle.inactiveHub([
    action.MOVE_NEUTRAL,
    action.PASS
])

# camp in neutral zone and send fuel to alliance area
shuttle = Instruction()
shuttle.activeHub([
    action.MOVE_NEUTRAL,
    action.PASS
])
shuttle.inactiveHub([
    action.MOVE_NEUTRAL,
    action.PASS
])

# camp in alliance zone and score fuel delivered by shuttlers when hub active, shuttle from neutral to alliance zone when inactive.
shoot = Instruction()
shoot.activeHub([
    action.MOVE_HOME,
    action.INTAKE,
    action.SCORE,
])
shoot.inactiveHub([
    action.MOVE_NEUTRAL,
    action.PASS
])

# test strategy, will show evidence of strategy working on graph. Probably won't win
test = Instruction()
test.activeHub([
    action.MOVE_NEUTRAL,
    action.PASS
])
test.inactiveHub([
    action.MOVE_NEUTRAL,
    action.PASS
])
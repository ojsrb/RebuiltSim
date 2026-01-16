from models.field import Field, fieldState
import time
from models.robot import Robot, alliance
from models.instructions import *
import models.display as display

# initialize field (contains match variables and field stats)
field = Field(0,0, 400, 0, 0)

# current frame
frame = 0

# Robot params:
# field: Field, color: alliance, shootSpeed: int (fuel/s), intakeSpeed: int (fuel/s), drive speed: int (inches/s), preload: bool, strategy: Instruction

# strategies are imported from instructions.py [cycle, shoot, shuttle]

# RED ALLIANCE (0-2)
robot0 = Robot(field, alliance.RED, 3, 3, 144, 8, True, cycle)
robot1 = Robot(field, alliance.RED, 3, 3, 144, 8, True, cycle)
robot2 = Robot(field, alliance.RED, 3, 3, 144, 8, True, cycle)

# BLUE ALLIANCE (3-5)
robot3 = Robot(field, alliance.BLUE, 3, 3, 144, 8, True, cycle)
robot4 = Robot(field, alliance.BLUE, 3, 3, 144, 8, True, cycle)
robot5 = Robot(field, alliance.BLUE, 3, 3, 144, 8, True, cycle)

print("beginning simulation.")

while True:
    start_time = time.time()
    field.update(frame)
    robot3.tick()
    robot4.tick()
    robot5.tick()
    robot0.tick()
    robot1.tick()
    robot2.tick()

    # increment frame number
    frame += 1

    # update graph
    display.update(field)

    # end sim if the field has ended the match
    if field.state == fieldState.OVER:
        break

display.displayGraph(field)

print("finished simulating.")
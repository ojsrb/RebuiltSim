from models.field import Field, fieldState
import time
from models.robot import Robot, alliance
from models.instructions import *
import models.display as display

field = Field(0,0, 400, 0, 0)

frame = 0

# RED ALLIANCE
robot0 = Robot(field, alliance.RED, 8, 8, 240, 45, True, cycle)
robot1 = Robot(field, alliance.RED, 8, 8, 240, 45, True, shuttle)
robot2 = Robot(field, alliance.RED, 8, 8, 240, 45, True, shoot)

# self, redFuel : int, blueFuel : int,neutralFuel : int,redScore : int,blueScore : int
# BLUE ALLIANCE
robot3 = Robot(field, alliance.BLUE, 8, 8, 240, 45, True, cycle)
robot4 = Robot(field, alliance.BLUE, 8, 8, 240, 45, True, cycle)
robot5 = Robot(field, alliance.BLUE, 8, 8, 240, 45, True, cycle)

elapsed_time = 1

while True:
    start_time = time.time()
    field.update(frame)
    robot3.tick()
    robot4.tick()
    robot5.tick()
    robot0.tick()
    robot1.tick()
    robot2.tick()
    # display.drawRobot(robot0)
    # display.drawRobot(robot1)
    # display.drawRobot(robot2)
    # display.drawRobot(robot3)
    # display.drawRobot(robot4)
    # display.drawRobot(robot5)

    print(
        f"{round(1/elapsed_time)}fps | "
        f"field state: {field.state} | "
        f"red: {field.redScore} | "
        f"blue: {field.blueScore} | "
        f"neutral: {field.neutralFuel} | "
        f"blue field fuel: {field.blueFuel} | "
        f"red field fuel: {field.redFuel} | ",
        flush=True,
    )
    frame += 1
    display.update(field)
    end_time = time.time()
    elapsed_time = end_time - start_time
    if field.state == fieldState.OVER:
        break

display.displayGraph(field)
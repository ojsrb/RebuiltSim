from models import display
from models.field import Field, fieldState
import time
from models.robot import Robot
from models.instructions import *
# import models.display as display

field = Field(0,0, 400, 0, 0)

frame = 0

robot0 = Robot(field, 0, 8, 8, 240, 45, True, redCycle)
# robot1 = Robot(field, 1, 8, 8, 240, 45, True, instructions.shuttleRed)
# robot2 = Robot(field, 2, 8, 8, 240, 45, True, instructions.shootRed)
#
# # self, redFuel : int, blueFuel : int,neutralFuel : int,redScore : int,blueScore : int
# # BLUE ALLIANCE
# robot3 = Robot(field, 3, 8, 8, 240, 45, True, instructions.blueCycle)
# robot4 = Robot(field, 4, 8, 8, 240, 45, True, instructions.blueCycle)
# robot5 = Robot(field, 5, 8, 8, 240, 45, True, instructions.blueCycle)

elapsed_time = 1

while True:
    start_time = time.time()
    field.update(frame)
    robot0.tick()
    display.drawRobot(robot0)
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
        end='\r'
    )
    frame += 1
    display.update(field)
    end_time = time.time()
    elapsed_time = end_time - start_time
    time.sleep(1/30)

    if field.state == fieldState.OVER:
        break


display.displayGraph(field)
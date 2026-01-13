from models.field import Field
import time
from models.robot import Robot
import models.instructions as instructions
import models.display as display

field = Field(0,0, 400, 0, 0)

frame = 0

testBot = Robot(field, 0, 1, 1, 10, 50, True, instructions.redCycle)

# self, redFuel : int, blueFuel : int,neutralFuel : int,redScore : int,blueScore : int
# RED ALLIANCE
# robot0 = Robot(0, 1, 1, 10, 8, True, [])
# robot1 = Robot(1, 1, 1, 10, 8, True, [])
# robot2 = Robot(2, 1, 1, 10, 8, True, [])
#
# # self, redFuel : int, blueFuel : int,neutralFuel : int,redScore : int,blueScore : int
# # BLUE ALLIANCE
# robot3 = Robot(3, 1, 1, 10, 8, False, [])
# robot4 = Robot(4, 1, 1, 10, 8, False, [])
# robot5 = Robot(5, 1, 1, 10, 8, False, [])

while True:
    field.update(frame)
    testBot.update(frame)
    display.drawRobot(testBot)

    print(
        f"field state: {field.state} | "
        f"red: {field.redScore} | "
        f"blue: {field.blueScore} | "
        f"neutral: {field.neutralFuel}",
        end="\r",
        flush=True
    )
    frame += 1
    display.update()
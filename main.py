import models.robot as robot
from models.field import Field
import time
from models.robot import Robot
import models.instructions as instructions

robots = []

field = Field(0,0, 400, 0, 0)

frame = 0

testBot = Robot(field, 0, 10, 10, 100, 50, True, instructions.testInstruction)

while True:
    field.update(frame)
    testBot.update(frame)
    print(field.redScore, field.state)
    frame += 1
    time.sleep(1/60)

import models.robot as robot
import models.field as field
import time

robots = []

field = field.Field(0,0, 400, 0, 0)

frame = 0

while True:
    field.update(frame)
    print(field)

    frame += 1
    time.sleep(0.001)

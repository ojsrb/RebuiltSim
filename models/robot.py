import threading
import time
from enum import Enum
from models.utils import *
from models.field import Field

class positions(Enum):
    RED = 0
    NEUTRAL = 1
    BLUE = 2

class states(Enum):
    MOVING = 0
    INTAKING = 1
    SHOOTING = 2
    STOPPED = 3
    SHUTTLING = 4

class Robot:
    def __init__(self, field: Field, number: int, shootSpeed: float, intakeSpeed: float, driveSpeed: float, capacity: int, preload: bool, instruction):
        self.number = number
        self.state = states.STOPPED
        self.shootSpeed = shootSpeed
        self.intakeSpeed = intakeSpeed
        self.driveSpeed = driveSpeed
        self.width = 25
        self.moving = None
        self.moveTime = 310 / self.driveSpeed # distance to drive
        if self.number <= 2:
            self.position = positions.RED
        else:
            self.position = positions.BLUE

        if preload:
            self.fuel = 8
        else:
            self.fuel = 0

        self.capacity = capacity

        self.instruction = instruction

        self.field = field

        thread =  threading.Thread(target=self.instruction, args=(self.field, self))
        thread.start()

    def moveTo(self, field, location):
        self.state = states.MOVING
        wait(field, self.moveTime)
        self.position = location
        self.state = states.MOVING


    def intake(self, field):
        if self.fuel < self.capacity and not self.moving:
            if self.state != states.INTAKING:
                time.sleep(self.moveTime / 4)
            self.state = states.INTAKING
            if self.position == positions.RED and field.redFuel > 0:
                field.redIntake()
            elif self.position == positions.BLUE and field.blueFuel > 0:
                field.blueIntake()
            elif self.position == positions.NEUTRAL and field.neutralFuel > 0:
                field.neutralIntake()
            else:
                return

            self.fuel += 1
            wait(field, 1 / self.intakeSpeed)

    def shoot(self, field):
        if self.fuel > 0 and not self.moving:
            self.state = states.SHOOTING
            if self.position == positions.RED:
                field.addRedScore()
                self.fuel -= 1
            elif self.position== positions.BLUE:
                field.addBlueScore()
                self.fuel -= 1
            else:
                return
            wait(field, 1 / self.shootSpeed)

    def shuttle(self, field, position):
        if self.fuel > 0 and not self.moving:
            self.state = states.SHOOTING
            if position == positions.RED:
                self.fuel -= 1
                field.shuttleRed()
            elif position == positions.BLUE:
                self.fuel -= 1
                field.shuttleBlue()
            wait(field, 1 / self.shootSpeed)
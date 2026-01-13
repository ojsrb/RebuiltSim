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

class Robot:
    def __init__(self, field: Field, number: int, shootSpeed: float, intakeSpeed: float, driveSpeed: float, capacity: int, preload: bool, instruction):
        self.number = number
        self.state = states.STOPPED
        self.shootSpeed = shootSpeed
        self.intakeSpeed = intakeSpeed
        self.driveSpeed = driveSpeed
        self.width = 25
        self.moving = None
        self.moveTime = 310 / (self.driveSpeed / 60) # distance to drive
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

    def moveTo(self, location, timestamp):
        if location == self.position or self.moving:
            return
        self.startedMoving = timestamp
        self.moving = location
        self.state = states.MOVING

    def update(self, timestamp):
        if self.moving:
            if self.startedMoving + self.moveTime <= timestamp:
                self.position = self.moving
                self.moving = None
        else:
            self.instruction(self.field, self, timestamp)

    def intake(self, field, timestamp):
        if not self.moving:
            self.state = states.INTAKING
        if timestamp % (60 / self.intakeSpeed) == 0 and self.fuel < self.capacity and not self.moving:
            if self.position == positions.RED:
                field.redIntake()
            elif self.position == positions.BLUE:
                field.blueIntake()
            else:
                field.neutralIntake()

            self.fuel += 1

    def shoot(self, field, timestamp):
        if not self.moving:
            self.state = states.INTAKING
        if timestamp % (60 / self.shootSpeed) == 0 and self.fuel > 0 and not self.moving:
            if self.position== positions.RED:
                field.addRedScore()
                self.fuel -= 1
            else:
                field.addBlueScore()
                self.fuel -= 1

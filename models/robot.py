from models.utils import *

class Robot:
    def __init__(self, number: int, shootSpeed: float, intakeSpeed: float, driveSpeed: float, preload: bool, instructions):
        self.number = number
        self.shootSpeed = shootSpeed
        self.intakeSpeed = intakeSpeed
        self.driveSpeed = driveSpeed
        self.instructions = instructions
        self.width = 25
        self.moving = None
        self.moveTime = self.driveSpeed * 60 * 310 # distance to drive
        if self.number <= 2:
            self.fieldArea = "RED"
        else:
            self.fieldArea = "BLUE"

        if preload:
            self.fuel = 8
        else:
            self.fuel = 0

        self.capacity = capacity

    def moveTo(self, location, timestamp):
        self.startedMoving = timestamp
        self.moving = location

    def update(self, timestamp):
        if self.moving and self.startedMoving + timestamp >= self.moveTime:
            self.fieldArea = self.moving
            self.moving = None

    def intake(self, field, timestamp):
        if timestamp % (60 / self.intakeSpeed) == 0 and self.fuel < self.capacity and not self.moving:
            if self.fieldArea == "RED":
                field.redIntake()
            elif self.fieldArea == "BLUE":
                field.blueIntake()
            else:
                field.neutralIntake()

            self.fuel += 1

    def shoot(self, field, timestamp):
        if timestamp % (60 / self.shootSpeed) == 0 and self.fuel > 0 and not self.moving:
            if self.fieldArea == "RED":
                field.redScore()
                self.fuel -= 1
            else:
                field.blueScore()
                self.fuel -= 1

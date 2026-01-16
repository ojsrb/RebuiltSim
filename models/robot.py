import math
import threading
import time
from enum import Enum
from models.utils import *
from models.field import Field, fieldState

class Instruction:
    def __init__(self):
        self.active = []
        self.inactive = []

    def activeHub(self, actions: list[action]):
        self.active = actions

    def inactiveHub(self, actions: list[action]):
        self.inactive = actions

class position(Enum):
    RED = 0
    NEUTRAL = 1
    BLUE = 2

class alliance(Enum):
    RED = 0
    BLUE = 1

class action(Enum):
    MOVE_HOME = 0
    MOVE_NEUTRAL = 1
    MOVE_OPP = 2

    INTAKE = 3
    SCORE = 4

    PASS = 5

class state(Enum):
    ACTIVE = 0
    INACTIVE = 1

class Robot:
    def __init__(self, field: Field, color: alliance, shootSpeed: float, intakeSpeed: float, driveSpeed: float, capacity: int, preload: bool, instruction: Instruction):
        self.color = color
        if self.color == alliance.RED:
            self.activeStates = [fieldState.RED_ACTIVE, fieldState.AUTO, fieldState.END, fieldState.TRANS]
            self.position = position.RED
            self.home = position.RED
            self.opp = position.BLUE
        elif self.color == alliance.BLUE:
            self.activeStates = [fieldState.BLUE_ACTIVE, fieldState.AUTO, fieldState.END, fieldState.TRANS]
            self.home = position.BLUE
            self.position = position.BLUE
            self.opp = position.RED
        self.shootSpeed = shootSpeed
        self.intakeSpeed = intakeSpeed
        self.driveSpeed = driveSpeed
        if preload:
            self.fuel = 8
        else:
            self.fuel = 0
        self.capacity = capacity
        self.instruction = instruction
        self.startedInstruction = 0
        self.field = field
        self.state = state.ACTIVE

        self.frame = 0
        self.index = 0

    def nextAction(self):
        self.index += 1
        self.startedInstruction = self.frame

    def tick(self):
        if self.field.state in self.activeStates and self.state == state.INACTIVE:
            self.state = state.ACTIVE
            self.index = 0
        elif self.field.state not in self.activeStates and self.state == state.ACTIVE:
            self.state = state.INACTIVE
            self.index = 0

        if self.state == state.ACTIVE:
            current = self.instruction.active[self.index]
            length = len(self.instruction.active)
        else:
            current = self.instruction.inactive[self.index]
            length = len(self.instruction.inactive)

        if current in [action.MOVE_HOME, action.MOVE_NEUTRAL, action.MOVE_OPP]:

            if (current == action.MOVE_HOME and self.position == self.home) or (current == action.MOVE_OPP and self.position == self.opp) or (current == action.MOVE_NEUTRAL and self.position == position.NEUTRAL):
                self.nextAction()
            elif self.frame - self.startedInstruction >= (310/self.driveSpeed)*30:

                if current == action.MOVE_HOME:
                    self.position = self.home
                elif current == action.MOVE_NEUTRAL:
                    self.position = position.NEUTRAL
                elif current == action.MOVE_OPP:
                    self.position = self.opp

                self.nextAction()

        elif current == action.INTAKE:
            if self.fuel < self.capacity:
                cooldown = math.floor((1 / self.intakeSpeed) * 30) # cooldown in frames between intakes
                if self.frame - self.startedInstruction >= cooldown:
                    if self.position == position.BLUE and self.field.blueFuel > 0:
                        self.field.blueFuel -= 1
                        self.fuel += 1
                        print("intaking blue", self.fuel)
                    elif self.position == position.NEUTRAL and self.field.neutralFuel > 0:
                        self.field.neutralFuel -= 1
                        self.fuel += 1
                        print("intaking neutral", self.fuel)
                    elif self.position == position.RED and self.field.redFuel > 0:
                        self.field.redFuel -= 1
                        self.fuel += 1
                        print("intaking red", self.fuel)
                    else:
                        self.nextAction()
                    if self.fuel == self.capacity:
                        self.nextAction()
            else:
                self.nextAction()

        elif current == action.SCORE:
            if self.fuel > 0:
                cooldown = math.floor((1 / self.shootSpeed) * 30) # cooldown in frames between intakes
                if self.frame - self.startedInstruction >= cooldown:
                    if self.position == position.BLUE and self.fuel > 0:
                        self.field.neutralFuel += 1
                        self.field.blueScore += 1
                        self.fuel -= 1
                        print("scoring blue", self.fuel)
                    elif self.position == position.RED and self.fuel > 0:
                        self.field.neutralFuel += 1
                        self.field.redScore += 1
                        self.fuel -= 1
                        print("scoring red", self.fuel)
                    if self.fuel == 0:
                        self.nextAction()
            else:
                self.nextAction()

        elif current == action.PASS:
            print(self.position)
            cooldown = math.floor((1 / self.shootSpeed) * 30) + math.floor((1 / self.intakeSpeed) * 30)
            if self.frame - self.startedInstruction >= cooldown and self.position == position.NEUTRAL and self.field.neutralFuel > 0:
                if self.color == alliance.RED:
                    self.field.neutralFuel -= 1
                    self.field.redFuel += 1
                else:
                    self.field.neutralFuel -= 1
                    self.field.blueFuel += 1

                self.nextAction()

        self.frame += 1

        if self.index == length:
            self.index = 0

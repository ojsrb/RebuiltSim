import math
import threading
import time
from enum import Enum
from models.utils import *
from models.field import Field, fieldState

class Instruction:
    def __init__(self, name: str):
        self.name = name
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
    def __init__(self, field: Field, number: int, shootSpeed: float, intakeSpeed: float, driveSpeed: float, capacity: int, preload: bool, instruction: Instruction):
        self.number = number
        if self.number <= 2:
            self.alliance = alliance.RED
            self.activeStates = [fieldState.RED_ACTIVE, fieldState.AUTO, fieldState.END, fieldState.TRANS]
            self.home = position.RED
            self.opp = position.BLUE
        else:
            self.alliance = alliance.BLUE
            self.activeStates= [fieldState.BLUE_ACTIVE, fieldState.AUTO, fieldState.END, fieldState.TRANS]
            self.home = position.BLUE
            self.opp = position.RED
        self.shootSpeed = shootSpeed
        self.intakeSpeed = intakeSpeed
        self.driveSpeed = driveSpeed
        if self.number <= 2:
            self.position = position.RED
        else:
            self.position = position.BLUE
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

            if (current == action.MOVE_HOME and self.position == self.home) or (current == action.MOVE_OPP and self.position == self.opp) or (current == action.MOVE_NEUTRAL and self.position == position.BLUE):
                self.index += 1
                self.startedInstruction = self.frame
            elif self.frame - self.startedInstruction >= (310/self.driveSpeed)*30:

                if current == action.MOVE_HOME:
                    self.position = self.home
                elif current == action.MOVE_NEUTRAL:
                    self.position = position.NEUTRAL
                elif current == action.MOVE_OPP:
                    self.position = self.opp

                self.index += 1
                self.startedInstruction = self.frame

        elif current == action.INTAKE:
            cooldown = math.floor((1 / self.intakeSpeed) * 30) # cooldown in frames between intakes
            if self.frame - self.startedInstruction >= cooldown and self.fuel < self.capacity:
                self.fuel += 1
                if self.position == position.BLUE:
                    self.field.blueIntake()
                elif self.position == position.NEUTRAL:
                    self.field.neutralIntake()
                elif self.position == position.RED:
                    self.field.redIntake()

            if self.fuel == self.capacity:
                self.index += 1
                self.startedInstruction = self.frame

        elif current == action.SCORE:
            cooldown = math.floor((1 / self.shootSpeed) * 30)
            if self.frame - self.startedInstruction >= cooldown and self.fuel > 0:
                self.fuel -= 1
                if self.position == position.BLUE:
                    self.field.addBlueScore()
                elif self.position == position.RED:
                    self.field.addRedScore()

            if self.fuel == 0:
                self.index += 1
                self.startedInstruction = self.frame

        elif current == action.PASS:
            cooldown = math.floor((1 / self.shootSpeed) * 30)
            if self.frame - self.startedInstruction >= cooldown and self.fuel > 0:
                self.fuel -= 1
                if self.alliance == alliance.RED:
                    self.field.addRedScore()
                elif self.alliance == alliance.BLUE:
                    self.field.addBlueScore()

                if self.fuel == 0:
                    self.index += 1
                    self.startedInstruction = self.frame

        self.frame += 1

        if self.index == length:
            self.index = 0

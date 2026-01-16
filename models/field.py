from enum import Enum
import random

class fieldState(Enum):
    AUTO = 1
    TRANS = 2
    RED_ACTIVE = 3
    BLUE_ACTIVE = 4
    END = 5
    OVER = 6

class Field:
    def __init__(self, redFuel : int, blueFuel : int,neutralFuel : int,redScore : int,blueScore : int):
        self.redFuel = redFuel
        self.blueFuel = blueFuel
        self.neutralFuel = neutralFuel
        self.redScore = redScore
        self.blueScore = blueScore
        self.state = fieldState.AUTO

        self.pastAuto = False
        self.redWonAuto = False
        self.timestamp = 0

    def calculateHubOrder(self):
        if not self.pastAuto:
            if self.redScore > self.blueScore:
                self.redWonAuto = True
            elif self.redScore == self.blueScore: # choose a random side to win if the scores are tied
                if random.randint(1, 2) == 1:
                    self.redWonAuto = True
                else:
                    self.redWonAuto = False
            else:
                self.redWonAuto = False
            self.pastAuto = True

    def update(self, timeStampInFrames: int):
        timeStampInFrames = timeStampInFrames * 2
        self.timestamp = timeStampInFrames
        if timeStampInFrames <= 1200/2:
            self.state = fieldState.AUTO
        elif timeStampInFrames <= 1800/2:
            self.state = fieldState.TRANS
            self.calculateHubOrder()
        if self.redWonAuto and (timeStampInFrames >= 1800): # set the times of shifts
            if timeStampInFrames <= 3300:
                self.state = fieldState.BLUE_ACTIVE
            elif timeStampInFrames <= 4800:
                self.state = fieldState.RED_ACTIVE
            elif timeStampInFrames <= 6300:
                self.state = fieldState.BLUE_ACTIVE
            elif timeStampInFrames <= 7800:
                self.state = fieldState.RED_ACTIVE
        elif not self.redWonAuto and (timeStampInFrames >= 1800):
            if timeStampInFrames <= 3300:
                self.state = fieldState.RED_ACTIVE
            elif timeStampInFrames <= 4800:
                self.state = fieldState.BLUE_ACTIVE
            elif timeStampInFrames <= 6300:
                self.state = fieldState.RED_ACTIVE
            elif timeStampInFrames <= 7800:
                self.state = fieldState.BLUE_ACTIVE
        if 7800 < timeStampInFrames <= 9300:
            self.state = fieldState.END
        if timeStampInFrames >= 9600:
            self.state = fieldState.OVER
            

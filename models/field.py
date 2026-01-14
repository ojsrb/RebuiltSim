from enum import Enum

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
    #score fuel/fuel back to neutral
    def addBlueScore(self):
        if self.state != fieldState.RED_ACTIVE:
            self.blueScore += 1
            self.neutralFuel += 1

    def addRedScore(self):
        if self.state != fieldState.BLUE_ACTIVE:
            self.redScore += 1
            self.neutralFuel += 1
    # lose fuel/fuel intaked

    def blueIntake(self):
        self.blueFuel -= 1
    def redIntake(self):
        self.redFuel -= 1
    def neutralIntake(self):
        self.neutralFuel -= 1

    def calculateHubOrder(self):
        if not self.pastAuto:
            if self.redScore > self.blueScore:
                self.redWonAuto = True
            else:
                self.redWonAuto = False
            self.pastAuto = True

    def shuttleRed(self):
        self.redFuel += 1

    def shuttleBlue(self):
        self.blueFuel += 1

    def update(self, timeStampInFrames: int):
        self.timestamp = timeStampInFrames
        if timeStampInFrames <= 1200:
            self.state = fieldState.AUTO
        elif timeStampInFrames <= 1800:
            self.state = fieldState.TRANS
            self.calculateHubOrder()
        if self.redWonAuto and (timeStampInFrames >= 1800): # set the times
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
            

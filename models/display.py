import sys
from models.robot import Robot, position
from models.field import Field
import matplotlib.pyplot as plt

# graphing metrics
scores = [0,0]
globalNeutralFuel = []
globalBlueFuel = []
globalRedFuel = []
time = []

# add graph metrics every frame
def update(matchInfo: Field):
    currentNeutralFuel = matchInfo.neutralFuel
    currentBlueField = matchInfo.blueFuel
    currentRedField = matchInfo.redFuel

    globalNeutralFuel.append(currentNeutralFuel)
    globalBlueFuel.append(currentBlueField)
    globalRedFuel.append(currentRedField)
    time.append(matchInfo.timestamp / 60)

# plot graph at the end of match simulation
def displayGraph(field : Field):
    autoWinner = ""
    plt.plot(time,globalNeutralFuel, c= "grey", label = "Fuel in Neutral")
    plt.plot(time,globalBlueFuel, c = "blue" ,label = "Fuel in Blue Posession")
    plt.plot(time,globalRedFuel, c = "red", label = "Fuel in Red Posession")

    plt.axvspan(0, 30, alpha=0.2, color="gray") # auto and transition highlight
    if field.redWonAuto:
        autoWinner = "Red"

        # highlight shifts
        plt.axvspan(30, 55, alpha=0.2, color="blue")
        plt.axvspan(55, 80, alpha=0.2, color="red")
        plt.axvspan(80, 105, alpha=0.2, color="blue")
        plt.axvspan(105, 130, alpha=0.2, color="red")
    else:
        autoWinner = "Blue"

        # highlight shifts
        plt.axvspan(30, 55, alpha=0.2, color="red")
        plt.axvspan(55, 80, alpha=0.2, color="blue")
        plt.axvspan(80, 105, alpha=0.2, color="red")
        plt.axvspan(105, 130, alpha=0.2, color="blue")

    # highlight endgame
    plt.axvspan(130, 160, alpha=0.2, color="gray")

    if field.redScore >= field.blueScore:
        plt.title(f"Red wins {field.redScore}-{field.blueScore}. Auto Winner: {autoWinner}")
    else:
        plt.title(f"Blue wins {field.blueScore}-{field.redScore}. Auto Winner: {autoWinner}")
    plt.xlabel("Time (s)")
    plt.ylabel("Fuel Amount")

    plt.legend()
    plt.show()
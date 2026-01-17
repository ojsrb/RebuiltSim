import sys
import io
import base64
from models.robot import Robot, position
from models.field import Field
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for web server compatibility
import matplotlib.pyplot as plt

# graphing metrics
scores = [0,0]
globalNeutralFuel = []
globalBlueFuel = []
globalRedFuel = []
time = []


def reset_graph_data():
    """Reset global tracking variables between simulations."""
    global globalNeutralFuel, globalBlueFuel, globalRedFuel, time, scores
    globalNeutralFuel = []
    globalBlueFuel = []
    globalRedFuel = []
    time = []
    scores = [0, 0]

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


def generate_graph_base64(field: Field) -> str:
    """
    Generate the graph and return as base64-encoded PNG.
    Does not call plt.show() - returns the image data instead.
    """
    plt.figure(figsize=(12, 6))

    autoWinner = ""
    plt.plot(time, globalNeutralFuel, c="grey", label="Fuel in Neutral")
    plt.plot(time, globalBlueFuel, c="blue", label="Fuel in Blue Possession")
    plt.plot(time, globalRedFuel, c="red", label="Fuel in Red Possession")

    plt.axvspan(0, 30, alpha=0.2, color="gray")  # auto and transition highlight

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

    # Save to bytes buffer and encode as base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()  # Close figure to free memory

    return img_base64
import sys
import pygame
from models.robot import Robot, position
from models.field import Field
import matplotlib.pyplot as plt

pygame.init()

screen = pygame.display.set_mode((325, 650))
pygame.display.set_caption("Field Display")

background = pygame.image.load('lib/field.bmp').convert()

scores = [0,0]
globalNeutralFuel = []
globalBlueFuel = []
globalRedFuel = []
time = []
def drawRobot(robot: Robot):
    width = 28
    x = 0
    y = 0

    if robot.position == position.RED:
        x = screen.get_width()/2
        y = 650 * 7/8
    elif robot.position == position.NEUTRAL:
        x = screen.get_width()/2
        y = screen.get_height()/2
    elif robot.position == position.BLUE:
        x = screen.get_width()/2
        y = 650 * 1/8
    if robot.number <= 2:
        color = pygame.Color('red')
    else:
        color = pygame.Color('blue')
    pygame.draw.rect(screen, color, pygame.Rect(x-(width/2), y-(width/2), width, width), 4)

def update(matchInfo: Field, visualize=False):
    currentNeutralFuel = matchInfo.neutralFuel
    currentBlueField = matchInfo.blueFuel
    currentRedField = matchInfo.redFuel

    globalNeutralFuel.append(currentNeutralFuel)
    globalBlueFuel.append(currentBlueField)
    globalRedFuel.append(currentRedField)
    time.append(matchInfo.timestamp)


    if visualize:
        pygame.display.update()
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def displayGraph(field : Field):
    autoWinner = ""
    plt.plot(time,globalNeutralFuel, c= "grey", label = "Fuel in Neutral")
    plt.plot(time,globalBlueFuel, c = "blue" ,label = "Fuel in Blue Posession")
    plt.plot(time,globalRedFuel, c = "red", label = "Fuel in Red Posession")
    if field.redWonAuto:
	    autoWinner = "Red"
    else:
        autoWinner = "Blue"
    if field.redScore >= field.blueScore:
        plt.title(f"Red wins with {field.redScore}. Auto Winner: {autoWinner}")
    else:
        plt.title(f"Blue wins with {field.blueScore}. Auto Winner: {autoWinner}")
    plt.xlabel("Time in Frames")
    plt.ylabel("Fuel Amount")

    plt.legend()
    plt.show()
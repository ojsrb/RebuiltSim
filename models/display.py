import sys

import pygame
from models.robot import Robot, positions, states

pygame.init()

screen = pygame.display.set_mode((325, 650))
pygame.display.set_caption("Field Display")

background = pygame.image.load('lib/field.bmp').convert()

def drawRobot(robot: Robot):
    width = 28
    x = 0
    y = 0

    if robot.position == positions.RED:
        x = screen.get_width()/2
        y = 650 * 7/8
    elif robot.position == positions.NEUTRAL:
        x = screen.get_width()/2
        y = screen.get_height()/2
    elif robot.position == positions.BLUE:
        x = screen.get_width()/2
        y = 650 * 1/8

    pygame.draw.rect(screen, pygame.Color('red'), pygame.Rect(x-(width/2), y-(width/2), width, width), 4)

    # text = font.render(str(robot.fuel), True, pygame.Color('white'))
    # textRect = text.get_rect()
    #
    # textRect.center = (x, y)
    # screen.blit(text, textRect)

def update():

    pygame.display.update()

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
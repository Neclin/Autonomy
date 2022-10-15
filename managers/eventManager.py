from turtle import left, width
import pygame
import math

from managers.placer import Placer
from item import Item
from managers.level import Level
from managers.renderer import Renderer
from managers.level import Level
from buildings.belt import Belt
from settings import cellSize, screenWidth, screenHeight


class EventManager:
    running = True
    start = True
    speed = 3
    leftMouseDown = False
    rightMouseDown = False
    checkRotation = False
    lastMousePos = pygame.Vector2(0, 0)
    lastArrayPos = pygame.Vector2(0, 0)

    @classmethod
    def checkEvents(cls):
        mousePos = pygame.mouse.get_pos()
        mousePos = (mousePos[0] + Renderer.screenPos.x, mousePos[1] + Renderer.screenPos.y)
        levelX = mousePos[0] // cellSize
        levelY = mousePos[1] // cellSize
        arrayPos = pygame.Vector2(levelX, levelY)

        # get the mouse pos and converts to a vector
        mousePos = pygame.mouse.get_pos()
        mousePos = pygame.Vector2(mousePos[0], mousePos[1])

        screenOffset = pygame.Vector2(Renderer.screenPos.x % cellSize, Renderer.screenPos.y % cellSize)

        roundedCellPos = (Renderer.screenPos + mousePos) // cellSize * cellSize
        # print(f"screen offset: {screenOffset}, rounded cell pos: {roundedCellPos}")

        # gets the direction of the mouse
        mouseDirection = (mousePos - cls.lastMousePos)
        if mouseDirection:
            mouseDirection = mouseDirection.normalize()

        mouseDirectionChanged = False
        arrayPosChanged = False

        x = abs((cls.lastMousePos.x - mousePos.x) * Placer.mouseDirection.y)
        y = abs((cls.lastMousePos.y - mousePos.y) * Placer.mouseDirection.x)

        if x + y >= 1:
            if (mousePos - cls.lastMousePos) != pygame.Vector2(0, 0):
                mouseDirection = (mousePos - cls.lastMousePos).normalize()

                # cast into cardinal directions
                if abs(mouseDirection.x) > abs(mouseDirection.y):  # prioritises horizontal
                    mouseDirection.x = math.copysign(1, mouseDirection.x)
                    mouseDirection.y = 0
                else:  # prioritises vertical
                    mouseDirection.x = 0
                    mouseDirection.y = math.copysign(1, mouseDirection.y)

                Placer.mouseDirection = mouseDirection
            cls.lastMousePos = mousePos
            mouseDirectionChanged = True

        if cls.lastArrayPos != arrayPos:
            cls.lastArrayPos = arrayPos
            if (mousePos - cls.lastMousePos) != pygame.Vector2(0, 0):
                if Placer.activeBuilding and (mouseDirection.x != -Placer.activeBuilding.startDirection.x
                                              or mouseDirection.y != -Placer.activeBuilding.startDirection.y):
                    Placer.rotation = mouseDirection.angle_to(pygame.Vector2(1, 0))
                    Placer.activeBuilding.endDirection = mouseDirection
                    Placer.activeBuilding.resetNext()
                    Placer.activeBuilding.update()

            Placer.activeBuilding = None
            arrayPosChanged = True

        # gets all active events from the pygame library
        for event in pygame.event.get():
            # checks if the X is pressed and quits the program
            if event.type == pygame.QUIT:
                cls.running = False
                pygame.quit()
                quit()

            # checks all keyboard events 
            elif event.type == pygame.KEYDOWN:
                # checks if escape is pressed and quits the program when in full screen mode
                if event.key == pygame.K_ESCAPE:
                    cls.running = False
                    pygame.quit()
                    quit()

                # sets the rotation of the placer module
                if event.key == pygame.K_r:
                    if isinstance(Placer.active, Belt) and cls.leftMouseDown:  # special rule for belts
                        cls.checkRotation = True
                    else:
                        Placer.rotation -= 90
                        Placer.rotation %= 360

                # debugging for items - places items on last belt
                if event.key == pygame.K_b:
                    building = Level.array[int(arrayPos.y)][int(arrayPos.x)]
                    if isinstance(building, Belt):
                        item = Item(building.points[0], 0)
                        item.belt = building
                        Level.items.append(item)

                # saves the current state of the level - not finalised
                if event.key == pygame.K_s:
                    Level.saveLevel("levels/save.txt")

                if event.key == pygame.K_UP:
                    cls.speed += 1
                if event.key == pygame.K_DOWN:
                    cls.speed -= 1

            # checks mouse presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # checks if the left mouse button is pressed and enables the placer function
                if event.button == 1:
                    cls.leftMouseDown = True
                    Placer.startPos = arrayPos

                    for button in Level.buttons:
                        if button.isPressed():
                            pass

                # checks if the right mouse button is pressed and enables the placer function
                if event.button == 3:
                    cls.rightMouseDown = True

            # checks if mouse is released
            elif event.type == pygame.MOUSEBUTTONUP:
                # checks if the left mouse button is pressed and disables the placer function
                if event.button == 1:
                    cls.leftMouseDown = False
                    Placer.startPos = None
                    Placer.activeBuilding = None

                # checks if the right mouse button is pressed and disables the placer function
                if event.button == 3:
                    cls.rightMouseDown = False

        if EventManager.leftMouseDown and Renderer.isPointInGrid(mousePos):
            directionVector = Placer.getVectorFromAngle(Placer.rotation)
            if not Placer.activeBuilding:
                Placer.activeBuilding = Placer.active.place(levelX, levelY, roundedCellPos, directionVector, directionVector,
                                                            cls.speed)
            else:
                if mouseDirectionChanged and (mouseDirection.x != -Placer.activeBuilding.startDirection.x
                                              or mouseDirection.y != -Placer.activeBuilding.startDirection.y):
                    Placer.rotation = mouseDirection.angle_to(pygame.Vector2(1, 0))
                    Placer.activeBuilding.endDirection = mouseDirection
                    Placer.activeBuilding.resetNext()
                    Placer.activeBuilding.update()

        if EventManager.rightMouseDown and Renderer.isPointInGrid(mousePos):
            building = Level.array[int(arrayPos.y)][int(arrayPos.x)]
            if building is not None:
                building.remove()

        # rotation based on belt direction
        if cls.checkRotation:
            pass

    @classmethod
    def checkScreenMovement(cls, DT):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and Renderer.screenPos.y - DT * Renderer.cameraVel.y >= 0:
            Renderer.screenPos.y -= DT * Renderer.cameraVel.y
        if keys[pygame.K_s] and Renderer.screenPos.y + DT * Renderer.cameraVel.y <= Level.height * cellSize - screenHeight:
            Renderer.screenPos.y += DT * Renderer.cameraVel.y
        if keys[pygame.K_a] and Renderer.screenPos.x - DT * Renderer.cameraVel.x >= 0:
            Renderer.screenPos.x -= DT * Renderer.cameraVel.x
        if keys[pygame.K_d] and Renderer.screenPos.x + DT * Renderer.cameraVel.x <= Level.width * cellSize - screenWidth:
            Renderer.screenPos.x += DT * Renderer.cameraVel.x

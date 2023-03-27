import pygame
import time

from gameObject import GameObject

from placement import *
from settings import CELLSIZE, WORLDPIXELWIDTH, WORLDPIXELHEIGHT, MOVEUP, MOVEDOWN, MOVELEFT, MOVERIGHT, ROTATE
from modules import *

class EventManager():
    def __init__(self):
        self.running = True

        self.lastFrameTime = time.time()
        self.lastAnimationFrameTime = time.time()
        self.deltaTime = 0

        self.position1 = None

        self.startDirection = pygame.Vector2(1, 0)
        self.endDirection = pygame.Vector2(1, 0)

        self.screenMousePosition = None
        self.worldMousePosition = None
        self.snappedWorldMousePosition = None
        self.arrayMousePosition = None

        self.timeSinceStart = 0

    def checkEvents(self, world, camera):   
        if self.timeSinceStart < 0.1:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.eventKill()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.eventKill()
                
                if event.key == pygame.K_RCTRL:
                    world.save()

                if event.key == ROTATE:
                    self.startDirection = rotateVectorByAngle(self.startDirection, 90)
                    self.endDirection = rotateVectorByAngle(self.endDirection, 90)
                
                if event.key == pygame.K_LEFT:  
                    self.startDirection = rotateVectorByAngle(self.startDirection, -90)
                
                if event.key == pygame.K_RIGHT:
                    self.startDirection = rotateVectorByAngle(self.startDirection, 90)

                if event.key == pygame.K_UP:
                    self.endDirection = rotateVectorByAngle(self.endDirection, -90)
                
                if event.key == pygame.K_DOWN:
                    self.endDirection = rotateVectorByAngle(self.endDirection, 90)

                if event.key == pygame.K_b:
                    mousePosition = pygame.mouse.get_pos()
                    mousePosition = pygame.Vector2(mousePosition[0], mousePosition[1])
                    worldMousePosition = camera.worldPosition - camera.position + mousePosition
                    placeItem(worldMousePosition.x, worldMousePosition.y, world)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                heldKeys = pygame.key.get_pressed()
                if event.button == 1:
                    # checks for mouse presses on GUI elements stored in the worlds container class
                    for container in world.containers:
                        container.checkMousePresses(event.pos)

                    # checks for the alternate placement of belts
                    if heldKeys[pygame.K_LSHIFT] and world.state == "Level":
                        if self.position1 is None:
                            self.position1 = self.snappedWorldMousePosition
                        else:
                            # place belts along the path created
                            if abs(self.startDirection.x) == 1:
                                anchor = pygame.Vector2(self.position1.x, self.snappedWorldMousePosition.y)
                            else:
                                anchor = pygame.Vector2(self.snappedWorldMousePosition.x, self.position1.y)
                            anchorArray = mapVectorToArrayNoCamera(anchor)
                            startDirection = placeBeltPath(self.position1, anchor, world)
                            endDirection = placeBeltPath(anchor, self.snappedWorldMousePosition, world)
                            if startDirection is not None and endDirection is not None:
                                removeGameObject(anchorArray.x, anchorArray.y, world)
                                placeBelt(anchorArray.x, anchorArray.y, anchor, world, startDirection, endDirection)
                            self.position1 = None
                        return



    def checkCameraMovement(self, camera):
        if self.timeSinceStart < 0.1:
            return
        
        keys = pygame.key.get_pressed()

        if keys[MOVEUP]:
            camera.worldPosition.y -= camera.velocity * self.deltaTime
        if keys[MOVEDOWN]:
            camera.worldPosition.y += camera.velocity * self.deltaTime
        if keys[MOVELEFT]:
            camera.worldPosition.x -= camera.velocity * self.deltaTime
        if keys[MOVERIGHT]:
            camera.worldPosition.x += camera.velocity * self.deltaTime

        camera.worldPosition.x = max(0, camera.worldPosition.x)
        camera.worldPosition.x = min(camera.worldPosition.x, WORLDPIXELWIDTH - camera.width - CELLSIZE)
        
        camera.worldPosition.y = max(0, camera.worldPosition.y)
        camera.worldPosition.y = min(camera.worldPosition.y, WORLDPIXELHEIGHT - camera.height - CELLSIZE)

    def checkMousePress(self, camera, world):
        if self.timeSinceStart < 0.1:
            return

        pressedMouseButtons = pygame.mouse.get_pressed()
        heldKeys = pygame.key.get_pressed()

        cameraOffset = pygame.Vector2(camera.worldPosition.x % CELLSIZE, camera.worldPosition.y % CELLSIZE)

        mousePosition = pygame.mouse.get_pos()
        self.screenMousePosition = pygame.Vector2(mousePosition[0], mousePosition[1]) - camera.position + cameraOffset
        self.worldMousePosition = self.screenMousePosition + camera.worldPosition

        self.snappedWorldMousePosition = snapVectorToGrid(self.screenMousePosition, camera)
        self.arrayMousePosition = mapVectorToArray(self.screenMousePosition, camera)

        if (self.worldMousePosition.x < camera.worldPosition.x or 
            self.worldMousePosition.x > camera.worldPosition.x + camera.width or
            self.worldMousePosition.y < camera.worldPosition.y or
            self.worldMousePosition.y > camera.worldPosition.y + camera.height):
            return

        
        arrayX = int(self.arrayMousePosition.x)
        arrayY = int(self.arrayMousePosition.y)

        if pressedMouseButtons[0]:
            if heldKeys[pygame.K_LSHIFT]:
                return
            # print(f"World position x:{worldMousePosition.x}, y:{worldMousePosition.y}")
            # print(f"Snapped world position x:{snappedWorldMousePosition.x}, y:{snappedWorldMousePosition.y}")
            # print(f"Array position x:{arrayMousePosition.x}, y:{arrayMousePosition.y}\n")
            if world.state == "Level":
                placeBelt(arrayX, arrayY, self.snappedWorldMousePosition, world, self.startDirection, self.endDirection)
            # PlaceGameObject(arrayX, arrayY, snappedWorldMousePosition, world) 
        
        if pressedMouseButtons[2]:
            # print("right mouse button pressed")
            removeGameObject(arrayX, arrayY, world)

    def eventKill(self):
        self.running = False
        pygame.quit()
        quit()
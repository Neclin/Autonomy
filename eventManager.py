import pygame
import time

from gameObject import GameObject

from placement import *
from settings import SCREENWIDTH, SCREENHEIGHT, CELLSIZE, WORLDPIXELWIDTH, WORLDPIXELHEIGHT
from modules import snapVectorToGrid, mapVectorToArray, rotateVectorByAngle

class EventManager():
    def __init__(self):
        self.running = True

        self.lastFrameTime = time.time()
        self.lastAnimationFrameTime = time.time()
        self.deltaTime = 0

        self.pos1 = None

        self.startDirection = pygame.Vector2(1, 0)
        self.endDirection = pygame.Vector2(1, 0)

    def checkEvents(self, world, camera):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                
                if event.key == pygame.K_RCTRL:
                    world.save("levels/level1.txt")

                if event.key == pygame.K_r:
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

            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     mousePosition = pygame.mouse.get_pos()
            #     # convert mouse position to a vector
            #     mousePosition = pygame.Vector2(mousePosition[0], mousePosition[1])

            #     if event.button == 1:
            #         print(f"mouse position x: {mousePosition.x}, y: {mousePosition.y}")


    def checkCameraMovement(self, camera):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            camera.worldPosition.y -= camera.velocity * self.deltaTime
        if keys[pygame.K_s]:
            camera.worldPosition.y += camera.velocity * self.deltaTime
        if keys[pygame.K_a]:
            camera.worldPosition.x -= camera.velocity * self.deltaTime
        if keys[pygame.K_d]:
            camera.worldPosition.x += camera.velocity * self.deltaTime

        camera.worldPosition.x = max(0, camera.worldPosition.x)
        camera.worldPosition.x = min(camera.worldPosition.x, WORLDPIXELWIDTH - camera.width - CELLSIZE)
        
        camera.worldPosition.y = max(0, camera.worldPosition.y)
        camera.worldPosition.y = min(camera.worldPosition.y, WORLDPIXELHEIGHT - camera.height - CELLSIZE)

    def checkMousePress(self, camera, world):
        pressedMouseButtons = pygame.mouse.get_pressed()

        cameraOffset = pygame.Vector2(camera.worldPosition.x % CELLSIZE, camera.worldPosition.y % CELLSIZE)

        mousePosition = pygame.mouse.get_pos()
        screenMousePosition = pygame.Vector2(mousePosition[0], mousePosition[1]) - camera.position + cameraOffset
        worldMousePosition = screenMousePosition + camera.worldPosition

        if (worldMousePosition.x < camera.worldPosition.x or 
            worldMousePosition.x > camera.worldPosition.x + camera.width or
            worldMousePosition.y < camera.worldPosition.y or
            worldMousePosition.y > camera.worldPosition.y + camera.height):
            return

        snappedWorldMousePosition = snapVectorToGrid(screenMousePosition, camera)
        arrayMousePosition = mapVectorToArray(screenMousePosition, camera)
        
        arrayX = int(arrayMousePosition.x)
        arrayY = int(arrayMousePosition.y)

        if pressedMouseButtons[0]:
            # print(f"World position x:{worldMousePosition.x}, y:{worldMousePosition.y}")
            # print(f"Snapped world position x:{snappedWorldMousePosition.x}, y:{snappedWorldMousePosition.y}")
            # print(f"Array position x:{arrayMousePosition.x}, y:{arrayMousePosition.y}\n")
            placeBelt(arrayX, arrayY, snappedWorldMousePosition, world, self.startDirection, self.endDirection)
            # PlaceGameObject(arrayX, arrayY, snappedWorldMousePosition, world)
        
        if pressedMouseButtons[2]:
            # print("right mouse button pressed")
            removeGameObject(arrayX, arrayY, world)



import pygame, time

from gameObject import GameObject
from modules import mapVectorToArrayNoCamera
from placement import *

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.worldArray = [[0 for x in range(width)] for y in range(height)]

        self.gameObjects = []
        self.containers = []
        
        self.state = "MainMenu"

    def load(self, directory):
        self.state = "Level"
        for gameObject in self.gameObjects:
            self.removeGameObject(gameObject)
        self.containers = []
        with open(directory, "r") as file:
            for line in file:
                gameObjectData = line.split(" ")
                type = gameObjectData[0]
                x = int(gameObjectData[1])
                y = int(gameObjectData[2])
                if type == "Item":
                    placeItem(x, y, self)
                    continue
                arrayX = int(gameObjectData[3])
                arrayY = int(gameObjectData[4])
                if type == "GameObject":
                    PlaceGameObject(arrayX, arrayY, pygame.Vector2(x, y), self)
                    continue
                if type == "Belt":
                    startDirection = pygame.Vector2(int(gameObjectData[5]), int(gameObjectData[6]))
                    endDirection = pygame.Vector2(int(gameObjectData[7]), int(gameObjectData[8]))
                    placeBelt(arrayX, arrayY, pygame.Vector2(x, y), self, startDirection, endDirection)
                    continue

    def save(self, directory):
        startTime = time.time()
        print("Saving...")
        with open(directory, "w") as file:
            for gameObject in self.gameObjects:
                arrayPosition = mapVectorToArrayNoCamera(pygame.Vector2(gameObject.worldPosition.x, gameObject.worldPosition.y))
                if gameObject.type == "GameObject":
                    file.write(f"GameObject {int(gameObject.worldPosition.x)} {int(gameObject.worldPosition.y)} {int(arrayPosition.x)} {int(arrayPosition.y)}\n")
                elif gameObject.type == "Belt":
                    file.write(f"Belt {int(gameObject.worldPosition.x)} {int(gameObject.worldPosition.y)} {int(arrayPosition.x)} {int(arrayPosition.y)} {int(gameObject.startDirection.x)} {int(gameObject.startDirection.y)} {int(gameObject.endDirection.x)} {int(gameObject.endDirection.y)}\n")
                elif gameObject.type == "Item":
                    file.write(f"Item {int(gameObject.worldPosition.x)} {int(gameObject.worldPosition.y)}\n")

        print("Saved! in " + str(time.time() - startTime) + " seconds")

    def updateWorld(self, deltaTime):
        for gameObject in self.gameObjects:
            gameObject.update(deltaTime)
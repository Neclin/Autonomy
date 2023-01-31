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

    def load(self, directory):
        with open(directory, "r") as file:
            for line in file:
                gameObjectData = line.split(" ")
                type = gameObjectData[0]
                x = int(gameObjectData[1])
                y = int(gameObjectData[2])
                arrayX = int(gameObjectData[3])
                arrayY = int(gameObjectData[4])
                if type == "GameObject":
                    PlaceGameobject(arrayX, arrayY, pygame.Vector2(x, y), self)

    def save(self, directory):
        startTime = time.time()
        print("Saving...")
        with open(directory, "w") as file:
            for gameObject in self.gameObjects:
                arrayPosition = mapVectorToArrayNoCamera(pygame.Vector2(gameObject.worldPosition.x, gameObject.worldPosition.y))
                file.write(f"GameObject {int(gameObject.worldPosition.x)} {int(gameObject.worldPosition.y)} {int(arrayPosition.x)} {int(arrayPosition.y)}\n")

        print("Saved! in " + str(time.time() - startTime) + " seconds")
from distutils.command.build import build
from msilib.schema import Directory
from os import remove
from tkinter import Place
import pygame

from settings import cellSize
from level import Level

class Belt():
    def __init__(self, x, y, type, rotation):
        self.x = x
        self.y = y
        self.type = type
        self.rotation = rotation
        # sets the sprite sheet for the type of belt
        if self.type == 0:
            self.spriteSheet = pygame.image.load("assets/light/belt.png")
        elif self.type == 1:
            self.spriteSheet = pygame.image.load("assets/light/beltL.png")
        elif self.type == 2:
            self.spriteSheet = pygame.image.load("assets/light/beltR.png")
        # sets the sprite to the first frame of the animation and resets the rotation
        self.sprite = self.spriteSheet.subsurface(0, 0, cellSize, cellSize)
        self.sprite = pygame.transform.rotate(self.sprite, rotation)
        
        self.directionVector = None
        self.next = None

    # draws the belt to the screen
    def show(self, offset, window, animationFrame):
        window.blit(self.sprite, (offset.x + self.x * cellSize, offset.y + self.y * cellSize))
        # updates the sprite
        self.sprite = self.spriteSheet.subsurface(animationFrame * cellSize, 0, cellSize, cellSize)
        self.sprite = pygame.transform.rotate(self.sprite, self.rotation) # rotates the sprite

    # places the belt
    def place(self, x, y, type, rotation, directionVector):
        x, y = int(x), int(y)

        # places the belt if its empty
        building = Level.array[y][x]
        if (building == None):
            belt = Belt(x, y, type, rotation)
            belt.directionVector = directionVector
            Level.array[y][x] = belt
            Level.belts.append(belt)

            # straight belts
            if type == 0:
                nextX = int(x + directionVector.x)
                nextY = int(y + directionVector.y)
                next = None
                if 0 <= nextX < Level.width and 0 <= nextY < Level.height:
                    next = Level.array[nextY][nextX]
                if (isinstance(next,Belt)):
                    belt.next = next

                prevX = int(x - directionVector.x)
                prevY = int(y - directionVector.y)
                prev = None
                if 0 <= prevX < Level.width and 0 <= prevY < Level.height:
                    prev = Level.array[prevY][prevX]
                if (isinstance(prev,Belt)):
                    prev.next = belt

        
        # overwrites the current belt
        elif (isinstance(building, Belt) and building.rotation != rotation):
            print("test")
            building.rotate(rotation)
    
    def rotate(self, rotation):
        belt = Belt(self.x, self.y, self.type, rotation)
        self.remove()
        belt.rotation = rotation

    def remove(self):
        print(self.directionVector)
        prevX = int(self.x - self.directionVector.x)
        prevY = int(self.y - self.directionVector.y)
        prev = None
        if 0 <= prevX < Level.width and 0 <= prevY < Level.height:
            prev = Level.array[prevY][prevX]
        if (isinstance(prev,Belt)):
                prev.next = None

        Level.array[self.y][self.x] = None
        for index, belt in enumerate(Level.belts):
            if belt == self:
                del(Level.belts[index])
                break
        del(self)
            
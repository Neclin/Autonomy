import pygame

from gameObject import GameObject

class Item(GameObject):
    def __init__(self, x, y, width, height, ):
        super().__init__(x, y, width, height, colour=(33,131,128), type="Item")

    def moveToPoint():
        pass

    def getNextPoint():
        pass

    def show(self, renderer, camera):
        super().show(renderer, camera)
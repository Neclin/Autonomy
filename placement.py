import pygame

from gameObject import GameObject
from belt import Belt
from item import Item
from settings import CELLSIZE

def PlaceGameObject(arrayX, arrayY, position, world):
    arrayX, arrayY = int(arrayX), int(arrayY)
    if world.worldArray[arrayY][arrayX] == 0:
        newGameObject = GameObject(position.x, position.y, CELLSIZE, CELLSIZE, (0,255,0), type="GameObject")
        world.worldArray[arrayY][arrayX] = newGameObject
        insertGameObjects(newGameObject, world)

def removeGameObject(arrayX, arrayY, world):
    arrayX, arrayY = int(arrayX), int(arrayY)
    if world.worldArray[arrayY][arrayX] != 0:
        gameObjectToRemove = world.worldArray[arrayY][arrayX]
        world.gameObjects.remove(gameObjectToRemove)
        world.worldArray[arrayY][arrayX] = 0

        if gameObjectToRemove.type == "Belt":
            if gameObjectToRemove.next != None:
                gameObjectToRemove.next.previous = None
            if gameObjectToRemove.previous != None:
                gameObjectToRemove.previous.next = None

def placeBelt(arrayX, arrayY, position, world, startDirection, endDirection):
    arrayX, arrayY = int(arrayX), int(arrayY)
    building = world.worldArray[arrayY][arrayX]
    if building != 0:
        if building.type == "Belt" and building.startDirection != startDirection and building.endDirection != endDirection:
            removeGameObject(arrayX, arrayY, world)
    if world.worldArray[arrayY][arrayX] == 0:
        newBelt = Belt(position.x, position.y, startDirection, endDirection, world)
        world.worldArray[arrayY][arrayX] = newBelt
        insertGameObjects(newBelt, world)

        if newBelt.previous != None:
            newBelt.previous.next = newBelt
        if newBelt.next != None:
            newBelt.next.previous = newBelt

def placeBeltPath(start, end, world):
    directionVector = None
    # horizontal
    if start.x != end.x:
        direction = (end.x - start.x) // abs(end.x - start.x)
        directionVector = pygame.Vector2(direction, 0)
        for i in range(int(start.x), int(end.x+direction*CELLSIZE), int(direction*CELLSIZE)):
            placeBelt(i//CELLSIZE, start.y//CELLSIZE, pygame.Vector2(i, start.y), world, directionVector, directionVector)
    
    # vertical
    if start.y != end.y:
        direction = (end.y - start.y) // abs(end.y - start.y)
        directionVector = pygame.Vector2(0, direction)
        for i in range(int(start.y), int(end.y+direction*CELLSIZE), int(direction*CELLSIZE)):
            placeBelt(start.x//CELLSIZE, i//CELLSIZE, pygame.Vector2(start.x, i), world, directionVector, directionVector)
    
    return directionVector

def placeItem(x, y, world):
    firstBelt = None
    for gameObject in world.gameObjects:
        if gameObject.type == "Belt":
            firstBelt = gameObject
            break
    newItem = Item(x, y, 4, 4)
    newItem.belt = firstBelt
    insertGameObjects(newItem, world)
    newItem.setNextPoint()

def insertGameObjects(gameObjectToInsert, world):
    for i, gameObject in enumerate(world.gameObjects):
        if gameObject.layer >= gameObjectToInsert.layer:
            world.gameObjects.insert(i, gameObjectToInsert)
            return
    world.gameObjects.append(gameObjectToInsert)
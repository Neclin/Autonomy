from gameObject import GameObject
from belt import Belt
from item import Item
from settings import CELLSIZE

def PlaceGameObject(arrayX, arrayY, position, world):
    arrayX, arrayY = int(arrayX), int(arrayY)
    if world.worldArray[arrayY][arrayX] == 0:
        newGameObject = GameObject(position.x, position.y, CELLSIZE, CELLSIZE, (0,255,0), type="GameObject")
        world.worldArray[arrayY][arrayX] = newGameObject
        world.gameObjects.append(newGameObject)

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
    if world.worldArray[arrayY][arrayX] == 0:
        newBelt = Belt(position.x, position.y, startDirection, endDirection, world)
        world.worldArray[arrayY][arrayX] = newBelt
        world.gameObjects.append(newBelt)

        if newBelt.previous != None:
            newBelt.previous.next = newBelt
        if newBelt.next != None:
            newBelt.next.previous = newBelt

def placeItem(x, y, world):
    newItem = Item(x, y, 4, 4)
    world.gameObjects.append(newItem)
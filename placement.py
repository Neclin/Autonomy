from gameObject import GameObject
from settings import CELLSIZE

def PlaceGameobject(arrayX, arrayY, position, world):
    arrayX, arrayY = int(arrayX), int(arrayY)
    if world.worldArray[arrayY][arrayX] == 0:
        newGameObject = GameObject(position.x, position.y,
                                    CELLSIZE, CELLSIZE, (0, 255, 0))
        world.worldArray[arrayY][arrayX] = newGameObject
        world.gameObjects.append(newGameObject)

def removeGameObject(arrayX, arrayY, world):
    arrayX, arrayY = int(arrayX), int(arrayY)
    if world.worldArray[arrayY][arrayX] != 0:
        gameObjectToRemove = world.worldArray[arrayY][arrayX]
        world.gameObjects.remove(gameObjectToRemove)
        world.worldArray[arrayY][arrayX] = 0
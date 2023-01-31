import pygame

from settings import CELLSIZE

def snapVectorToGridNoCamera(vector):
    snappedVector = pygame.Vector2(vector.x // CELLSIZE * CELLSIZE,
                                vector.y // CELLSIZE * CELLSIZE)
    return snappedVector

def snapVectorToGrid(vector, camera):
    cameraOffset = pygame.Vector2(camera.worldPosition.x % CELLSIZE,
                                camera.worldPosition.y % CELLSIZE)
    gridAlignedCamera = camera.worldPosition - cameraOffset
    snappedVector = pygame.Vector2(vector.x // CELLSIZE * CELLSIZE,
                                vector.y // CELLSIZE * CELLSIZE)
    return gridAlignedCamera + snappedVector

def mapVectorToArrayNoCamera(vector):
    snappedVector = snapVectorToGridNoCamera(vector)
    return pygame.Vector2(snappedVector.x // CELLSIZE, 
                          snappedVector.y // CELLSIZE)

def mapVectorToArray(vector, camera):
    snappedVector = snapVectorToGrid(vector, camera)
    return pygame.Vector2(snappedVector.x // CELLSIZE, 
                          snappedVector.y // CELLSIZE)


def convertRelativePositionToWorld(relativePosition, camera):
    return relativePosition + camera.worldPosition
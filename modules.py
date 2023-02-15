import pygame, math

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

def convertWorldToScreenPosition(worldPosition, camera):
    return worldPosition - camera.worldPosition + camera.position

def rotateVectorByAngle(Vector, Angle):
    rotatedVector = pygame.Vector2(round(Vector.x * math.cos(math.radians(Angle)) - Vector.y * math.sin(math.radians(Angle))),
                                    round(Vector.x * math.sin(math.radians(Angle)) + Vector.y * math.cos(math.radians(Angle))))
    return rotatedVector

def quadraticBezierCurve(p0, p1, p2, t):
    return (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2
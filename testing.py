import pygame

from renderer import Camera
from modules import snapVectorToGrid

camera = Camera(0, 0, 800, 800, 100, None)

def test_1(value):
    print(f"input: ({0}, {value}) output: ", snapVectorToGrid(pygame.Vector2(0, value), camera))
    print(f"input: ({value}, {0}) output: ", snapVectorToGrid(pygame.Vector2(value, 0), camera))
    print(f"input: ({value}, {value}) output: ", snapVectorToGrid(pygame.Vector2(value, value), camera))

print("input: (0, 0) output: ", snapVectorToGrid(pygame.Vector2(0, 0), camera))
test_1(40)
test_1(799)
test_1(801)

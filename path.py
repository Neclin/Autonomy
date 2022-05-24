import pygame
from settings import screenHeight, screenWidth

class Path():
    def __init__(self):
        self.head = None
        self.last = None

        for y in range(100, screenHeight - 100, 20):
            node = Node(pygame.Vector2(100, y))
            self.addNode(node)

        for x in range(100, screenWidth - 100, 20):
            node = Node(pygame.Vector2(x, screenHeight - 100))
            self.addNode(node)
    
    def addNode(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def show(self, window):
        self.temp = self.head
        while self.temp != None:
            point = self.temp.pos
            pygame.draw.circle(window, (255, 255, 255), (int(point.x), int(point.y)), 1)
            if self.temp.occupied:
                pygame.draw.circle(window, (0, 255, 0), (int(point.x), int(point.y)), 1)
            self.temp = self.temp.next

class Node():
    def __init__(self, pos):
        self.pos = pos
        self.occupied = False
        self.next = None
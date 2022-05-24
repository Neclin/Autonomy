import pygame
from settings import screenHeight, screenWidth

class Path():
    def __init__(self):
        self.head = None
        self.tail = None

        gap = 16

        for y in range(100, screenHeight - 100, gap):
            node = Node(pygame.Vector2(100, y))
            self.addNode(node)

        for x in range(100, screenWidth - 100, gap):
            node = Node(pygame.Vector2(x, screenHeight - 100))
            self.addNode(node)
        
        for y in range(screenHeight - 100, 100, -gap):
            node = Node(pygame.Vector2(screenHeight - 100, y))
            self.addNode(node)

        for x in range(screenWidth - 100, 100, -gap):
            node = Node(pygame.Vector2(x, 100))
            self.addNode(node)
        
        self.tail.next = self.head
        
    
    def addNode(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def show(self, window):
        self.temp = self.head
        lastPoint = None
        start = True

        while self.temp != self.head or start:
            start = False
            point = self.temp.pos
            # if self.temp.occupied:
            #     pygame.draw.circle(window, (0, 255, 0), (int(point.x), int(point.y)), 2)
            if lastPoint != None:
                pygame.draw.line(window, (0,0,0), lastPoint, point)
            lastPoint = point
            self.temp = self.temp.next

    def free():
        del(self)

class Node():
    def __init__(self, pos):
        self.pos = pos
        self.occupied = False
        self.next = None
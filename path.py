import pygame
from settings import screenHeight, screenWidth

class Path():
    def __init__(self):
        self.head = None
        self.tail = None
        
    
    def addNode(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
            
    def addNodeEnd(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head = node

    def show(self, window):
        self.temp = self.head
        lastPoint = None
        start = True

        while self.temp != None and (self.temp.next != self.head or start):
            start = False
            point = self.temp.pos
            # if self.temp.occupied:
            #     pygame.draw.circle(window, (0, 255, 0), (int(point.x), int(point.y)), 2)
            if lastPoint != None:
                pygame.draw.line(window, (0,0,0), lastPoint, point)
            lastPoint = point
            self.temp = self.temp.next

    def free(self):
        del(self)

class Node():
    def __init__(self, pos):
        self.pos = pos
        self.occupied = False
        self.next = None
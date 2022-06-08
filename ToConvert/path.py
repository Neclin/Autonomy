import pygame

class Path():
    def __init__(self):
        self.head = None
        self.tail = None
        
    # adds a node to the end of the path
    def addNode(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    # adds a node to the beginning of the path            
    def addNodeStart(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head = node

    # draws the path
    def show(self, window):
        self.temp = self.head
        lastPoint = None
        start = True

        # loops throught the path until the end
        while self.temp != None and (self.temp.next != self.head or start): # checks for loops
            start = False
            point = self.temp.pos
            # draws a line between neighboring points
            if lastPoint != None:
                pygame.draw.line(window, (0,0,0), lastPoint, point)
            # increments last point and the next node
            lastPoint = point
            self.temp = self.temp.next

    def free(self):
        del(self)

class Node():
    def __init__(self, pos):
        self.pos = pos
        self.occupied = False
        self.next = None
import pygame

from level import Level
from path import Path, Node
from conveyor import Conveyor
from settings import cellSize

class Placer():

    rotation = 0
    startPos = None
    anchor = None
    
    points = []

    @classmethod
    def getCoord(self, x, y):
        return pygame.Vector2((x - Level.offset.x) // cellSize, (y - Level.offset.y) // cellSize)
    
    @classmethod
    def getWindowPos(self, x, y):
        return pygame.Vector2(x * cellSize + Level.offset.x, y * cellSize + Level.offset.y)

    @classmethod
    def conveyor(self, x = None, y = None, type = None, rotation = None):
        if x == None and y == None:
            pos = pygame.mouse.get_pos()
            pos = self.getCoord(pos[0], pos[1])
        else:
            pos = pygame.Vector2(x, y)
        
        if rotation == None:
            rotation = self.rotation
        
        if Level.array[int(pos.y)][int(pos.x)] == 0:
            conveyor = Conveyor(int(pos.x), int(pos.y), 0, rotation)
            conveyor.getPorts(Level)
            point1, point2 = self.conveyorPathPoints(conveyor, rotation)
            node1 = Node(point1)
            node2 = Node(point2)
            if conveyor.loader == None and conveyor.ejector == None: # start a new path
                path = Path()
                path.addNode(node1)
                path.addNode(node2)
                conveyor.path = path
                Level.paths.append(path)
                
            elif conveyor.loader != None and conveyor.ejector != None:
                print("test 1")
                conveyor.loader.path.addNode(node1)
                conveyor.loader.path.addNode(node1)
                print("test 2")
                if conveyor.ejector.path != conveyor.loader.path:
                    print("test 3")
                    while conveyor.ejector.path.head != None:
                        conveyor.loader.path.addNode(conveyor.ejector.path.head)
                        conveyor.ejector.path.head = conveyor.ejector.path.head.next
                    Level.paths.remove(conveyor.ejector.path)
                else:
                    conveyor.loader.path.tail.next = conveyor.loader.path.head
                print("test 4")
                
            elif conveyor.loader != None: # add to the end of an existing path
                conveyor.loader.path.addNode(node1)
                conveyor.loader.path.addNode(node2)
                conveyor.path = conveyor.loader.path
            
            elif conveyor.loader == None: # add to the start of an existing path
                conveyor.ejector.path.addNodeEnd(node2)
                conveyor.ejector.path.addNodeEnd(node1)
                conveyor.path = conveyor.ejector.path
            
                
            Level.conveyors.append(conveyor)
            Level.array[int(pos.y)][int(pos.x)] = conveyor
    
    @classmethod
    def conveyorPathPoints(self, conveyor, rotation):
        topLeft = self.getWindowPos(conveyor.x, conveyor.y)
        if rotation == 0:
            point1 = pygame.Vector2(topLeft.x + 8, topLeft.y + 16)
            point2 = pygame.Vector2(topLeft.x + 24, topLeft.y + 16)
        elif rotation == 90:
            point1 = pygame.Vector2(topLeft.x + 16, topLeft.y + 24)
            point2 = pygame.Vector2(topLeft.x + 16, topLeft.y + 8)
        elif rotation == 180:
            point1 = pygame.Vector2(topLeft.x + 24, topLeft.y + 16)
            point2 = pygame.Vector2(topLeft.x + 8, topLeft.y + 16)
        elif rotation == 270:
            point1 = pygame.Vector2(topLeft.x + 16, topLeft.y + 8)
            point2 = pygame.Vector2(topLeft.x + 16, topLeft.y + 24)
        return point1, point2
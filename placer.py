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
    def getWindowPoint(self, x, y):
        return pygame.Vector2(x * cellSize + Level.offset.x, y * cellSize + Level.offset.y)
    
    @classmethod
    def getBuildingAtPoint(self, x, y):
        arrayPoint = self.getCoord(x, y)
        return Level.array[arrayPoint.y][arrayPoint.x]
    
    @classmethod
    def getBuildingAtPos(self, pos):
        arrayPoint = self.getCoord(pos.x, pos.y)
        return Level.array[int(arrayPoint.y)][int(arrayPoint.x)]

    @classmethod
    def conveyor(self, x = None, y = None, variation = None, rotation = None):
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
            
            if conveyor.loader != None:
                if conveyor.loader != self.getBuildingAtPos(conveyor.loader.path.tail.pos):
                    conveyor.loader = None
            
            if conveyor.ejector != None:
                if conveyor.ejector != self.getBuildingAtPos(conveyor.ejector.path.head.pos):
                    conveyor.ejector = None
            
            point1, point2 = self.conveyorPathPoints(conveyor, rotation)
            node1 = Node(point1)
            node2 = Node(point2)
            self.points.append(point1)
            self.points.append(point2)
            if conveyor.loader == None and conveyor.ejector == None: # start a new path
                path = Path()
                path.addNode(node1)
                path.addNode(node2)
                conveyor.path = path
                Level.paths.append(path)
                
            elif conveyor.loader != None and conveyor.ejector != None: # connect two paths
                conveyor.loader.path.addNode(node1)
                conveyor.loader.path.addNode(node2)
                if conveyor.ejector.path != conveyor.loader.path:
                    conveyorsToChange = []
                    while conveyor.ejector.path.head != None:
                        conveyor.loader.path.addNode(conveyor.ejector.path.head)
                        
                        building = self.getBuildingAtPos(conveyor.ejector.path.head.pos)
                        if type(building) == Conveyor:
                            if building.path == conveyor.ejector.path: # checks if the path is the old path
                                conveyorsToChange.append(building) # stores any that need to change to be changed after so no loops are caused
                        
                        conveyor.ejector.path.head = conveyor.ejector.path.head.next
                    # removes the old path so its not using space
                    Level.paths.remove(conveyor.ejector.path)
                    # changes the path of all conveyors with the old path
                    for conveyor_ in conveyorsToChange:
                        conveyor_.path = conveyor.loader.path
                else:
                    conveyor.loader.path.addNode(node1)
                    conveyor.loader.path.addNode(node2)
                    conveyor.loader.path.tail.next = conveyor.loader.path.head
                
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
        topLeft = self.getWindowPoint(conveyor.x, conveyor.y)
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
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

    @classmethod # gets the x and y index in the array for a point
    def getCoord(self, x, y): 
        return pygame.Vector2((x - Level.offset.x) // cellSize, (y - Level.offset.y) // cellSize)
    
    @classmethod # returns the top left position of the x and y index of the array
    def getWindowPoint(self, x, y): 
        return pygame.Vector2(x * cellSize + Level.offset.x, y * cellSize + Level.offset.y)
    
    @classmethod # returns the element at the x and y index of the array from a x and y point
    def getBuildingAtPoint(self, x, y):
        arrayPoint = self.getCoord(x, y)
        return Level.array[arrayPoint.y][arrayPoint.x]
    
    @classmethod # overload for getBuildingAtPoint for a vector point instead of x and y
    def getBuildingAtPos(self, pos):
        arrayPoint = self.getCoord(pos.x, pos.y)
        return Level.array[int(arrayPoint.y)][int(arrayPoint.x)]

    # places a conveyor with the given x and y or the mouse position if not specified
    @classmethod # parrameters are only used when loading a level and calling the function 
    def conveyor(self, x = None, y = None, variation = None, rotation = None):
        if x == None and y == None: # if x and y are not specified use the mouse position
            pos = pygame.mouse.get_pos()
            pos = self.getCoord(pos[0], pos[1]) # gets the x and y indexs at that point
        else:
            pos = pygame.Vector2(x, y) # if specified make x and y a 2d vector
        
        if rotation == None: # sets the rotaion if not specified
            rotation = self.rotation
            
        # checks the position is empty
        if Level.array[int(pos.y)][int(pos.x)] == None:
            # creates a conveyor at the position and gets the ejector and loader
            conveyor = Conveyor(int(pos.x), int(pos.y), 0, rotation)
            conveyor.getPorts(Level)
            
            # checks the loader exists and that it is the end of a path
            if conveyor.loader != None:
                if conveyor.loader != self.getBuildingAtPos(conveyor.loader.path.tail.pos):
                    conveyor.loader = None
            
            # checks the ejector exists and that it is the end of a path
            if conveyor.ejector != None:
                if conveyor.ejector != self.getBuildingAtPos(conveyor.ejector.path.head.pos):
                    conveyor.ejector = None
            
            # creates 2 points for nodes to be created to add to the path
            point1, point2 = self.conveyorPathPoints(conveyor, rotation)

            # creates 2 nodes at the points
            node1 = Node(point1)
            node2 = Node(point2)

            # used to draw the points on the screen - debug
            self.points.append(point1)
            self.points.append(point2)

            # all configurations a conveyor can be added
            if conveyor.loader == None and conveyor.ejector == None: # start a new path
                path = Path() # makes a new path
                path.addNode(node1) # adds both nodes to the path
                path.addNode(node2)
                conveyor.path = path # sets the path to the conveyor
                Level.paths.append(path) # adds it to the list of paths in the level
                
            elif conveyor.loader != None and conveyor.ejector != None: # connect two paths
                conveyor.loader.path.addNode(node1) # adds both nodes to the loader path
                conveyor.loader.path.addNode(node2)
                # checks the path is not a loop
                if conveyor.ejector.path != conveyor.loader.path:
                    conveyorsToChange = [] # used to store the conveyors to change

                    # loops through the paths
                    while conveyor.ejector.path.head != None:
                        conveyor.loader.path.addNode(conveyor.ejector.path.head)
                        
                        building = self.getBuildingAtPos(conveyor.ejector.path.head.pos)
                        if type(building) == Conveyor:
                            if building.path == conveyor.ejector.path: # checks if the path is the old path
                                conveyorsToChange.append(building) # stores any that need to change to be changed after so no loops are caused
                        # iterates to the next node
                        conveyor.ejector.path.head = conveyor.ejector.path.head.next

                    # removes the old path so its not using space
                    Level.paths.remove(conveyor.ejector.path)

                    # changes the path of all conveyors with the old path
                    for conveyor_ in conveyorsToChange:
                        conveyor_.path = conveyor.loader.path

                # the conveyor is a loop
                else:
                    conveyor.loader.path.addNode(node1) # adds both nodes to the loader path
                    conveyor.loader.path.addNode(node2)
                    conveyor.loader.path.tail.next = conveyor.loader.path.head # makes the list into a loop
                
            elif conveyor.loader != None: # add to the end of an existing path
                conveyor.loader.path.addNode(node1) # adds both nodes to the end of the path
                conveyor.loader.path.addNode(node2)
                conveyor.path = conveyor.loader.path # sets the conveyors path to be the same as the loader path
            
            elif conveyor.loader == None: # add to the start of an existing path
                conveyor.ejector.path.addNodeStart(node2) # adds bothe nodes in reverse order to the start of the path
                conveyor.ejector.path.addNodeStart(node1)
                conveyor.path = conveyor.ejector.path # sets the conveyors path to be the same as the ejectors path
            
            # adds the conveyor to the list of conveyors and sets it position in the array
            Level.conveyors.append(conveyor)
            Level.array[int(pos.y)][int(pos.x)] = conveyor
    
    @classmethod # generates points for each conveyor depending onm the rotaion and type
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
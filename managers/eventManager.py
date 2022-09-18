from turtle import left
import pygame
import math

from managers.placer import Placer
from item import Item
from managers.level import Level
from managers.renderer import Renderer
from buildings.belt import Belt

class EventManager():
    running = True
    start = True
    speed = 3
    leftMouseDown = False
    rightMouseDown = False
    checkRotation = False
    lastMousePos = pygame.Vector2(0,0)
    lastArrayPos = pygame.Vector2(0,0)

    @classmethod
    def checkEvents(self):
        # get the mouse pos and converts to a vector
        mousePos = pygame.mouse.get_pos()
        mousePos = pygame.Vector2(mousePos[0], mousePos[1])
        arrayPos = Placer.getCoord(mousePos.x, mousePos.y)

        mouseDirectionChanged = False
        arrayPosChanged = False

        x = abs((self.lastMousePos.x - mousePos.x) * Placer.mouseDirection.y)
        y = abs((self.lastMousePos.y - mousePos.y) * Placer.mouseDirection.x)

        if x+y >= 1:
            if (mousePos - self.lastMousePos) != pygame.Vector2(0, 0):
                mouseDirection = (mousePos - self.lastMousePos).normalize()

                # cast into cardinal directions
                if abs(mouseDirection.x) > abs(mouseDirection.y): # prioritises horizontal
                    mouseDirection.x = math.copysign(1, mouseDirection.x)
                    mouseDirection.y = 0
                else:                                             # prioritises vertical
                    mouseDirection.x = 0
                    mouseDirection.y = math.copysign(1, mouseDirection.y)

                Placer.mouseDirection = mouseDirection 
            self.lastMousePos = mousePos
            mouseDirectionChanged = True
        
        if self.lastArrayPos != arrayPos:
            self.lastArrayPos = arrayPos
            if (mousePos - self.lastMousePos) != pygame.Vector2(0, 0):
                mouseDirection = (mousePos - self.lastMousePos).normalize()
                if Placer.activeBuilding and (mouseDirection.x != -Placer.activeBuilding.startDirection.x or mouseDirection.y != -Placer.activeBuilding.startDirection.y):
                    Placer.rotation = mouseDirection.angle_to((1,0))
                    Placer.activeBuilding.endDirection = mouseDirection
                    Placer.activeBuilding.resetNext()
                    Placer.activeBuilding.update()
        
            Placer.activeBuilding = None
            arrayPosChanged = True

        # gets all active events from the pygame library
        for event in pygame.event.get():
            # checks if the X is pressed and quits the program
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                quit()
            
            # checks all keyboard events 
            elif event.type == pygame.KEYDOWN:
                # checks if escape is pressed and quits the program when in full screen mode
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    pygame.quit()
                    quit()
                
                # sets the rotaion of the placer module
                if event.key == pygame.K_r:
                    if isinstance(Placer.active, Belt) and self.leftMouseDown: # special rule for belts
                        self.checkRotation = True
                    else:
                        Placer.rotation -= 90
                        Placer.rotation %= 360

                # debugging for items - places items on last belt
                if event.key == pygame.K_b:
                    building = Level.array[int(arrayPos.y)][int(arrayPos.x)]
                    if isinstance(building, Belt):
                        item = Item(building.points[0], 0)
                        item.belt = building
                        Level.items.append(item)
                
                # saves the current state of the level - not finaliesed
                if event.key == pygame.K_s:
                    f = open("levels/save.txt","w")
                    f.write(str(Level.width)+","+str(Level.height)+"\n")
                    for belt in Level.belts:
                        f.write("belt "+str(belt.x)+" "+str(belt.y)+" "+str(belt.type)+" "+str(belt.rotation)+" "+str(int(belt.directionVector.x))+","+str(int(belt.directionVector.y))+" "+str(belt.vel)+"\n")
                    f.close()

                if event.key == pygame.K_UP:
                    self.speed += 1
                if event.key == pygame.K_DOWN:
                    self.speed -= 1
            
            # checks mouse presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # checks if the left mouse button is pressed and enbables the placer function
                if event.button == 1:
                    self.leftMouseDown = True
                    Placer.startPos = arrayPos

                    for button in Level.buttons:
                        if button.isPressed():
                            pass

                # checks if the right mouse button is pressed and enables the placer function
                if event.button == 3:
                    self.rightMouseDown = True
            
            # checks if mouse is released
            elif event.type == pygame.MOUSEBUTTONUP:
                # checks if the left mouse button is pressed and disables the placer function
                if event.button == 1:
                    self.leftMouseDown = False
                    Placer.startPos = None
                    Placer.activeBuilding = None

                # checks if the right mouse button is pressed and disables the placer function
                if event.button == 3:
                    self.rightMouseDown = False


        if EventManager.leftMouseDown and Renderer.isPointInGrid(mousePos):
            directionVector = Placer.getVectorFromAngle(Placer.rotation)
            if not Placer.activeBuilding:
                Placer.activeBuilding = Placer.active.place(arrayPos.x, arrayPos.y, directionVector, directionVector, self.speed) 
            else:
                if mouseDirectionChanged and (mouseDirection.x != -Placer.activeBuilding.startDirection.x or mouseDirection.y != -Placer.activeBuilding.startDirection.y):
                    Placer.rotation = mouseDirection.angle_to((1,0))
                    Placer.activeBuilding.endDirection = mouseDirection
                    Placer.activeBuilding.resetNext()
                    Placer.activeBuilding.update()
            
        if EventManager.rightMouseDown and Renderer.isPointInGrid(mousePos):
            building = Level.array[int(arrayPos.y)][int(arrayPos.x)]
            if building != None:
                building.remove()

        # rotation based on belt direction
        if self.checkRotation:
            pass

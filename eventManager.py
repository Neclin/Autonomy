from tkinter import Place
from turtle import speed
import pygame

from placer import Placer
from item import Item
from level import Level
from renderer import Renderer
from belt import Belt

class EventManager():
    running = True
    start = True
    speed = 3
    leftMouseDown = False
    rightMouseDown = False

    @classmethod
    def checkEvents(self):
        # get the mouse pos and converts to a vector
        mousePos = pygame.mouse.get_pos()
        mousePos = pygame.Vector2(mousePos[0], mousePos[1])
        arrayPos = Placer.getCoord(mousePos.x, mousePos.y)

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
                
                # sets the roation of the placer module
                if event.key == pygame.K_r:
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
                        f.write("belt "+str(belt.x)+" "+str(belt.y)+" "+"0 "+str(belt.rotation)+"\n")
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
                    Place.startPos = mousePos

                    for button in Level.buttons:
                        if button.isPressed():
                            pass

                # checks if the right mouse button is pressed and enbables the placer function
                if event.button == 3:
                    self.rightMouseDown = True
            
            # checks if mouse is released
            elif event.type == pygame.MOUSEBUTTONUP:
                # checks if the left mouse button is pressed and disables the placer function
                if event.button == 1:
                    self.leftMouseDown = False
                    Place.startPos = None

                # checks if the right mouse button is pressed and disables the placer function
                if event.button == 3:
                    self.rightMouseDown = False

        #
        #____________________________________________________

        if EventManager.leftMouseDown and Renderer.isPointInGrid(mousePos):

            Placer.active.place(arrayPos.x, arrayPos.y, 0, Placer.rotation, Placer.getVectorFromAngle(Placer.rotation), self.speed)
            
        if EventManager.rightMouseDown and Renderer.isPointInGrid(mousePos):
            building = Level.array[int(arrayPos.y)][int(arrayPos.x)]
            if building != None:
                building.remove()
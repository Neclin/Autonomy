import pygame

from placer import Placer
from item import Item
from level import Level

class EventManager():
    running = True
    start = True
    leftMouseDown = False
    rightMouseDown = False

    @classmethod
    def checkEvents(self):
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
                
                # saves the current state of the level - not finaliesed
                if event.key == pygame.K_s:
                    f = open("levels/save.txt","w")
                    f.write(str(Level.width)+","+str(Level.height)+"\n")
                    for belt in Level.belts:
                        f.write("belt "+str(belt.x)+" "+str(belt.y)+" "+"0 "+str(belt.rotation)+"\n")
                    f.close()
            
            # checks mouse presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # checks if the left mouse button is pressed and enbables the placer function
                if event.button == 1:
                    self.leftMouseDown = True

                # checks if the right mouse button is pressed and enbables the placer function
                if event.button == 3:
                    self.rightMouseDown = True
            
            # checks if mouse is released
            elif event.type == pygame.MOUSEBUTTONUP:
                # checks if the left mouse button is pressed and disables the placer function
                if event.button == 1:
                    self.leftMouseDown = False

                # checks if the right mouse button is pressed and disables the placer function
                if event.button == 3:
                    self.rightMouseDown = False

import pygame

from settings import screenHeight, screenWidth, cellSize
from GUI.button import Button

class Level():

    array = []
    width = 0
    height = 0

    offset = None

    items = []
    belts = []
    paths = []

    buttons = []
    buttonList = ["belt", "forge"]

    @classmethod # loads the level from a file
    def loadLevel(self, directory, Placer):
        with open(directory) as f:
            # first line of the file is the dimensions of the level
            dimensions = f.readline().split(',')
            self.width = int(dimensions[0])
            self.height = int(dimensions[1])
            # calculates the offset of the level so it is in the center
            self.offset = pygame.Vector2(screenWidth/2 - (self.width * cellSize)/2, screenHeight/2 - (Level.height * cellSize)/2)

            # create an empty array
            self.array = [[None for x in range(self.width)] for y in range(self.height)]

            # creates the buttons for the level
            for index in range(len(self.buttonList)):
                offset = (screenWidth - 100 * len(self.buttonList)) // 2
                button = Button(pygame.Vector2(offset + 100 * index, screenHeight-100), self.buttonList[index])
                self.buttons.append(button)

            # reads each line and uses the first word to determine what to do
            for line in f:
                line = line.split(" ")
                if line[0] == "belt":
                    # adds a belt to the level
                    startDirection = line[3].split(",")
                    startDirection = pygame.Vector2(int(startDirection[0]), int(startDirection[1]))
                    endDirection = line[4].split(",")
                    endDirection = pygame.Vector2(int(endDirection[0]), int(endDirection[1]))
                    Placer.belt.place(int(line[1]), int(line[2]), startDirection, endDirection, int(line[5]))
    
    @classmethod
    def saveLevel(self, directory):
        with open(directory, "w") as f:
            f.write(str(Level.width)+","+str(Level.height)+"\n")
            for belt in Level.belts:
                startDirectionStr = str(int(belt.startDirection.x))+","+str(int(belt.startDirection.y))
                endDirectionStr = str(int(belt.endDirection.x))+","+str(int(belt.endDirection.y))
                f.write(f"belt {belt.x} {belt.y} {startDirectionStr} {endDirectionStr} {belt.vel}\n")

        print("saved")
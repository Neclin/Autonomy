from gameObject import GameObject
from placement import insertGameObjects

from settings import SCREENWIDTH, SCREENHEIGHT

def loadMainMenu(world):
    world.state = "MainMenu"
    for gameObject in world.gameObjects:
        world.removeGameObject(gameObject)

    rootContainer = Container(50, 50, SCREENWIDTH-100, SCREENHEIGHT-100, (51,51,51), (31,31,31))
    insertGameObjects(rootContainer, world)
    world.containers.append(rootContainer)

    titleHeight = 100
    width = 200
    height = 350
    x = (SCREENWIDTH-width)//2
    y = (SCREENHEIGHT-height-titleHeight)//2
    centralContainer = Container(x, y+titleHeight, width, height, (51,51,51))
    rootContainer.addChild(centralContainer)

    title = GameObject(50, 50, SCREENWIDTH-100, titleHeight, (51,51,51), (31,31,31), text="Autonomy")
    rootContainer.addChild(title)

    playButton = Button(0, 0, 0, 0, (51,51,51), (31,31,31), text="play")
    playButton.onClick = lambda: world.load("levels/level1.txt")
    leaderboardButton = Button(0, 0, 0, 0, (51,51,51), (31,31,31), text="leaderboard")
    settingsButton = Button(0, 0, 0, 0, (51,51,51), (31,31,31), text="settings")
    quitButton = Button(0, 0, 0, 0, (51,51,51), (31,31,31), text="quit")

    centralContainer.addChild(playButton)
    centralContainer.addChild(leaderboardButton)
    centralContainer.addChild(settingsButton)
    centralContainer.addChild(quitButton)
    centralContainer.sortVertical(10)

def loadLevelSelect(world):
    world.state = "LevelSelect"
    for gameObject in world.gameObjects:
        world.removeGameObject(gameObject)

    rootContainer = Container(50, 50, SCREENWIDTH-100, SCREENHEIGHT-100, (51,51,51), (31,31,31))
    insertGameObjects(rootContainer, world)
    world.containers.append(rootContainer)


class Container(GameObject):
    def __init__(self, x, y, width, height, colour, borderColour=None):
        super().__init__(x, y, width, height, colour, borderColour, type="Container")
        self.children = []
        self.layer = 10
        self.screenPinned = True

    def addChild(self, child):
        self.children.append(child)

    def removeChild(self, child):
        if child in self.children:
            self.children.remove(child)
        else:
            print("Child not found")
    
    def sortHorizontal(self, gap):
        totalGap = gap * (len(self.children)+1)
        width = (self.width - totalGap)//len(self.children)
        height = self.height - gap*2
        for i, child in enumerate(self.children):
            child.width = width
            child.height = height
            child.worldPosition.x = self.worldPosition.x + gap + (width + gap) * i
            child.worldPosition.y = self.worldPosition.y + gap
    
    def sortVertical(self, gap):
        totalGap = gap * (len(self.children)+1)
        height = (self.height - totalGap)//len(self.children)
        width = self.width - gap*2
        for i, child in enumerate(self.children):
            child.width = width
            child.height = height
            child.worldPosition.x = self.worldPosition.x + gap
            child.worldPosition.y = self.worldPosition.y + gap + (height + gap) * i

    def show(self, renderer, camera):
        super().show(renderer, camera)
        for child in self.children:
            child.show(renderer, camera)

    def checkMousePresses(self, mousePos):
        for child in self.children:
            if type(child) == Container:
                child.checkMousePresses(mousePos)
            else:
                child.checkPressed(mousePos)


class Button(GameObject):
    def __init__(self, x, y, width, height, colour, borderColour=None, onClick=None, text=""):
        super().__init__(x, y, width, height, colour, borderColour, type="Button", text=text)
        self.onClick = onClick
        self.layer = 10
        self.screenPinned = True

    def checkPressed(self, mousePos):
        if self.rect.collidepoint(mousePos):
            if self.onClick:
                self.onClick()
from gameObject import GameObject
from placement import insertGameObjects

from settings import SCREENWIDTH, SCREENHEIGHT

def loadLevel(world, eventmanager, i):
    return lambda: world.load("levels/level "+str(i)+".txt", eventmanager)

def loadMainMenu(world, eventManager):
    world.state = "MainMenu"
    world.clearArrays(eventManager)

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
    title.screenPinned = True
    rootContainer.addChild(title)

    playButton = Button(0, 0, 0, 0, (51,51,51), (31,31,31), text="play")
    playButton.onClick = lambda: loadLevelSelect(world, eventManager)
    leaderboardButton = Button(0, 0, 0, 0, (51,51,51), (31,31,31), text="leaderboard")

    settingsButton = Button(0, 0, 0, 0, (51,51,51), (31,31,31), text="settings")
    settingsButton.onClick = lambda: loadSettings(world, eventManager)
    quitButton = Button(0, 0, 0, 0, (51,51,51), (31,31,31), text="quit")
    quitButton.onClick = lambda: eventManager.eventKill()

    centralContainer.addChild(playButton)
    centralContainer.addChild(leaderboardButton)
    centralContainer.addChild(settingsButton)
    centralContainer.addChild(quitButton)
    centralContainer.sortVertical(10)

def loadLevelSelect(world, eventManager):
    world.state = "LevelSelect"
    world.clearArrays(eventManager)

    margin = 25
    titleHeight = 100
    backButtonWidth = 150
    filterBarHeight = 25

    rootContainer = Container(margin, margin, SCREENWIDTH-margin*2, SCREENHEIGHT-margin*2, (51,51,51), (31,31,31))
    insertGameObjects(rootContainer, world)
    world.containers.append(rootContainer)

    leftContainer = Container(margin*2, margin*2, rootContainer.width*(3/5)-margin, rootContainer.height-margin*2, (51,51,51), (31,31,31))
    rootContainer.addChild(leftContainer)
    rightContainer = Container(rootContainer.width*(3/5)+margin-2, margin*2, rootContainer.width*(2/5)-margin+2, rootContainer.height-margin*2, (51,51,51), (31,31,31))
    rootContainer.addChild(rightContainer)

    backButton = Button(leftContainer.worldPosition.x, leftContainer.worldPosition.y, backButtonWidth, titleHeight, (51,51,51), (31,31,31), text="Back")
    backButton.onClick = lambda: loadMainMenu(world, eventManager)
    leftContainer.addChild(backButton)
    levelSelectTitle = GameObject(leftContainer.worldPosition.x+backButtonWidth-2, leftContainer.worldPosition.y, leftContainer.width-backButtonWidth+2, titleHeight, (51,51,51), (31,31,31), text="Level Select")
    levelSelectTitle.screenPinned = True
    leftContainer.addChild(levelSelectTitle)
    filterContainer = Container(leftContainer.worldPosition.x, leftContainer.worldPosition.y+titleHeight-2, leftContainer.width, filterBarHeight+2, (51,51,51), (31,31,31))
    leftContainer.addChild(filterContainer)
    levelContainer = Container(leftContainer.worldPosition.x, leftContainer.worldPosition.y+titleHeight+filterBarHeight-4, leftContainer.width, leftContainer.height-titleHeight-filterBarHeight+4, (51,51,51), (31,31,31))
    leftContainer.addChild(levelContainer)

    graphTitle = GameObject(rightContainer.worldPosition.x, rightContainer.worldPosition.y, rightContainer.width, titleHeight, (51,51,51), (31,31,31), text="Graph")
    graphTitle.screenPinned = True
    rightContainer.addChild(graphTitle)
    graphContainer = Container(rightContainer.worldPosition.x, rightContainer.worldPosition.y+titleHeight-2, rightContainer.width, rightContainer.height-titleHeight+2, (51,51,51), (31,31,31))
    rightContainer.addChild(graphContainer) 

    speedGraph = GameObject(0, 0, 0, 0, (51,51,51), (31,31,31), text="speed")
    speedGraph.screenPinned = True
    sizeGraph = GameObject(0, 0, 0, 0, (51,51,51), (31,31,31), text="size")
    sizeGraph.screenPinned = True
    efficiencyGraph = GameObject(0, 0, 0, 0, (51,51,51), (31,31,31), text="efficiency")
    efficiencyGraph.screenPinned = True
    graphContainer.addChild(speedGraph)
    graphContainer.addChild(sizeGraph)
    graphContainer.addChild(efficiencyGraph)

    graphContainer.sortVertical(margin)

    for i in range(1, 15):
        levelButton = Button(0, 0, 0, 0, (51,51,51), (31,31,31), text="level "+str(i))
        levelButton.onClick = loadLevel(world, eventManager, i)
        levelContainer.addChild(levelButton)

    levelContainer.sortVertical2Rows(margin)


def loadSettings(world, eventManager):
    world.state = "Settings"
    world.clearArrays(eventManager)

    margin = 25
    navBarHeight = 50

    rootContainer = Container(margin, margin, SCREENWIDTH-margin*2, SCREENHEIGHT-margin*2, (51,51,51), (31,31,31))
    insertGameObjects(rootContainer, world)
    world.containers.append(rootContainer)

    navBar = Container(margin*2, margin*2, rootContainer.width-margin*2, navBarHeight, (51,51,51), (31,31,31))
    rootContainer.addChild(navBar)
    backButton = Button(0, 0, 0, 0, (51,51,51), (31,31,31), text="Back")
    backButton.onClick = lambda: loadMainMenu(world, eventManager)
    navBar.addChild(backButton)
    gameplayButton = Button(0, 0, 0, 0, (51,51,51), (31,31,31), text="Gameplay")
    navBar.addChild(gameplayButton)
    graphicsButton = Button(0, 0, 0, 0, (51,51,51), (31,31,31), text="Graphics")
    navBar.addChild(graphicsButton)
    audioButton = Button(0, 0, 0, 0, (51,51,51), (31,31,31), text="Audio")
    navBar.addChild(audioButton)
    controlsButton = Button(0, 0, 0, 0, (51,51,51), (31,31,31), text="Controls")
    navBar.addChild(controlsButton)
    navBar.sortHorizontal(0)

    settingsContainer = Container(margin*2, margin*2+navBarHeight-2, rootContainer.width-margin*2, rootContainer.height-margin*2-navBarHeight+2, (51,51,51), (31,31,31))
    rootContainer.addChild(settingsContainer)

    leftSettingsContainer = Container(settingsContainer.worldPosition.x, settingsContainer.worldPosition.y, settingsContainer.width*(2/3), settingsContainer.height, (51,51,51), (31,31,31))
    settingsContainer.addChild(leftSettingsContainer)
    rightSettingsContainer = Container(settingsContainer.worldPosition.x+settingsContainer.width*(2/3)-2, settingsContainer.worldPosition.y, settingsContainer.width*(1/3)+3, settingsContainer.height, (51,51,51), (31,31,31))
    settingsContainer.addChild(rightSettingsContainer)

def loadSettingsList(world, eventManager):
    pass

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
        totalGap = (gap-2) * (len(self.children)+1)
        width = (self.width - totalGap)//len(self.children)
        height = self.height - gap*2
        for i, child in enumerate(self.children):
            if i != len(self.children)-1:
                child.width = width
            else:
                child.width = width-2
            child.height = height
            child.worldPosition.x = self.worldPosition.x + gap + (width + gap-2) * i
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
    
    def sortVertical2Rows(self, gap):
        totalGap = gap * (len(self.children)/2+1)
        height = (self.height - totalGap)//(len(self.children)/2)
        width = (self.width - gap*3)//2
        for i, child in enumerate(self.children):
            child.width = width
            child.height = height
            child.worldPosition.x = self.worldPosition.x + gap + (width + gap) * (i%2)
            child.worldPosition.y = self.worldPosition.y + gap + (height + gap) * (i//2)

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
                print(self.text)
                self.onClick()
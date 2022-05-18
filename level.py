from conveyor import Conveyor

class Level():

    array = []
    width = 0
    height = 0

    conveyors = []

    @classmethod
    def loadLevel(self, path):
        with open(path) as f:
            dimensions = f.readline().split(',')
            for line in f:
                line = line.split(" ")
                if line[0] == "conveyor":
                    self.conveyors.append(Conveyor(int(line[1]), int(line[2]), int(line[3]), int(line[4])))
        self.width = int(dimensions[0])
        self.height = int(dimensions[1])

        # create an empty array
        self.array = [[0 for x in range(self.width)] for y in range(self.height)]

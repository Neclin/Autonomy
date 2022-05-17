class Level():

    array = []
    width = 0
    height = 0

    @classmethod
    def loadLevel(self, path):
        with open(path) as f:
            for line in f:
                line = line.strip("\n")
                line = line.split(',')
                self.array.append(line)
        self.height = len(self.array)
        self.width = len(self.array[0])
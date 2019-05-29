from Task.AbstractTask import AbstractTask
import configparser

class Ant:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.value = "®"
        self.front = "EAST"
        #Possible values are EAST, WEST, NORTH and South
        return

class ArtificialAnt(AbstractTask):
    """This is supposed to simulate the artificial ant problem, yet it is far from perfection"""
    def __init__(self):
        self.GRN = None
        h = 32
        w = 32
        self.board = [["." for x in range(w)] for y in range(h)]
        self.make_trail()
        self.score = 0
        self.ant = Ant()
        self.board[self.ant.x][self.ant.y] = self.ant.value
        self.max_move = 400
        self.move_count = 1

    def requirements(self):
        # first element is input count and the second element is the output count
        req = {
            "inputs": 1,
            "outputs": 3,
            "evolution": True
        }
        return req

    def gConfig():
        conf = {
        }
        return conf

    def setGRN(self, grn):
        self.GRN = grn

    def start(self):
        actionList = ["LEFT", "RIGHT", "MOVE"]
        while self.move_count < self.max_move:
            # set the inputs
            # self.GRN.reset()
            self.GRN.setInput(0, self.sense())
            self.GRN.regulate(10)
            # print()
            self.action(actionList[self.GRN.getOutput()])
        return self.score


    def action(self, value):
        # print(value)  
        if value == "LEFT":
            if self.ant.front == "NORTH":
                self.ant.front = "WEST"
            elif self.ant.front == "WEST":
                self.ant.front = "SOUTH"
            elif self.ant.front == "SOUTH":
                self.ant.front = "EAST"
            elif self.ant.front == "EAST":
                self.ant.front = "NORTH"
        elif value == "RIGHT":
            if self.ant.front == "NORTH":
                self.ant.front = "EAST"
            elif self.ant.front == "EAST":
                self.ant.front = "SOUTH"
            elif self.ant.front == "SOUTH":
                self.ant.front = "WEST"
            elif self.ant.front == "WEST":
                self.ant.front = "NORTH"
            pass
        elif value == "MOVE":
            if self.ant.front == "NORTH":
                if self.ant.x - 1 >= 0:
                    if self.board[self.ant.x - 1][self.ant.y] == "X":
                        self.score += 1
                    self.board[self.ant.x - 1][self.ant.y] = self.ant.value
                    self.board[self.ant.x][self.ant.y] = "."
                    self.ant.x -= 1
                else:
                    if self.board[31][self.ant.y] == "X":
                        self.score += 1
                    self.board[31][self.ant.y] = self.ant.value
                    self.board[self.ant.x][self.ant.y] = "."
                    self.ant.x = 31
            elif self.ant.front == "WEST":
                if self.ant.y - 1 >= 0:
                    if self.board[self.ant.x][self.ant.y - 1] == "X":
                        self.score += 1
                    self.board[self.ant.x][self.ant.y - 1] = self.ant.value
                    self.board[self.ant.x][self.ant.y] = "."
                    self.ant.y -= 1
                else:
                    if self.board[self.ant.x][31] == "X":
                        self.score += 1
                    self.board[self.ant.x][31] = self.ant.value
                    self.board[self.ant.x][self.ant.y] = "."
                    self.ant.y = 31
            elif self.ant.front == "SOUTH":
                if self.ant.x + 1 < 32:
                    if self.board[self.ant.x + 1][self.ant.y] == "X":
                        self.score += 1
                    self.board[self.ant.x + 1][self.ant.y] = self.ant.value
                    self.board[self.ant.x][self.ant.y] = "."
                    self.ant.x += 1
                else:
                    if self.board[31][self.ant.y] == "X":
                        self.score += 1
                    self.board[31][self.ant.y] = self.ant.value
                    self.board[self.ant.x][self.ant.y] = "."
                    self.ant.x = 31
            elif self.ant.front == "EAST":
                if self.ant.y + 1 < 32:
                    if self.board[self.ant.x][self.ant.y + 1] == "X":
                        self.score += 1
                    self.board[self.ant.x][self.ant.y + 1] = self.ant.value
                    self.board[self.ant.x][self.ant.y] = "."
                    self.ant.y += 1
                else:
                    if self.board[self.ant.x][0] == "X":
                        self.score += 1
                    self.board[self.ant.x][0] = self.ant.value
                    self.board[self.ant.x][self.ant.y] = "."
                    self.ant.y = 0
        self.move_count += 1
        # print("the ant is facing ", self.ant.front, " in the position of ", self.ant.x, " and ", self.ant.y)
        return

    def sense(self):
        if self.ant.front == "EAST":
            try:
                if self.board[self.ant.x][self.ant.y + 1] == "X":
                    return 1
                return 0
            except:
                if self.board[self.ant.x][0] == "X":
                    return 1
                return 0
        elif self.ant.front == "WEST":
            try:
                if self.board[self.ant.x][self.ant.y - 1] == "X":
                    return 1
                return 0
            except:
                if self.board[self.ant.x][31] == "X":
                    return 1
                return 0
        elif self.ant.front == "NORTH":
            try:
                if self.board[self.ant.x - 1][self.ant.y] == "X":
                    return 1
                return 0
            except:
                if self.board[31][self.ant.y] == "X":
                    return 1
                return 0
        elif self.ant.front == "SOUTH":
            try:
                if self.board[self.ant.x + 1][self.ant.y] == "X":
                    return 1
                return 0
            except:
                if self.board[0][self.ant.y] == "X":
                    return 1
                return 0
        return 0

    def make_trail(self):
        #first 20
        for i in range(4, 24):
            self.board[8][i] = "X"
        #next 21
        for i in range(9, 30):
            self.board[i][23] = "X"
        #next 9
        for i in range(14, 23):
            self.board[29][i] = "X"
        #next 17
        for i in range(12, 29):
            self.board[i][14] = "X"
        #next 3
        for i in range(11, 14):
            self.board[12][i] = "X"
        #next 10
        for i in range(13, 23):
            self.board[i][11] = "X"

    def show_board(self):
        for row in self.board:
            for item in row:
                print(item, end=' ')
            print('')

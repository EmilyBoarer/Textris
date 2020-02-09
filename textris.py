import random
import os
import time

def clear_screen():
    os.system("cls")

BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW2 = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_WHITE = "\033[1;37m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NEGATIVE = "\033[7m"
CROSSED = "\033[9m"
END = "\033[0m"

WIDTH = 10
HEIGHT = 20


class Square:
    def __init__(self, col):
        self.col = col
    def __str__(self):
        return self.col + "#"

class EmptySquare:
    def __str__(self):
        return " "

class Shape:
    def __init__(self, adj = [(-1,-1),(0,-1),(1,-1)], col = PURPLE, x=WIDTH//2, y=HEIGHT-2):
        self.x = x 
        self.y = y
        self.adj=adj
        self.col = col
    def place(self):
        canplace = True
        for a in self.adj+[(0,0)]:
            x = self.x+a[1] 
            y = self.y-a[0]
            print(x, y)
            if type(grid[y][x]) != EmptySquare: # if the target square is already occupied
                canplace = False
        if canplace:
            self.showingrid()
        return canplace
    def showingrid(self):
        grid[self.y][self.x] = Square(self.col)
        for a in self.adj:
            try:
                grid[self.y+a[1]][self.x+a[0]] = Square(self.col)
            except IndexError:# trying to show a piece that is not on screen
                pass
    def removefromgrid(self):
        grid[self.y][self.x] = EmptySquare()
        for a in self.adj:
            try:
                grid[self.y+a[1]][self.x+a[0]] = EmptySquare()
            except IndexError: # trying to show a piece that is not on screen
                pass
    def move(self):
        safe = True
        self.removefromgrid() # remove else it causes check issues
        for relpos in self.adj+[(0,0)]:
            x = self.x+relpos[0]
            y = self.y+relpos[1] - 1 # -1 is the new position
            if not type(grid[y][x]) == EmptySquare: # cannot move
                safe = False
            if y < 0:
                safe = False
        if safe: # move down 1
            self.y -= 1
            self.showingrid()
        else: # consolidate to grid as individual squares of this correct colour
            for relpos in self.adj+[(0,0)]:
                x = self.x+relpos[0]
                y = self.y+relpos[1]
                grid[y][x] = Square(self.col)
        return safe # true if it can be moved
    def rotate(self):
        self.removefromgrid()
        rta = True
        for a in self.adj+[(0,0)]:
            x = self.x+a[1] 
            y = self.y-a[0]
            if x > WIDTH-1: # rotate through right wall
                rta = False
            elif x < 0: # rotate through left wall
                rta = False
            elif y < 0 or y > HEIGHT - 1: # check the top and bottom of the 
                rta = False
            elif type(grid[y][x]) != EmptySquare: # if the target square is already occupied
                rta = False
        if rta:
            temp = []
            for a in self.adj:
                a = [a[1],-a[0]]
                temp.append(a)
            self.adj = temp
        self.showingrid()
    def side(self, dx):
        move = True
        for a in self.adj+[(0,0)]:
            x = self.x+a[0]
            if dx > 0 and x == WIDTH-1: # moving right
                move = False
            if dx < 0 and x == 0:
                move = False
        if move:
            self.removefromgrid()
            self.x += dx
            self.showingrid()

tetrominoes = [
    ([(-1,0),(1,0),(2,0)],CYAN),
    ([(-1,0),(0,1),(1,0)],PURPLE),
    ([(-1,-1),(-1,0),(1,0)],BLUE),
    ([(-1,1),(-1,0),(1,0)],YELLOW2),
    ([(-1,0),(-1,-1),(0,-1)],YELLOW),
    ([(1,0),(-1,-1),(0,-1)],GREEN),
    ([(-1,0),(0,-1),(1,-1)],RED),
]

grid = [[ EmptySquare() for _ in range(WIDTH)] for _ in range(HEIGHT)]

def display():
    clear_screen()
    print(RED+"TE"+YELLOW+"XT"+GREEN+"RI"+CYAN+"S\nS"+BLUE+"CO"+PURPLE+"RE: "+YELLOW2+str(score))
    print(DARK_GRAY+"="*(WIDTH+2))
    for row in grid[::-1]:
        print("|"+"".join([str(s) for s in row]) + DARK_GRAY + "|")
    print(DARK_GRAY+"="*(WIDTH+2)+END)

score = 0

random.shuffle(tetrominoes)
shuffcounter = 0
shuffcountermax = len(tetrominoes) - 1 
a1,a2 = tetrominoes[shuffcounter]
s = Shape(a1,a2)
s.place()
display()

running = True
while running: # mainloop
    m = input("Press Enter to drop, Space followed by Enter to rotate, A then Enter to move to the left, and D then Enter to the right")
    if m == " ":
        s.rotate()
    elif m.lower() == "a":
        s.side(-1)
    elif m.lower() == "d":
        s.side(1)
    else: # move down
        if not s.move():
            if s.y >= 18:
                running = False
            #check to see if can remove grid
            counter = 0
            removes = []
            for row in grid:
                full = True
                for squ in row:
                    if type(squ) == EmptySquare:
                        full = False
                if full:
                    removes.append(counter)
                counter += 1
            if len(removes) == 1:
                score += 40
            elif len(removes) == 2:
                score += 100
            elif len(removes) == 3:
                score += 300
            elif len(removes) >= 4: # just in case, although should only ever be equal to 4
                score += 1200
            for r in removes[::-1]:
                grid.pop(r) # pop the highest index first (else would mess with the following indexes)
                grid.append([EmptySquare() for _ in range(WIDTH)])
            
            shuffcounter += 1
            if shuffcounter > shuffcountermax:
                shuffcounter = 0
                random.shuffle(tetrominoes)
            a1,a2 = tetrominoes[shuffcounter]
            s = Shape(a1,a2)
            if not s.place(): # cannot place
                running = False
    display()

i=""
while i != "exit":
    i=input("type exit to close")



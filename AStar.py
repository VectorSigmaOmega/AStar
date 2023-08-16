import pygame
import sys

pygame.init()

HEIGHT = 700
WIDTH = 1000
CELL = 10
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (64, 224, 208)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (0, 0, 255)


class Cell:
    def __init__(self, x, y):
        self.font = pygame.font.SysFont('Arial', 25)
        self.x = x;
        self.y = y;
        self.distanceFromTop = y*CELL
        self.distanceFromLeft = x*CELL
        self.color = WHITE
        self.neighbours = []
        self.previous = None
        self.gScore = float("inf")
        self.hScore = float("inf")
        self.fScore = float("inf")

    def setStart(self):
        self.color = ORANGE

    def setEnd(self):
        self.color =  BLUE

    def makeBarrier(self):
        self.color = BLACK

    def isBarrier(self):
        return self.color == BLACK

    def clearCell(self):
        self.color = WHITE

    def drawCell(self):
        pygame.draw.rect(SCREEN, self.color, (self.distanceFromLeft, self.distanceFromTop, CELL, CELL))

    def atEnd(self):
        self.color = TURQUOISE

    def setClosed(self):
        self.color = RED

    def makePath(self):
        self.color = PURPLE

    def inOpenList(self):
        self.color = GREEN

    def findNeighbours(self, grid):
        if self.x > 0 and not grid[self.y][self.x - 1].isBarrier():
            self.neighbours.append(grid[self.y][self.x - 1])
        if self.x < ((WIDTH//CELL) - 1) and not grid[self.y][self.x + 1].isBarrier():
            self.neighbours.append(grid[self.y][self.x + 1])
        if self.y > 0 and not grid[self.y - 1][self.x].isBarrier():
            self.neighbours.append(grid[self.y - 1][self.x])
        if self.y < ((HEIGHT//CELL) - 1) and not grid[self.y + 1][self.x].isBarrier():
            self.neighbours.append(grid[self.y + 1][self.x])

def draw(grid):
    SCREEN.fill(WHITE)
    for y in grid:
        for x in y:
            x.drawCell()
    for i in range(WIDTH//CELL):
        pygame.draw.line(SCREEN, GREY, (0, i*CELL), (WIDTH, i*CELL))
        pygame.draw.line(SCREEN, GREY, (i*CELL, 0), (i*CELL, HEIGHT))
    pygame.display.flip()


def gridCells():
    grid = []
    for y in range((HEIGHT//CELL)):
        grid.append([])
        for x in range((WIDTH//CELL)):
            cell = Cell(x,y)
            grid[y].append(cell)
    return grid

def h(node, end):
    return abs(node.distanceFromTop - end.distanceFromTop) + abs(node.distanceFromLeft - end.distanceFromLeft)

def path(grid, end):
    current = end
    while current is not None:
        current.makePath()
        current = current.previous
    draw(grid)

def ssort(llist):

    if len(llist)>1:
        pivot = llist[0]
        left = []
        right = []
        count = len(llist)-1
        while(count!=0):
            if(llist[count][0]>pivot[0]):
                right.append(llist[count])
            elif(llist[count][0]<pivot[0]):
                left.append(llist[count])
            elif(llist[count][1]>pivot[1]):
                right.append(llist[count])
            elif(llist[count][0]<pivot[1]):
                left.append(llist[count])
            else:
                left.append(llist[count])
            count -= 1
        llist = ssort(left) + [pivot] + ssort(right)
        
    return llist
    

def astar(grid, start, end):
    count = 0
    openList = []
    openList = [[0, count, start]]
    start.gScore = 0
    start.fScore = h(start, end)
    openListHash = {start}
    
    while len(openList) != 0:
        current = openList[0][2]
        del openList[0]
        openListHash.remove(current)
        if current == end:
            path(grid, end)
            end.atEnd()
            start.atEnd()
            break

        for i in current.neighbours:
            if (current.gScore + 1) < i.gScore:
                i.previous = current
                i.gScore = current.gScore + 1
                i.fScore = i.gScore + h(i, end)

                if i not in openListHash:
                    count += 1
                    openListHash.add(i)
                    openList.append([i.fScore, count, i])
                    i.inOpenList()

        draw(grid)
        

        if current != start:
            current.setClosed()

        openList = ssort(openList)



def main():
    grid = gridCells()
    start = None
    end = None
    running = True
    while running:
        draw(grid)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.mouse.get_pressed()[0]:
            x , y = pygame.mouse.get_pos()
            cell = grid[(y//CELL)][(x//CELL)]
            if not start and cell != end:
                start = cell
                start.setStart()
            elif not end and cell != start:
                end = cell
                end.setEnd()
            elif cell != start and cell != end:
                cell.makeBarrier()
        elif pygame.mouse.get_pressed()[2]:

            x , y = pygame.mouse.get_pos()
            cell = grid[y//CELL][x//CELL]
            cell.clearCell()
            if cell == start:
               start = None
            elif cell == end:
               end = None


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT and start and end:
                for y in grid:
                    for x in y:
                        x.findNeighbours(grid)

                astar(grid, start, end)

            if event.key == pygame.K_LCTRL:
                start = None
                end = None
                grid = gridCells()
    pygame.quit()
    sys.exit()

main()
from pygame.locals import *
from random import randint
import pygame
import time
import heapq

"""
Queue used from Pacman project code
"""
class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

class Apple:
    """
    Apple class: Used for storing apple location
    """
    x = 0
    y = 0
    step = 44

    def __init__(self,x,y):
        """
        Initializes apple location using given x and y values
        """
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        """
        Draws apple
        """
        surface.blit(image,(self.x, self.y))


class Computer:
    """
    Computer class: Searches for apple and finds path to it using BFS, then makes move
    """
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3

    updateCountMax = 2
    updateCount = 0

    def __init__(self, length):
        """
        Initializes length of snake and creates body/head
        """
        self.length = length
        for i in range(0,235):
            self.x.append(-100)
            self.y.append(-100)

        # initial positions, no collision.
        self.x[0] = 1*44
        self.y[0] = 4*44

    def update(self):
        """
        moves snake based on given direction. Updates tail and head based on move
        """

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]

            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step

            self.updateCount = 0


    def moveRight(self):
        """
        Move snake Right
        """
        self.direction = 0

    def moveLeft(self):
        """
        Move snake Left
        """
        self.direction = 1

    def moveUp(self):
        """
        Move snake Up
        """
        self.direction = 2

    def moveDown(self):
        """
        Move snake Down
        """
        self.direction = 3

    def getSuccessors(self,newX,newY):
        """
        Checks if movement would cause the snake to die. Successors include full
        snake if moved in certain direction
        """
        d = [True,True,True,True]
        succ = []
        for i in range(1, self.length):
            if (((newX[0] + self.step) == newX[i]) and (newY[0] == newY[i])) or ((newX[0] + self.step) >= 800):
                d[0] = False
            if (((newX[0] - self.step) == newX[i]) and (newY[0] == newY[i])) or ((newX[0] - self.step) <= 0):
                d[1] = False
            if (((newY[0] - self.step) == newY[i]) and (newX[0] == newX[i])) or ((newY[0] - self.step) <= 0):
                d[2] = False
            if (((newY[0] + self.step) == newY[i]) and (newX[0] == newX[i])) or ((newY[0] + self.step) >= 600):
                d[3] = False
        #print(d)

        if d[0]:

            nx = [x for x in newX]
            ny = [y for y in newY]
            for i in range(self.length-1,0,-1):
                nx[i] = nx[i-1]
                ny[i] = ny[i-1]
            nx[0] += self.step
            succ.append(((nx[0],ny[0]),0,nx,ny))
        if d[1]:
            nx = [x for x in newX]
            ny = [y for y in newY]
            for i in range(self.length-1,0,-1):
                nx[i] = nx[i-1]
                ny[i] = ny[i-1]
            nx[0] -= self.step
            succ.append(((nx[0],ny[0]),1,nx,ny))
        if d[2]:
            nx = [x for x in newX]
            ny = [y for y in newY]
            for i in range(self.length-1,0,-1):
                nx[i] = nx[i-1]
                ny[i] = ny[i-1]
            ny[0] -= self.step
            succ.append(((nx[0],ny[0]),2,nx,ny))
        if d[3]:
            nx = [x for x in newX]
            ny = [y for y in newY]
            for i in range(self.length-1,0,-1):
                nx[i] = nx[i-1]
                ny[i] = ny[i-1]
            ny[0] += self.step
            succ.append(((nx[0],ny[0]),3,nx,ny))
        return succ

    def euclideanDistance(self, dx, dy, x, y):
        """
        Returns euclidean distance between x and y values
        """
        return ( (x - dx) ** 2 + (y - dy) ** 2 ) ** 0.5

    def target(self,dx,dy):
        """
        Finds apple using BFS, then makes a move in the direction of apple
        """

        startPosition = (self.x[0],self.y[0])
        # list of visited nodes for finding shortest path
        visited = []
        # queue for accessing nodes
        queue = Queue()
        # adds current node to visited list
        visited.append(startPosition)
        # path used to retrace steps from current node to start
        full_path = []
        newX = [x for x in self.x]
        newY = [y for y in self.y]
        # start off queue with starting node and starting path
        queue.push((startPosition,full_path,newX,newY))

        # start search using queue until no more paths are left
        while(not queue.isEmpty()):
            # gets the next node and path off of queue
            current,full_path,nx,ny = queue.pop()

            # adds current node to list of visited nodes
            visited.append(current)

            succ = self.getSuccessors(nx,ny)
            for element in succ:
                # makes sure element has not already been visited
                if(element[0] not in visited):
                    # if apple then make movement
                    if (element[0][0] == dx) and (element[0][1] == dy):
                        full_path = full_path + [element[1]]

                        if full_path[0] == 0:
                            self.moveRight()
                        elif full_path[0] == 1:
                            self.moveLeft()
                        elif full_path[0] == 2:
                            self.moveUp()
                        elif full_path[0] == 3:
                            self.moveDown()
                        return

                    # puts element and path to element in queue for further evaluation
                    queue.push((element[0],full_path + [element[1]],element[2],element[3]))
                    # add next item to visited
                    visited.append(element[0])

        return

    def draw(self, surface, image):
        """
        Draws Snake
        """
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i]))


class Game:
    """
    Checks if there is a collision between two points
    """
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 <= x2:
            if y1 >= y2 and y1 <= y2:
                return True
        if x1 > 800 or x1 < 0:
            return True
        if y1 > 600 or y1 < 0:
            return True
        return False

class App:
    """
    Main app class: Runs playthroughs
    """
    windowWidth = 800
    windowHeight = 600
    player = 0
    apple = 0

    def __init__(self):
        """
        Initializes running value, display values, game, score, apple location,
        and starting computer
        """
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.score = 0
        self.apple = Apple(8,5)
        self.computer = Computer(5)

    def on_init(self):
        """
        Sets up all display values and running values at start
        """
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.image.load("pygame.png").convert()
        self._apple_surf = pygame.image.load("apple.png").convert()

    def on_event(self, event):
        """
        Stops running cleanly if quit
        """
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        """
        Main loop: moves computer, checks if apple is gotten (if so creates new apple)
        Checks if computer dies or wins, ends running if so
        """
        self.computer.target(self.apple.x, self.apple.y)
        self.computer.update()

        # does computer eat apple?
        for i in range(0,self.computer.length):
            if self.game.isCollision(self.apple.x,self.apple.y,self.computer.x[i], self.computer.y[i],44):
                newApp = True
                self.score += 10

                while(newApp):
                    app_x = randint(1,17) * 44
                    app_y = randint(1,12) * 44
                    found = False
                    for j in range(0,self.computer.length):
                        if self.game.isCollision(app_x,app_y,self.computer.x[j], self.computer.y[j],44):
                            found = True
                    if not found:
                        self.apple.x = app_x
                        self.apple.y = app_y
                        newApp = False


                self.computer.length = self.computer.length + 1

        # does computer snake collide with itself?
        for i in range(1,self.computer.length):
            if self.game.isCollision(self.computer.x[0],self.computer.y[0],self.computer.x[i], self.computer.y[i],40):
                print("Computer loses! Collision: ")
                print("Score:", self.score)
                self._running = False
                break

        # is it a win
        if(self.computer.length >= 234):
            print("Computer wins!")
            print("Score:", self.score)
            self._running = False
        pass

    def on_render(self):
        """
        Renders all graphics for game
        """
        self._display_surf.fill((0,0,0))
        self.apple.draw(self._display_surf, self._apple_surf)
        self.computer.draw(self._display_surf, self._image_surf)
        pygame.display.flip()

    def on_cleanup(self):
        """
        Cleanly quits game
        """
        pygame.quit()

    def on_execute(self):
        """
        Parent loop: catches init if failed. Runs playthrough, Times playthrough
        Resets score
        """
        if self.on_init() == False:
            self._running = False
        startTime = time.perf_counter()

        while( self._running ):
            pygame.event.get()

            self.on_loop()
            self.on_render()

            time.sleep (50.0 / 1000.0);
        endTime = time.perf_counter()
        self.score = 0
        print(f"Time elapsed in seconds = {endTime-startTime:0.4f}")
        self.on_cleanup()

if __name__ == "__main__" :
    """
    Initializes number of games to be played, plays games
    """
    games = 10
    n = 0
    theApp = App()
    a = theApp
    while(n < games):
        a.on_execute()
        a = App()
        n+=1

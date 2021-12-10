from pygame.locals import *
from random import randint
import pygame
import time
import heapq

"""
Priority Queue used from Pacman code
"""
class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

class Apple:
    """
    Apple Class: Used for storage of apple information
    """
    x = 0
    y = 0
    step = 44

    def __init__(self,x,y):
        """
        Initializes apple location with given x and y values
        """
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        """
        Draws Apple
        """
        surface.blit(image,(self.x, self.y))


class Computer:
    """
    Computer class: Uses A* search to find apple and make a move towards it
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
        Initializes length of snake, along with snake head and tail
        """
        self.length = length
        self.x = [0]
        self.y = [0]
        for i in range(0,235):
            self.x.append(-100)
            self.y.append(-100)

       # initial positions, no collision.
        self.x[0] = 1*44
        self.y[0] = 4*44

    def update(self):

        """
        Updates head and tail locations based on movement
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
        Moves snake right
        """
        self.direction = 0

    def moveLeft(self):
        """
        Moves snake left
        """
        self.direction = 1

    def moveUp(self):
        """
        Moves snake up
        """
        self.direction = 2

    def moveDown(self):
        """
        Moves snake down
        """
        self.direction = 3

    def getSuccessors(self,newX,newY):
        """
        Checks if a movement will cause snake to collide with itself.
        Returns list of new moved snakes based on moves which don't kill snake
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
        Gets euclidean distance between given x and y pairs
        """
        return ( (x - dx) ** 2 + (y - dy) ** 2 ) ** 0.5

    def target(self,dx,dy):
        """
        Uses A* Search to find a best move for snake, then moves
        """

        startPosition = (self.x[0],self.y[0])
        # list of visited nodes for finding shortest path
        visited = []
        # priority queue for accessing nodes
        queue = PriorityQueue()
        # adds current node to visited list
        visited.append(startPosition)
        # path used to retrace steps from current node to start
        full_path = []
        newX = [x for x in self.x]
        newY = [y for y in self.y]
        # start off queue with starting node and starting path
        queue.push((startPosition,full_path,newX,newY,0),0)

        # start search using queue until no more paths are left
        while(not queue.isEmpty()):
            # gets the next node and path off of queue
            current,full_path,nx,ny,cost = queue.pop()

            # adds current node to list of visited nodes
            visited.append(current)
            succ = self.getSuccessors(nx,ny)
            for element in succ:
                # makes sure element has not already been visited
                if(element[0] not in visited):
                    # if apple found move snake
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
                    # sets priority to manhattan distance between position and closest food
                    priority = self.euclideanDistance(dx,dy,element[0][0],element[0][1])+cost+1
                    # puts element and path to element in queue for further evaluation
                    # with priority as euclidean distance + path cost distance
                    queue.push((element[0],full_path + [element[1]],element[2],element[3],cost + 1),priority)
                    # add next item to visited
                    visited.append(element[0])
        return

    def draw(self, surface, image):
        """
        Draws snake
        """
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i]))


class Game:
    """
    Checks if two points collide with each other
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
    Main app class: runs and renders games
    """
    windowWidth = 800
    windowHeight = 600
    player = 0
    apple = 0

    def __init__(self):
        """
        Initialize running, display items, game, score, starting apple, and computer
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
        Initializes pygame and all images, computer, and apple
        """
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)

        self.apple = Apple(8,5)
        self.computer = Computer(5)
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.image.load("pygame.png").convert()
        self._apple_surf = pygame.image.load("apple.png").convert()

    def on_event(self, event):
        """
        Stops running if quit chosen
        """
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        """
        Main loop: moves computer, checks if it found apple (if so make new apple)
        checks if computer collides with itself or wins
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
        Draws everything in game
        """
        self._display_surf.fill((0,0,0))
        self.apple.draw(self._display_surf, self._apple_surf)
        self.computer.draw(self._display_surf, self._image_surf)
        pygame.display.flip()

    def on_cleanup(self):
        """
        Quits cleanly
        """
        pygame.quit()

    def on_execute(self):
        """
        Main parent loop: catches problems with init, runs playthrough, times
        playthrough, resets score at end
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
    Initializes number of games. Runs playthroughs
    """
    games = 10
    n = 0
    theApp = App()
    a = theApp
    while(n < games):
        a.on_execute()
        n+=1

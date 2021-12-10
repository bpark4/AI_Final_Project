from pygame.locals import *
from random import randint
import pygame
import time
import heapq
import random


"""
Counter retrieved from Pacman project files
"""
class Counter(dict):
    """
    A counter keeps track of counts for a set of keys.

    The counter class is an extension of the standard python
    dictionary type.  It is specialized to have number values
    (integers or floats), and includes a handful of additional
    functions to ease the task of counting data.  In particular,
    all keys are defaulted to have value 0.  Using a dictionary:

    a = {}
    print(a['test'])

    would give an error, while the Counter class analogue:

    >>> a = Counter()
    >>> print(a['test'])
    0

    returns the default 0 value. Note that to reference a key
    that you know is contained in the counter,
    you can still use the dictionary syntax:

    >>> a = Counter()
    >>> a['test'] = 2
    >>> print(a['test'])
    2

    This is very useful for counting things without initializing their counts,
    see for example:

    >>> a['blah'] += 1
    >>> print(a['blah'])
    1

    The counter also includes additional functionality useful in implementing
    the classifiers for this assignment.  Two counters can be added,
    subtracted or multiplied together.  See below for details.  They can
    also be normalized and their total count and arg max can be extracted.
    """
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def incrementAll(self, keys, count):
        """
        Increments all elements of keys by the same count.

        >>> a = Counter()
        >>> a.incrementAll(['one','two', 'three'], 1)
        >>> a['one']
        1
        >>> a['two']
        1
        """
        for key in keys:
            self[key] += count

    def argMax(self):
        """
        Returns the key with the highest value.
        """
        if len(self.keys()) == 0: return None
        all = self.items()
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def sortedKeys(self):
        """
        Returns a list of keys sorted by their values.  Keys
        with the highest values will appear first.

        >>> a = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> a['third'] = 1
        >>> a.sortedKeys()
        ['second', 'third', 'first']
        """
        sortedItems = self.items()
        compare = lambda x, y:  sign(y[1] - x[1])
        sortedItems.sort(cmp=compare)
        return [x[0] for x in sortedItems]

    def totalCount(self):
        """
        Returns the sum of counts for all keys.
        """
        return sum(self.values())

    def normalize(self):
        """
        Edits the counter such that the total count of all
        keys sums to 1.  The ratio of counts for all keys
        will remain the same. Note that normalizing an empty
        Counter will result in an error.
        """
        total = float(self.totalCount())
        if total == 0: return
        for key in self.keys():
            self[key] = self[key] / total

    def divideAll(self, divisor):
        """
        Divides all counts by divisor
        """
        divisor = float(divisor)
        for key in self:
            self[key] /= divisor

    def copy(self):
        """
        Returns a copy of the counter
        """
        return Counter(dict.copy(self))

    def __mul__(self, y ):
        """
        Multiplying two counters gives the dot product of their vectors where
        each unique label is a vector element.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['second'] = 5
        >>> a['third'] = 1.5
        >>> a['fourth'] = 2.5
        >>> a * b
        14
        """
        sum = 0
        x = self
        if len(x) > len(y):
            x,y = y,x
        for key in x:
            if key not in y:
                continue
            sum += x[key] * y[key]
        return sum

    def __radd__(self, y):
        """
        Adding another counter to a counter increments the current counter
        by the values stored in the second counter.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> a += b
        >>> a['first']
        1
        """
        for key, value in y.items():
            self[key] += value

    def __add__( self, y ):
        """
        Adding two counters gives a counter with the union of all keys and
        counts of the second added to counts of the first.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a + b)['first']
        1
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] + y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = y[key]
        return addend

    def __sub__( self, y ):
        """
        Subtracting a counter from another gives a counter with the union of all keys and
        counts of the second subtracted from counts of the first.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a - b)['first']
        -5
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] - y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = -1 * y[key]
        return addend

class Apple:
    """
    Apple class: holds information on current Apple.
    """
    x = 0
    y = 0
    step = 44

    def __init__(self,x,y):
        """
        Initialize apple with parameters
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
    Computer Class: Runs policy Q-Values given by Trainer
    """
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3

    updateCountMax = 0
    updateCount = 0

    def __init__(self, length):
        """
        Initializes tail, head, starting length, apple location, and empty
        counter for policy
        """
        self.length = length
        self.x = [0]
        self.y = [0]
        for i in range(0,250):
            self.x.append(-100)
            self.y.append(-100)

        # initial positions, no collision.
        self.x[0] = 1*44
        self.y[0] = 4*44
        self.apple = []
        self.values = Counter()

    def updateApple(self, apple):
        """
        Updates apple with current apple coordinates
        """
        self.apple = apple

    def update(self):
        """
        Moves computers snake based on current direction of movement
        Updates tail and head
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
        Changes direction to right
        """
        self.direction = 0

    def moveLeft(self):
        """
        Changes direction to left
        """
        self.direction = 1

    def moveUp(self):
        """
        Changes direction to up
        """
        self.direction = 2

    def moveDown(self):
        """
        Changes direction to down
        """
        self.direction = 3

    def getLegalActions(self,state):
        """
        Checks if an action will cause the snake to run into itself of a wall
        Returns list of actions which do not kill the snake.
        """
        newX,newY = state
        d = [True,True,True,True]
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
        actions = []
        if d[0]:
            actions.append(0)
        if d[1]:
            actions.append(1)
        if d[2]:
            actions.append(2)
        if d[3]:
            actions.append(3)
        return actions

    def computeActionFromQValues(self):
        """
        Gets Q-Values for all legal actions, chooses best action.
        If there is a tie it chooses an action at random from tied actions
        """
        state = [self.x,self.y]
        legalActions = self.getLegalActions(state)
        maxQ = -9999999
        maxList = [0]
        for action in legalActions:
            qVal = self.getQValue(state,action)
            if(qVal > maxQ):
                maxQ = qVal
                maxList = [action]
            elif(qVal == maxQ):
                maxList.append(action)
        return random.choice(maxList)

    def getQValue(self,state,action):
        """
        Returns Q-Value with indexing as the snake head, whether the apple is
        right, down, up, left, and the desired action
        """
        newX = state[0][0]
        newY = state[1][0]
        finalState = (newX,newY)
        app = (self.isAppleX(),self.isAppleY())
        v = self.values[(finalState,app,action)]
        return v

    def isAppleX(self):
        """
        Checks if the apple is left, right, or center of snake head
        """
        if self.x[0] < self.apple[0]:
            return 1
        elif self.x[0] > self.apple[0]:
            return -1
        else:
            return 0

    def isAppleY(self):
        """
        Checks if the apple is up, down, or center of snake head
        """
        if self.y[0] < self.apple[1]:
            return 1
        elif self.y[0] > self.apple[1]:
            return -1
        else:
            return 0

    def go(self):
        """
        Chooses action based on policy, moves based on action
        """
        action = self.computeActionFromQValues()
        if action == 0:
            self.moveRight()
        if action == 1:
            self.moveLeft()
        if action == 2:
            self.moveUp()
        if action == 3:
            self.moveDown()

    def draw(self, surface, image):
        """
        Draws snake
        """
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i]))


class Game:
    """
    Checks if there is a collision between given x and y values
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

class Trainer:
    """
    Trainer class: Creates a Q-Value policy for the computer to use
    """
    def __init__(self,numTraining=1000, epsilon=0.5, alpha=0.2, gamma=1, values = Counter()):
        """
        Initializes:
        the number of training episodes (default 1000)
        epsilon (default 0.5)
        alpha (default 0.2)
        discount (default 1)
        Q-values (default empty Counter)

        Also initializes current training level, current score, previous score, snake length
        current state, previous state, and apple location
        """
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)
        self.values = values
        self.step = 44
        self.curTraining = 0
        self.curScore = 0
        self.lastScore = 0
        self.length = 0
        self.eOver = False
        self.curState = []
        self.lastState = []
        self.apple = []

    def isTraining(self):
        """
        Checks if the Trainer is still in training mode
        """
        if self.curTraining >= self.numTraining:
            return False
        else:
            return True

    def getQValue(self,state,action):
        """
        Gets current Q-Value for an action state pair, including relative location
        of apple
        """
        newX = state[0][0]
        newY = state[1][0]
        finalState = (newX,newY)
        app = (self.isAppleX(state),self.isAppleY(state))
        v = self.values[(finalState,app,action)]
        return v

    def getLegalActions(self,state):
        """
        Checks if action would run into tail or wall
        Returns list of actions which do not kill snake
        """
        newX,newY = state
        d = [True,True,True,True]
        for i in range(1, self.length):
            if (((newX[0] + self.step) == newX[i]) and (newY[0] == newY[i])) or ((newX[0] + self.step) > 800):
                d[0] = False
            if (((newX[0] - self.step) == newX[i]) and (newY[0] == newY[i])) or ((newX[0] - self.step) < 0):
                d[1] = False
            if (((newY[0] - self.step) == newY[i]) and (newX[0] == newX[i])) or ((newY[0] - self.step) < 0):
                d[2] = False
            if (((newY[0] + self.step) == newY[i]) and (newX[0] == newX[i])) or ((newY[0] + self.step) > 600):
                d[3] = False
        #print(d)
        newX = []
        newY = []
        actions = []
        if d[0]:
            actions.append(0)
        if d[1]:
            actions.append(1)
        if d[2]:
            actions.append(2)
        if d[3]:
            actions.append(3)
        return actions

    def computeActionFromQValues(self, state):
        """
        Finds best action based on Q-Values. If there is a tie chooses
        randomly between the tied values
        """
        legalActions = self.getLegalActions(state)
        maxQ = -9999999
        maxList = [0]
        for action in legalActions:
            qVal = self.getQValue(state,action)
            if(qVal > maxQ):
                maxQ = qVal
                maxList = [action]
            elif(qVal == maxQ):
                maxList.append(action)
        return random.choice(maxList)

    def getAction(self,state):
        """
        Chooses an actions, either random or based on Q-Value, based on epsilon
        """
        legalActions = self.getLegalActions(state)
        action = 0
        if(len(legalActions) == 0):
            return action
        else:
            r = random.random()
            flipResult = (r < self.epsilon)
            if(flipResult):
                action = random.choice(legalActions)
            else:
                action = self.computeActionFromQValues(state)
            return action

        return action

    def startEpisode(self,state,length):
        """
        Initializes the start of a training episode.
        Sets current state to given state.
        Current score to 0, previous score to 0, episode over to false,
        previous state to empty, length to given length, apple to random
        location.
        Increments training episode number
        """
        self.curState = state
        self.curScore = 0
        self.lastScore = 0
        self.eOver = False
        self.lastState = []
        self.length = length
        self.apple = [randint(1,17) * 44,randint(1,12) * 44]
        self.curTraining += 1

    def episodeEnd(self):
        """
        Checks if game is over based on collision with tail or win
        """
        state = self.curState
        for i in range(2,self.length):
            if self.isCollision(state[0][0],state[1][0],state[0][i],state[1][i],40):
                self.lastScore = self.curScore
                self.curScore -= 10
                return True

        # is it a win
        if(self.length >= 234):
            self.lastScore = self.curScore
            self.curScore += 100000
            return True

        return False

    def isCollision(self,x1,y1,x2,y2,bsize):
        """
        Checks if given x and y values collide with each other
        """
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        if x1 > 800 or x1 < 0:
            return True
        if y1 > 600 or y1 < 0:
            return True
        return False

    def doAction(self,state,action):
        """
        Updates snake based on given action.
        Updates previous position.
        Checks if it gets an apple, updates current score and previous score.
        Updates apple location
        """
        newX = [x for x in state[0]]
        newY = [y for y in state[1]]
        for i in range(self.length-1,0,-1):
            newX[i] = newX[i-1]
            newY[i] = newY[i-1]

        # update position of head of snake
        if action == 0:
            newX[0] = newX[0] + self.step
        if action == 1:
            newX[0] = newX[0] - self.step
        if action == 2:
            newY[0] = newY[0] - self.step
        if action == 3:
            newY[0] = newY[0] + self.step
        lastX = [x for x in state[0]]
        lastY = [y for y in state[1]]
        self.lastState = [lastX,lastY]
        self.curState = [newX,newY]
        for i in range(0,self.length):
            if self.isCollision(self.apple[0],self.apple[1],self.curState[0][i], self.curState[1][i],44):
                newApp = True
                n = 0
                #print("Finding New Apple")
                while(newApp and n < 100000):
                    app_x = randint(1,17) * 44
                    app_y = randint(1,12) * 44
                    found = False
                    for j in range(0,self.length):
                        if self.isCollision(app_x,app_y,self.curState[0][j], self.curState[1][j],44):
                            found = True
                    if not found:
                        self.apple[0] = app_x
                        self.apple[1] = app_y
                        newApp = False
                        #print("New Apple Found")
                    n += 1
                self.lastScore = self.curScore
                self.curScore += 10
                self.length = self.length + 1


    def nextStep(self):
        """
        Increments steps by doing action, checking if action ends game, and updating
        Q-values accordingly
        """
        state = self.curState
        action = self.getAction(state)
        self.doAction(state,action)
        self.eOver = self.episodeEnd()
        self.update(self.lastState,action,self.curState,self.curScore-self.lastScore)
        self.lastScore = self.curScore

    def episodeIsOver(self):
        """
        Checks if episode is over
        """
        if self.eOver:
            return True
        else:
            return False

    def getValues(self):
        """
        Returns a policy
        """
        return self.values

    def update(self, state, action, nextState, reward):
        """
        Updates Q-Values based on state action pair and relative location to Apple
        Uses standard Q-Update equation to find new Q-Values
        """
        newX = state[0][0]
        newY = state[1][0]
        reward -= 1
        finalState = (newX,newY)
        app = (self.isAppleX(state),self.isAppleY(state))
        nextAction = self.computeActionFromQValues(nextState)
        self.values[(finalState,app,action)] = ((1-self.alpha)*self.getQValue(state,action)) + (self.alpha*(reward + (self.discount*self.getQValue(nextState,nextAction))))
        v = self.values[(finalState,app,action)]
        #print("value",v)
        #print("last v",v)
        return v

    def isAppleX(self, state):
        """
        Gets whether apple is left, right, or straight from snake head
        """
        if state[0][0] < self.apple[0]:
            return 1
        elif state[0][0] > self.apple[0]:
            return -1
        else:
            return 0

    def isAppleY(self, state):
        """
        Gets whether apple is up, down, or straight from snake head
        """
        if state[1][0] < self.apple[1]:
            return 1
        elif state[1][0] > self.apple[1]:
            return -1
        else:
            return 0

    def draw(self, surface, image):
        """
        Draws Snake
        """
        for i in range(0,self.length):
            surface.blit(image,(self.curState[0][i],self.curState[1][i]))

class App:
    """
    Main app class, holds all functions for game functionality including training
    """
    windowWidth = 800
    windowHeight = 600
    score = 0
    apple = 0

    def __init__(self):
        """
        Initializes Values for running, images, game, starting apple, computer,
        and trainer
        """
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.apple = Apple(8,5)
        self.computer = Computer(5)
        self.trainer = Trainer()

    def on_init(self):
        """
        Used to restart values at the beginning of each playthrough
        """
        pygame.init()
        self.computer.updateApple([self.apple.x,self.apple.y])
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        self.computer = Computer(5)

        #Computer gets trainer values as policy
        self.computer.values = self.trainer.getValues()

        self.apple = Apple(randint(1,17),randint(1,12))
        self.computer.updateApple([self.apple.x,self.apple.y])
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.image.load("pygame.png").convert()
        self._apple_surf = pygame.image.load("apple.png").convert()

    def on_event(self, event):
        """
        If player quits ends cleanly
        """
        if event.type == QUIT:
            self._running = False

    def train(self):
        """
        Training function. Continues as long as the trainer is still going through
        training mode. Does nextStep of episode until episode ends. Prints score.
        Lets computer fill in to full length before starting training. Copies
        computer starting location for each iterationn of training
        """
        while self.trainer.isTraining():

            time.sleep(50.0 / 1000.0)
            if self.trainer.curTraining == 0:

                for i in range(self.computer.length):
                    self.computer.update()

            print(self.trainer.curTraining)
            trainX = [x for x in self.computer.x]
            trainY = [y for y in self.computer.y]
            self.trainer.startEpisode([trainX,trainY],self.computer.length)
            while not self.trainer.episodeIsOver():
                self.trainer.nextStep()
            print("Score:",self.trainer.curScore)
        self.computer.values = self.trainer.getValues()

    def on_loop(self):
        """
        Main loop to move computer.
        If it gets the apple, spawns a new Apple
        If collides with itself or wall, or wins, ends the game
        """
        self.computer.go()

        self.computer.update()
        # does computer eat apple?
        for i in range(0,self.computer.length):
            if self.game.isCollision(self.apple.x,self.apple.y,self.computer.x[i], self.computer.y[i],44):
                newApp = True
                n = 0

                while(newApp and n < 100000):
                    app_x = randint(1,17) * 44
                    app_y = randint(1,12) * 44
                    found = False
                    for j in range(0,self.computer.length):
                        if self.game.isCollision(app_x,app_y,self.computer.x[j], self.computer.y[j],44):
                            found = True
                    if not found:
                        self.apple.x = app_x
                        self.apple.y = app_y
                        self.computer.updateApple([self.apple.x,self.apple.y])
                        newApp = False

                    n += 1
                self.score += 10
                self.computer.length = self.computer.length + 1

        # does computer snake collide with itself?
        for i in range(1,self.computer.length):
            if self.game.isCollision(self.computer.x[0],self.computer.y[0],self.computer.x[i], self.computer.y[i],40):
                print("Computer loses! Collision: ")

                print("Score:",self.score)
                self._running = False
                break


        # is it a win
        if(self.computer.length >= 234):
            print("Computer wins!")
            print("Score:", self.score)
            self._running = False


    def on_render(self):
        """
        Renders snake and apple
        """
        self._display_surf.fill((0,0,0))
        self.apple.draw(self._display_surf, self._apple_surf)
        self.computer.draw(self._display_surf, self._image_surf)

        pygame.display.flip()


    def on_cleanup(self):
        """
        quits pygame
        """
        pygame.quit()

    def on_execute(self):
        """
        Parent loop catches if init doesn't work.
        Times playthrough.
        Runs playthrough.
        """
        if self.on_init() == False:
            self._running = False


        startTime = time.perf_counter()
        while( self._running ):
            pygame.event.get()
            self.on_loop()
            self.on_render()
            keys = pygame.key.get_pressed()

            # Escape if in loop
            if (keys[K_ESCAPE]):
                self._running = False
                print("Score:",self.score)


            time.sleep (50.0 / 1000.0)
        endTime = time.perf_counter()
        self.score = 0
        print(f"Time elapsed in seconds = {endTime-startTime:0.4f}")
        self.on_cleanup()

if __name__ == "__main__" :
    """
    initializes number of games to be played. Trains and then plays games
    """
    games = 10
    n = 0
    theApp = App()
    theApp.train()
    while(n < games):
        theApp.on_execute()
        n+=1

import numpy as np

class Robot():
    def __init__(self):

        self.actions = ["left", "right", "up", "down", "stop"]
        self.reward = 0
        self.done = False
        self.state = [100,100]
        self.target = [320,240]
        self.movementTarget = [320, 240]
        self.reachedMovementTarget = False
        self.distance = 282
        self.tempDistance = 0
        self.rewardDistance = 0
        self.rewardsSum = 0

        # List out our bandits. Currently arms 4, 2, and 1 (respectively) are the most optimal.
        #self.robots = np.array([[1, 1, 1, 1]])

        self.num_robots = 1
        self.num_actions = 5

    def getRobot(self):
        return self.state

    def respawn(self):
        self.done = False
        self.state[0] = np.random.randint(630) + 10
        self.state[1] = np.random.randint(470) + 10
        self.rewardDistance = self.calculateDistanceToTarget()

    def calculateDistanceToTarget(self):
        self.tempDistance = np.sqrt(np.power(self.state[0] - self.target[0], 2) + np.power(self.state[1] - self.target[1], 2))
        return self.tempDistance

    def getDistanceToTarget(self):
        return self.state

    def setMovementTarget(self):
        self.done = False
        self.rewardDistance = self.calculateDistanceToTarget()
        self.reachedMovementTarget = False
        self.movementTarget[0] = np.random.randint(630) + 10
        self.movementTarget[1] = np.random.randint(470) + 10

    def getMovementTarget(self):
        return self.movementTarget

    def moveToMovementTarget(self):

        if abs(self.movementTarget[0] - self.state[0]) < 12 and abs(self.movementTarget[1] - self.state[1]) < 12:
            self.reachedMovementTarget = True

        if self.reachedMovementTarget == False:

            if self.movementTarget[0] > self.state[0]:
                self.state[0] += 1
            else:
                self.state[0] -= 1

            if self.movementTarget[1] > self.state[1]:
                self.state[1] += 1
            else:
                self.state[1] -= 1

    def moveRobot(self, action):


        if self.state[0] > 640:
            self.reward = -100
            self.respawn()

        if self.state[1] > 480:
            self.reward = -100
            self.respawn()


        if self.state[0] < 0:
            self.reward = -100
            self.respawn()

        if self.state[1] < 0:
            self.reward = -100
            self.respawn()


        if action == 0: #up
            #print("up")
            self.state[1] += 1
        if action == 1: #down
            #print("down")
            self.state[1] -= 1

        if action == 2: #left
            #print("left")
            self.state[0] += 1

        if action == 3: #right
            #print("right")
            self.state[0] -= 1

        if action == 4: #stop
            #print("right")
            self.state[0] += 0
            self.state[1] += 0

        self.calculateDistanceToTarget()

        if self.tempDistance <= 30 and action == 4:
            self.reward = 100
            self.done = True

        if self.tempDistance <= 30 and action != 4:
            self.reward = -1
            self.done = True

        if self.tempDistance >= self.rewardDistance:
            self.rewardDistance = self.tempDistance
            self.reward = -1
        else:
            self.rewardsSum += 1
            self.rewardDistance = self.tempDistance
            self.reward = +1

        return np.array(self.state), self.reward, self.done, {}
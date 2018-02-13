# -*- coding: utf-8 -*-
import numpy as np

from robot_arena import Arena
from robot_dqnagent import DQNAgent
from robot_env import Robot

EPISODES = 10000

if __name__ == "__main__":

    arena = Arena()
    myRobot = Robot()

    state_size = 2
    action_size = 5
    agent = DQNAgent(state_size, action_size)
    agent.load('trekker_5000_refactored.h5')

    done = False
    batch_size = 32

    for e in range(EPISODES):
        #print(e)
        myRobot.respawn()
        #myRobot.setMovementTarget()
        state = myRobot.getRobot()
        state = np.reshape(state, [1, state_size])
        for time in range(800):

            arena.drawRobot(state)
            #print(myRobot.tempDistance)
            action = agent.act_execute(state)
            arena.setText(action)
            arena.setPos(np.array_str(state))
            #myRobot.moveToMovementTarget()
            next_state, reward, done, _ = myRobot.moveRobot(action)
            #reward = reward
            next_state = np.reshape(next_state, [1, state_size])  #what is happening here ?
            #agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                #agent.update_target_model()
                myRobot.respawn()
                print("episode: {}/{}, score: {}, e: {:.2}"
                      .format(e, EPISODES, time, agent.epsilon))
                break
        print(e)

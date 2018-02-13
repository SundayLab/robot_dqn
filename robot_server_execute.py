from __future__ import print_function

import asyncio
import random
import threading
import time
import numpy as np
import websockets
from websocket import create_connection
from robot_dqnagent import DQNAgent
from robot_arena import Arena




class MSGWorker (threading.Thread):


  def __init__(self):
    self.coords = [100, 100]
    state_size = 2
    action_size = 5
    self.currentAction = ""
    self.agent = DQNAgent(state_size, action_size)
    self.agent.load('trekker_5000_refactored.h5')
    threading.Thread.__init__(self)
    self.connected = set()

  def run(self):
    while True:
      time.sleep(0.001)

  def act(self,x,y):

      state = np.array([x,y])
      #arena.drawRobot(state)

      #arena.setPos(np.array_str(state))

      mops= np.reshape(state, [1, 2])
      arena.drawRobot(state)


      action = self.agent.act_execute(mops)
      if action == 0 and self.currentAction != 0:  # up
          print("up")
          self.currentAction = 0
          ws = create_connection("ws://192.168.178.61:8080")
          ws.send("camup")
          ws.close()

      if action == 1 and self.currentAction != 1:  # down
          print("down")
          self.currentAction = 1
          ws = create_connection("ws://192.168.178.61:8080")
          ws.send("camdown")
          ws.close()

      if action == 2 and self.currentAction != 2:  # left
           print("left")
           self.currentAction = 2
           ws = create_connection("ws://192.168.178.61:8080")
           ws.send("left,1")
           ws.close()
      if action == 3 and self.currentAction != 3:  # right
           print("right")
           self.currentAction = 3
           ws = create_connection("ws://192.168.178.61:8080")
           ws.send("right,1")
           ws.close()

  @asyncio.coroutine
  def handler(self, websocket, path):
    self.connected.add(websocket)
    try:   
      name = yield from websocket.recv()
      commaindex = name.find(",")
      commandlength = len(name)
      direction = name[0:commaindex]
      self.speed = name[commaindex+1:commandlength]

      self.act(direction,self.speed)
    
      #print(direction+','+self.speed)

      # here are the coordinates coming -> handled to the message worker !
          
    except websockets.exceptions.ConnectionClosed:
      pass
    finally:
      self.connected.remove(websocket)

  def sendData(self, data):
    for websocket in self.connected.copy():
      #print("Sending data: %s" % data)
      coro =yield from websocket.send(data)
      future = asyncio.run_coroutine_threadsafe(coro, loop)

if __name__ == "__main__":
  print('AI Server')
  msgWorker = MSGWorker()
  arena = Arena()

  try:

    msgWorker.start()
    ws_server = websockets.serve(msgWorker.handler, '192.168.178.67', 8080)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ws_server)
    loop.run_forever()
  except KeyboardInterrupt:
    stopFlag = True
    #TODO: close ws server and loop correctely
    print("Exiting program...")
  

import gym
import numpy as np
import threading, time, random

# global env is just for Q-table size
game = "Taxi-v2"
envGlobal = gym.make(game)

# global Q-table, which contains final results
Q = np.zeros([envGlobal.observation_space.n, envGlobal.action_space.n])
Q_init = False

# hyper parameters
lr = .01  # learning rate
y = .99   # discount factor

# training parameters
threadcount = 5
num_episodes = 20000
num_steps = envGlobal.spec.timestep_limit

start_time = int(time.time()*1000)

# create a lock for Q-Table
lock = threading.Lock()

def agent(number, verify):
  # all agents update the global Q-table
  global Q
  global Q_init
  rand_th = 1

  if verify:
    Q_loc = Q.copy()
  else:
    # local Q, so that agents are not correlated to each other
    Q_loc = np.zeros([envGlobal.observation_space.n, envGlobal.action_space.n])

  #every agent has its own environment
  env = gym.make(game)
  total_reward = 0

  for i in range(num_episodes):
    d = False
    s = env.reset()
    rand_th -= 0.001

    for step in range(num_steps): 
              
      # choose an action by greedily (with noise) picking from Q-Table
      a = env.action_space.sample() if (random.random() < rand_th) else np.argmax(Q_loc[s,:])

      # execute action
      next_s, reward, done, _ = env.step(a)

      if not verify:
        # update Q-Table with new knowledge
        Q_loc[s,a] += lr*( reward + y*np.max(Q_loc[next_s,:]) - Q_loc[s,a])

      # move agent to next state
      s = next_s

      # stop if we are done
      if done == True:
        break

      total_reward += reward

    # update global Q-Table and local Q-Table after 1000 episodes
    if ((i % 1000) == 0 and i > 0):
      lock.acquire()
      Q = (Q+Q_loc.copy())

      # check if the global table is zero
      if(Q_init):
        Q = Q/2.0 
      else:
        Q_init = True

      # copy global Q-Table
      Q_loc = Q.copy()
      lock.release()

      print("Agent: {}, Episode: {},  Avg-Reward: {}".format(number, i, total_reward/1000.0))
      total_reward = 0


# start multiple agents in different threads
threads = []
print ("start {} agents".format(threadcount))
for i in range(threadcount):
  t = threading.Thread(target=agent, args=(i+1, False, ))
  threads.append(t)
  t.start()

# wait until all agents have finished
for t in threads:
  t.join() 

print("running time: {}".format ((int(time.time()*1000) - start_time)/1000) ) 

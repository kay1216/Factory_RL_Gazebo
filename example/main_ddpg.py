#!/usr/bin/env python
import gym
import RL_mlcs
import time
import numpy
import random
import time

from module import ddpg, replay, liveplot

from ddpg_config import config

def render():
    render_skip = 0 #Skip first X episodes.
    render_interval = 50 #Show render Every Y episodes.
    render_episodes = 10 #Show Z episodes every rendering.

    if (x%render_interval == 0) and (x != 0) and (x > render_skip):
        env.render()
    elif ((x-render_episodes)%render_interval == 0) and (x != 0) and (x > render_skip) and (render_episodes < x):
        env.render(close=True)

if __name__ == '__main__':

    env = gym.make('factory-v0')

    outdir = '/tmp/gazebo_gym_experiments'
    env = gym.wrappers.Monitor(env, outdir, force=True)
    env.action_space=3
    plotter = liveplot.LivePlot(outdir)

    last_time_steps = numpy.ndarray(0)

    ddpg = ddpg.DDPG(config)

    memory = replay.Replay(config.max_buffer, config.batch_size)

    initial_epsilon = ddpg.epsilon

    epsilon_discount = 0.9986

    start_time = time.time()
    total_episodes = 10000
    highest_reward = 0

    for x in range(config.max_episode):
        done = False

        cumulated_reward = 0 #Should going forward give more reward then L/R ?

        ranges0,sonars0,rgb0,depth0 = env.reset()

        if ddpg.epsilon > 0.05:
            ddpg.epsilon *= epsilon_discount

        #render() #defined above, not env.render()

        #state = ''.join(map(str, observation))

        for i in range(config.max_step):

            # Pick an action based on the current state
            action = ddpg.chooseAction(ranges0,sonars0,rgb0,depth0)

            # Execute the action and get feedback
            ranges1,sonars1,rgb1,depth1,reward,done,info = env.step(action)
            
            memory.add({
                'lidar0':ranges0,
                'sonar0':sonars0,
                'rgb0':rgb0,
                'depth0':depth0,
                'lidar1':ranges1,
                'sonar1':sonars1,
                'rgb1':rgb1,
                'depth1':depth1,
                'action0':action,
                'reward':reward,
                'done':done
            })

            cumulated_reward += reward

            if highest_reward < cumulated_reward:
                highest_reward = cumulated_reward

            #nextState = ''.join(map(str, observation))

            batch=memory.batch()
            ddpg.learn(batch)

            env._flush(force=True)

            if not(done):
                ranges0 = ranges1
                sonars0 = sonars1
                rgb0 = rgb1
                depth0 = depth1
            else:
                last_time_steps = numpy.append(last_time_steps, [int(i + 1)])
                break

        if x%100==0:
            plotter.plot(env)

        m, s = divmod(int(time.time() - start_time), 60)
        h, m = divmod(m, 60)
        print ("EP: "+str(x+1)+" - Reward: "+str(cumulated_reward)+"     Time: %d:%02d:%02d" % (h, m, s))

    #Github table content
    print ("\n|"+str(total_episodes)+"|"+str(highest_reward)+"| PICTURE |")

    l = last_time_steps.tolist()
    l.sort()

    #print("Parameters: a="+str)
    print("Overall score: {:0.2f}".format(last_time_steps.mean()))
    print("Best 100 score: {:0.2f}".format(reduce(lambda x, y: x + y, l[-100:]) / len(l[-100:])))

    env.close()

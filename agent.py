#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017/09/01

@author: Hitoshi Kono
'''
import time
import threading
import logging
import csv
import sys
from datetime import datetime

from scipy import *

import learning
import world
import environment
import graph
import world

import scipy
import numpy

import matplotlib.pyplot as plt
import matplotlib.gridspec as gsc

'''
This parameter is controlled start/stop of the simulation,
and to cooperate the pygame's key input program in the environment module.
'''

class Agent(threading.Thread):

    def __init__(self, _config, reusePolicyfilename):
        super(Agent, self).__init__()
        self.daemon = True
        self.stop_event = threading.Event()
        self.config = _config

        self.hunter1 = learning.Learning(self.config, reusePolicyfilename)
        logging.basicConfig(format='%(levelname)s:%(thread)d:%(module)s:%(message)s', level=logging.DEBUG)

        self.RUNNING = False
        self.DATE = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.POLNUM = ("%d" % self.config.POLICY_NUMBER)


    '''
    Deployment (reset) the agent and goal position in the world.
    If you add the other type of agent, you have to add in the following
    statements.
    '''
    def resetWorld(self, tmpState):
        world.GRID[ world.START[1] ][ world.START[0] ] = environment.AGT
        world.GRID[ world.GOAL[1] ][ world.GOAL[0] ] = environment.GOAL
        tmpState[:] = world.START   # Copy the default position from list of START coordinates


    '''
    This method composes the episodes (e.g. [1,2,3,4, ... ,n]) and steps (e.g. [y1,y2,y3,...ym]).
    First array's structure is two rows matrix, so second statement is processed it
    to transposed matrix like bellow:
    1, y1
    2, y2
    3, y3
    4, y4
    -
    -
    -
    n, ym
    Moreover, if the data is NumPy array, we can put the csv write function directory.
    '''
    def loggerStepEpisode(self, filename, episodes, steps):
        tmpSteps = []
        for i in range(len(episodes)):
             tmpSteps.append([episodes[i],steps[i]])
        with open(filename,mode="w",buffering=-1) as w:
            writer = csv.writer(w, lineterminator='\n')
            writer.writerows(tmpSteps)
        return 1


    '''
    Q-taable logger. This method using Numpy's function, so file format is not CSV.
    Take care!
    '''
    def loggerQtable(self, filename, policy):
        tmpdate = []
        tmp_f = 0
        tmp_g = 0
        tmp_h = 0
        tmp_i = 0
        tmp_e = 0
        tmp_j = 0
        tmp_k = 0
        tmp_l = 0
        tmp_m = 0
        
        # x:i y:j a:k
        for i in range(1,world.GRID.shape[0]-1):
           for j in range(1,world.GRID.shape[1]-1):
               #マップチップ番号は0=路,1=壁なので注意(高桑さんのデータとは違う)
                try:
                   tmp_f = world.GRID[j-1][i-1]
                except IndexError:
                    logging.info("f is out of index")
                try:
                   tmp_g = world.GRID[j-1][i]
                except IndexError:
                    logging.info("g is out of index")
                try:
                   tmp_h = world.GRID[j-1][i+1]
                except IndexError:
                    logging.info("h is out of index")
                try:
                   tmp_i = world.GRID[j][i-1]
                except IndexError:
                    logging.info("i is out of index")
                try:
                   tmp_e = world.GRID[j][i]
                except IndexError:
                    logging.info("e is out of index")
                try:
                   tmp_j = world.GRID[j][i+1]
                except IndexError:
                    logging.info("j is out of index")
                try:
                   tmp_k = world.GRID[j+1][i-1]
                except IndexError:
                    logging.info("k is out of index")
                try:
                   tmp_l = world.GRID[j+1][i]
                except IndexError:
                    logging.info("l is out of index")
                try:
                   tmp_m = world.GRID[j+1][i+1]
                except IndexError:
                    logging.info("m is out of index")
                for k in range(0,5):
                    #上・右・下・左・静止
                    #logging.info("x:",i,"y:",j,"a:",k,"Q:",policy[i][j][0][0][k],tmp_e,tmp_f,tmp_g,tmp_h,tmp_i,tmp_j,tmp_k,tmp_l,tmp_m)
                    tmpdate.append( [i,j,k,policy[i][j][0][0][k],tmp_e,tmp_f,tmp_g,tmp_h,tmp_i,tmp_j,tmp_k,tmp_l,tmp_m,world.START[0],world.START[1]] )
        with open(str(filename), mode="w", buffering=-1) as w:
            writer = csv.writer(w, lineterminator='\n')
            writer.writerows(tmpdate)
        return 1

    '''
    Method of the learning agent.
    '''
    def learner(self, num):

        '''
        Learning proccess of the agent.
        '''
        while self.config.NEPISODES <= self.config.FINISH_EPISODE[num]:
            if self.RUNNING == True:
                self.hunter1.action(self.hunter1.STATE, self.hunter1.OLD_STATE, self.hunter1.POLICY, self.hunter1.REUSEPOLICY, self.hunter1.ACT)
                self.config.NSTEPS = self.config.NSTEPS + 1

                if (self.hunter1.STATE == world.GOAL) == True:
                    self.hunter1.updateQ(self.hunter1.STATE, self.hunter1.OLD_STATE, self.hunter1.POLICY, num, self.hunter1.ACT, self.config.REWARD_POSITIVE[num])
                    self.config.STEPS.append(self.config.NSTEPS)          # Append to list the number of steps
                    self.config.EPISODES.append(self.config.NEPISODES)    # Append to list the number of episodes

                    #Learning progress
                    self.progress = (float(self.config.NEPISODES) / float(self.config.FINISH_EPISODE[num])) * 100.0
                    sys.stdout.write("\rLearning..... " + str(self.progress) + "% EPISODE:" + str(self.config.NEPISODES) + " STEP:" + str(self.config.NSTEPS) + "     ")
                    sys.stdout.flush()

                    self.config.NEPISODES = self.config.NEPISODES + 1     # Add one to number of episodes
                    self.config.NSTEPS = 0                           # Set default value as 0 step
                    self.config.TREWARD = self.config.TREWARD + self.config.REWARD_POSITIVE[num] # Final sum of the goal reward
                    self.config.TREWARDS.append(self.config.TREWARD)      # Append to list the total reward
                    self.config.TREWARD = 0
                    self.resetWorld(self.hunter1.STATE)              # Reset the coordinates
                elif self.hunter1.ACT[2] < 0:
                    self.hunter1.updateQ(self.hunter1.STATE, self.hunter1.OLD_STATE, self.hunter1.POLICY, num, self.hunter1.ACT, self.config.REWARD_NEGATIVE[num])
                    self.config.TREWARD = self.config.TREWARD + self.config.REWARD_NEGATIVE[num]
                else:
                    self.hunter1.updateQ(self.hunter1.STATE, self.hunter1.OLD_STATE, self.hunter1.POLICY, num, self.hunter1.ACT, self.config.REWARD_ZERO)
                    self.config.TREWARD = self.config.TREWARD + self.config.REWARD_ZERO

                time.sleep(self.config.TIMESTEP)

            else:
                time.sleep(0.1)                                 # Sleeping time of wait for start
        logging.info('learning finished!')


    '''
    Described following codes are execution codes in the thread.
    '''
    def run(self):
        logging.info('Thread start')

        # Deploying the agent and goal.
        self.resetWorld(world.START)

        # Call the learning function based on selected type of learning
        # First call is Reinforcement Learning
        if self.config.LEARNING_MODE == 1:
            fileStepsRL = r"" + self.config.Steps_filename + self.POLNUM + "_" + self.DATE + ".csv"
            fileQtableRL = r"" + self.config.Qtable_filename + self.POLNUM + "_" + self.DATE + ".csv"
            logging.info("filename:" + fileQtableRL)
            self.config.POLICY_NUMBER = self.config.POLICY_NUMBER + 1
            self.POLNUM = ("%d" % self.config.POLICY_NUMBER)
            logging.info('Reinforcement learning (Source task) start')
            self.learner(0)
            logging.info('Source task is terminated')
            
            # Declaration of subfigures with gridspec
            """
            graphname = "./source/graphs_" + DATE + ".png"
            logging.info("graphname %s",graphname)
            gs = gsc.GridSpec(2, 7)
            fig = plt.figure(figsize=(10,7))
            graph1 = fig.add_subplot(gs[1, 0:7])
            graph2 = fig.add_subplot(gs[0, 0:4])
            # Setting of pyplot
            graph1.set_title("Learning curve")
            graph1.set_ylabel("Number of steps")
            graph1.set_xlabel("Number of episodes")
            graph2.set_title("Transition of total rewards")
            graph2.set_ylabel("Total rewards")
            graph2.set_xlabel("Number of episodes")
            # Adjust to fit amoung graphs
            fig.tight_layout()
            # Loop of representation of graphs in plot window
            MAX_NEPISODE = self.config.FINISH_EPISODE[0]  # Reinforcement learning
            logging.info("MAX_NEPISODE %s",MAX_NEPISODE)
            graph1.plot(self.config.EPISODES, self.config.STEPS)
            graph2.plot(self.config.EPISODES, self.config.TREWARDS)
            plt.show()
            """
        # Second call is Transfer Learning
        elif self.config.LEARNING_MODE == 2:
            fileStepsTL = r"" + self.config.TSteps_filename + self.POLNUM + "_" + self.DATE + ".csv"
            fileQtableTL = r"" + self.config.TQtable_filename + self.POLNUM + "_" + self.DATE + ".csv"
            logging.info("filename:" + fileQtableTL)
            self.config.POLICY_NUMBER = self.config.POLICY_NUMBER + 1
            self.POLNUM = ("%d" % self.config.POLICY_NUMBER)
            logging.info('Transfer learning (Target task) start')
            self.learner(1)
            min_episode = 0
            while (True):
                if self.config.STEPS[min_episode] == self.config.STEPS[min_episode+1] and self.config.STEPS[min_episode] == self.config.STEPS[min_episode+2] and self.config.STEPS[min_episode] == self.config.STEPS[min_episode+3] and self.config.STEPS[min_episode] == self.config.STEPS[min_episode+4]:
                    logging.info("this episode:%i",min_episode)
                    break
                min_episode = min_episode + 1
            logging.info('Target task is terminated')
            
        else:
            logging.warning ('mode error')
        self.config.TERMINATE = False
    
    def stop(self):
        self.stop_event.set()

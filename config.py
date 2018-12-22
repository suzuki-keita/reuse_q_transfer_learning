#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017/09/01

@author: Hitoshi Kono
'''
class Config:
    def __init__(self):
        
        """
        回数
        """

        self.EPOCH = 100

        '''
        Save to CSV file
        '''

        self.Steps_filedir = "/Users/takashi/Documents/knowledge/total_step/"
        self.Steps_filename = "/Users/takashi/Documents/knowledge/total_step/data_ver2.csv"
        
        '''
        Setup parameters of this simulation.
        If you select the '2' as DIMENSION, grid world
        is deployed in the environment. On the other hand
        If '3' was selected, 3D world is deployed in the
        environment
        '''

        self.DIMENSION = 2   # 2 or 3

        '''
        Type of simulation.
        1: Reinforcement learning (Source task)
        2: Transfer learning (Target task)
        '''
        self.LEARNING_MODE = 2   # 1 or 2

        '''
        Waiting time in each action (step).
        If you set this value without 0,
        Simulation speed becomes down.
        '''
        self.TIMESTEP = 0.0

        '''
        System variables' declerations
        '''
        # Experimental parameters
        self.TERMINATE = True

        # List for the graphs
        self.NEPISODES = 1   # Do not modify
        self.NSTEPS = 0      # Do not modify
        self.TREWARD = 0     # Do not modify
        self.EPISODES = []
        self.STEPS = []
        self.TREWARDS = []
        # From this line, for the learning parameters
        self.LEARNING_RATE = []
        self.DISCOUNT_RATE = []
        self.FINISH_EPISODE = []
        self.BOLTZMANN_TEMP = []
        self.REWARD_POSITIVE = []
        self.REWARD_NEGATIVE = []
        self.REWARD_ZERO = 0

        '''
        Reinforcement learning parameters
        '''
        self.LEARNING_RATE.append(0.1)
        self.DISCOUNT_RATE.append(0.99)
        self.FINISH_EPISODE.append(500)
        self.BOLTZMANN_TEMP.append(0.05)
        self.REWARD_POSITIVE.append(1.0)     # You have to set this value not integer
        # You have to set this value not integer
        self.REWARD_NEGATIVE.append(0.0)

        '''
        Transfer learning parameters
        '''
        self.LEARNING_RATE.append(0.1)
        self.DISCOUNT_RATE.append(0.99)
        self.FINISH_EPISODE.append(500)
        self.BOLTZMANN_TEMP.append(0.05)
        self.REWARD_POSITIVE.append(1.0)     # You have to set this value not integer
        self.REWARD_NEGATIVE.append(-1.0)   # You have to set this value not integer
        self.TRANSFER_RATE = 0.1
        self.POLICY_NUMBER = 1



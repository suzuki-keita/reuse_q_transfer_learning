#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017/08/31

@author: Hitoshi Kono
'''
import sys
import time
import threading
import logging
import pygame
import glob
import csv
import random
from datetime import datetime

import config
import agent
#import scope
import environment
import graph
import world
DEBUG_MODE = 0

KNOWLEDGE_NAME = "2018-12-11_unrated_knowledge_predict.csv"
MAP_NAME = "2018-12-11_rated_map_category.csv"
random.seed = 114514

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(thread)d:%(module)s:%(message)s', level=logging.DEBUG)
    logging.info('Threads start')

    if DEBUG_MODE == 0:
        logging.info('MAIN_MODE!')
        knowledge_filename = []
        knowlege_qtable_category = []
        map_filename = []
        map_qtable_category = []
        total_step = []
        
        step_filename = r"" + config.Config().Steps_filedir + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"

        with open(KNOWLEDGE_NAME, 'r') as o:
            dataReader = csv.reader(o)
            for row in dataReader:
                knowledge_filename.append(str(row[0]))
                knowlege_qtable_category.append(int(row[1]))
        with open(MAP_NAME, 'r') as o:
            dataReader = csv.reader(o)
            for row in dataReader:
                map_filename.append(str(row[0]))
                map_qtable_category.append(int(row[1]))
                total_step.append(int(row[3]))
        
        for i in range(0, config.Config().EPOCH):
            k = random.randrange(0, len(map_filename))
            for j in range(0, max(knowlege_qtable_category)+1):
                configs = config.Config()
                configs.step_filename = step_filename
                #環境をロード
                world.GRID = world.GRID_FIRST
                with open(map_filename[k], 'r') as o:
                    dataReader = csv.reader(o)
                    for row in dataReader:
                        if int(row[4]) == environment.GOAL:
                            world.GRID[int(row[1])][int(row[0])] = environment.ROAD
                            world.GOAL[0] = int(row[0])
                            world.GOAL[1] = int(row[1])
                        elif int(row[4]) == environment.WALL:
                            world.GRID[int(row[1])][int(row[0])] = environment.WALL
                        else:
                            world.GRID[int(row[1])][int(row[0])] = environment.ROAD
                        world.START[0] = int(row[13])
                        world.START[1] = int(row[14])
                while (True):
                    r = random.randrange(0,len(knowledge_filename))
                    if j == knowlege_qtable_category[r]:
                        world.MAP_FILENAME = map_filename[k]
                        world.KNOWLEDGE_FILENAME = knowledge_filename[r]
                        world.MAP_TOTAL_STEP = total_step[k]
                        world.MAP_CATEGORY = map_qtable_category[k]
                        world.KNOWLEDGE_CATEGORY = knowlege_qtable_category[r]

                        logging.info('map filename:%s', world.MAP_FILENAME)
                        logging.info('map category:%i', world.MAP_CATEGORY)
                        logging.info('map total_step:%i', world.MAP_TOTAL_STEP)
                        logging.info('knowledge filename:%s',world.KNOWLEDGE_FILENAME)
                        logging.info('knowledge category:%i',world.KNOWLEDGE_CATEGORY)
                        break
                #転移学習
                th1 = agent.Agent(configs, knowledge_filename[r])
                if configs.DIMENSION == 2:
                    #th2 = environment.Environment(configs,th1);    # PyGame (2D)
                    pass
                elif configs.DIMENSION == 3:
                    #th3 = scope.Scope();             # PyOpenGL (3D)
                    pass
                else:
                    logging.warning('Error of const.DIMENSION')
                    logging.info('Simulation shutting down...')
                    sys.exit()
                    #th4 = graph.Graph();                    # MatPlotLib

                '''
                Starting proccess of the threads
                '''

                th1.start()
                if configs.DIMENSION == 2:
                    #th2.start()
                    pass
                elif configs.DIMENSION == 3:
                    #th3.start()
                    pass
                #th4.start()

                '''
                PyGame control with key event function
                '''
                """
                pygame.init()
                while configs.TERMINATE == True:
                    for event in pygame.event.get():        # Input of keyboard
                        if event.type == pygame.QUIT:       # PyGame quit proccess
                            pygame.quit()
                            configs.TERMINATE = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:  # 'ESC' press, termination of the pygame
                                pygame.quit()
                                configs.TERMINATE = False
                            elif event.key == pygame.K_s:     # 's' press, start or stop
                                th1.RUNNING = not th1.RUNNING
                    th1.RUNNING = True
                    pygame.time.wait(10)
                """
                th1.RUNNING = True
                th1.join()
        logging.info('All threads are terminated')

    elif DEBUG_MODE == 1:
        logging.info('DEBUG_MODE')
        map_index = 2
        knowledge_index = 3
        knowledge_filename = []
        knowlege_qtable_category = []
        map_filename = []
        map_qtable_category = []
        total_step = []
        
        with open(KNOWLEDGE_NAME, 'r') as o:
            dataReader = csv.reader(o)
            for row in dataReader:
                knowledge_filename.append(str(row[0]))
                knowlege_qtable_category.append(int(row[1]))
        with open(MAP_NAME, 'r') as o:
            dataReader = csv.reader(o)
            for row in dataReader:
                map_filename.append(str(row[0]))
                map_qtable_category.append(int(row[1]))
                total_step.append(int(row[3]))
        configs = config.Config()

        #環境をロード
        world.GRID = world.GRID_FIRST
        with open(map_filename[map_index], 'r') as o:
            dataReader = csv.reader(o)
            for row in dataReader:
                if int(row[4]) == environment.GOAL:
                    world.GRID[int(row[1])][int(row[0])] = environment.ROAD
                    world.GOAL[0] = int(row[0])
                    world.GOAL[1] = int(row[1])
                elif int(row[4]) == environment.WALL:
                    world.GRID[int(row[1])][int(row[0])] = environment.WALL
                else:
                    world.GRID[int(row[1])][int(row[0])] = environment.ROAD
        world.START[0] = int(row[13])
        world.START[1] = int(row[14])

        logging.info('map filename:%s', map_filename[map_index])
        logging.info('map category:%i', map_qtable_category[map_index])
        logging.info('map total_step:%i', total_step[map_index])
        logging.info('knowledge filename:%s', knowledge_filename[knowledge_index])
        logging.info('knowledge category:%i', knowlege_qtable_category[knowledge_index])
            
        #転移学習
        th1 = agent.Agent(configs, knowledge_filename[knowledge_index])
        if configs.DIMENSION == 2:
            th2 = environment.Environment(configs,th1);    # PyGame (2D)
            pass
        elif configs.DIMENSION == 3:
            #th3 = scope.Scope();             # PyOpenGL (3D)
            pass
        else:
            logging.warning('Error of const.DIMENSION')
            logging.info('Simulation shutting down...')
            sys.exit()
        #th4 = graph.Graph();                    # MatPlotLib
        '''
        Starting proccess of the threads
        '''
        
        th1.start()
        if configs.DIMENSION == 2:
            th2.start()
            pass
        elif configs.DIMENSION == 3:
            #th3.start()
            pass
        #th4.start()
        '''
        PyGame control with key event function
        '''
        pygame.init()
        while configs.TERMINATE == True:
            for event in pygame.event.get():        # Input of keyboard
                if event.type == pygame.QUIT:       # PyGame quit proccess
                    pygame.quit()
                    configs.TERMINATE = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # 'ESC' press, termination of the pygame
                        pygame.quit()
                        configs.TERMINATE = False
                    elif event.key == pygame.K_s:     # 's' press, start or stop                            th1.RUNNING = not th1.RUNNING
                        th1.RUNNING = True
            pygame.time.wait(10)
        th1.join()
        logging.info('All threads are terminated')

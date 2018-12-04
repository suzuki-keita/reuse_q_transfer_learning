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
from scipy import *

import world
import learning


'''
Constant values for the PyGame. Do not change if you can.
'''
CS = 25                             # Constant number, grid size and window size rate.
SCR_X = world.GRID.shape[1] * CS    # column
SCR_Y = world.GRID.shape[0] * CS    # row
SCR_RECT = pygame.Rect(0,0,SCR_X,SCR_Y)    # Rect(left,top,width,height)
START = 0

GOAL = 1
ROAD = 2
WALL = 3
AGT = 4

LEFT = 3
RIGHT = 1
UP = 0
DOWN = 2
STOP = 4

'''
Control paramenter from main module via a PyGame event function
'''
DRAW_SWITCH = True


class Environment(threading.Thread):

    logging.basicConfig(format='%(levelname)s:%(thread)d:%(module)s:%(message)s', level=logging.DEBUG)

    def __init__(self,_config,_agent):
        super(Environment, self).__init__()
        self.daemon = True
        self.stop_event = threading.Event()
        self.config = _config
        self.agent = _agent
        pygame.init()
        self.screen = pygame.display.set_mode(SCR_RECT.size)   #以下、self.名称はアトリビュートを追加
        pygame.display.set_caption(u"Environment")
        self.font = pygame.font.SysFont("timesnewroman",20)
        #self.cursor = [int(world.GRID.shape[1]/2), int(world.GRID.shape[0]/2)]
        self.reflect(self.screen)                       # First drawing of grid world
        self.screen.fill((255,255,255))

    '''
    Attention!!!
    This method is conpatible with learing.Learning.argMaxQ(),
    but it is used for only this module. Take care to control.
    '''
    def argMaxQ(self, state, policy, nAct):
        tmpValue = zeros(nAct)
        for i in range (0, nAct):
            tmpValue[i] = policy[state[0]][state[1]][0][0][i]

        tmpMaxValue = 0
        numAct = 0
        for j in range (0, nAct):
            if tmpMaxValue <= tmpValue[j]:
                tmpMaxValue = tmpValue[j]
                numAct = j

        return numAct

    '''
    This method has same situation as argMaxQ().
    This is included Inter task mapping for Transfer Learning.
    '''
    def argMaxT(self, state, policy, nAct):
        tmpValue = zeros(nAct)
        for i in range (0, nAct):
            tmpValue[i] = self.agent.hunter1.iTaskMap(state, i, policy)

        tmpMaxValue = 0
        numAct = 0
        for j in range (0, nAct):
            if tmpMaxValue <= tmpValue[j]:
                tmpMaxValue = tmpValue[j]
                numAct = j

        return numAct


    '''
    Value function method based on Q-value in the grid.
    This is different from argMaxQ() because this returns value is actual Q-value.
    '''

    def maxQvalue(self, state, policy, nAct):
        tmpMaxValue = 0
        for i in range (0, nAct):
            if tmpMaxValue < policy[state[0]][state[1]][0][0][i]:
                tmpMaxValue = policy[state[0]][state[1]][0][0][i]

        return tmpMaxValue

    '''
    This function represent grid world infor mation for display.
    '''
    def reflect(self, screen):
        for x in range(0, world.GRID.shape[1]):
            for y in range(0, world.GRID.shape[0]):
                '''
                Here, why GRID[y][x] is inverted compared with window coordinates?
                Because thsi is descrived based on NumPy arrays row and column.
                '''
                if world.GRID[y][x] == WALL:
                    pygame.draw.rect(screen, (0,0,0), pygame.Rect(x*CS,y*CS,CS,CS))         # Painting with black
                elif world.GRID[y][x] == ROAD:
                    pygame.draw.rect(screen, (255,255,255), pygame.Rect(x*CS,y*CS,CS,CS))   # Painting with white
                    pygame.draw.rect(screen, (0,0,0), pygame.Rect(x*CS,y*CS,CS,CS), 1)      # and black lines

                    '''
                    Represantation for Transfer learning.
                    Reusing policy's action value is painted blue color.
                    '''
                    if self.config.LEARNING_MODE == 2:
                        transferValue = self.config.TRANSFER_RATE * self.maxQvalue( [x,y], self.agent.hunter1.REUSEPOLICY, 5)
                        if transferValue != 0:
                            '''
                            This part is positive action value
                            '''
                            if transferValue > 1:
                                transferValue = 1     # Fitting to limit
                            if transferValue > 0:
                                transferValue = transferValue * 255.0
                                color = (255 - transferValue, 255 - transferValue, 255)
                                pygame.draw.rect(screen, color, pygame.Rect(x*CS,y*CS,CS,CS))
                                pygame.draw.rect(screen, (0,0,0), pygame.Rect(x*CS,y*CS,CS,CS), 1)      # and black lines
                            '''
                            This part is representation of the direction of maximum action value
                            '''
                            actDirection = self.argMaxT([x, y], self.agent.hunter1.REUSEPOLICY, 5)
                            direction = u""
                            if actDirection == UP:
                                direction = u"↑"
                            elif actDirection == RIGHT:
                                direction = u"→"
                            elif actDirection == DOWN:
                                direction = u"↓"
                            elif actDirection == LEFT:
                                direction = u"←"
                            else:
                                direction = u""
                            screen.blit(self.font.render(direction, True, (0,0,0)), (x*CS,y*CS))

                    '''
                    Arrow painting based on the value function with action values.
                    This method used unrecommended variable referenced form Agent class like a global variables.
                    '''
                    actionValue = self.maxQvalue([x, y], self.agent.hunter1.POLICY, 5)
                    if actionValue != 0:
                        '''
                        This part is positive action value
                        '''
                        if actionValue > 1:
                            actionValue = 1     # Fitting to limit
                        if actionValue > 0:
                            actionValue = actionValue * 255.0
                            color = (255, 255 - actionValue, 255 - actionValue)
                            pygame.draw.rect(screen, color, pygame.Rect(x*CS,y*CS,CS,CS))
                            pygame.draw.rect(screen, (0,0,0), pygame.Rect(x*CS,y*CS,CS,CS), 1)      # and black lines
                        '''
                        This part is representation of the direction of maximum action value
                        '''
                        actDirection = self.argMaxQ([x, y], self.agent.hunter1.POLICY, 5)
                        direction = u""
                        if actDirection == UP:
                            direction = u"↑"
                        elif actDirection == RIGHT:
                            direction = u"→"
                        elif actDirection == DOWN:
                            direction = u"↓"
                        elif actDirection == LEFT:
                            direction = u"←"
                        else:
                            direction = u""
                        screen.blit(self.font.render(direction, True, (0,0,0)), (x*CS,y*CS))

                elif world.GRID[y][x] == GOAL:
                    pygame.draw.rect(screen, (25,135,22), pygame.Rect(x*CS,y*CS,CS,CS))     # Painting with green
                elif world.GRID[y][x] == AGT:                                               # Painting with blue circle as agent
                    pygame.draw.circle(screen, (0,0,255), ( int((x*CS)+(CS/2)), int((y*CS)+(CS/2)) ), int(CS/3))
        '''
        This progmra was disabled about the cursor function.
        If you would like to use it, please disable follwoing comment out,
        and please implement your self the value function view program.
        '''
        #pygame.draw.rect(screen, (0,255,0), pygame.Rect(self.cursor[0]*CS, self.cursor[1]*CS,CS,CS), 3)   #0,255,0=緑　カーソルの淵


    '''
    Described following codes are execution codes in the thread.
    '''
    def run(self):
        logging.info('Thread start')

        while(1):   #To show the grid after end of learning (You can close the window with Esc or Quit)
            #clock.tick(1000)                  # Invalid over 1000 fps

            if DRAW_SWITCH == True:            # Tで描画のON,OFFをtoggleで切り替え
                self.reflect(self.screen)
                pygame.display.update()

            time.sleep(0.01)
    
    def stop(self):
            self.stop_event.set()

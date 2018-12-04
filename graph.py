#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017/09/06

@author: Hitoshi Kono
'''

import sys
import time
import threading
import logging

import matplotlib.pyplot as plt
import matplotlib.gridspec as gsc

import config
import agent

class Graph(threading.Thread):

    logging.basicConfig(format='%(levelname)s:%(thread)d:%(module)s:%(message)s', level=logging.DEBUG)

    def __init__(self):
        super(Graph, self).__init__()
        self.daemon = True
        self.stop_event = threading.Event()

    '''
    Described following codes are execution codes in the thread.
    '''
    logging.info('Thread start')
    def run(self):
        while config.NEPISODES <= MAX_NEPISODE:
            logging.info("NEPISODES %s",config.NEPISODES)
            logging.info("EPISODES %s",config.EPISODES)
            logging.info("STEPS %s",config.STEPS)
            logging.info("TREWARDS %s",config.TREWARDS)
            time.sleep(0.1)

        if config.LEARNING_MODE == 1:
            graphname = "./source/graphs_" + agent.DATE + ".png"  #20170615 Storing graph
        elif config.LEARNING_MODE == 2:
            graphname = "./target/graphs_" + agent.DATE + ".png"

        # Declaration of subfigures with gridspec
        logging.info("graphname %s",graphname)
        gs = gsc.GridSpec(2, 7)
        fig = plt.figure(figsize=(10,7))
        graph1 = fig.add_subplot(gs[1, 0:7])
        graph2 = fig.add_subplot(gs[0, 0:4])
        graph3 = fig.add_subplot(gs[0, 4:7])
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
        if config.LEARNING_MODE == 1:
            MAX_NEPISODE = config.FINISH_EPISODE[0]  # Reinforcement learning
        elif config.LEARNING_MODE ==2:
            MAX_NEPISODE = config.FINISH_EPISODE[1]  # Transfer learning
        logging.info("MAX_NEPISODE %s",MAX_NEPISODE)
        graph1.set_data(config.EPISODES, config.STEPS)
        graph2.set_data(config.EPISODES, config.TREWARDS)
        plt.draw()
        """
        while config.NEPISODES <= MAX_NEPISODE:
            '''
            Number of episode is under 2, graphs are not printed
            because lists are empty
            '''
            if config.NEPISODES >= 2:

                #Reflesh graph of learning curve
                #plt.clf()
                '''
                graph1.clear()
                graph2.clear()
                graph3.clear()
                #Setting of labels and related function in pyplot
                graph1.set_title("Learning curve")
                graph1.set_ylabel("Number of steps")
                graph1.set_xlabel("Number of episodes")
                graph1.set_yscale("log", nonposy='clip')
                graph2.set_title("Transition of total rewards")
                graph2.set_ylabel("Total rewards")
                graph2.set_xlabel("Number of episodes")
                graph3.set_title("None")
                graph3.set_ylabel("None")
                graph3.set_xlabel("None")
                fig.tight_layout()     # This function is not recommended for the figure printing,
                                        # because sometimes frame of graph is oscilation.
                '''
                if config.NEPISODES < 10:
                    graph1.set_xlim(1, 10)
                    graph2.set_xlim(1, 10)
                    #plt.xlim(1, 10)
                elif config.NEPISODES >= 10:
                    graph1.set_xlim(1, ( int(config.NEPISODES * 1.05) ))
                    graph2.set_xlim(1, ( int(config.NEPISODES * 1.05) ))
                    #plt.xlim(1, ( e + 1 ))
                graph1.set_ylim(1, max(config.STEPS) + 10)
                graph2.set_ylim( min(config.TREWARDS) * 1.2, max(config.TREWARDS) * 1.2)
                graph1.set_data(config.EPISODES, config.STEPS)
                graph2.set_data(config.EPISODES, config.TREWARDS)
                plt.draw()

            logging.info("NEPISODES %s",config.NEPISODES)
            logging.info("EPISODES %s",config.EPISODES)
            logging.info("STEPS %s",config.STEPS)
            logging.info("TREWARDS %s",config.TREWARDS)
            time.sleep(0.1)


        '''
        Storing of the current graphs to png file.
        And waiting for the temination of the simulation which is PyGame.
        '''
        plt.savefig(graphname)
        while config.TERMINATE == True:
            time.sleep(0.1)
        plt.close()                     #Close graph window
        """
    def stop(self):
            self.stop_event.set()
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 13:46:22 2018

@author: paulo
"""
import matplotlib.pylab as plt
import os


class plotJV():
    """docstring for plotJV."""
    def __init__(self, x, y, figname, directory, save=False, show=False):
        self.xx = x
        self.yy = y
        self.time = x
        self.figname = figname
        self.dir = directory
        self.save = save
        self.show = show
    def plot_jv(self, cell, sentido, measure):
        self.cell = cell
        self.sentido = sentido
        self.measure = measure
        self.celuls = '-Measure-' + str(self.measure) + '-Cell-' +  str(self.cell) + '-' +  str(self.sentido)
        def dirplot(self):
            self.plotDir = self.dir + 'plots/'
            if not os.path.exists(self.plotDir):
                os.makedirs(self.plotDir)
            return self.plotDir



        def plot_config(xlabel, ylabel):
            plt.legend(fontsize=16)

            plt.xticks(fontsize=16)
            plt.tick_params(direction='in', which='major', length=7)

            plt.yticks(fontsize=16)
            plt.ylabel(xlabel, size=16)
            plt.xlabel(ylabel, size=16)
            plt.title(self.figname + self.celuls)

        self.fig=plt.figure(figsize=(10, 8))
        plt.plot(self.xx,self.yy, color = 'red', label = self.figname)
        plot_config('Voltage (V)','Current Density (mA/cmÂ²)')
#        plt.savefig(dirplot(self) + self.figname + '.png', format='png')
#        if self.show:
#            plt.show()

        if self.save:
            plt.savefig(dirplot(self) + self.figname + self.celuls + '.png', format='png')

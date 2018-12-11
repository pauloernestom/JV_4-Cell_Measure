#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 12:50:03 2018

@author: paulo
"""

import numpy as np
import os



class PhotovCalc():
    """docstring for PhotovCalc"""
    def __init__(self, path, xvalues2, yvaluesj, yvalues2, sample_name, Pot_luz):
        self.xvalues2 = xvalues2
        self.yvaluesj = yvaluesj
        self.yvalues2 = yvalues2
        self.sample_name = sample_name
        self.Pot_luz = Pot_luz
        self.path = path

        zip(self.xvalues2,self.yvaluesj)

    def param(self, cell, sentido, measure):
        self.cell = cell
        self.sentido = sentido
        self.measure = measure
        if self.sentido == 'Forward':
            def voc(self):
                self.voc = np.interp(0, -self.yvaluesj, self.xvalues2)
                return self.voc

            def jsc(self):
                self.jsc = np.interp(0, self.xvalues2, self.yvaluesj)
                return self.jsc

            def power(self):
                self.power = np.array(self.xvalues2 * self.yvaluesj)
                self.maxpow = (max(self.power))
                return self.maxpow

            def filfactor(self):
                self.FF = (power(self)/(voc(self)*jsc(self)))
                self.FF2= self.FF*100
                return self.FF2

            def efficiency(self):
                self.efficiency = ((self.jsc*self.voc*self.FF)/self.Pot_luz)*100
                return self.efficiency

        else:
            def voc(self):
                self.voc = np.interp(0, self.yvaluesj, self.xvalues2)
                return self.voc

            def jsc(self):
                self.jsc = np.interp(0, -self.xvalues2, self.yvaluesj)
                return self.jsc

            def power(self):
                self.power = np.array(self.xvalues2 * self.yvaluesj)
                self.maxpow = (max(self.power))
                return self.maxpow

            def filfactor(self):
                self.FF = (power(self)/(voc(self)*jsc(self)))
                self.FF2= self.FF*100
                return self.FF2

            def efficiency(self):
                self.efficiency = ((self.jsc*self.voc*self.FF)/self.Pot_luz)*100
                return self.efficiency


        self.par_print = []
        self.voc_ar=round(voc(self), 2)
        self.jsc_ar=round(jsc(self), 2)
        self.FF_ar =round(filfactor(self), 2)
        self.efficiency_ar= round(efficiency(self), 2)

        self.par_print.append(self.sample_name+"\n")
        self.par_print.append('Cell ' +  str(self.cell) + ' ' + str(self.sentido) + ' Measure ' + str(self.measure )+"\n")
        self.par_print.append("Voc= " + str(self.voc_ar) + " V \n")
        self.par_print.append("Jsc= "+ str(self.jsc_ar) + " mA/cm² \n")
        self.par_print.append("FF= " + str(self.FF_ar) + " %  \n")
        self.par_print.append("n = " + str(self.efficiency_ar) + " % \n")

        return print(print(str(self.sample_name)+":\n%s"%"\n".join(self.par_print)))





    def saveTab(self, cell, sentido, measure):
        self.cell = cell
        self.sentido = sentido
        self.measure = measure
        self.celuls = '-Measure-' + str(self.measure) + '-Cell-' +  str(self.cell) + '-' +  str(self.sentido)
        def dirdata(self):
            self.pathTab = self.path + 'data/'
            if not os.path.exists(self.pathTab):
                os.makedirs(self.pathTab)
            return self.pathTab


        self.directory = dirdata(self)

        self.dir_tabela= os.path.join(self.directory + self.sample_name + '-JV'+ self.celuls +".txt")
        with open(self.dir_tabela, 'w') as tabelaf:
            return np.savetxt(self.dir_tabela, list(zip(self.xvalues2, self.yvaluesj, self.yvalues2)), fmt='%.4e %.12e %.12e', delimiter='  ',newline='\r\n')
            tabelaf.close()

    def savePar(self, cell, sentido, measure):
        self.cell = cell
        self.sentido = sentido
        self.measure = measure
        self.celuls = '-Measure-' + str(self.measure)
        if self.sentido == 'Forward':
            def voc(self):
                self.voc = np.interp(0, -self.yvaluesj, self.xvalues2)
                return self.voc

            def jsc(self):
                self.jsc = np.interp(0, self.xvalues2, self.yvaluesj)
                return self.jsc

            def power(self):
                self.power = np.array(self.xvalues2 * self.yvaluesj)
                self.maxpow = (max(self.power))
                return self.maxpow

            def filfactor(self):
                self.FF = (power(self)/(voc(self)*jsc(self)))
                self.FF2= self.FF*100
                return self.FF2

            def efficiency(self):
                self.efficiency = ((self.jsc*self.voc*self.FF)/self.Pot_luz)*100
                return self.efficiency

        else:
            def voc(self):
                self.voc = np.interp(0, self.yvaluesj, self.xvalues2)
                return self.voc

            def jsc(self):
                self.jsc = np.interp(0, -self.xvalues2, self.yvaluesj)
                return self.jsc

            def power(self):
                self.power = np.array(self.xvalues2 * self.yvaluesj)
                self.maxpow = (max(self.power))
                return self.maxpow

            def filfactor(self):
                self.FF = (power(self)/(voc(self)*jsc(self)))
                self.FF2= self.FF*100
                return self.FF2

            def efficiency(self):
                self.efficiency = ((self.jsc*self.voc*self.FF)/self.Pot_luz)*100
                return self.efficiency

        def dirdata(self):
            self.pathTab = self.path + 'Par/'
            if not os.path.exists(self.pathTab):
                os.makedirs(self.pathTab)
            return self.pathTab


        self.directory = dirdata(self)
        self.relat= os.path.join(self.directory + self.sample_name + '-Par' + self.celuls + ".txt")

        self.arquivo = open(self.relat,'a')
        self.arquivo.write(self.sample_name + ' Measure ' + str(self.measure)  + "\n")
        self.arquivo.write('Cell ' +  str(self.cell) + ' ' + str(self.sentido) + "\n")
        self.arquivo.write("Voc= "+ str(round(voc(self), 2)) + " V \n")
        self.arquivo.write("Jsc= "+ str(round(jsc(self), 2)) + " mA/cmÂ² \n")
        self.arquivo.write("FF= " + str(round(filfactor(self), 2)) + " %  \n")
        self.arquivo.write("n= " + str(round(efficiency(self), 2)) + " % \n")
        self.arquivo.write("\n")
        self.arquivo.write("\n")

        self.arquivo.close()
        return self.arquivo

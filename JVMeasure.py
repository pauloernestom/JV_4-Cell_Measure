#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 14:59:06 2018

@author: paulo
"""
import numpy as np
import pyfirmata
import pyvisa

class Arduino_Control():
    """docstring for Arduino_Control"""
    def __init__(self, porta=''):
        self.porta=porta

    def Arduino(self):
        self.arduino = pyfirmata.Arduino(self.porta)
        return self.arduino

    def contactOff(self, rele='', par=1):
        #relay = 2 4 6 8
        self.rele=rele
        self.par=par #1 = off; 0 = on
        self.arduino.digital[self.rele].write(self.par)

    def contactOn(self, rele='', par=0):#connect arduino relay
        self.rele=rele
        self.par=par #1 = off; 0 = on
        self.arduino.digital[self.rele].write(self.par)

class Keithley_Control():
    """docstring for Keithley_Control"""
    def __init__(self, port='', t_stab='', V_start='', V_end='', step='', delay=''):
        self.port = port
        self.Vstart = V_start
        self.Vend = V_end
        self.step = step
        self.t_stab=t_stab
        self.delay = delay
        self.points = (self.Vend - self.Vstart)/self.step
        self.scanspeed = (self.step/self.delay)/1000

    def conectKeithley(self):

        self.rm = pyvisa.ResourceManager()
        self.rm.list_resources()
        self.Keithley = self.rm.open_resource(self.rm.list_resources()[0]) #on windows, change to self.rm.list_resources()[1]
        self.Keithley.write("*RST")
        self.Keithley.timeout = 2500000
        self.Keithley.write(":SENS:FUNC:CONC OFF")
        self.Keithley.write(":SOUR:FUNC VOLT")
        self.Keithley.write(":SENS:FUNC 'CURR:DC' ")
        self.Keithley.write(":SYST:RCM MULT")
        self.Keithley.write(":SOUR:SOAK " + str(self.t_stab))
        return self.rm

    def paramKeithley(self):

#Start/final voltage and step
        self.Keithley.write(":SOUR:VOLT:STAR " + str(self.Vstart))
        self.Keithley.write(":SOUR:VOLT:STOP " + str(self.Vend))
        self.Keithley.write(":SOUR:VOLT:STEP " + str(self.step))
        self.Keithley.write(":SOUR:SWE:RANG AUTO")

#current limit, direction of sweep and number of points
        self.Keithley.write(":SENS:CURR:PROT 1")
        self.Keithley.write(":SOUR:SWE:SPAC LIN")
        self.Keithley.write(":SOUR:SWE:POIN " + str(int(self.points)))
        self.Keithley.write(":TRIG:DEL 0.00001")
        self.Keithley.write(":TRIG:COUN " + str(int(self.points)))
        self.Keithley.write(":FORM:ELEM CURR")




    def measureCurrent(self, sentido=' '):
        #scan start
        self.sentido = sentido

        if self.sentido == 'Reverse':
            self.Keithley.write(":SOUR:SWE:DIR DOWN")
        else:
            self.Keithley.write(":SOUR:SWE:DIR UP")
        self.Keithley.write(":SOUR:VOLT:MODE SWE")
        self.Keithley.write(":SOUR:DEL " + str(self.delay))
        self.Keithley.write(":OUTP ON")

        self.result = self.Keithley.query(":READ?")
        self.yvalues2 = np.array(self.Keithley.query_ascii_values(":FETC?"))*1000
        self.Keithley.write(":OUTP OFF")
        self.Keithley.write(":SOUR:VOLT 0")
        return self.yvalues2

    def potential_values(self, sentido):
        self.sentido = sentido
        if self.sentido == 'Forward':
            self.xvalues2 = np.array(np.arange(self.Vstart,self.Vend,self.step)[0:-1])
        else:
            self.xvalues2 = np.array(np.arange(self.Vend, self.Vstart, -self.step)[0:-1])
        return self.xvalues2

    def current_density(self, actv_area):
        self.actv_area = actv_area
        self.yvaluesj = (self.yvalues2/self.actv_area)*-1
        return self.yvaluesj

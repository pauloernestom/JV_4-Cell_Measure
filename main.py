#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 13:03:34 2018

@author: paulo
"""
#########################################################################################################
#You must have the Arduino IDE installed on your computer to compile and upload the sketch into the arduino.
#
#The sketch used here is the "StandardFirmata.ino" (found in Arduino IDE examples)
####################################################################################################

import time
start_time = time.time()
import JVMeasure as jvm
from serial.tools import list_ports
import PlotJV_view as pjv
import PhotovCalc as pvc
import time





# Use name. A folder will be created with this name, so, try to use the same name and format for your measurements
User = str(input('User:'))


Measure_name = str(input('Experiment name:'))  # use a name to identify the folder of your measurements

# General directory to save the measuder data

path = ' '

if path == ' ':
	path = str(input('General directory:') or '/home/')




diretorio= path + User + '/' + time.strftime('%d-%b-%Y') + '/' + Measure_name +'/'

parameters =  str(input(' V_start = -0.1;\n V_end = 1.1;\n Active area = 0.12;\n step = 0.01;\n delay = 0.25;\n stabilization time = 2; or \n light power = 100 \n Change parameter?[y/N]:') or 'n')

if parameters == 'n':
    Vinicio = -0.1
    Vfinal = 1.1
    actv_area = 0.12
    passo = 0.01
    delay = 0.25
    estab = 2
    Pot_luz = 100

else:

    while parameters != 'n':

        if parameters == 'y':

            # Initial potential
            Vinicio = float(input('V start:') or -0.1) #Vinicio = -0.1

            # Final potential
            Vfinal = float(input('V end:') or 1.1) #Vfinal = 1.1

            # Active area (cm^2)

            actv_area = float(input('Active area:') or 0.12)
            # Define the step between the potentials, in volts (will change the scan speed)
            # The step should be a multiple of the potential range
            # That is ,Vend-Vstar = step x (integer)
            passo = float(input('Step:') or 0.01)   #0.01

            # Delay between applying the potential and measure the current
            # For step  = 0.01 V the speed will be (delay - 0.1 = 100 mv/s ; 0.2 = 50 mV/s ; 1 = 10 mV/s)
            # speed = step/delay
            delay = float(input('Delay:') or 0.25)   #0.25

            # Stabilization time, with applied potential (in seconds) before starting the scan.
            estab = int(input('Stabilization time:') or 2)
            #Light power (mW/cm^2)
            Pot_luz = int(input('Light power:') or 100)

            parameters =  str(input(' V_start = ' + str(Vinicio) + ';\n V_end = ' + str(Vfinal) + ';\n Active area = ' + str(actv_area) + ';\n step = ' + str(passo) + ';\n delay = ' + str(delay) + ';\n stabilization time = ' + str(estab) + '; or \n light power = ' + str(Pot_luz) + ' \n Change parameter?[y/N]:') or 'n')



        else:
             parameters =  str(input(' V_start = -0.1;\n V_end = 1.1;\n Active area = 0.12;\n step = 0.01;\n delay = 0.25;\n stabilization time = 2; or \n light power = 100 \n Change parameter?[y/N]:') or 'n')
    #----------------------------------------------------- -------------------------------------------------

#
ports = list_ports.comports();
print("Availabe ports:\n%s"%"\n".join(["\t%d: %s"%(portIndex,str(ports[portIndex])) for portIndex in range(len(ports))]))

  #Arduino port. (On windows the port name may change.)
 #   Veja a saída de ports ("Availabe ports: ...."")
for i in range(0,len(ports)):
    if (ports[i].description.find("USB2.0-Serial")==0):
        porta = ports[i].device






vfinal = float(Vfinal)
vinicio = float (Vinicio)
passo2 = float (passo)



 #connecting keithley -----------------------------------------------------------

Kyt_contr=jvm.Keithley_Control(t_stab=estab, V_start=vinicio, V_end=vfinal, step=passo2, delay=delay)

Kyt_contr.conectKeithley()

ard_contr = jvm.Arduino_Control(porta=porta)

arduino = ard_contr.Arduino()




sentido = ['Forward', 'Reverse']
reles = [2, 4, 6, 8]


Moremeasures = str(input('Start new sample?[y/n]:'))
if Moremeasures == 'n':
    ard_contr.contactOff(rele = 2)
    ard_contr.contactOff(rele = 4)
    ard_contr.contactOff(rele = 6)
    ard_contr.contactOff(rele = 8)

while Moremeasures != 'n':

    if Moremeasures == 'y':
         ###############################################################################
         # Sample name (Do not forget to change the name after each measurement, otherwise the data will be overwritten)
        sample_name = str(input('Sample name:'))
         ###############################################################################
        numberofmeasures = int(input('Number of consecutive measures:')) # Number of consecutive measures for the same device
        for measure in range(0, numberofmeasures):
            print('Measure ' + str(measure+1))

            ard_contr.contactOff(rele = 2)
            ard_contr.contactOff(rele = 4)
            ard_contr.contactOff(rele = 6)
            ard_contr.contactOff(rele = 8)

            for i in range(0, len(reles)):

                ard_contr.contactOff(rele=reles[i-1])

                ard_contr.contactOn(rele=reles[i]) #arduino

                Kyt_contr.paramKeithley()




                for s in sentido:
                    print("Measuring Cell " + str(i+1) + " - " + str(s) + " - Wait ... ")
                    yvalues2 = Kyt_contr.measureCurrent(sentido=s)

                    xvalues2 = Kyt_contr.potential_values(s)

                    yvaluesj = Kyt_contr.current_density(actv_area)


                    plotador = pjv.plotJV(xvalues2,yvaluesj,sample_name, diretorio,save=True, show=True)

                    plotador.plot_jv((i+1), s, (measure+1))


                    calc = pvc.PhotovCalc(diretorio, xvalues2, yvaluesj, yvalues2, sample_name, Pot_luz)

                    params = calc.param((i+1), s, (measure+1))

                    calc.saveTab((i+1), s, (measure+1))

                    calc.savePar((i+1), s, (measure+1))
            ard_contr.contactOff(rele = 2)
            ard_contr.contactOff(rele = 4)
            ard_contr.contactOff(rele = 6)
            ard_contr.contactOff(rele = 8)

        Moremeasures = str(input('Start new sample?[y/n]:'))



    else:
        Moremeasures = str(input('Start new sample?[y/n]:'))


ard_contr.contactOff(rele = 2)
ard_contr.contactOff(rele = 4)
ard_contr.contactOff(rele = 6)
ard_contr.contactOff(rele = 8)

print('\n  --- %s seconds --- \n'% (time.time() - start_time))

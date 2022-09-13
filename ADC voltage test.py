# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 21:16:31 2022
Testing the ADC: 
    To read and save data from the two channels of the ADC

Based on ABElectronics file "demo_adcread.py" and 'Demo_ADC_Speed_v3'

Requires SPI Interface Enabled in Raspberry Pi Configuration
 
Requires pre-instalation of SPI_Dev  https://github.com/doceme/py-spidev

Requires ADCDACPi.py from ABElectronics

@author: Caiyi Liu
"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

import time
import os
import numpy as np
import datetime
import matplotlib.pyplot as plt

try:
    from ADCDACPi import ADCDACPi
except ImportError:
    print("Failed to import ADCDACPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from ADCDACPi import ADCDACPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")



def scroll_read(): # Looped read from channel 1, scrolling display

    # create an instance of the ADCDAC Pi with a DAC gain set to 1
    adcdac = ADCDACPi(1)

    # set the reference voltage.  this should be set to the exact voltage
    # measured on the raspberry pi 3.3V rail.
    adcdac.set_adc_refvoltage(3.3)

    while True:
        # clear the console
        os.system('clear')	# Appears not to work on Raspbian

        # read channel 1 in single ended mode
        # and display on the screen

        volts_in_1 = adcdac.read_adc_voltage(1, 0)
        volts_in_2 = adcdac.read_adc_voltage(2, 0)

        #print("Channel 1 ", volts_in_1, " Channel 2 ", volts_in_2)

        time.sleep(0.1)
        
        
def stats_read(samples): # Read N samples of voltage data, do indicative stats.

    samples = max(3, samples) # Set minmum of 3 sample

    samples = int(samples)

    adcdac = ADCDACPi(1)     # create instance of ADCDAC Pi with DAC gain of 1
    
    adcdac.set_adc_refvoltage(3.3)  # set the reference voltage.  


    voltage_data_1 = np.arange(samples * 1.0)
    #voltage_data_2 = np.arange(samples * 1.0)
    time = np.arange(samples * 1.0)
    
    # record start time
    starttime = datetime.datetime.now()

    while samples >= 0 :     # Populate data array

        samples = samples -1
    
        volts_in_1 = adcdac.read_adc_voltage(1, 0)
        #volts_in_2 = adcdac.read_adc_voltage(2, 0)

        voltage_data_1[samples] = volts_in_1
        #voltage_data_2[samples] = volts_in_2
        
        timenow = datetime.datetime.now() #present time
        timeinterval = (timenow - starttime).total_seconds()# time interval converted to seconds
        time[samples] = timeinterval
    return voltage_data_1, 
#voltage_data_2, 
time

def save_data(x, y):
    data = np.column_stack((x, y))
    np.savetxt('ADC_test_data.dat', data)

def plot_data(voltage_data):
    params = {	
	"axes.labelsize": 16,
	"font.size": 12,
	"legend.fontsize": 12,
	"xtick.labelsize": 12,
	"ytick.labelsize": 12,
	"figure.figsize": [12, 6]} 
    
    plt.rcParams.update(params)
    plt.plot(voltage_data, "x", mew=2, ms=5, color="blue") 
    plt.xlabel("Sample")
    plt.ylabel("Voltage")
    plt.title("Raw Voltage Data") 
	
    plt.show()
    
def plot_data_time(time, voltage_data):
     params = {	
	 "axes.labelsize": 16,
	 "font.size": 12,
	 "legend.fontsize": 12,
	 "xtick.labelsize": 12,
	 "ytick.labelsize": 12,
	 "figure.figsize": [12, 6]}  
    
     plt.rcParams.update(params)
     plt.plot(time, voltage_data, "x", mew=2, ms=5, color="blue") 
     plt.xlabel("time")
     plt.ylabel("Voltage")
     plt.title("Raw Voltage Data") 

samples = 10000
time,voltage = stats_read(samples)
plot_data_time(time, voltage)
save_data(time,voltage)


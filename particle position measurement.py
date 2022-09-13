# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 16:01:09 2022

Meaure, store and save the position of the optically trapped particle through reading from the 2-channel ADC

Requires SPI Interface Enabled in Raspberry Pi
 
Requires pre-instalation of SPI_Dev  https://github.com/doceme/py-spidev

Requires ADCDACPi.py from ABElectronics

@author: LCY
"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

#import time
import os
import numpy as np
import datetime
import matplotlib.pyplot as plt


from ADCDACPi import ADCDACPi

        
def stats_read(samples): # Read N samples of voltage data, do indicative stats.

    samples = max(3, samples) # Set minmum of 3 sample

    samples = int(samples)

    adcdac = ADCDACPi(1)     # create instance of ADCDAC Pi with DAC gain of 1
    
    adcdac.set_adc_refvoltage(3.3)  # set the reference voltage.  


    voltage_data_1 = np.arange(samples * 1.0)
    voltage_data_2 = np.arange(samples * 1.0)
    time = np.arange(samples * 1.0) 
    #position_data = np.arange(samples * 1.0)
    
    # record start time
    starttime = datetime.datetime.now()

    while samples >= 0 :     # Populate data array

        samples = samples -1
    
        volts_in_1 = adcdac.read_adc_voltage(1, 0)
        volts_in_2 = adcdac.read_adc_voltage(2, 0)

        voltage_data_1[samples] = volts_in_1
        voltage_data_2[samples] = volts_in_2
        
        timenow = datetime.datetime.now() #present time
        timeinterval = (timenow - starttime).total_seconds()# time interval converted to seconds
        time[samples] = timeinterval
    
     #convertinig into voltage output of the PSD
        
    v_psd_1 = 0.10548 + 0.28319 * voltage_data_1
    v_psd_2 = 0.11319 + 0.2813 * voltage_data_2
    
        
    position_data = np.divide((v_psd_1 - v_psd_2),(v_psd_1 + v_psd_2))
    x_mean = np.mean(position_data)
    print(x_mean)
    return time, position_data    

def save_data(x, y):
    data = np.column_stack((x, y))
    np.savetxt('22_position 100000_LIT ON.dat', data)
    
def plot_data_time(time, data):
     params = {	
	 "axes.labelsize": 16,
	 "font.size": 12,
	 "legend.fontsize": 12,
	 "xtick.labelsize": 12,
	 "ytick.labelsize": 12,
	 "figure.figsize": [50, 6]}  
    
     plt.rcParams.update(params)
     plt.plot(time, data, "x-", mew=2, ms=5, color="blue") 
     plt.xlabel("time")
     plt.ylabel("Particle Position")
     plt.title("Particle Postion vs Time")
     plt.show()
     
samples = 100000
time,position_data= stats_read(samples)
plot_data_time(time, position_data)
save_data(time,position_data)

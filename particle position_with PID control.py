# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 16:01:09 2022

Measure the position of the optically trapped particle with and without the PID control

Requires SPI Interface Enabled in Raspberry Pi Configuration
 
Requires pre-instalation of SPI_Dev  https://github.com/doceme/py-spidev

Requires ADCDACPi.py from ABElectronics

@author: LCY
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


def stats_read(zs_samples, samples):
	'''
	Read from ADC and measure the position of the particle
	
Args:
        zs_samples: number of samples when PID is turned off
        samples: number of samples when PID is turned on
Returns: 
	time: An array of time data
	position_data: an array contains the position of the particle corresponding to each time
	zs: set point
	u_data: A array of PID controller signal
	
	'''
.

    adcdac = ADCDACPi(1)     # create instance of ADCDAC Pi with DAC gain of 1
    
    adcdac.set_adc_refvoltage(3.3)  # set the reference voltage.  
    
   # Find the setpoint ys
    #zs_samples = 25000
    #zs_data = np.arange(zs_samples * 1.0)
    time = [] 
    position_data = []
    i = 0
    u_data = []
    
    # record start time
    starttime = datetime.datetime.now()
    

    while i <= zs_samples - 1:     # Populate data array
        u_bias = 0.5
        adcdac.set_dac_voltage(1, u_bias)
        u_data.append(u_bias)
        
        volts_in_1 = adcdac.read_adc_voltage(1, 0)
        volts_in_2 = adcdac.read_adc_voltage(2, 0)
        
        #convertinig into voltage output of the PSD
        v_psd_1 = 0.10548 + 0.28319 * volts_in_1
        v_psd_2 = 0.11319 + 0.2813 * volts_in_2
        
        z = (v_psd_1 - v_psd_2)/ (v_psd_1 + v_psd_2)
        position_data.append(z)
        
        timenow = datetime.datetime.now() #present time
        timeinterval = (timenow - starttime).total_seconds()# time interval converted to seconds
        time.append(timeinterval)
        i = i+1
    
    #setpoint
    zs = np.mean(position_data)+0.05

        
    # Take data with PID control
    samples = max(3, samples) # Set minmum of 3 sample

    samples = int(samples) + zs_samples
    #PID settings
    u_i = 0 # initialise integrator
    k = 15
    ki = 1
    kd = 0

    while i <= samples - 1 :     # Populate data array
    
        volts_in_1 = adcdac.read_adc_voltage(1, 0)
        volts_in_2 = adcdac.read_adc_voltage(2, 0)
        
        #convertinig into voltage output of the PSD
        v_psd_1 = 0.10548 + 0.28319 * volts_in_1
        v_psd_2 = 0.11319 + 0.2813 * volts_in_2
        
        z = (v_psd_1 - v_psd_2)/ (v_psd_1 + v_psd_2)
        position_data.append(z)
        
        timenow = datetime.datetime.now() #present time
        timeinterval = (timenow - starttime).total_seconds()# time interval converted to seconds
        time.append(timeinterval)
        
        # Averaging/smoothing the data
        n = 20# number of data to average
        z1 = np.mean(position_data[-1*n:])
        z2 = np.mean(position_data[-1*n-1:-2]) # previous block of data
        
        # PID
        timestep = timestep = timeinterval - time[i -1]
        u_p = k * (zs - z1)
        u_i = u_i + ki * (zs - z1) * timestep
        u_d = kd * (z2 - z1) / timestep
        u = u_p + u_i + u_d + u_bias
        
        if u > 2.04:
            u = 2.04 
        elif u < 0:
            u = 0
        
        #print(u)
        adcdac.set_dac_voltage(1,u)
        u_data.append(u)
        i = i+1
	
#Take more data with PID turned off
        
    while i <= samples + zs_samples - 1:     # Populate data array
        u_bias = 0.5
        adcdac.set_dac_voltage(1, u_bias)
        u_data.append(u_bias)
        
        volts_in_1 = adcdac.read_adc_voltage(1, 0)
        volts_in_2 = adcdac.read_adc_voltage(2, 0)
        
        #convertinig into voltage output of the PSD
        v_psd_1 = 0.10548 + 0.28319 * volts_in_1
        v_psd_2 = 0.11319 + 0.2813 * volts_in_2
        
        z = (v_psd_1 - v_psd_2)/ (v_psd_1 + v_psd_2)
        position_data.append(z)
        
        timenow = datetime.datetime.now() #present time
        timeinterval = (timenow - starttime).total_seconds()# time interval converted to seconds
        time.append(timeinterval)
        i = i+1
        
    return time, position_data, zs, u_data    

def save_data(x, y, z):
    data = np.stack((x, y,z),axis = -1)
    np.savetxt('22 15 1 0 20_SHIELD_LIT OFF_ZS0.05.dat', data)
    
def plot_data_time(time, data):
    plt.figure(1)
    params = {	
	 "axes.labelsize": 16,
	 "font.size": 12,
	 "legend.fontsize": 12,
	 "xtick.labelsize": 12,
	 "ytick.labelsize": 12,
	 "figure.figsize": [12, 6]}  
    
    plt.rcParams.update(params)
    plt.plot(time, data, "x", mew=2, ms=5, color="blue") 
    plt.xlabel("time")
    plt.ylabel("Particle Position")
    plt.title("Particle Postion vs Time")
    plt.show()

   
def variance(x, zs_samples,samples):
'''
Calculate the vairance of particle's position with and without PID  

Args:
        x: a array of particle's position
	zs_samples: number of samples when PID is turned off
        samples: number of samples when PID is turned on
Returns: 
	variance1: The variance of the position of the particle without PID
	variance2: The variance of the position of the particle with PID
	
'''
    data1 = x[:zs_samples]
    data2 = x[zs_samples:(zs_samples+samples)]
    
    mean1 = np.mean(data1)
    variance1 = np.sum((data1 - mean1)**2)/ len(data1) # position data without PID
    
    mean2 = np.mean(data2)
    variance2 = np.sum((data2 - mean2)**2)/ len(data2) # position data with PID
    print('variance2 -  variance 1 = ', variance2-variance1)
    print('variance2 / variance 1 = ', variance2/variance1)
    
    return variance1, variance2

# Plot the position of the particle
def plot_difference(time,data,zs):
'''
	Plot the position of the particle relative to the set point
	
'''
    diff = data - zs
    plt.figure(2)
    params = {	
	 "axes.labelsize": 16,
	 "font.size": 12,
	 "legend.fontsize": 12,
	 "xtick.labelsize": 12,
	 "ytick.labelsize": 12,
	 "figure.figsize": [12, 6]}  
    
    plt.rcParams.update(params)
    plt.plot(time, diff, "x", mew=2, ms=5, color="blue") 
    plt.xlabel("time")
    plt.ylabel("Difference")
    plt.title("Deviation from the setpoint")
    plt.show()

# Plot the 
def plot_pid(time,u):
'''
Plot the PID controller signal as a function of time
	
'''
    plt.figure(3)
    params = {	
	 "axes.labelsize": 16,
	 "font.size": 12,
	 "legend.fontsize": 12,
	 "xtick.labelsize": 12,
	 "ytick.labelsize": 12,
	 "figure.figsize": [12, 6]}  
    
    plt.rcParams.update(params)
    plt.plot(time, u_data, "x", mew=2, ms=5, color="blue") 
    plt.xlabel("time")
    plt.ylabel("u")
    plt.show()
    
    
def plot_pidandpos(time,u,pos):
'''
Plot the PID controller signal and the position of the particle as a function of time
	
'''
    plt.figure(3)
    params = {	
	 "axes.labelsize": 16,
	 "font.size": 12,
	 "legend.fontsize": 12,
	 "xtick.labelsize": 12,
	 "ytick.labelsize": 12,
	 "figure.figsize": [12, 6]}  
    
    plt.rcParams.update(params)
    plt.plot(time, u, "x-", mew=2, ms=5, color="blue")
    plt.plot(time, pos, "x-", mew=2, ms=5, color="r") 
    plt.xlabel("time")
    plt.ylabel("u")
    plt.show()

zs_samples = 10000 # number of samples when PID is turned off
samples = 10000 # number of samples when PID is turned on 
time,position_data,zs ,u_data = stats_read(zs_samples, samples)
plot_data_time(time, position_data)
plot_difference(time,position_data,zs)
plot_pid(time,u_data)
plot_pidandpos(time,u_data,position_data)
variance(position_data,zs_samples,samples)
save_data(time,position_data, u_data)

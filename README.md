# Optical-Levitation-Trap-Project

This project containts Python codes that simulates an optically trapped particle, calculates the beam radius of the trapping beam and records data from the ADC board.

<pre>
Simulation of Optically Trapped Particle:
  'Optical trap spring model.ipynb'
      * contains a model for the optically trapped particle based on a damped harmonic oscillator. 
      * The equation of motion for the damped harmonic oscillator system was solved. 
      * The buoyancy force was also added to the system
     
  'Brownina Motion.ipynb'
      * simulates a Brownian particle in a visous fluid
      * Plots the Fourier transform of its motion
      
      
Calculation of the Beam Radius:
  'Beam Radius Measurement_D4Sigma.ipynb'
      * Measures the beam radius for a greyscale image
      * Beam radius defined according to the D4 Sigma definition following ISO 11146-1 section 9
      
Data Collection and PID Controll:
The software below works for the ADCDAC board based on the Microchip MCP3202 A/D converter from AB Electronics.
They require 
  * SPI Interface Enabled in Raspberry Pi Configuration
  * pre-instalation of SPI_Dev  https://github.com/doceme/py-spidev
  * Python module ADCDACPI.py from AB Electronics

  'ADC voltage test.py'
    * Read and plot the output of the 2-channel ADC
    
  'particle position measurement.py'
    * Meaure, store and save the position of the optically trapped particle through reading from the 2-channel ADC
    * Plot the position as a function of time
    
  'particle position_with PID control.py '
    * Meaure, store and save the position of the optically trapped particle through reading from the 2-channel ADC
    * Implement a Proportional Intefral Derivative (PID) Control through interacting with the DAC
    * Plot the position as a function of time
    * Calculate variance with and without the PID control
    

      
</pre>

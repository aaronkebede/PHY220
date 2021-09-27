# -*- coding: utf-8 -*-
import numpy as np;import matplotlib.pyplot as plt
import math
from lmfit import Model, Parameters

frequency, amplitude,phase = np.loadtxt("Rc_Filter_Data.csv",delimiter=',',unpack=True,skiprows=1)
plt.figure(1) #create our first figure, to plot data, initial guess, and final result.
plt.plot(frequency,amplitude,'b.')
plt.show()

RC=0.00001

def graph(formula, x_range):  
    x = np.array(x_range)  
    y = formula(x)# <- note now we're calling the function 'formula' with x
    
    plt.plot(x, y)  
    plt.show() 
       
pi=math.pi
  
def my_formula(x):
    value =320/np.sqrt(1+(2*pi*RC*x)**2)
    return value

graph(my_formula, range(0, 100000))

def Amplitude_of_Filter(x,amp,RC):
    amplitude=amp/np.sqrt(1+(2*pi*RC*x)**2)
    return amplitude
    

model = Model(Amplitude_of_Filter)

print ("Independent vars: ", model.independent_vars) #print out to confirm what we just did
print ("Parameters: ", model.param_names)

p = Parameters()
p.add_many(('amp', 320, True, 0, 350, None), # params for first fit, 
           ('RC', 0.00001, True, None, None, None))
                
#Parameters:	
#name (None or string – will be overwritten during fit if None.) – parameter name
#value – the numerical value for the parameter
#vary (boolean (True/False) [default True]) – whether to vary the parameter or not.
#min – lower bound for value (None = no lower bound).
#max – upper bound for value (None = no upper bound).
#expr (None or string) – mathematical expression to use to evaluate value during fit.


result =model.fit(amplitude, x=frequency, params=p, weights = None )

plt.figure(2)
plt.plot(frequency,amplitude,'b.')
plt.plot(frequency, result.init_fit, 'b--', label="Initial Guess", linewidth=1)
plt.plot(frequency, result.best_fit, 'r--', label="One oscillator fit", linewidth=1)
#print result.fit_report() 
R=700
p = result.params
value_dictionary= p.valuesdict()
RC_value=value_dictionary['RC']
print (RC_value)
print (RC_value/700)
def my_formula2(x):
    value =-180/pi*np.arctan(2*pi*RC*x)
    return value
#now let's fit the phase

def Phase_of_Filter(x,RC,offset):
    Phase=-180/pi*np.arctan(2*pi*RC*x)+offset
    return Phase
model2= Model(Phase_of_Filter)   
print ("Independent vars: ", model2.independent_vars) #print out to confirm what we just did
print ("Parameters: ", model2.param_names)

p = Parameters()
p.add_many(('RC', RC_value, True, None, None, None),('offset', 0, False, None, None, None))
result =model2.fit(phase, x=frequency, params=p, weights = None )
plt.figure(3)
plt.plot(frequency,phase,'b.')
plt.plot(frequency, result.init_fit, 'b--', label="Initial Guess", linewidth=1)
plt.plot(frequency, result.best_fit, 'r--', label="One oscillator fit", linewidth=1)

p = result.params
value_dictionary= p.valuesdict()
RC_value=value_dictionary['RC']
Offset=value_dictionary['offset']
print (RC_value)
print (RC_value/700)
print (Offset)


#graph(my_formula2, range(0, 100000))
#plt.plot(frequency,phase,'r+')
plt.show()

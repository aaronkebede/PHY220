import numpy as np;import matplotlib.pyplot as plt
from lmfit import Model, Parameters

wl, t1,t2,t3 = np.loadtxt("Transmission_of_3_films.txt",unpack=True,skiprows=1) #first data row is incomplete. Let's just skip it.

data = np.concatenate((t3,t2,t1)) #assemble a data array by concatenating the three data sets.
wl = np.concatenate((wl+6000,wl+3000,wl)) #assemble the corresponding wavelength array, taking care of shifting the data sets so that they can be recognized by the function, based on the wavelength value.

c = 2.99792458e8

def sqr(v):
    return v*v
    
def Transmission(x,ns,s1,lam1,alpha0,alpha0_lam,d_lam,d1,d2,d3):
    d = np.where(x<3000,d3,np.where(x<6000,d2,d1)) #These  identifies which data set we need to calculate the transmission for, based on the wavelength
    x = np.where(x<3000,x,np.where(x<6000,x-3000,x-6000)) # data sets are identified by offsets in the wavelength. Remove the offset for the calculations
    
    n = np.sqrt(s1/(1-sqr(lam1/x))+1)
    nu = c/(x*1E-9)
    nu0 = c/(alpha0_lam*1E-9)
    deltanu = c/sqr(alpha0_lam*1E-9)*d_lam*1E-9 # this is the delta_nu corresponding to the wavelength interval d_lam around the abs wavelength of lam0
    alpha = alpha0*np.exp(-sqr((nu-nu0)/deltanu))
    taf = 2*n/(1+n)
    tfs = 2*ns/(n+ns)
    rfa = (1-n)/(1+n)
    rfs = (ns-n)/(ns+n)
    k = 2*np.pi/x * n 
    
    tf = taf*tfs*np.exp(-alpha*d/2)/( 1 - rfa*rfs*np.exp(2*1.j*d*k)*np.exp(-alpha*d) )
    tsa=2*1/(ns+1)
    return sqr(np.abs(tf)*tsa)
    

model = Model(Transmission)


p = Parameters()
p.add_many(('ns', 1.5, False, None, None, None), # params for first fit, only one oscillator and the correction for the infrared
           ('s1', 2, True, 0, 10, None),
           ('lam1', 400, True, None, None, None),
           ('alpha0', 0.01, True, None, None, None),
           ('alpha0_lam', 500, True, None, None, None),
           ('d_lam', 50, True, None, None, None),
           ('d1', 300, True, None, None, None),
           ('d2', 600, True, None, None, None),
           ('d3', 900, True, None, None, None))

result =model.fit(data, x=wl, params=p ) 

plt.figure(1)
plt.plot(wl,data,'g.')
plt.plot(wl, result.init_fit, 'r--', linewidth=1)
plt.plot(wl, result.best_fit, 'b-', linewidth=2)
plt.legend()
plt.show()

plt.figure(2) # create a second figure, for plotting the residuals
plt.plot(wl, result.best_fit - data, 'b.', label="Residuals") #residuals are the difference between best fit and data
plt.axhline(y=0, xmin=0.0, xmax=1,  color = 'r') # add an horizontal line at zero.
plt.legend()
plt.show()


print result.fit_report()
fig=result.plot() 
fig.show()
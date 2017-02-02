# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 15:50:20 2017

@author: bling
"""
import matplotlib.pyplot as plt
import numpy as np
u=np.load('u.npy')
#t=np.load('time.npy')
udr=np.load('udr.npy')
vdr=np.load('vdr.npy')
v=np.load('v.npy')
um=np.load('umo.npy')
vm=np.load('vmo.npy')
plt.figure()
plt.title('u')
plt.plot(u,'g-',label='mooring B01')
plt.plot(udr,'r-',label='drifter')
plt.plot(um,'b-',label='model')
plt.ylabel('m/s')
plt.xlabel('hours')
#plt.ylim('2017, 1, 27, 0, 0','2017, 1, 31, 17, 0')
plt.legend(loc='best')
plt.savefig('u',dpi=700)
plt.figure()
plt.title('v')
plt.plot(v,'g-',label='mooring B01')
plt.plot(vdr,'r-',label='drifter')
plt.plot(vm,'b-',label='model')
plt.legend(loc='best')
plt.ylabel('m/s')
plt.xlabel('hours')
plt.savefig('v',dpi=700)

# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 16:34:20 2016
calculate drifter v and v
INPUT: output of "data_processing.py" which creates segments of drifter tracks in individual csv file
OUTPUT: individual npy file for time, u, v,etc but why not make one file?
@author: xiaojian
"""

import datetime as dt
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy import  interpolate
from matplotlib.dates import date2num,num2date
######## Hard codes ##########
F='data/'
ii=0
uu=[]
vv=[]
lon11=[]
lat11=[]
ttii=[]
for a in np.arange(9): # 9 segments
    drifters = np.genfromtxt(F+str(a)+'.csv',dtype=None,names=['ids','time','lon','lat','depth'],delimiter=',',skip_header=1)  
    start_times=datetime.strptime(drifters['time'][0], '%Y-%m-%d'+'T'+'%H:%M:%SZ')       
    rawtime=[]
    for a in np.arange(len(drifters['time'])):
        print drifters['time'][a]
        rawtime.append(date2num(datetime.strptime(drifters['time'][a], '%Y-%m-%d'+'T'+'%H:%M:%SZ')))
    print rawtime
    t1=np.ceil(np.min(rawtime)*24.)/24.
    t2=np.floor(np.max(rawtime)*24.)/24.
    tdh=np.arange(t1,t2,1./(24*6)) #interpolation
    print tdh
    for m in np.arange(len(tdh)):
        print num2date(tdh[m])
    try:
        
        lo=interpolate.interp1d(rawtime,drifters['lon'],kind='cubic')  
        la=interpolate.interp1d(rawtime,drifters['lat'],kind='cubic')
        dr=dict(lon=[],lat=[],time=[])
        for a in np.arange(len(tdh)):
            dr['lon'].append(lo(tdh[a]))
            dr['lat'].append(la(tdh[a]))
            dr['time'].append(tdh[a])
    except:
        continue
    print dr['time']
    ii=ii+1
    print ii
    drift=dict(lon=[],lat=[],time=[])
    for a in np.arange(len(tdh)):
        if num2date(tdh[a]).minute==0 and num2date(tdh[a]).second==0:
            drift['lon'].append(dr['lon'][a])
            drift['lat'].append(dr['lat'][a])
            drift['time'].append((num2date(tdh[a])).replace(tzinfo=None))
    print drift['time']    
    ND=len(drift['time'])
    print ND
    udh=[]#np.zeros(ND,dtype=float)   
    vdh=[]#np.zeros(ND,dtype=float)
    th=[]
    lo=[]
    la=[]
    for i in range(1,ND-1):
        print i
        udh.append((drift['lon'][i+1]-drift['lon'][i-1])*np.cos(drift['lat'][i]*np.pi/180.)*111111/float(60*60*2))
        vdh.append((drift['lat'][i+1]-drift['lat'][i-1])*111111/float(60*60*2))
        th.append(drift['time'][i])
        lo.append(drift['lon'][i])
        la.append(drift['lat'][i])
    plt.plot(dr['lon'],dr['lat'],'r-') 
    plt.plot(drifters['lon'],drifters['lat'],'b-')
    plt.plot(drift['lon'],drift['lat'],'yo-')
    uu.append(udh)
    vv.append(vdh)
    lon11.append(lo)
    lat11.append(la)
    ttii.append(th)
plt.plot(np.hstack(lon11),np.hstack(lat11),'go-')
np.save('udr',np.hstack(uu))
np.save('vdr',np.hstack(vv))
np.save('lon',np.hstack(lon11))
np.save('lat',np.hstack(lat11))
np.save('th',np.hstack(ttii))

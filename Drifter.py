# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 16:34:20 2016

@author: hxu
"""

import datetime as dt
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy import  interpolate
from matplotlib.dates import date2num,num2date
#from barycentric_polygonal_interpolation import get_drifter_track,get_fvcom,get_roms,calculate_SD,drifterhr
######## Hard codes ##########
drifter_data_type='erddap'#'raw''csv','erddap','npy'  the method of get drifter data
Model=['30yr']#'GOM3','massbay','30yr','ROMS'# model want to be compair with drifter track
drifter_ID =[]#if drifter_ID=[],get drifter id from list  
drifter_list=[]
depth =[-1]
track=12
days=42#>=3
track_days=1
restart_days=1
start_times =[dt.datetime(2010,5,19,9,13,0,0)]
wind_get_type='FVCOM'
wind=0 
F='data/'
file_drID=[]

if 'ROMS' in Model:
    romstmeandis=[];romstmindis=[];romstmaxdis=[];romsdmeandis=[];romsdmindis=[];romsdmaxdis=[]
if '30yr' in Model:
    spdis=[];disrat=[];idddd=[];lllo=[];llla=[]
if 'GOM3' in Model:
    gomtmeandis=[];gomtmindis=[];gomtmaxdis=[];gomdmeandis=[];gomdmindis=[];gomdmaxdis=[]
if 'massbay' in Model:
    masstmeandis=[];masstmindis=[];masstmaxdis=[];massdmeandis=[];massdmindis=[];massdmaxdis=[]
ii=0
uu=[]
vv=[]
lon11=[]
lat11=[]
ttii=[]
plt.figure()
for a in np.arange(9):
    #print a
    iiiii=a
    drifters = np.genfromtxt(F+str(a)+'.csv',dtype=None,names=['ids','time','lon','lat','depth'],delimiter=',',skip_header=1)  
    try:
        day=(datetime.strptime(drifters['time'][-1], '%Y-%m-%d'+'T'+'%H:%M:%SZ')-datetime.strptime(drifters['time'][0], '%Y-%m-%d'+'T'+'%H:%M:%SZ')).days
    except:
        continue
    
    if day<0.16:
        continue
    #ii=ii+1
    #print ii
    aa=a
    d_time=datetime.strptime(drifters['time'][0], '%Y-%m-%d'+'T'+'%H:%M:%SZ')       
    start_times=d_time
    rawtime=[]
    for a in np.arange(len(drifters['time'])):
        rawtime.append(date2num(datetime.strptime(drifters['time'][a], '%Y-%m-%d'+'T'+'%H:%M:%SZ')))
    t1=np.ceil(np.min(rawtime)*24.)/24.
    t2=np.floor(np.max(rawtime)*24.)/24.
    tdh=np.arange(t1,t2,1./(24*6))
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
    ii=ii+1
    print ii
    #if ii==61:
    #   print iiiii
    #   break
        
    drift=dict(lon=[],lat=[],time=[])
    for a in np.arange(len(tdh)):
        if num2date(tdh[a]).minute==0 and num2date(tdh[a]).second==0:
            drift['lon'].append(dr['lon'][a])
            drift['lat'].append(dr['lat'][a])
            drift['time'].append((num2date(tdh[a])).replace(tzinfo=None))
        
    #print drifter_points
    ND=len(drift['time'])
    udh=[]#np.zeros(ND,dtype=float)   
    vdh=[]#np.zeros(ND,dtype=float)
    th=[]
    lo=[]
    la=[]
    Coef=111111./86400. # deg/day -> m/s
    #print Coef
    for i in range(1,ND-1):
        print i
        udh.append((drift['lon'][i+1]-drift['lon'][i-1])/(float(2))*Coef*np.cos(drift['lat'][i]*np.pi/180.))
        vdh.append((drift['lat'][i+1]-drift['lat'][i-1])/(float(2))*Coef)
        th.append(drift['time'][i])
        lo.append(drift['lon'][i])
        la.append(drift['lat'][i])
    plt.plot(dr['lon'],dr['lat'],'r-') 
    plt.plot(drifters['lon'],drifters['lat'],'b-')
    uu.append(udh)
    vv.append(vdh)
    lon11.append(lo)
    lat11.append(la)
    ttii.append(th)
np.save('udr',np.hstack(uu))
np.save('vdr',np.hstack(vv))
np.save('lon',np.hstack(lon11))
np.save('lat',np.hstack(lat11))
np.save('th',np.hstack(ttii))
    
    #print ii
'''
    #plt.xlim(-70,-65)
    #plt.ylim(41,43)
    #plt.show()
    lonnn=[]
    lattt=[]
    distance=[]
    meantimedis=[]
    meandisdist=[]
    model_points_s=[]
    model_points =dict(lon=[],lat=[],time=[])
    iiiiiiiiiii=0
    plt.show()
    days=(num2date(dr['time'][-1])-num2date(dr['time'][0])).days

    for nday in np.arange(1,days,restart_days): 
        modelpoints = dict(lon=[],lat=[],time=[]) 
        wmodelpoints = dict(lon=[],lat=[],time=[])
        start_time=drift['time'][(nday-1)*24]
        end_times=drift['time'][(nday-1+track_days)*24]
        #print start_time
        #print end_times

        i=Model[0]
        GRIDS= ['GOM3','massbay','30yr']
        if i in GRIDS:
            get_obj =  get_fvcom(i)
            url_fvcom = get_obj.get_url(start_time,end_times)                
            b_points = get_obj.get_data(url_fvcom)
            #print '##########################'
            #print drifter_points['lon_hr'][(nday-1)*24]
            #print drifter_points['lat_hr'][(nday-1)*24]
            #print start_time
            try:
                modelpoints,windspeed= get_obj.get_track(drift['lon'][(nday-1)*24],drift['lat'][(nday-1)*24],drifters['depth'][0],start_time,wind,wind_get_type)
                
            except:
                print 'There is no model-point near the given-point'
                continue
        if i=='ROMS':        
            get_obj = get_roms()
            url_roms = get_obj.get_url(start_time,end_times)
            get_obj.get_data(url_roms)
            
            modelpoints ,windspeed= get_obj.get_track(drift['lon'][nday*24],drift['lat'][nday*24],drifters['depth'][0],start_time,wind,wind_get_type)
            
        model_points['lon'].append(modelpoints['lon']); model_points['lat'].append(modelpoints['lat']);model_points['time'].append(modelpoints['time'])
        
        dist=[]
        
        if len(modelpoints['lon'])-1==24*track_days:
            dist,meantdis,meandisdis=calculate_SD(modelpoints,drift['lon'][(nday-1)*24:(nday-1+track_days)*24+1],drift['lat'][(nday-1)*24:(nday-1+track_days)*24+1],drift['time'][(nday-1)*24:(nday-1+track_days)*24+1]) 
        else:
            continue
        #dist,meantdis,meandisdis=calculate_SD(modelpoints,drifter_points['lon_hr'][(nday-1)*24:(nday-1+track_days)*24+1],drifter_points['lat_hr'][(nday-1)*24:(nday-1+track_days)*24+1],drifter_points['h_hr'][(nday-1)*24:(nday-1+track_days)*24+1]) 
        iiiiiiiiiii=iiiiiiiiiii+1 
        if meantdis>100000000000000 or meandisdis>10000000000000000:
            continue
        distance.append(dist)#one drifter one model all distance 
        meandisdist.append(meandisdis) #one drifter one model per day mean distance/dist                
        meantimedis.append(dist[-1])#one drifter one model per day mean distance/day
        lonnn.append(drift['lon'][(nday-1)*24])
        lattt.append(drift['lat'][(nday-1)*24])
    try:
        
        plt.figure(1) 
        plt.title('id=%s drifter track vs modle=%s'%(drifters['ids'][0],Model[0]))
        for haha in np.arange(0,iiiiiiiiiii,restart_days):#drifters['days'][num]-2,restart_days): drifters['days'][num]-2,restart_days):#
            plt.plot(model_points['lon'][haha],model_points['lat'][haha],'ro-')
        
        plt.plot(drift['lon'][0:],drift['lat'][0:],'bo-')
        plt.grid(True)
        plt.savefig('id=%s drifter track vs modle=%s '%(drifters['ids'][0],Model[0]))  
        plt.show()
        
        plt.figure(2)
        plt.title('id=%s drifter  vs modle=%s distance'%(drifters['ids'][0],Model[0]))
        iddd=[]
        for x in range(len(distance)):
            plt.plot(distance[x][:])
            plt.text(track_days*24-3,distance[x][-1],'meandis=%.2f' %(meantimedis[x]),color='red',fontsize=12)
            iddd.append(drifters['ids'][0])
        plt.ylabel('distance(km)')   
        plt.xlabel('time')
        #plt.savefig('id=%s drifter   vs modle=%s distance'%(drifters['ids'][a],Model[0]))
        plt.show()
        
        if Model[0] == 'ROMS':
            romstmeandis.append(np.mean(meantimedis))
            romstmindis.append(min(meantimedis))
            romstmaxdis.append(max(meantimedis))
            romsdmeandis.append(np.mean(meandisdist))
            romsdmindis.append(min(meandisdist))
            romsdmaxdis.append(max(meandisdist))
        if Model[0] == '30yr':
            idddd.append(iddd)
            spdis.append(meantimedis)
            disrat.append(meandisdist)
            lllo.append(lonnn)
            llla.append(lattt)
        if Model[0] == 'GOM3':
            gomtmeandis.append(np.mean(meantimedis))
            gomtmindis.append(min(meantimedis))
            gomtmaxdis.append(max(meantimedis))
            gomdmeandis.append(np.mean(meandisdist))
            gomdmindis.append(min(meandisdist))
            gomdmaxdis.append(max(meandisdist))
        if Model[0] == 'massbay':
            masstmeandis.append(np.mean(meantimedis))
            masstmindis.append(min(meantimedis))
            masstmaxdis.append(max(meantimedis))
            massdmeandis.append(np.mean(meandisdist))
            massdmindis.append(min(meandisdist))
            massdmaxdis.append(max(meandisdist))
        file_drID.append(drifters['ids'][0])
    except:
        continue

data=[];tdata=[];model=[];dataaa=[]
if 'ROMS' in Model:
    data.append(romstmeandis);data.append(romstmindis);data.append(romstmaxdis);data.append(romsdmeandis);data.append(romsdmindis);data.append(romsdmaxdis);
    model.append('ROMS')
if '30yr' in Model:
    tdata.append(np.hstack(idddd));tdata.append(np.hstack(lllo));tdata.append(np.hstack(llla));data.append(np.hstack(spdis));data.append(np.hstack(disrat))
    model.append('30yr')
if 'GOM3' in Model:
    data.append(gomtmeandis);data.append(gomtmindis);data.append(gomtmaxdis);data.append(gomdmeandis);data.append(gomdmindis);data.append(gomdmaxdis);
    model.append('GOMS')
if 'massbay' in Model:
    data.append(masstmeandis);data.append(masstmindis);data.append(masstmaxdis);data.append(massdmeandis);data.append(massdmindis);data.append(massdmaxdis);
    model.append('massbay')
    
#tdata.append(file_drID)
for w in range(0,len(data),1):
    ldata=[]    
    for e in data[w]:
        e="%.2f" %e
        ldata.append(e)
    tdata.append(ldata)
            
chat=map(list, zip(*tdata))  
csvfile = file('drifter_vs_model use hourly data.csv', 'wb')
writer = csv.writer(csvfile)
fh=['ids']
fh.append('lon')
fh.append('lat')
for z in range(len(model)):
    fh.append('%s_separation(km/day)' %model[z] )
    fh.append('%s_separation(km/km)' %model[z] )
writer.writerow(fh)
writer.writerows(chat)
csvfile.close()
'''

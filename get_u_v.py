# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 16:15:52 2017

@author: bling
"""
import numpy as np
import netCDF4
import math
import datetime as dt
from datetime import datetime,timedelta
def get_u_v(time,lon,lat,layer):
    url='''http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/Seaplan_33_Hindcast_v1/gom3_201111.nc?lonc[0:1:90414],latc[0:1:90414],Times[0:1:720],u[0:1:720][0:1:44][0:1:90414],v[0:1:720][0:1:44][0:1:90414]'''
    #url='''http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/archives/necofs_mb?lonc[0:1:165094],latc[0:1:165094],Times[0:1:34655],u[0:1:34655][0:1:9][0:1:165094],v[0:1:34655][0:1:9][0:1:165094]'''
    #url = '''http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3?u[0:1:333551][0:1:44][0:1:90414],v[0:1:333551][0:1:44][0:1:90414]'''       
    nc = netCDF4.Dataset(url)
    args=['u','v','Times','lonc','latc']
    data = {}
    for arg in args:
        data[arg] = nc.variables[arg]
    Times=data['Times'][:]
    lonc1=data['lonc'][:]
    latc1=data['latc'][:]
    np.save('Tim',Times)
    np.save('lonc',lonc1)
    np.save('latc',latc1)
    Times=np.load('Tim.npy')
    #print 'Times',Times[0]
    Time=[]
    for a in np.arange(len(Times)):
        #print Times[a]
        #print Times[a][-9:-7]
        '''
        if Times[a][-9:-7]=='60':
            #print Times[a][:-10]
            #print Times[a][:-7]
            mm=str(datetime.strptime(Times[a][:-10], '%Y-%m-%d'+'T'+'%H:%M')+timedelta(hours=1/float(60)))+':00'
            Times[a]=mm
            #print Times[a]
            Time.append(datetime.strptime(Times[a][:], '%Y-%m-%d'+' '+'%H:%M:%S:00'))
            continue
        '''
        #print 'Times[a][:13]',str(Times[a][0])+str(Times[a][1])+str(Times[a][2])+str(Times[a][3]),str(Times[a][5])+str(Times[a][6]),str(Times[a][8])+str(Times[a][9]),str(Times[a][11])+str(Times[a][12])
        #Time.append(datetime.strptime(Times[a][:], '%Y-%m-%d'+' '+'%H:%M:%S:00'))
        Time.append(dt.datetime(int(str(Times[a][0])+str(Times[a][1])+str(Times[a][2])+str(Times[a][3])),int(str(Times[a][5])+str(Times[a][6])),int(str(Times[a][8])+str(Times[a][9])),int(str(Times[a][11])+str(Times[a][12]))))#,datetime.strptime(str(Times[a][0:13]), '%Y-%m-%d'+'T'+'%H'))
    lonc=np.load('lonc.npy')
    latc=np.load('latc.npy')
    t=[]
    #print 'len(Time)',len(Time)
    #print time
    for a in np.arange(len(Time)):
        t.append(abs(Time[a]-time))
    #print Time
    print 't',len(t)
    t1=np.argmin(t)
    print 't1',t1
    print time
    print Time[t1]
    dis=[]
    for a in np.arange(len(lonc)):
        dis.append((lonc[a]-lon)*(lonc[a]-lon)+(latc[a]-lat)*(latc[a]-lat))
    l=np.argmin(dis)
    print 'l',l#,data['u'][t1][layer][l],data['v'][t1][layer][l]
    print lon,lat
    print lonc[l],latc[l]
    return data['u'][t1][layer][l],data['v'][t1][layer][l]
'''
time='1985-07-01T12:00:00'#start_times =[dt.datetime(2010,5,19,9,13,0,0)]
time=datetime.strptime(time, '%Y-%m-%d'+'T'+'%H:%M:%S')
lon=-68.1202774
lat=43.80513
layer=0
u,v=get_u_v(time,lon,lat,layer)
print u,v
''' 
data = np.genfromtxt('1.csv',dtype=None,names=['s','time','c','sudu','e','jiao','g','tem','i','lon','lat','depth'],delimiter=',',skip_header=2)  
u=[]
v=[]
    
layer=0  
time=[]
lon=[]
lat=[]
#for a in np.arange(len(data['time'])):
for a in np.arange(len(data['time'])):
    #if datetime.strptime(data['time'][a], '%Y-%m-%d'+'T'+'%H:%M:%SZ')>=dt.datetime(2017,1,27,0,0,0,0):
    print a
    time.append(datetime.strptime(data['time'][a], '%Y-%m-%d'+'T'+'%H:%M:%SZ'))
    v.append(float(data['sudu'][a])*np.cos(float(data['jiao'][a])/float(180)*math.pi)*0.01)
    u.append(float(data['sudu'][a])*np.sin(float(data['jiao'][a])/float(180)*math.pi)*0.01)
    lon.append(data['lon'][a])
    lat.append(data['lat'][a])
np.save('u',u)
np.save('v',v)
np.save('time',time)
uu=[]
vv=[]
n=[]

for a in np.arange(len(lon)):
    print 'a',a
    #try:
    u1,v1=get_u_v(time[a],lon[a],lat[a],layer)
    #except:
        #continue
    
    n.append(a)
    uu.append(u1)
    vv.append(v1)
np.save('umo',uu)
np.save('vmo',vv)
np.save('n',n)


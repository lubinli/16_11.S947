# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 11:14:27 2016

@author: C
"""

#http://stackoverflow.com/questions/15843123/reading-multiple-csv-files-into-python-pandas-dataframe 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def merge24():
    hours = range(0,24)
    df24 = pd.DataFrame()
    
    for hour in hours:
        path ='data/Hourly Flows/Rn_OD_%d-%d.txt' % (hour, hour+1)
        frame = pd.read_csv(path, header=None, names=['oid', 'did', 'close_rid_origin', 'close_rid_dest', 'flow'])
    
        oid_list = frame['oid'].tolist()
        did_list = frame['did'].tolist()
    
        indice = []   
        for i in range(len(oid_list)):
            indice.append(str(oid_list[i]) + '-' + str(did_list[i]))    

        frame['OD'] = indice
        frame.set_index('OD', inplace=True)
    
        if hour == 0:
            df24 = df24.append(frame)
        else: 
            df24 = df24.join(frame['flow'], how = 'outer', lsuffix='-h%d' % (hour-1), rsuffix='-h%d' % (hour))

    return df24

#-------
merged = merge24()

hours = range(0,24)
hour_list = []

for hour in hours:
    hour_list.append('flow-h%d' % (hour))

    merged['flow-h%d' % (hour)].fillna(value=0, inplace=True)

merged.drop(['did','close_rid_origin','close_rid_dest'], inplace=True)

#Grouping O-D flows by oid, since there are otherwise too many entries to meaningfully visualize
grouped = merged.groupby('oid').sum()

#However, after some exploration, I realized that there are even too many OIDs to graph well.
#So I will graph the hourly flow of the 10 OIDs with the highest DAILY flow
grouped['OID total'] = grouped[hour_list].sum(axis=1, skipna=False)
grouped.sort('OID total', ascending=False)

grouped[hour_list].head(n=10).transpose().plot(kind='area', stacked=False, legend=True, title='10 OIDs with highest daily flows', label='OID')   


#The average flow values across all towers
df24['average'] = df24[hour_list].mean(axis=0, skipna=False)

#The maximum flow values across all towers
df24['max'] = df24[hour_list].max(axis=0, skipna=False)

#The minimum flow values across all towers
df24['min'] = df24[hour_list].min(axis=0, skipna=False)

#The median flow values across all towers
df24['median']=df24[hour_list].median(axis=0, skipna=False)

print df24.head(n=10)

#df24['average','max','min','median'].transpose().plot(kind='area', stacked=False, legend=True, title='Tower Flows')


#PART II
towers=pd.read_csv("data/Hourly Flows/towers_index.txt", header=None, names=['Latitude', 'Longitude', 'Closest node ID'])
towers.reset_index(level=0, inplace=True)

all_hours = pd.DataFrame()

for hour in hours:
    path ='data/Hourly Flows/Rn_OD_%d-%d.txt' % (hour, hour+1)
    frame = pd.read_csv(path, header=None, names=['oid', 'did', 'close_rid_origin', 'close_rid_dest', 'flow'])
    grouped = frame[['flow','oid']].groupby('oid').mean()
    grouped.reset_index(level=0, inplace=True)
    OD_location = grouped.join(towers, on='oid')
    
    if hour == 0:
        all_hours = all_hours.append(OD_location)
    else:
        all_hours = all_hours.join(frame['flow'], how = 'outer', lsuffix='-h%d' % (hour-1), rsuffix='-h%d' % (hour))

all_hours.fillna(value=0, inplace=True)

print all_hours.head(n=40)

hour_list = []
for hour in hours:
    hour_list.append('flow-h%d' % (hour))

import matplotlib.pyplot as plt
import matplotlib.cm as cm
#from matplotlib import colors
#from matplotlib.colors import LinearSegmentedColormap

def color(array, colors):
    #array = a numpy array or Pandas Dataseries
    #colors = a list or sequence, each element containing three floats in the range 0 to 1, \
    #which are the red, green and blue values of the sequence of colors, \
    #e.g. ((0, 0, 0), (1, 1, 1))
    min = array.min()
    max = array.max()
    
    t = np.linspace(min, max, 10)
    return plt.cm.coolwarm(t)
       
    
#    matplotlib.cm.ScalarMappable(norm=None, cmap=None)
    

#    return LinearSegmentedColormap.from_list('color range', colors, N=5, gamma=1.0)
#    
#useful links
#http://matplotlib.org/1.4.1/api/colors_api.html#matplotlib.colors.LinearSegmentedColormap.from_list
#http://matplotlib.org/api/cm_api.html

array = np.array([0, 2, 5, 2, 8, 10])
color_list = ((0, 0, 0), (1, 1, 1))

color(array, color_list)

#A plot that visualizes the average flow values using the 24 hour range
all_hours['average'] = all_hours[hour_list].mean(axis=1, skipna=False)

#A plot that visualizes the maximum flow values using the 24 hour ranges. 
all_hours['max'] = all_hours[hour_list].max(axis=1, skipna=False)

#A plot that visualizes the minimum flow values using the 24 hour ranges.
all_hours['min'] = all_hours[hour_list].min(axis=1, skipna=False)
'''
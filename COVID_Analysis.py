#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 16:53:12 2020

@author: bchoskins
"""

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
#%matplotlib inline

confirmed = pd.read_csv("~/Downloads/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/Confirmed_US.csv")

dead = pd.read_csv("~/Downloads/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/Dead_US.csv")

recovered = pd.read_csv("~/Downloads/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/Recovered_US.csv")


print('\n Data Types:')
print(confirmed.dtypes)

#Convert confirmed:
from datetime import datetime
con=confirmed['Date']
confirmed['Date']=pd.to_datetime(confirmed['Date'])
confirmed.set_index('Date', inplace=True)
#check datatype of index
confirmed.index

#convert to time series:
ts_confirmed = confirmed['Confirmed']
ts_confirmed.head(10) 

#Convert dead:
from datetime import datetime
d=dead['Date']
dead['Date']=pd.to_datetime(dead['Date'])
dead.set_index('Date', inplace=True)
#check datatype of index
dead.index

#convert to time series:
ts_dead = dead['Deceased']
ts_dead.head(10) 

#Convert recovered:
from datetime import datetime
rec=recovered['Date']
recovered['Date']=pd.to_datetime(recovered['Date'])
recovered.set_index('Date', inplace=True)
#check datatype of index
recovered.index

#convert to time series:
ts_recovered = recovered['Recovered']
ts_recovered.head(10) 


###################################Confirmed#####################################

#######PLOT FOR CONFIRMED#################
# Create figure and plot space
fig, ax = plt.subplots(figsize=(12, 12))

# Add x-axis and y-axis
ax.bar(ts_confirmed.index.values,
       ts_confirmed,
       color='blue')

# Set title and labels for axes
ax.set(xlabel="Date",
       ylabel="Confirmed COVID-19 Cases",
       title="Total Confirmed COVID-19 Cases in the US (Since 22-Jan-2020)")

plt.xticks(rotation = 90)

plt.show()

######Harvard Estimates (Say 10x current report)#########
ts_confirmed_Est = confirmed['Confirmed'].apply(lambda x: x*10)
# Create figure and plot space
fig, ax = plt.subplots(figsize=(12, 12))

# Add x-axis and y-axis
ax.bar(ts_confirmed_Est.index.values,
       ts_confirmed_Est,
       color='blue')

# Set title and labels for axes
ax.set(xlabel="Date",
       ylabel="Estmiated Confirmed COVID-19 Cases",
       title="Total Estimated Confirmed COVID-19 Cases in the US (Since 22-Jan-2020)")

plt.xticks(rotation = 90)

plt.show()

########Confirmed vs Estimated#########
fig = plt.figure(figsize = (9,9))

plt.plot(ts_confirmed, color="blue", label="Confirmed")
plt.plot(ts_confirmed_Est, color="red", label="Estimated")
    
plt.legend(bbox_to_anchor=(0.3,1.0), loc='upper_left', borderaxespad=0.)

fig.suptitle("Total Estimated vs Confirmed COVID-19 Cases in the US (Since 22-Jan-2020)", fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('COVID-19 Cases', fontsize=12)
#fig.autofmt_xdate()
plt.xticks(rotation=90)
plt.show()
fig.savefig('compare_conf.png')



##########Playing around with forecasting (confirmed and death)###########

############Additive Model####################

plt.plot(confirmed.index, confirmed['Confirmed'])
plt.title('Confirmed')
plt.ylabel('COVID-19 Cases')
plt.xlabel('Days')
plt.show()

plt.plot(dead.index, dead['Deceased'], 'r')
plt.title('Deaths')
plt.ylabel('COVID-19 Cases')
plt.xlabel('Days')
plt.show();

# Merge the two datasets and rename the columns
both = confirmed.merge(dead, how='inner', on='Date')

plt.figure(figsize=(10, 8))
plt.plot(both['Date'], both['Confirmed'], 'b-', label = 'Confirmed')
plt.plot(both['Date'], both['Deceased'], 'r-', label = 'Deceased')
plt.xlabel('Date'); plt.ylabel('COVID-19 Cases'); plt.title('Confirmed vs. Deceased COVID-19')
plt.xticks(rotation=90)
plt.legend();

import fbprophet
# Prophet requires columns ds (Date) and y (value)
conf = confirmed.rename(columns={'Date': 'ds', 'Confirmed': 'y'})

# Make the prophet model and fit on the data
#increase scale = greater model flexbility | decrease = lesser flexibility
conf_prophet = fbprophet.Prophet(changepoint_prior_scale=0.15)
conf_prophet.fit(conf)

# Make a future dataframe for 2 years
conf_forecast = conf_prophet.make_future_dataframe(periods=14, freq='D')
# Make predictions
conf_forecast = conf_prophet.predict(conf_forecast)

conf_prophet.plot(conf_forecast, xlabel = 'Date', ylabel = 'COVID-19 Cases')
plt.title('30-Day Esitmate of Confirmed COVID-19 Cases');
plt.savefig('30_Day_confirmed_est.png')

# Prophet requires columns ds (Date) and y (value)
d = dead.rename(columns={'Date': 'ds', 'Deceased': 'y'})

# Make the prophet model and fit on the data
#increase scale = greater model flexbility | decrease = lesser flexibility
d_prophet = fbprophet.Prophet(changepoint_prior_scale=0.15)
d_prophet.fit(d)

# Make a future dataframe for 2 years
d_forecast = d_prophet.make_future_dataframe(periods=30, freq='D')
# Make predictions
d_forecast = d_prophet.predict(d_forecast)

d_prophet.plot(d_forecast, xlabel = 'Date', ylabel = 'COVID-19 Cases')
plt.title('30-Day Esitmate of Deceased COVID-19 Cases');
plt.savefig('30_Day_death_est.png')

############Logistic Regression####################



##############################DECEASED#########################################

#######PLOT FOR DECEASED#################
# Create figure and plot space
fig, ax = plt.subplots(figsize=(12, 12))

# Add x-axis and y-axis
ax.bar(ts_dead.index.values,
       ts_dead,
       color='red')

# Set title and labels for axes
ax.set(xlabel="Date",
       ylabel="Deceased COVID-19 Cases",
       title="Total Deceased COVID-19 Cases in the US (Since 22-Jan-2020)")

plt.xticks(rotation = 90)

plt.show()



##############################DECEASED#########################################

#######PLOT FOR Recovered#################
# Create figure and plot space
fig, ax = plt.subplots(figsize=(12, 12))

# Add x-axis and y-axis
ax.bar(ts_recovered.index.values,
       ts_recovered,
       color='green')

# Set title and labels for axes
ax.set(xlabel="Date",
       ylabel="Recovered COVID-19 Cases",
       title="Total Recovered COVID-19 Cases in the US (Since 22-Jan-2020)")

plt.xticks(rotation = 90)

plt.show()


##############################COMBINED#########################################

#Plot all three together:
fig = plt.figure(figsize = (12,12))

import itertools

colors = itertools.cycle(["b", "r", "g"])

for frame in [ts_confirmed, ts_dead, ts_recovered]:
    plt.plot(frame, color=next(colors))
    
plt.xticks(rotation=90)

plt.show()







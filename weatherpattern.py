import pandas as pd
import numpy as np 
import matplotlib as mpl
import matplotlib.pyplot as plt
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/acf46bb2b793e5e615670cf275d675245936b79f164b80c628bd7748.csv')
df['Data_Value'] = df['Data_Value'] * 0.1
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Day'] = df['Date'].dt.day
df['Month'] = df['Date'].dt.month

df_2015 = df.copy()
df_2015 = df_2015[df_2015['Year'] == 2015]
dfmax_2015 = df_2015.groupby(['Month','Day'])['Data_Value'].agg({'Data_Value':np.max})
dfmin_2015 = df_2015.groupby(['Month','Day'])['Data_Value'].agg({'Data_Value':np.min}) 

df = df[(df['Year'] < 2015) & (df['Year'] >= 2005)]
df = df[(df['Day'] != 29) | (df['Month'] != 2)]

dfmax = df[df['Element'] == 'TMAX']
dfmin = df[df['Element'] == 'TMIN']
dfmax = dfmax.groupby(['Month','Day'])['Data_Value'].agg({'Data_Value':np.max})
dfmin = dfmin.groupby(['Month','Day'])['Data_Value'].agg({'Data_Value':np.min})
dfmin1 = dfmin.copy()
dfmax1 = dfmax.copy()
dfmin = dfmin.reset_index()
dfmin = dfmin.drop(['Month','Day'],axis=1)
dfmax = dfmax.reset_index()
dfmax = dfmax.drop(['Month','Day'],axis=1)
dfmax['Days'] = np.arange(len(dfmax))
dfmax['Days'] = dfmax['Days'] + 1
dfmin['Days'] = dfmax['Days']
dfmin = dfmin.set_index('Days')
dfmax = dfmax.set_index('Days')

plt.figure(figsize=(16,10))
plt.title('Ten Year Record (2005-2014) Was Broken in 2015')
plt.xlabel('365 days')
plt.ylabel('Temprature')
X = dfmin.iloc[:,0]
Y = dfmax.iloc[:,0]
plt.plot(X,c='blue',label='Record Low')
plt.plot(Y,c='red',label='Record High')
plt.fill_between(np.arange(len(X)),X,Y,facecolor='#2F99B4',alpha=0.35)
all_max = pd.merge(dfmax1.reset_index(), dfmax_2015.reset_index(), left_index=True, on = ['Month','Day'])
all_min = pd.merge(dfmin1.reset_index(), dfmin_2015.reset_index(), left_index=True, on = ['Month','Day'])
break_max = all_max[all_max['Data_Value_y'] > all_max['Data_Value_x']]
break_min = all_min[all_min['Data_Value_y'] < all_min['Data_Value_x']]
break_max = break_max[break_max['Month'] < 9]
plt.scatter(break_max.index.tolist(), break_max['Data_Value_y'].values, c = 'black', label = "Broken High in 2015")
plt.scatter(break_min.index.tolist(), break_min['Data_Value_y'].values, c = 'green', label = "Broken Low in 2015")

x = np.arange(0, 365)
labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ticks = np.arange(min(x), max(x)+len(x)/12, len(x)/12)
minor_ticks = ticks + (len(x)/12)/2
minor_ticks = minor_ticks[:len(minor_ticks)-1]
ax = plt.gca()
ax.set_xticks(ticks)
ax.set_xticklabels('')
ax.set_xticks(minor_ticks, minor = True)
ax.set_xticklabels(labels, minor = True)
ax.tick_params(axis='x', which = 'minor', length= 0)
plt.legend(loc = 4, fontsize=12, frameon = False)
plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='on', labelbottom='on')
plt.show()

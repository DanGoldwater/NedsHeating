#%%

import csv
import codecs
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily
from numpy import number

Nottinghamlocation = Point(52.97255, -1.16344,)



# Plot line chart including average, minimum and maximum temperature
# data.plot(y=['tavg', 'tmin', 'tmax'])
# plt.show()
# data['tavg']

def get_year_data(year):
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    data = Daily(Nottinghamlocation, start, end)
    data = data.fetch()
    return data

def plot_year(year):
    data  = get_year_data(year)
    # Plot line chart including average, minimum and maximum temperature
    data.plot(y=['tavg', 'tmin', 'tmax'])
    plt.show()
    
def get_year_avg_list(year):
    data = get_year_data(year)
    avg_list = data['tavg'].tolist()
    avg_list = [a for a in avg_list if str(a) != 'nan']
    return avg_list

# avg_list_2018 = get_year_avg_list(2018)


    
    
    



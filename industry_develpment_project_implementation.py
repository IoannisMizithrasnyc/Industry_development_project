#industry develpment project implementation
#Ioannis Mizithras


#import libraries

import sys
import csv
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter
import numpy as np
from itertools import cycle
import pandas as pd
import statistics

########################


#functions

def parameters():
    param_list = []
    print("\nInsert country code OR type \""+ print_graph_message.lower() +"\" to print plots OR type \""+ exit_message.lower() +"\" to exit the software")
    code = input().upper()
    
    param_list.append(code)
    if (code == exit_message or code == print_graph_message):
        return param_list
    while True:
        s_date = input("Start date (YYYY-MM-DD)")
        if (len(s_date)==10):
            param_list.append(s_date)
            break
        else:
            print(date_format_error)
    while True:
        e_date = input("End date (YYYY-MM-DD)")
        if (len(e_date)==10):
            param_list.append(e_date)
            break
    num = int(input("Enter 0-6 \n 0: All Parameters \n 1: Retail \n 2: Grocery \n 3: Parks \n 4: Transit \n 5: Workplaces \n 6: Residential\n"))
    if (num <1 or num > 6):
        num = 0
    param_list.append(num-7)
    return param_list

def plot_data(datalist):
    if(datalist):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for country in datalist:
            temp = []
            dates = [] 
            for entry in country:
                dates.append(entry[1])
                if (entry[2]==0):   
                    for i in range (6):
                        temp.append(int(entry[3+i]))
                    
                else:
                    temp.append(int(entry[3]))
            arr = np.array(temp)
            x = pd.date_range(start=dates[0], end=dates[-1])
            if (entry[2]==0):
                arr = np.array_split(arr,arr.shape[0]/6)
                arr = np.transpose(arr)
                for i in range (arr.shape[0]):
                    ax.plot_date(x,arr[i,:], '-', label=entry[0] + " " + datapoints[i], color=next(colors))
            else:
                arr=arr.reshape(1,arr.shape[0])
                ax.plot_date(x, arr[0,:],'-',label=entry[0] + " " + datapoints[int(entry[2])-1], color=next(colors))
        ax.grid(axis='y')
        ax.legend(loc="center",bbox_to_anchor=(0.5,-0.06),ncol=arr.shape[0])
        plt.show()
    else:
            print(no_data_to_print_message)
    return

########################


#main body

colors = cycle(["blue", "red", "grey", "yellow", "green", "aqua", "lime", "maroon", "navy", "olive", "purple", "silver", "teal","black"])
datapoints = ["retail","grocery","parks","transit","workplaces","residential"]
exit_message = "EXIT"
print_graph_message = "PRINT"
invalid_input_message = "!!! invalid input !!!\n"
date_format_error = "!!! wrong date format !!!"
no_data_to_print_message = "There is no data selected to be printed\n"
greetings_message = "Welcome to the Google community mobility reports data visualization and processing system"
farewell_message = "\nMay you find peace in your endeavors" 

file = open("Global_Mobility_Report.csv", encoding = "utf8")
csvreader = csv.reader(file)
print(greetings_message)
while True:
    datalist = [] 
    while True:
        param_list=parameters()
        code = param_list[0]
        if code == exit_message or code == print_graph_message:
            break   
        found = False
        file.seek(0)
        next(csvreader)
        current_data = []
        for row in csvreader:
            if (row[0]==code):
                found = True
                if (row[8]>=param_list[1] and row[8] <= param_list[2]):
                    if (param_list[3]==-7):
                        current_data.append([row[0], row[8], param_list[3]+7, row[-6], row[-5], row[-4], row[-3], row[-2], row[-1]])
                    else:
                        current_data.append([row[0], row[8], param_list[3]+7, row[param_list[3]]])
                elif(row[8]>param_list[2]):
                    break
            elif (row[0]>code):
                if (found): break
                else: 
                    print(invalid_input_message)
                    break
                
        if (current_data):
            if (param_list[3]==-7):
                for i in range (6):
                    temp=[]
                    for entry in current_data:
                        temp.append(int(entry[i+3]))
                    print(datapoints[i] + ":\n Mean: ", "{:.4f}".format(statistics.mean(temp)), ", Median: ", statistics.median(temp), ", Mode: ", statistics.mode(temp), "\n")
            else:
                temp = []
                for entry in current_data:
                    temp.append(int(entry[3]))
                print(datapoints[int(entry[2])-1] + ":\n Mean: ", "{:.4f}".format(statistics.mean(temp)), ", Median: ", statistics.median(temp), ", Mode: ", statistics.mode(temp), "\n")

            datalist.append(current_data)
            
    if code == print_graph_message:
        plot_data(datalist)
    elif code == exit_message:
        break
        
user_input = input(farewell_message)
file.close()
sys.exit()

########################


"""
NOTES:



"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 20:20:17 2020

@author: Alex Thumwood

Purpose: collection of functions for reading in NasaTLX data
"""
import json
import numpy as np
import matplotlib.pyplot as plt
import math

##Reads in the json file. In case the name didn't give that away##

def file_reader(file_name):
    with open(file_name) as f:
        array = json.load(f)
        print("File Read")
        return array
    
###############################################

## Function for isolating the results to a particular condition/experiment ##
def condition_iso(expID, results_array): 
    cond_array = []

    for x in results_array:
        if x['experimentID'] == expID:
                 cond_array.append(x)
    if cond_array != []:
        return cond_array
    else:
        return "That condition could not be found"

#############################################################  

##Function for isolating the results for a particular participant ##             
             
def participant_iso(partID, results_array): 
    part_array = []

    for x in results_array:
        if x['participantID'] == partID:
                 part_array.append(x)
                     
    if part_array != []:
        return part_array
    else:
        return "That participant ID could not be found"

#############################################################  

## Function for isolating a particular gender ##        
    
def gender_iso(gender, results_array): 
    gender_array = []

    for x in results_array:
         if x['gender'] == gender:
                 gender_array.append(x) 
                     
    if gender_array != []:
        return gender_array
    else:
        return "Either you've forgotten to capitalise, or you really need to diversify your pool of participants"

#############################################################  

## Function for isolating a particular age bracket ##                 
def age_iso(age, results_array):
    age_array = []
    for x in results_array:
        if x['age'] == age:
                 age_array.append(x)               
    if age_array != []:
        return age_array
    else:
        return "That age bracket could not be found"
    
#############################################################  

##fucntion for calculting the mean taskload of experiments in an array##
def mean_cal(results_array, val):
    mean_array = []
    for x in results_array:
        #print(x['participantID'], ": ", x[val])
        mean_array.append(x[val])
        
    return np.mean(mean_array)

#############################################################

def cond_bar_chart(y_array, labels, to_comp, ylabel, title):
    num_bars = len(labels)
    to_plot = []
    sdiv = []
    for x in range(0, num_bars):
        #print(labels[x])
        current = condition_iso(labels[x], y_array)
        all_results = all_res(current, to_comp)
        mean = mean_cal(current, to_comp)
        standard_div = np.std(all_results, dtype=np.float64)
        to_plot.append(mean)
        sdiv.append(standard_div)
    
    #print(to_plot)
    #print(sdiv)
    y_pos = np.arange(len(labels))
    plt.bar(y_pos, to_plot, align='center', alpha=0.5, yerr=sdiv, capsize=5)
    plt.xticks(y_pos, labels)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.show()
    
################################################################

def ww_bar_chart(y_array, labels, to_comp, ylabel, title):
    num_bars = len(labels)
    to_plot = []
    sdiv = []
    
    for x in range(0, num_bars):
        all_results = []
        current = condition_iso(labels[x], y_array)
        print("")
        print(labels[x])
        for y in current:
            ww = y['weightedWorkload']
            all_results.append(ww[to_comp])
            print (ww['Effort'])
        mean = np.mean(all_results)
        standard_div = np.std(all_results, dtype=np.float64)
        to_plot.append(mean)
        sdiv.append(standard_div)
    
    #print(to_plot)
    #print(sdiv)
    y_pos = np.arange(len(labels))
    plt.bar(y_pos, to_plot, align='center', alpha=0.5, yerr=sdiv)
    plt.xticks(y_pos, labels)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.show()
    
################################################################

def two_split_bar(groups, list_1, list_2, label_1, label_2, y_array, to_comp):
    n_groups = len(groups)
    
    mean_1 = []
    mean_2 = []
    sdiv_1 = []
    sdiv_2 = []
    
    for x in range(0, (len(list_1))):
        all_results = []
        current = condition_iso(list_1[x], y_array)
        all_results = all_res(current, to_comp)
        mean = mean_cal(current, to_comp)
        standard_div = np.std(all_results, dtype=np.float64)
        mean_1.append(mean)
        sdiv_1.append(standard_div)
        
    for x in range(0, (len(list_2))):
        all_results = []
        current = condition_iso(list_2[x], y_array)
        all_results = all_res(current, to_comp)
        mean = mean_cal(current, to_comp)
        standard_div = np.std(all_results, dtype=np.float64)
        mean_2.append(mean)
        sdiv_2.append(standard_div)
    
    
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
    
    rects1 = plt.bar(index, mean_1, bar_width,
    alpha=opacity,
    color='b',
    label= label_1, yerr=sdiv_1, capsize=5)
    
    rects2 = plt.bar(index + bar_width, mean_2, bar_width,
    alpha=opacity,
    color='g',
    label= label_2, yerr=sdiv_2, capsize=5)
    
    plt.xlabel('Condition')
    plt.ylabel('Taskload')
    plt.title('Mean taskload per condition')
    plt.xticks(index + bar_width, groups)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    
    plt.tight_layout()
    plt.show()
    
################################################################

def two_split_bar_dd(groups, list_1, list_2, label_1, label_2, y_array, to_comp):
    n_groups = len(groups)
    
    mean_1 = []
    mean_2 = []
    sdiv_1 = []
    sdiv_2 = []
    
    for x in range(0, (len(list_1))):
        all_results = []
        current = condition_iso(list_1[x], y_array)
        for y in current:
            s = y['scale']
            all_results.append(s[to_comp])
            #print (ww['Effort'])
        mean = np.mean(all_results)
        standard_div = np.std(all_results, dtype=np.float64)
        standard_err = standard_div/math.sqrt(18)
        mean_1.append(mean)
        sdiv_1.append(standard_err)
        #print(mean, '1')
        #print(standard_div, '1')
        
    for x in range(0, (len(list_2))):
        all_results = []
        current = condition_iso(list_2[x], y_array)
        for y in current:
            s = y['scale']
            all_results.append(s[to_comp])
            #print (s[to_comp])
        mean = np.mean(all_results)
        #print(mean, '2')
        standard_div = np.std(all_results, dtype=np.float64)
        standard_err = standard_div/math.sqrt(18)
        #print(standard_div, '2')
        mean_2.append(mean)
        sdiv_2.append(standard_err)
    
    
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
    
    rects1 = plt.bar(index, mean_1, bar_width,
    alpha=opacity,
    color='b',
    label= label_1, yerr=sdiv_1, capsize=5)
    
    rects2 = plt.bar(index + bar_width, mean_2, bar_width,
    alpha=opacity,
    color='g',
    label= label_2, yerr=sdiv_2, capsize=5)
    
    plt.xlabel('Condition')
    plt.ylabel(to_comp)
    title = "Mean " + to_comp + " per condition"
    print(title)
    plt.title(title)
    plt.xticks(index + bar_width, groups)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    
    plt.tight_layout()
    plt.show()
    
################################################################

def ww_print(y_array, labels, to_comp):
    num = len(labels)
    
    for x in range(0, num):
        all_results = []
        current = condition_iso(labels[x], y_array)
        print("")
        print(labels[x])
        for y in current:
            ww = y['weightedWorkload']
            all_results.append(ww[to_comp])
            print (ww[to_comp])
        mean = np.mean(all_results)
        print("")
        print(mean)
        print("")
    
###############
################################################################

def s_print(y_array, labels, to_comp):
    num = len(labels)
    
    for x in range(0, num):
        all_results = []
        current = condition_iso(labels[x], y_array)
        print("")
        print(labels[x])
        for y in current:
            ww = y['scale']
            all_results.append(ww[to_comp])
            print (ww[to_comp])
        mean = np.mean(all_results)
        print("")
        print(mean)
        print("")
    
###############

def all_res(array, to_extract):
    res = []
    for x in array:
        print(x)
        res.append(x[to_extract])
    return res
    

#Calculations for the line plot #

def extract_sort(val, results_array):
    vals_array = []
    for x in results_array:
        vals_array.append(x[val])
    vals_sorted = np.sort(vals_array)
    return vals_sorted


    
##########################

def quick_print(partID, to_print, results_array):
    array = participant_iso(partID, results_array)
    
################################

    
## Function for testing the functions ##
## AKA: 'Throw sh*t at the wall and see what sticks' ##
def tester():
    
    all_results = file_reader("nasa final.json")
    labels = ["SC1", "SC2", "SC3", "SC4", "LC1", "LC2", "LC3", "LC4"]
    

    #SC1_mean = mean_taskload(condition_iso("SC1", all_results), 'taskload')
    #SC2_mean = mean_taskload(condition_iso("SC2", all_results), 'taskload')
    #print("The mean taskload across all particpiants for SC1 was: ", SC1_mean)
    #print("The mean taskload across all particpiants for SC2 was: ", SC2_mean)
    #to_plot = [SC1_mean, SC2_mean]
    #bar_chart(to_plot, ("SC1", "SC2"))
    
    cond_bar_chart(all_results, labels, 'taskload')
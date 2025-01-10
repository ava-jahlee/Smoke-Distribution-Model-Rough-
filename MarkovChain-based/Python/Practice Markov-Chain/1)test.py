import numpy as np
import random as rm

# the statespace
states = ["Sleep", "Icecream","Run"]

#possible sequences of events
transitionName = [["SS","SR","SI"], ["RS","RR","RI"],["IS","IR","II"]]

#Probabilities matrix(transition matrix)
transitionMatrix = [[0.2, 0.6, 0.2],[0.1, 0.6, 0.3],[0.2, 0.7, 0.1]]

if sum(transitionMatrix[0]) + sum(transitionMatrix[1]) + sum(transitionMatrix[1]) != 3:
    print("error")

# A function that implements the Markov model to forecast the state/mood.
def activity_forecast(days):
    #Choose the starting state
    activityToday = "Sleep"
    print("Start state: "+activityToday)
    #Shall store the sequence of states taken. So this only has the starting state for now.
    activityList = [activityToday]
    i = 0
    # To calculate the probabitlity of the activityList
    prob = 1
    while i != days:
        if activityToday == "Sleep":
            change = np.random.choice(transitionName[0], replace=True,p=transitionMatrix[0])
            if change == "SS":
                prob = prob * 0.2
                activityList.append("Sleep")
                pass
            elif change == "SR":
                prob = prob * 0.6
                activityToday = "Run"
                activityList.append("Run")
            else:
                prob = prob * 0.2
                activityToday = "Icecream"
                activityList.append("Icecream")

        elif activityToday == "Run":
            change = np.random.choice(transitionName[1], replace=True, p=transitionMatrix[1])
            if change == "RR":
                prob = prob * 0.5
                activityList.append("Run")
                pass
            elif change == "RS":
                prob = prob * 0.2
                activityToday = "Sleep"
                activityList.append("Sleep")
            else:
                prob = prob * 0.3
                activityToday = "Icecream"
                activityList.append("Icecream")

        elif activityToday == "Icecream":
            change = np.random.choice(transitionName[2],replace=True,p=transitionMatrix[2])
            if change == "II":
                prob = prob * 0.1
                activityList.append("Icecream")
                pass
            elif change == "IS":
                prob = prob * 0.2
                activityToday = "Sleep"
                activityList.append("Sleep")
            else:
                prob = prob * 0.7
                activityToday = "Run"
                activityList.append("Run")

        i+=1
    return activityList
    """
    print("Possible states: " + str(activityList))
    print("End state after " + str(days) + " days: " + activityToday)
    print("Probability of the possible sequence of states: " + str(prob))
    """

"""
#Function that forecasts the possible state for the next 2 days
activity_forecast(2)
"""

# 모든 activity 저장
list_activity = []
count = 0

#range starts from the first count up until but excluding the last count:
for iterations in range(1,10000):
    list_activity.append(activity_forecast(2))

# Check out all the `activityList` we collected
print(list_activity)

# Iterate through the list to get a count of all activities ending in state:'Run'
for smaller_list in list_activity:
    if(smaller_list[2] == "Run"):
        count += 1

# Calculate the probability of starting from state:'Sleep' and ending at state:'Run'
percentage = (count/10000) * 100
print("The probability of starting at state:'Sleep' and ending at state:'Run'= " + str(percentage) + "%")
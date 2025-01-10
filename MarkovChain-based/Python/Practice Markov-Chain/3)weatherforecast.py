import function as f
import numpy as np

statesList = ['rainy', 'sunny']
nameList = f.matrix_generator(statesList)
probabilityList = [0.7, 0.3, 0.4, 0.6]

matrixNameList = np.array(nameList).reshape(2,2)
matrixProbabilityList = np.array(probabilityList).reshape(2,2)
probabilityDictionary = dict(zip(nameList,probabilityList))

f.check_this_matrix(matrixProbabilityList)

def weather_forecast(first_weather,days):
    weatherList = [first_weather]
    i, prob = 0, 1
    present_activity = first_weather
    #move_path = []

    while i != days:
        statesIndex = statesList.index(present_activity)

        choice = np.random.choice(matrixNameList[statesIndex], replace=True, p=matrixProbabilityList[statesIndex])
        prob = prob * probabilityDictionary[choice]
        statesIndexColumn = list(matrixNameList[statesIndex]).index(choice)
        present_activity = statesList[statesIndexColumn]
        #move_path.append(choice)
        weatherList.append(present_activity)
        i += 1

    return weatherList

# 상태 rainy로 시작해서 다섯번 상태가 전이되는, iteration을 만번 반복하고 iteration_list에 저장한다.
iteration_list = f.iteration_transitionMatrix(weather_forecast, firstState = 'rainy' ,numberth = 3, iterations = 10000)

# 상태 sunny로 끝난 경우를 세고, 그 확률을 계산한다.
probability = f.probability_of_endState(iteration_list, endState = 'sunny', numberth = 3, iterations = 10000)

# 결과를 출력한다.
print(len(iteration_list), "iterations list:", iteration_list)
print("The probability:", str(probability) + "%")
print(f.solution(matrixProbabilityList, 2))
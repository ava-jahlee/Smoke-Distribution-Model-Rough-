import numpy as np
import function as f

statesList = f.get_states_list(4)
nameList = f.matrix_generator(statesList)
probabilityList = [0,0.2,0.3,0.5,0.2,0.6,0.1,0.1,0.1,0.5,0.1,0.3,0.1,0.8,0.05,0.05]

matrixNameList = np.array(nameList).reshape(4,4)
matrixProbabilityList = np.array(probabilityList).reshape(4,4)
probabilityDictionary = dict(zip(nameList,probabilityList))

f.check_this_matrix(matrixProbabilityList)

def sugar_prediction(first_activity,numberth):
    activityList = [first_activity]
    i, prob = 0, 1
    present_activity = first_activity
    #move_path = []

    while i != numberth:
        statesIndex = statesList.index(present_activity)

        choice = np.random.choice(matrixNameList[statesIndex], replace=True, p=matrixProbabilityList[statesIndex])
        prob = prob * probabilityDictionary[choice]
        statesIndexColumn = list(matrixNameList[statesIndex]).index(choice)
        present_activity = statesList[statesIndexColumn]
        #move_path.append(choice)
        activityList.append(present_activity)
        i += 1

    return activityList

# 상태 sleep으로 시작해서 두번 상태가 전이되는, iteration을 만번 반복하고 iteration_list에 저장한다.
iteration_list = f.iteration_transitionMatrix(sugar_prediction, 'walk', numberth=10, iterations=10000)
# 상태 eat으로 끝난 경우를 센다.# 상태 eat으로 끝난 확률을 계산한다.
probability = f.probability_of_endState(iteration_list, 'walk', numberth=10, iterations=10000)

# 결과를 출력한다.
print("Iteration list:", iteration_list)
print("The probability:", str(probability) + "%")
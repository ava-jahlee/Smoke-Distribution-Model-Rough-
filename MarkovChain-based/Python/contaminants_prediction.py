import function as f
import numpy as np
import pprint

# ref: markov-chain-based probabilistic approach
# to optimize sensor network against deliberately released pollutants
# in buildings with ventilation systems.


statesList = f.get_states_list(13)
nameList = f.matrix_generator(statesList)

matrixNameList = np.array(nameList).reshape(13, 13)
print("Matrix Namelist:", matrixNameList)
matrixProbabilityList = f.get_matrix_xlsx(12, 12)[1]          #excel에 나열된 데이터 추출하여 행렬 형태로 나타내기

probabilityList = matrixProbabilityList.reshape(1, 13*13)[0]
probabilityDictionary = dict(zip(nameList,probabilityList))

f.check_this_matrix(matrixProbabilityList)

def contaminantPosition_prediction(first_position,numberth):
    positionList = [first_position]
    i, prob = 0, 1
    present_position = first_position
    #move_path = []

    while i != numberth:
        statesIndex = statesList.index(present_position)

        choice = np.random.choice(matrixNameList[statesIndex], replace = True, p = matrixProbabilityList[statesIndex])
        prob = prob * probabilityDictionary[choice]
        statesIndexColumn = list(matrixNameList[statesIndex]).index(choice)

        present_position = statesList[statesIndexColumn]
        positionList.append(present_position)
        i += 1

    return positionList

iteration_list = f.iteration_transitionMatrix(contaminantPosition_prediction, firstState='Zone11',numberth=60, iterations =10000)
#probability = f.probability_of_endState(iteration_list, endState='Node8',numberth=60, iterations=10000)
probabilities_result = f.probability_States_everystep(iteration_list, statesList, numberth=60, iterations=10000)

#print(len(iteration_list), "iterations list:", iteration_list)
print("The probabilities:\n", str(probabilities_result) + "%")

f.export_matrix_csv(probabilities_result)




import numpy as np
import os
import pandas as pd
import openpyxl
import xlrd
from tkinter import filedialog
from tkinter import messagebox

def get_states_list(states_num):
    """states_num 인자에 상태의 갯수를 입력하고, 갯수만큼 상태들을 입력하여 states_list를 반환한다."""
    states_list = []
    text = "Enter the states."
    print(text)
    for i in range(states_num):
        text = str(input())
        states_list.append(text)
    return states_list
def matrix_generator(statesList):
    name_list = []
    for i in range(len(statesList)):
        for j in range(len(statesList)):
            name_list.append(str(i) + str(j))
    return name_list

def check_this_matrix(matrixProbabilityList):
    for i in matrixProbabilityList:
        sum_in_row = 0
        for j in range(len(i)):
            sum_in_row += i[j]
        print("row", i, "is ok") if round(sum_in_row, 2) == 1 else print("Error")

def iteration_transitionMatrix(matrixName,firstState,numberth,iterations):
    iteration_list = []
    for iteration in range(iterations):
        iteration_list.append(matrixName(firstState,numberth))

    return iteration_list
def probability_of_endState(iteration_list,endState,numberth,iterations):
    count = 0
    for smaller_list in iteration_list:
        if(smaller_list[numberth] == endState):
            count += 1
    percentage = (count / iterations) * 100
    return percentage

def probability_States_everystep(iteration_list, statesList, numberth, iterations):
    probabilities = []
    for num in range(numberth):
        count = [0] * len(statesList)
        for state in range(len(statesList)):
            for iteration in range(iterations):
                if iteration_list[iteration][num] == statesList[state]:
                    count[state] += 1
        k = [i * 100 / iterations for i in count]
        probabilities.append(k)

    return np.array(probabilities).reshape(numberth,len(statesList))

def solution(matrixName, power):
    original, result = matrixName, matrixName
    i = 1
    while i != power:
        result = np.dot(matrixName, original).tolist()
        i+=1
    return result

def get_matrix_xlsx(Row, Column):
    file_num, xml_file, file_gbxml, save_path = 0, '', '', ''
    while file_num < 1:
        xlsx_file = filedialog.askopenfilenames(initialdir="/", title="데이터를 읽어올 xlsx 파일을 선택하세요.", filetypes=(
        ("xlsx files", "*.xlsx"), ("csv files", "*.csv"), ("all files", "*.*")))
        if xlsx_file == '':
            messagebox.showwarning("경고!", "파일을 추가 하세요.")
            pass
        else:
            Location = os.path.split(xlsx_file[0])[0]
            File = os.path.split(xlsx_file[0])[1]
            data_pd = pd.read_excel('{}/{}'.format(Location, File), sheet_name = 0,
                                    header = None, names = None, index_col = None)
            data_np = pd.DataFrame.to_numpy(data_pd)
            file_num += 1

            return data_pd, \
                   data_np, data_np[Row][Column]

def export_matrix_csv(matrixName):
    file_num, save_location, save_fileName = 0, '', ''
    while file_num < 1:
        save_location = filedialog.askdirectory(initialdir="/", title="결과를 저장할 경로를 선택하세요.")
        if save_location == '':
            messagebox.showwarning("경고!", "경로를 선택하세요.")
        else:
            print("추출결과를 저장할 파일 이름을 입력하세요.")
            save_fileName = input()
        file_num += 1
    transformToDataFrame = pd.DataFrame(matrixName)
    transformToDataFrame.to_excel(save_location + '/' + str(save_fileName) + '.xlsx', index=False, index_label=False)
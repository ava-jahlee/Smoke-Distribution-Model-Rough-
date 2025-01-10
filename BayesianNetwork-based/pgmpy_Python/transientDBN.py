from ast import literal_eval
from copy import copy

from pgmpy.base import *
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models.DynamicBayesianNetwork import DynamicBayesianNetwork as DBN
from pgmpy.models.DynamicBayesianNetwork import DynamicNode
import pgmpy.inference
from pgmpy.base import DAG

import math
import pprint
import pandas as pd

import numpy as np

import os
from openpyxl import load_workbook

import graphDBN1 as gDBN

print("Time slice?")
timeslice = int(input())

np.set_printoptions(threshold=np.Inf, linewidth=np.Inf)

gNodes = gDBN.G.nodes
gEdges = gDBN.G.edges
testDBN = gDBN.DBN

#그래프로부터 edge 목록 읽어오기
edgeList = []
for ed in gEdges:
    changeToList = list(ed)
    edgeList.append(changeToList)

edgeTsZero, edgeTsOne = [], []
for ed01 in edgeList:
    edgeTsZero.append([(ed01[0], 0), (ed01[1], 0)])
    edgeTsOne.append([(ed01[0], 1), (ed01[1], 1)])

#TIMESLICE간 자신노드 추가
nodeList = []
tsZeroToOne = []
for no in gNodes:
    nodeList.append((no,0))
    nodeList.append((no,1))
    timeSliceSelf = [(no, 0), (no, 1)]
    tsZeroToOne.append(timeSliceSelf)

# 필요한 conditional probability distribution 목록을 나열
totalEdge = edgeTsZero + edgeTsOne + tsZeroToOne
evidenceList, variableList = [], []
for nodes in nodeList:
    for edges in totalEdge:
        if edges[1] == nodes:
            variableList.append(edges[1])
            evidenceList.append(edges[0])
        else:
            pass

variableSet = []
for x in variableList:
    if x not in variableSet:
        variableSet.append(x)

#variableSet = list(set(variableList)) ##variableList 중복제거한 List
print(variableSet)
lastVariableList, lastEvidenceList, tabCPDList = [], [], []

print('You need *CPD(s)* for:')
for vS in variableSet:
    lastVariableList.append(vS)
    indexList = list(filter(lambda x: variableList[x] == vS, range(len(variableList))))
    specifiedVAREVIs = []
    for index in indexList:
        specifiedVAREVIs.append(evidenceList[index])
    lastEvidenceList.append(specifiedVAREVIs)
    print('P(', vS, '|', specifiedVAREVIs, ')')

print('Root probability of ', gDBN.G.get_roots(), ' :')
rootcpdInput = list(map(float, input().split()))
root_cpd = TabularCPD((gDBN.G.get_roots()[0], 0), 2, [[rootcpdInput[0]], [1-rootcpdInput[0]]])
testDBN.add_cpds(root_cpd)
print(root_cpd, '\n')

filename = 'dasan1F.xlsx'
load_wb = load_workbook(os.path.join(os.getcwd(), filename))

# 여기에 inference 결과들을 저장할 빈 list를 만들어주기
## inferenceResult = []
i = 0
list_cpd = []
while i < timeslice:

    load_ws = load_wb[str(i)]
    sheet_rows = load_ws.rows

    for num, row in enumerate(sheet_rows):
        globals()['row{}'.format(num)] = []
        for cell in row:
            globals()['row{}'.format(num)].append(cell.value)

        globals()['row{}'.format(num)] = [cell for cell in globals()['row{}'.format(num)] if cell is not None]

        print('! Please enter the proper *CPDs* for:')
        print('P(', lastVariableList[num], '|', lastEvidenceList[num], ')')

        cpdInput_rest = []
        for cpd in globals()['row{}'.format(num)]:
            if cpd == 1:
                cpdInput_rest.append(0)
            elif cpd == 0:
                cpdInput_rest.append(1)
            else:
                rest = len(str(cpd).split('.')[1])
                cpdInput_rest.append(round(1 - cpd, rest))

        print(globals()['row{}'.format(num)])
        print(cpdInput_rest)

        nums = []
        for n in range(len(lastEvidenceList[num])):
            nums.append(2)

        cpd = TabularCPD(lastVariableList[num],
                         2,
                         [globals()['row{}'.format(num)], cpdInput_rest],
                         evidence = lastEvidenceList[num],
                         evidence_card = nums)

        testDBN.add_cpds(cpd)
        list_cpd.append(cpd)
        print(cpd)

    # 이 indent에서 i번째에서 i+1번째로 넘어갈 때의 **각 노드에서의** 확률을 계산하는 코드를 작성해주어야 한다...



    ## 여기에 inference로 나온 결과에 대해, 해당 시행의 동적변수를 이름으로 빈 리스트를 작성한다.
    ### inferenceResults.append(동적변수)




    # 작성한 이후, i+1번째로 넘어가는 코드로 구성을 하고, 이를 반복시행하도록 한다.


    i += 1


# Check the model
testDBN.initialize_initial_state()   ##이걸 안하면 value error 뜸.. 'No CPD associated with aim0030_0'
testDBN.check_model()

#make inference
evidence_map = {0: 'MOVE', 1: 'STAY'}
variable_map = {0: 'TO THIS NODE', 1: 'TO OTHER NODES'}
dbnInference = pgmpy.inference.DBNInference(testDBN)

print('----------------------------------------------')

network_nodes = []
for node in testDBN.nodes:
    ni = (str(node).split('('))[1].split(')')[0]
    ni2 = str('\'') + str(ni[0:7]) + str('\'') + str(',') + str(ni[8:10])
    modnode = ni2.replace(' ', '')
    network_nodes.append(modnode)

for node in network_nodes:
    test_selves =  str('(') + str(node) + str(')')
    node.replace('(', '').replace(')', '')
    test_parents = testDBN.get_parents(node = (node[1:8], int(node[10])))
    test_list, self_query_list, parent_query_list = [], [], []
    # make self query input
    self_query_list.append([str(test_selves) + str(':') + str((0)), str(test_selves) + str(':') + str((1))])

    print('|------------------------------------------------------------------------------------------------|')
    for parent in range(len(test_parents)):
        test = str('(') + (str(test_parents[parent]).split('('))[1].split(')')[0] + str(')')
        test_list.append(test)
        print('| node: ', test_selves, ' / parents: ', test_list)
    for parent in test_parents:
        # make parent query input
        parent_query_list.append([str(parent) + str(':') + str((0)), str(parent) + str(':') + str((1))])
    print('| self query: ', self_query_list)
    print('| parent query: ', parent_query_list)
    print('|------------------------------------------------------------------------------------------------|')

    # query로 0이랑 1일 때 반복해서 추론

cpd_dictionary = {}
for element in list_cpd:
    dict_evi = element.get_evidence()
    dict_vari = element.variable
    dict_value = element.values

    i = 0
    array_frame = np.zeros(shape=(len(dict_evi), 2 ** len(dict_evi)))
    while i < len(dict_evi):
        line01 = ('0 ' * int((2 ** (len(dict_evi)-i))/2) + '1 ' * int((2 ** (len(dict_evi)-i))/2)) * ( 2 ** (len(dict_evi) - ((len(dict_evi)-i))))
        splitline01 = line01.split(' ')
        changeint = [int(li) for li in splitline01[0:-1]]
        array_frame[i] = changeint

        i = i+1

    print(array_frame)
    cpd_dictionary[(tuple(dict_evi), tuple([dict_vari]))] = dict_value

    for evi in range(len(dict_evi)):
        print(dict_evi[evi])
        tup1 =  "".join(tuple((str(dict_evi[evi]) + str(array_frame[evi])))), tuple([dict_vari])
        cpd_dictionary[tup1] = dict_value

    #cpd_dictionary[( tuple(dict_evi), tuple([dict_vari]) )] = dict_value   # (키) = 값

pprint.pprint(cpd_dictionary)

#for key in list(cpd_dictionary.keys()):



#nodes = testDBN.nodes
#for node in nodes:
#    k = DBN.get_ancestral_graph(testDBN, [(node)])
#    print(k.edges())





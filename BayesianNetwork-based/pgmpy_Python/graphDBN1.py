from gbxml import Gbxml
from pgmpy.base import *
from pgmpy.models import DynamicBayesianNetwork
import matplotlib.pyplot as plt

import networkx as nx

###GBXML in graph
g = Gbxml(r'C:\Users\lablj\Desktop\SmoBuil\2room.gbxml')
G = DAG()
DBN = DynamicBayesianNetwork()

###class 정의
class Space:
    id_type = 'Space'
    def __init__(self):
        self.id = 'aim0001'
        self.area = 0
        self.volume = 0

    def getxmldata(self, id, area, volume):
        self.id = id
        self.area = area
        self.volume = volume

class Surface:
    id_type = 'Surface'
    def __init__(self):
        id = 'aim0002'
        spaceIdRef = 'aim0001'
        surfacetype = 'Shade'

    def getxmldata(self, id, spaceIdRef, surfacetype):
        self.id = id
        self.spaceIdRef = spaceIdRef
        self.surfacetype = surfacetype

    def printInfo(self):
        print('-----------------------------------------')
        print('| Surface Id:', self.id)
        print('| Space Id Reference:', self.spaceIdRef)
        print('| Surface Type:', self.surfacetype)
        print('-----------------------------------------')

class Opening:
    id_type = 'Opening'
    def __init__(self):
        id = 'aim0003'
        surface_id = 'aim0002'
        openingtype = 'Window'
        area = 0

    def getxmldata(self, id, surface_id, openingtype, area):
        self.id = id
        self.surface_id = surface_id
        self.openingtype = openingtype
        self.area = area

    def printInfo(self):
        print('-----------------------------------------')
        print('| Opening Id:', self.id)
        print('| Surface Id:', self.surface_id)
        print('| Opening Type:', self.openingtype)
        print('| Area:', self.area)
        print('-----------------------------------------')

### gbxml로부터 클래스 인스턴스 생성 및 속성 부여
space_ids = g.get_ids(tag = 'Space')
filtered_surface = []
for spid in space_ids:
    globals()[f'{spid}'] = Space()
    globals()[f'{spid}'].getxmldata(spid,
                                    g.get_child_tag_text(id=spid, child_tag='Area'),
                                    g.get_child_tag_text(id=spid, child_tag='Volume'))

    spaceboundary_ids = sorted(g.get_space_surface_ids(id = spid))

    surface_with_openings = []
    for sbid in spaceboundary_ids:
        surface_child_tags = g.get_child_tags(id = sbid)
        if 'Opening' in surface_child_tags:
            surface_with_openings.append(sbid)
            filtered_surface.append(sbid)

    for swo in surface_with_openings:
        sIR = []
        globals()[f'{swo}'] = Surface()
        att = g.get_child_tag_attributes(id = str(swo), child_tag= 'AdjacentSpaceId')
        [sIR.append(e['spaceIdRef']) for e in att]
        globals()[f'{swo}'].getxmldata(id=swo,
                                       spaceIdRef = sIR,
                                       surfacetype = g.get_attributes(id=swo).get('surfaceType'))
        globals()[f'{swo}'].printInfo()

        openings = g.get_surface_opening_ids(id = str(swo))
        for op in openings:
            globals()[f'{op}'] = Opening()

            if g.get_attributes(id = op)['openingType'].count('Door') >= 1:
                globals()[f'{op}'].getxmldata(id = op,
                                              surface_id = swo,
                                              openingtype = 'Door',
                                              area = g.get_opening_area(id = str(op)))
            elif g.get_attributes(id = op)['openingType'].count('Window') >= 1:
                globals()[f'{op}'].getxmldata(id = op,
                                              surface_id = swo,
                                              openingtype = 'Window',
                                              area = g.get_opening_area(id = str(op)))
            elif g.get_attributes(id = op)['openingType'].count('Air') >= 1:
                globals()[f'{op}'].getxmldata(id = op,
                                              surface_id = swo,
                                              openingtype = 'Air',
                                              area = g.get_opening_area(id = str(op)))
            globals()[f'{op}'].printInfo()

### G 생성: space node와 opening이 있는 surface edge
surface_ids = []
for spid in space_ids:
    surface_ids = sorted(g.get_space_surface_ids(id = spid))
    G.add_node(node = spid)
    for sfid in surface_ids:

        if sfid in filtered_surface:
            surfSpaces = globals()[f'{sfid}'].spaceIdRef

            if len(surfSpaces) == 2 and surfSpaces[0] != surfSpaces[1]:
                G.add_edge(surfSpaces[0], surfSpaces[1])

            else:
                pass

        else:
            pass


def showgraph(graph, w=30, h=30):
    plt.figure(figsize=(w, h))
    pos = nx.kamada_kawai_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_size = 500, node_color = "#FFA07A", alpha = 0.7, node_shape = 'o',  )
    nx.draw_networkx_labels(graph, pos, font_size = 10, font_family = 'Sans-serif', font_color = 'Black')
    nx.draw_networkx_edges(graph, pos, edge_color= '#DE3163', alpha = 1.0, arrowsize = 20,
                           min_source_margin = 3, min_target_margin = 3)
    plt.show()

###firstorder dbn
def firstorder_dbn(DBN):
    for node in G.nodes:
        DBN.add_node(node)
        DBN.add_edges_from([((node, 0), (node, 1))])

    edge_list = []
    for edge in G.edges:
        edge_list.append(list(edge))

    for el in range(len(edge_list)):
        DBN.add_edges_from([((edge_list[el][0], 0), (edge_list[el][1], 0))])

firstorder_dbn(DBN)
print(DBN)

# showgraph(DBN)

### networkx node position 고정하는 코드





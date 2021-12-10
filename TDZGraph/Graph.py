from copy import deepcopy
from math import inf

import numpy as np
from pandas import DataFrame


class Graph:
    _representation = []
    _transitions = []
    _vertices = None
    _edges = None
    _cyclic = False

    def get_transitions_target(self, input_node):
        targets = []
        for i in self.transitions:
            if i[0] == input_node:
                targets.append(i[2])
        return targets

    def have_cycle(self, visited=None, current_node=0):
        if visited is None:
            visited = []

        visited = deepcopy(visited)
        visited.append(current_node)

        transitions_list = self.get_transitions_target(current_node)

        for i in transitions_list:
            if i in visited:
                return True

        for j in transitions_list:
            if self.have_cycle(visited, j):
                return True

        return False

    def reset(self):
        print('reset')
        self.representation = []
        self.vertices = None
        self.edges = None

    def load_str(self, str_graph):
        lines = str_graph.split('\n')

        self.vertices = lines.pop(0)
        assert self.vertices is not None

        self.edges = lines.pop(0)
        assert self.edges is not None

        self.representation = list(list((inf if j != i else 0) for j in range(self.vertices)) for i in range(self.vertices))

        self.transitions = []
        for i in lines:
            try:
                self.transitions.append(list(int(x) for x in i.split()))
                # print(self.transitions[-1])
                self.representation[self.transitions[-1][0]][self.transitions[-1][2]] = self.transitions[-1][1]
            except ValueError:
                raise AssertionError()
        assert not(not(len(self.transitions)))

        self.representation = DataFrame(np.array(self.representation), columns=list(i for i in range(self.vertices)))

    def load_file(self, filename):
        with open(filename, 'r') as fileGraph:
            graph = fileGraph.read()
        # --- load file ---
        self.load_str(graph)

    @property
    def representation(self):
        return self._representation

    @representation.setter
    def representation(self, value):
        self._representation = value

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, nb_edges):
        try:
            self._edges = int(nb_edges)
        except ValueError:
            print('invalid input (edge) : ', nb_edges)
            # self.reset()
            raise ValueError

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, nb_vertices):
        try:
            self._vertices = int(nb_vertices)
        except ValueError:
            print('invalid input (vertices) : ', nb_vertices)
            # self.reset()
            raise ValueError

    @property
    def transitions(self):
        return self._transitions

    @transitions.setter
    def transitions(self, value):
        self._transitions = value

    @property
    def cyclic(self):
        return self._cyclic


if __name__ == "__main__":
    graph1str = """4
5
0 1 1
0 5 2
1 -3 2
1 5 3
2 2 3"""
    graph1 = Graph()
    graph1.load_str(graph1str)
    print(graph1.representation)
    print("Graph 1 is cyclic : ", graph1.have_cycle())

    graph3str = """4
6
0 1 1
0 -5 2
2 4 1
1 -3 2
1 2 3
2 2 3"""
    graph3 = Graph()
    graph3.load_str(graph3str)
    print(graph3.representation)
    print("Graph 3 is cyclic : ", graph3.have_cycle())

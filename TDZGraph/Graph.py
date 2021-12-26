import os
import sys
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

    def shortest_path(self, initial_point=None, final_point=None):
        """
        Compute the shortest path between all pair of vertices (allowing negative edge) with the Floyd-Warshall
        algorithm.

        It can take as input an initial and final point to compute the shortest path between those.

        If no input is given, the method display all the steps of the algorithm as well as the matrices L and P (before
        and after the process)
        :param initial_point: initial point of the wanted path
        :param final_point: final point of the wanted path
        :return: either the entire L matrix or the cost of the computed path
        """
        # if the shortest path from a certain point is asked we do not display the process only the output
        if (initial_point and final_point) is not None:
            assert initial_point in self._representation.columns
            assert final_point in self._representation.columns
            sys.stdout = open(os.devnull, 'w')

        print('Shortest path of the graph through Floyd-Warshall Algorithm')

        # initialization
        print('Initialization')
        l = deepcopy(self._representation).applymap(lambda x: inf if x is None else x)
        p = deepcopy(self._representation)
        counter = 0  # steps index

        def display_l_p():
            print('\nMatrix L :')
            print(l)
            print('\nMatrix P :')
            print(p)
            print('\n')

        for i in range(len(l)):
            l[i][i] = 0
            for j in range(len(l[i])):
                p[i][j] = j if p[i][j] is not None else p[i][j]
        old_l = deepcopy(l)
        old_p = deepcopy(p)
        display_l_p()

        print('\nComputing the shortest path')
        change = True
        absorbent = False
        while change and not(absorbent := (True in map(lambda x: x < 0, np.diag(l)))):
            change = False
            print(f'Step {(counter := counter+1)}')
            display_l_p()
            for i in l.columns:
                for j in l.columns:
                    for k in l.columns:
                        if l[j][k] > l[j][i] + l[i][k]:
                            l[j][k] = l[j][i] + l[i][k]
                            p[j][k] = p[i][k]
                            change = True

        print(f'Ended at step {counter} {("due to an absorbent circuit" if absorbent else "")}with :')
        display_l_p()
        print(f'Original L matrix : \n{old_l}\n')
        print(f'Original P matrix : \n{old_p}\n')

        if (initial_point and final_point) is not None:
            sys.stdout = sys.__stdout__
            print(f'Shortest path from {initial_point} to {final_point} cost {l[final_point][initial_point]}')
            return l[final_point][initial_point]

        return l

    def get_transitions_target(self, input_node):
        """
        Return all the successors of the given node
        :param input_node: node of the graph
        :return: array of successors of the given node
        """
        targets = []
        for i in self.transitions:
            if i[0] == input_node:
                targets.append(i[2])
        return targets

    def have_cycle(self, visited=None, current_node=0):
        """
        Function to compute if the graph contains cycles
        :return: boolean
        """
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
        """
        Reset the object
        """
        print('reset')
        self.representation = []
        self.vertices = None
        self.edges = None

    def load_str(self, str_graph):
        """
        Load a graph into the object given a string
        :param str_graph: graph under string form
        :return: the loaded graph
        """
        lines = str_graph.split('\n')

        self.vertices = lines.pop(0)
        assert self.vertices is not None

        self.edges = lines.pop(0)
        assert self.edges is not None

        # self.representation = list(
        #     list((None if j != i else 0) for j in range(self.vertices)) for i in range(self.vertices)
        # )
        self.representation = list(list(None for j in range(self.vertices)) for i in range(self.vertices))

        self.transitions = []
        for i in lines:
            try:
                self.transitions.append(list(int(x) for x in i.split()))
                # print(self.transitions[-1])
                self.representation[self.transitions[-1][0]][self.transitions[-1][2]] = self.transitions[-1][1]
            except ValueError:
                raise AssertionError()
        assert len(self.transitions) == self.edges

        self.representation = DataFrame(np.array(self.representation), columns=list(i for i in range(self.vertices)))
        return self.representation

    def load_file(self, filename):
        """
        Load a graph into the object given a file
        :param filename: path of the graph file
        :return: loaded graph
        """
        with open(filename, 'r') as fileGraph:
            graph = fileGraph.read()
        # --- load file ---
        return self.load_str(graph)

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
    print("*-------*")
    print("|graph 1|")
    print("*-------*")
    print(graph1.representation)
    print("Graph 1 is cyclic : ", graph1.have_cycle())
    print("Floyd-Warshall's algorithm on graph 1")
    graph1.shortest_path()

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
    print("\n*-------*")
    print("|graph 3|")
    print("*-------*")
    print(graph3.representation)
    print("Graph 3 is cyclic : ", graph3.have_cycle())
    print("Shortest path from 1 to 3 in graph 3 using Floyd-Warshall's algorithm")
    graph3.shortest_path(initial_point=1, final_point=3)


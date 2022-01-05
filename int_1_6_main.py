from os import listdir, path

from int_1_6_TDZGraph.int_1_6_Graph import Graph


def ui(temp=None):
    """
    User Interface (more info in the README file)
    :param temp: stored graphs
    """
    if temp is None:
        temp = {}

    graphs = list(filter(None, (tempGraphs := [str(i) if 'int_1_6_graph' in str(i) else None for i in listdir('./')]) +
                         [str(i) if str(i) not in tempGraphs else None for i in temp.keys()]))
    print("""
*--------------------------------------------------------*
|Search for shortest paths using Floyd-Warshall algorithm|
|a tdz program                                           |
*--------------------------------------------------------*
please select a graph
(enter -1 to load a graph which isn't in the following list)
(enter -2 to write a graph)""")
    for graph in graphs:
        print(f"\t{str(graphs.index(graph) + 1)} - {graph}")

    selected_graph: int
    try:
        selected_graph = int(input()) - 1
        if selected_graph == -2:
            graphs.append(input('enter the graph path : '))
            assert path.isfile(graphs[-1])
            selected_graph = -1
        elif selected_graph == -3:
            graphs.append(input('enter graph name : '))
            selected_graph = -1

            def ask_size():
                try:
                    v1 = int(input('enter the number of Vertex : '))
                    v2 = int(input('enter the number of Vertices : '))
                    assert v1 > 0
                    assert v2 >= 0
                    return v1, v2
                except ValueError or AssertionError:
                    print("wrong input")
                    return ask_size()

            vertex, vertices = ask_size()
            temp[graphs[-1]] = str(vertex) + '\n' + str(vertices)

            def ask_vertices(index: int, col: int):
                try:
                    i = int(input(f'Enter the source vertex for vertice {index} : '))
                    e = int(input(f'Enter the cost for vertice {index} : '))
                    f = int(input(f'Enter the source vertex for vertice {index} : '))
                    assert col > i >= 0
                    assert col > f >= 0
                    return '\n' + str(i) + ' ' + str(e) + ' ' + str(f)
                except ValueError or AssertionError:
                    print('wrong input')
                    return ask_vertices(index, col)

            for i in range(vertices):
                print('\n')
                temp[graphs[-1]] += ask_vertices(i, vertex)

            with open(graphs[-1] + '.txt', 'w') as f:
                f.write(temp[graphs[-1]])

            temp_graph = Graph()
            try:
                temp_graph.load_str(temp[graphs[-1]])
            except AssertionError or ValueError or IndexError:
                print('The graph is corrupted, try another graph')
                temp.pop(graphs[-1])
                ui(temp=temp)
                return
            temp[graphs[-1]] = temp_graph
            print('\n')
    except ValueError:
        print("wrong input")
        ui(temp=temp)
        return
    except AssertionError:
        print("The asked graph doesn't exist")
        ui(temp=temp)
        return

    graph: Graph
    if graphs[selected_graph] in temp.keys():
        graph = temp[graphs[selected_graph]]
    else:
        graph = Graph()
        try:
            graph.load_file(filename='./' + graphs[selected_graph])
        except AssertionError or ValueError or IndexError:
            print(f'The graph {graphs[selected_graph]} is corrupted, try another graph')
            ui(temp=temp)
        temp[graphs[selected_graph]] = graph

    print(graph.representation)
    print(
        f'Graph {selected_graph + 1} {"have" if (cyclic := graph.have_absorbent_cycle()) else "haven t"} an absorbent cycle')

    def ask_display_matrix():
        if (display := input("\nDisplay shortest path matrix ? (y/n) : ")).lower() == 'y' or display.lower() == 'yes':
            graph.shortest_path()
        elif not (display.lower() == 'n' or display.lower() == 'no'):
            ask_display_matrix()

    ask_display_matrix()

    def ask_shortest_path(g):
        if not g.cyclic and (
                (display := input("\nDisplay a shortest path ? (y/n) : ")).lower() == 'y' or display.lower() == 'yes'):
            initial: int
            final: int
            try:
                initial = int(input('Enter the initial vertex: '))
                assert graph.vertices > initial >= 0
                final = int(input('Enter the final vertex: '))
                assert graph.vertices > final >= 0
            except ValueError:
                print("wrong input")
                ask_shortest_path(g)
                return
            except AssertionError:
                print("the vertex aren't in the graph")
                ask_shortest_path(g)
                return
            graph.shortest_path(initial_point=initial, final_point=final)

    ask_shortest_path(graph)

    def ask_load_graph():
        if (again := input("\nload another graph ? (y/n) : ")).lower() == 'y' or again.lower() == 'yes':
            ui(temp=temp)
        elif not (again.lower() == 'n' or again.lower() == 'no'):
            ask_load_graph()

    ask_load_graph()


if __name__ == "__main__":
    ui()

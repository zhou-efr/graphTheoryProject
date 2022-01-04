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
please select a graph (enter -1 to load a graph which isn't in the following list)""")
    for graph in graphs:
        print(f"\t{str(graphs.index(graph)+1)} - {graph}")

    selected_graph: int
    try:
        selected_graph = int(input())-1
        if selected_graph == -2:
            graphs.append(input('enter the graph path : '))
            assert path.isfile(graphs[-1])
            selected_graph = -1
        else:
            assert len(graphs) > selected_graph >= 0
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
        graph.load_file(filename='./' + graphs[selected_graph])
        temp[graphs[selected_graph]] = graph

    print(graph.representation)
    print(f'Graph {selected_graph+1} {"have" if (cyclic := graph.have_absorbent_cycle()) else "haven t"} an absorbent cycle')

    def ask_display_matrix():
        if (display := input("\nDisplay shortest path matrix ? (y/n) : ")).lower() == 'y' or display.lower() == 'yes':
            graph.shortest_path()
        elif not(display.lower() == 'n' or display.lower() == 'no'):
            ask_display_matrix()
    ask_display_matrix()

    def ask_shortest_path(g):
        if not g.cyclic and (d := input("\nDisplay a shortest path ? (y/n) : ")).lower() == 'y' or d.lower() == 'yes':
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
        elif not(again.lower() == 'n' or again.lower() == 'no'):
            ask_load_graph()
    ask_load_graph()


if __name__ == "__main__":
    ui()

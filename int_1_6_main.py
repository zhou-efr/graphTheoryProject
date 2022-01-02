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
            graphs.append(input())
            assert path.isfile(graphs[-1])
            selected_graph = -1
        else:
            assert len(graphs) > selected_graph >= 0
    except ValueError:
        print("wrong input")
        ui()
        return
    except AssertionError:
        print("The asked graph doesn't exist")
        ui()
        return

    graph: Graph
    if graphs[selected_graph] in temp.keys():
        graph = temp[graphs[selected_graph]]
    else:
        graph = Graph()
        graph.load_file(filename='./' + graphs[selected_graph])
        temp[graphs[selected_graph]] = graph

    print(graph.representation)
    print(f'Graph {selected_graph+1} {"have" if (cyclic := graph.have_cycle()) else "haven t"} an absorbent cycle')
    # if not cyclic and ((display := input("\nDisplay shortest path ? (y/n) : ")).lower() == 'y' or display.lower()
    # == 'yes'):
    if not cyclic:
        graph.shortest_path()

    def ask_load_graph():
        if (again := input("\nload another graph ? (y/n) : ")).lower() == 'y' or again.lower() == 'yes':
            ui(temp=temp)
        elif not(again.lower() == 'n' or again.lower() == 'no'):
            ask_load_graph()
    ask_load_graph()


if __name__ == "__main__":
    ui()

from os import listdir, path

from TDZGraph.Graph import Graph


def ui(temp=None):
    """
    User Interface
    :param temp: stored graphs
    """
    if temp is None:
        temp = {}
    graphs = listdir('./graphs') + [str(i) if str(i) not in listdir('./graphs') else None for i in temp.keys()]
    print("""
*--------------------------------------------------------*
|Search for shortest paths using Floyd-Warshall algorithm|
|a tdz program                                           |
*--------------------------------------------------------*
please select a graph (enter -1 to load a graph which isn't in the following list)""")
    for graph in graphs:
        graph_index = graphs.index(graph)
        if graph is None:
            graphs.pop(graph_index)
        else:
            print(f"\t{str(graph_index+1)} - {graph}")

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
        graph.load_file(filename='./graphs/' + graphs[selected_graph])
        temp[graphs[selected_graph]] = graph

    print(graph.representation)
    print(f'Graph {selected_graph+1} {"have" if (cyclic := graph.have_cycle()) else "haven t"} an absorbent cycle')
    # if not cyclic and ((display := input("\nDisplay shortest path ? (y/n) : ")).lower() == 'y' or display.lower()
    # == 'yes'):
    if not cyclic:
        graph.shortest_path()

    if (again := input("\nload another graph ? (y/n) : ")).lower() == 'y' or again.lower() == 'yes':
        ui(temp=temp)


if __name__ == "__main__":
    ui()

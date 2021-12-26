from os import listdir

from TDZGraph.Graph import Graph


def ui():
    graphs = listdir('./graphs')
    print("""
*--------------------------------------------------------*
|Search for shortest paths using Floyd-Warshall algorithm|
|a tdz program                                           |
*--------------------------------------------------------*
please select a graph""")
    for graph in graphs:
        print(f"\t{str(graphs.index(graph)+1)} - {graph}")

    try:
        selected_graph = int(input())-1
        assert len(graphs) > selected_graph >= 0
    except ValueError:
        print("wrong input")
        ui()
        return
    except AssertionError:
        print("index out of range")
        ui()
        return

    graph = Graph()
    graph.load_file(filename='./graphs/' + graphs[selected_graph])
    print(graph.representation)
    print(f'Graph {selected_graph+1} {"is" if graph.have_cycle() else "isn t"} cyclic')
    if (display := input("\nDisplay shortest path ? (y/n) : ")).lower() == 'y' or display.lower() == 'yes':
        graph.shortest_path()

    if (again := input("\nload another graph ? (y/n) : ")).lower() == 'y' or again.lower() == 'yes':
        ui()


if __name__ == "__main__":
    ui()

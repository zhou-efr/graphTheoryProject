# Search for shortest paths using Floyd-Warshall algorithm
![python-3.9.8](https://img.shields.io/badge/python-3.9.8-green) ![](https://img.shields.io/badge/pandas-1.3.4-lightgrey)
## Installation
This code includes feature of python >= 3.8, please make sure to have a compatible version of python.
### Dependencies
The dependencies of this project are listed in the file `requirements.txt`. I recommend you to use a 
[virtual environment](https://docs.python.org/fr/3/library/venv.html) yet you only need to run `pip install -r 
requirements.txt` having a `venv` or not. 
### Run code
The main code with the user interface is in `main.py`, however, each independent file (except initialization ones) 
contains a sample code.
## Use
### Main program
First, all the files contained in the folder `/graphs` will be displayed by the program. Then you'll be asked to choose one,
If the input isn't an integer, the program will display *wrong error* then repeat the question. If the requested graph 
doesn't exist (wrong index), the program will display *Index out of range* and repeat the question.

Once a graph is selected, it is displayed as a table of edges. Then the program asks you whether you want to display the
application of Floyd-Warshall's shortest path algorithm on the selected graph or not. Answer in the affirmative will
detail all the steps of the algorithm, ending with the comparison of result matrices L and P and the original ones.

Else way it will simply ask if you want to load another graph.
### Sample programs
Samples programs are without interactions, those are juste used for demonstration.
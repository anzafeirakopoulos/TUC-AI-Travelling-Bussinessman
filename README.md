### About the project
This project was part of the Artificial Intelligence course of ECE Technical University of Crete.

## Installation

No libraries where used other than what is integrated in python 3.8.0. 

1. Navigate to the project directory .../AI-project1.
2. In the terminal: python main.py.
3. From the menu navigate which file to run the program with.

# Offline Search Optimization

This project is a study on searching tree data structures and finding optimal or near optimal solutions in an offline environment.

### The problem
A bussinessman living in a big city has to travel everyday for the next 80 days to go to work. The night before each day, he has to make a decision about which path to choose in the morning in order to avoid as much traffic as possible. In the morning, he follows the path he made for himself the previous night and determines what was the real traffic compared to his assumptions.

* The program takes as an input one of three graphs.
* Each graph represents all the possible paths that the businessman can take to go to work.
* In the graph, the nodes represent streets on a map, and the edges the cost of traffic for each street.
* The traffic that connects two nodes is an enumeration {heavy, normal, low}.
* The traffic described in the graph is a prediction made by the businessman. The accuracy of his prediction is based on a probability. F.e a road has heavy traffic with p1 = 0.6 and has normal of low trafic with p2=p3=0.2.
* After the passing of each day, the businessman can reconsider the accuracy of his probabilities.

# Implementation
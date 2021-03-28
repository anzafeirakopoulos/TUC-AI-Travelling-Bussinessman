import main
import pprint
import random
import bisect
from operator import itemgetter

average_cost_per_road = 0


class Graph:

    def __init__(self, graph_dict, p1, p2, p3, h_dict):
        self.graph_dict = graph_dict
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.h_dict = h_dict


    # getter methods.
    def get_p1(self):
        return self.p1

    def get_p2(self):
        return self.p2

    def get_p3(self):
        return self.p3

    # setter methods.
    def set_p1(self, x):
        self.p1 = x

    def set_p2(self, x):
        self.p2 = x

    def set_p3(self, x):
        self.p3 = x

    def set_h_dict(self, hdict):
        self.h_dict = hdict


    # Roll a dice to select the predicted traffic status based on the current traffic propability distribution.
    # Each traffic status has a range that is based on the possibility of actually appearing.
    def select_propability_coefficient(self):

        temp_p1 = self.get_p1() * 100
        temp_p2 = self.get_p2() * 100
        # temp_p3 = self.get_p3() * 100

        # Select a number randomly between 1 and 100.
        r_number = random.randint(1, 100)

        if (r_number >= 1) and (r_number < temp_p1):

            traffic = "low"

        elif (r_number >= temp_p1)  and (r_number < temp_p2 + temp_p1):

            traffic = "normal"

        elif (r_number >= temp_p2 + temp_p1) and (r_number <= 100):

            traffic = "heavy"


        return traffic


    # Parsing the file, extracting information and populating the graph.
    def read_graph(self, file):

        average_cost_per_road = 0
        read_graph_flag = False
        predictions_line = 0
        actual_traffic_line = 0
        roads_count = 0

        for number, line in enumerate(file):

            if(line.startswith("<Source>")):

                source = main.remove_tags(line)

            elif(line.startswith("<Destination>")):

                destination = main.remove_tags(line)

            elif(line == "<Roads>\n"):

                read_graph_flag = True

            elif(line == "</Roads>\n"):

                read_graph_flag = False

            elif(read_graph_flag is True):

                roads_count += 1
                graph_array = line.split(';' ' ', 4)
                average_cost_per_road += int(graph_array[3])
                self.populate_graph(graph_array[0], graph_array[1],
                                    graph_array[2], graph_array[3].rstrip())

            elif(line == "<ActualTrafficPerDay>\n"):

                actual_traffic_line = number + 1

            elif(line == "<Predictions>\n"):

                predictions_line = number + 1

        average_cost_per_road = average_cost_per_road / roads_count

        return source, destination, actual_traffic_line, predictions_line, roads_count


    # Find the heuristic function values. Start from the destination node.
    def myheuristic(self, source, destination):

        heur_dict = {}
        fringe = []
        visited = []

        # expand the destination node.
        for child in self.graph_dict[source]:

            fringe.append(child)
            visited.append(child)

            # find the minimum road if there are more than 1.
            min_rcost = min(self.graph_dict[source][child].items(), key=itemgetter(1))
            # road_path.append(temp[0])

            if child not in heur_dict:

                heur_dict[child] = int(min_rcost[1])

        # print(heur_dict)
        # print(fringe)
        # print(visited)
        self.my_heur(heur_dict, source, fringe)


    # Continuation of the function above.
    def my_heur(self, heur_dict, source, fringe):

        visited = []

        # expanding the neighboors.
        for node in fringe:

            visited.append(node)
            # Insert temporary heuristic g(n) value for node.
            cost = heur_dict[node]

            for child in self.graph_dict[node]:

                if child is not source:

                    if child not in visited:
                        # Keep expanding the fringe until all nodes have been assigned an h(n) value.
                        # extends the external loop to include this.
                        fringe.append(child)

                    # Calculate the minimum road between the node and the child.
                    min_rcost = min(self.graph_dict[node][child].items(), key=itemgetter(1))
                    connecting_path = min(self.graph_dict[node][child].items(), key=itemgetter(1))

                    # If the child node is found for first time, set the heuristic value as the min(step-cost) + g(n).
                    if child not in heur_dict:

                        heur_dict[child] = int(min_rcost[1]) + cost

                    # If another path to the child already exists,
                    # check if the currently explored path is the smaller than the one already assigned.
                    elif (heur_dict[child] > int(connecting_path[1]) + cost):

                        heur_dict[child] = int(connecting_path[1]) + cost

        # pprint.pprint(heur_dict)
        # print(fringe)
        self.set_h_dict(heur_dict)


    # Calculates the cost for a path returned by BFS.
    def calculate_cost_bfs(self, path):

        cost_per_road = []
        road_path = []
        total_cost = 0

        pipis = 0
        sifis = 1

        # For every node in the path
        while sifis <= len(path) - 1:

            # If the node path[sifis] is a neighboor of the node path[pipis]
            if path[sifis] in self.graph_dict[path[pipis]]:

                # Select the minimum road that connects the two neighboors.
                temp = min(self.graph_dict[path[pipis]][path[sifis]].items(), key=itemgetter(1))
                cost_per_road.append(int(temp[1]))
                road_path.append(temp[0])

            else:
                # Since BFS explores every node in a level before continuing,
                pipis += 1

                # If the node path[sifis] is not a child of path[pipis],
                # search continually for the nodes that are next of list at index pipis.
                while path[sifis] not in self.graph_dict[path[pipis]]:

                    pipis += 1

                # Select the minimum road that connects the two neighboors.
                temp = min(self.graph_dict[path[pipis]][path[sifis]].items(), key=itemgetter(1))
                cost_per_road.append(int(temp[1]))
                road_path.append(temp[0])

            sifis += 1

        total_cost = sum(cost_per_road)

        return total_cost, cost_per_road, road_path


    # Calculate the total cost for IDA* based on the predicted traffic statuses.
    def calculate_base_cost_ida(self, path, roads):

        total_cost = []

        for index in range(len(path) - 1):

            total_cost.append(self.graph_dict[path[index]][path[index+1]][roads[index]])
            total_cost[index] = int(total_cost[index])

        return total_cost

    # Inserting nodes into the graph.
    def populate_graph(self, road, node1, node2, cost):

        # Insert node1 into the graph.
        if not(node1 in self.graph_dict):

            self.graph_dict[node1] = {}

        # Assign node2 as neighboor.
        if not(node2 in self.graph_dict[node1]):

            self.graph_dict[node1][node2] = {}

        # Create bidirectionality.
        if not(node2 in self.graph_dict):

            self.graph_dict[node2] = {}

        # Assign node1 as neighboor.
        if not(node1 in self.graph_dict[node2]):

            self.graph_dict[node2][node1] = {}

        # Assign the road cost between the two neighboors.
        self.graph_dict[node1][node2][road] = cost
        self.graph_dict[node2][node1][road] = cost


    # BFS algorithm.
    def breadth_first_search(self, source, destination):

        node = source
        fringe = list()
        visited = list()

        fringe.append(node)
        while fringe:

            node = fringe.pop(0)
            visited.append(node)

            if node == destination:

                return visited

            for child in self.graph_dict[node]:

                # Guarantee no circle (infinite loop) exists.
                if (child not in visited) and (child not in fringe):

                    fringe.append(child)


    # Return the heuristic value that was calculated for given node by myheuristic-my_heur functions.
    def heuristic(self, node):
        return self.h_dict[node]


    # IDA* algorithm.
    def ida_star(self, predicted_traffic, source, destination):

        limit = self.heuristic(source)
        path = [source]
        path_of_roads = []
        cost_of_path = []

        while True:

            t = self.search(predicted_traffic, source, destination, path_of_roads, cost_of_path, path, 0, limit)

            # Found the destination node! .
            if t == -1:
                return path, path_of_roads, cost_of_path

            # Limit was reached, reevaluate the limit and execute again.
            limit = t


    def search(self, predicted_traffic, source, destination, path_of_roads, cost_of_path, path, g, limit):

        # Get the last node of the path.
        node = path[-1]

        # Construct the evalution function.
        f = g + self.heuristic(node)

        # Limit was reached.
        if f > limit:
            return f

        # Goal node found, return.
        if node == destination:
            return -1

        min = float("inf")

        # Calculate the successors by cheapest order.
        # The 3 returned lists hold correlational values in a 1-1 index position.
        successors, succ_roads, succ_road_cost = self.sorted_successors(predicted_traffic, node)
        counter = 0
        for child in successors:

            if child not in path:

                # Deduct the heuristic value that was added for for f(n) purposes.
                step_cost = succ_road_cost[counter] - self.heuristic(child)

                # Add/Keep track of the current path exploration values.
                path.append(child)
                path_of_roads.append(succ_roads[counter])
                cost_of_path.append(step_cost)
                # step_cost, step_road = self.min_road_cost(predicted_traffic, node, child)

                # Depening recursion based on the new f(n).
                t = self.search(predicted_traffic, source, destination, path_of_roads, cost_of_path, path, g + step_cost, limit)

                # Destination node was reached.
                if t == -1:
                    return -1
                # Select cheapest previous new limit.
                if t < min:
                    min = t

                # Deduct the information of the node that hit the limit.
                path.pop()
                path_of_roads.pop()
                cost_of_path.pop()

            counter += 1

        return min


    # Between two neighbooring nodes, find the cheapest road after including the predicted traffic weight influence.
    def min_road_cost(self, predicted_traffic, node, child):

        min_cost = float("inf")

        for road, cost in self.graph_dict[node][child].items():

            # traffic_status = predicted_traffic[road]
            traffic = self.select_propability_coefficient()

            if(traffic == "low"):

                temp_cost = int(cost)*0.9

            elif(traffic == "normal"):

                temp_cost = int(cost)

            else:

                temp_cost = int(cost)*1.25

            if temp_cost < min_cost:

                min_cost = temp_cost
                min_road = road

        return min_cost, min_road


    # Acquire successors of a node and put the in ascending list order.
    def sorted_successors(self, predicted_traffic, node):

        # Some declarations.
        # The three lists hold their values 1-1.
        cheapest_path = []
        cheapest_road = []
        cheapest_road_cost = []

        for child in self.graph_dict[node]:

            # Between two neighbooring nodes, find the cheapest road after including the predicted traffic weight influence.
            temp0_cost, temp_road = self.min_road_cost(predicted_traffic, node, child)

            # Sort the successors by calculating f(n), since all children have the same father, only the step cost and h(n) change.
            temp_cost = temp0_cost + self.heuristic(child)

            # If list of successors is empty.
            if not cheapest_road_cost:

                cheapest_road_cost.append(temp_cost)
                cheapest_road.append(temp_road)
                cheapest_path.append(child)

            else:
                
                # Find in the list the position index, so that after the insertion, the list is still of ascending order.
                x = bisect.bisect_left(cheapest_road_cost, temp_cost)

                # If the road cost is the most expensive add at the end.
                if x == len(cheapest_road_cost):
                    cheapest_road_cost.append(temp_cost)
                    cheapest_road.append(temp_road)
                    cheapest_path.append(child)

                # Insert at the position that is specified by bisect.
                else:
                    cheapest_road_cost.insert(x, temp_cost)
                    cheapest_road.insert(x, temp_road)
                    cheapest_path.insert(x, child)


        return cheapest_path, cheapest_road, cheapest_road_cost

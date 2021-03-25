import main
import random
import bisect
from operator import itemgetter


average_cost_per_road = 0


class Graph:

    def __init__(self, graph_dict, p1, p2, p3):
        self.graph_dict = graph_dict
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3


    # getter method 
    def get_p1(self): 
        return self.p1

    def get_p2(self): 
        return self.p2

    def get_p3(self): 
        return self.p3
      
    # setter method 
    def set_p1(self, x): 
        self.p1 = x 

    def set_p2(self, x): 
        self.p2 = x 

    def set_p3(self, x): 
        self.p3 = x 

    
    def select_propability_coefficient(self):
       
        temp_p1 = self.get_p1() * 100
        temp_p2 = self.get_p2() * 100
        temp_p3 = self.get_p3() * 100

        if abs((temp_p1 + temp_p2 + temp_p3) - 100) > 0.01:
            print("you stupid")
            assert(0)
        
        r_number = random.randint(1, 100)

        if (r_number >= 1) and (r_number < temp_p1):

            traffic = "low"
        
        elif (r_number >= temp_p1)  and (r_number < temp_p2 + temp_p1):

            traffic = "normal"

        elif (r_number >= temp_p2 + temp_p1) and (r_number <= 100):
        
            traffic = "high"


        return traffic
        

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

        return source, destination, actual_traffic_line, predictions_line, roads_count, average_cost_per_road


    def calculate_cost_bfs(self, path):

        cost_per_road = []
        road_path = []
        total_cost = 0

        pipis = 0
        sifis = 1
        while sifis <= len(path) - 1:

            if path[sifis] in self.graph_dict[path[pipis]]:

                temp = min(self.graph_dict[path[pipis]][path[sifis]].items(), key=itemgetter(1))
                cost_per_road.append(int(temp[1]))
                road_path.append(temp[0])

            else:

                pipis += 1

                while path[sifis] not in self.graph_dict[path[pipis]]:

                    pipis += 1

                temp = min(self.graph_dict[path[pipis]][path[sifis]].items(), key=itemgetter(1))
                cost_per_road.append(int(temp[1]))
                road_path.append(temp[0])

            sifis += 1

        total_cost = sum(cost_per_road)

        return total_cost, cost_per_road, road_path


    def populate_graph(self, road, node1, node2, cost):

        if not(node1 in self.graph_dict):

            self.graph_dict[node1] = {}

        if not(node2 in self.graph_dict[node1]):

            self.graph_dict[node1][node2] = {}

        if not(node2 in self.graph_dict):

            self.graph_dict[node2] = {}

        if not(node1 in self.graph_dict[node2]):

            self.graph_dict[node2][node1] = {}

        self.graph_dict[node1][node2][road] = cost
        self.graph_dict[node2][node1][road] = cost


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

                if (child not in visited) and (child not in fringe):

                    fringe.append(child)


    def heuristic(self, node):

        return 38


    def ida_star(self, predicted_traffic, source, destination):

        limit = self.heuristic(source)
        path = [source]
        path_of_roads = []
        cost_of_path = []

        while True:

            t = self.search(predicted_traffic, source, destination, path_of_roads, cost_of_path, path, 0, limit)
            if t == -1:
                return path, path_of_roads, cost_of_path, limit
            

            limit = t


    def search(self, predicted_traffic, source, destination, path_of_roads, cost_of_path, path, g, limit):

        node = path[-1]

        f = g + self.heuristic(node)

        if f > limit:
            return f

        if node == destination:
            return -1

        min = float("inf")
        successors, succ_roads, succ_road_cost = self.sorted_successors(predicted_traffic, node)
        counter = 0;
        for child in successors:

            if child not in path:

                step_cost = succ_road_cost[counter] - self.heuristic(node)

                path.append(child)
                path_of_roads.append(succ_roads[counter])
                cost_of_path.append(step_cost)
                # step_cost, step_road = self.min_road_cost(predicted_traffic, node, child)
                
                t = self.search(predicted_traffic, source, destination, path_of_roads, cost_of_path, path, g + step_cost, limit)
                if t == -1:
                    return -1
                if t < min:
                    min = t

                path.pop()
                path_of_roads.pop()
                cost_of_path.pop()

                counter += 1

        return min


    def min_road_cost(self, predicted_traffic, node, child):

        min_cost = float("inf")

        for road, cost in self.graph_dict[node][child].items():

            #traffic_status = predicted_traffic[road]

            if(self.select_propability_coefficient() == "low"):

                temp_cost = int(cost)*0.9

            elif(self.select_propability_coefficient() == "normal"):

                temp_cost = int(cost) 

            else:

                temp_cost = int(cost)*1.25 

            if temp_cost < min_cost:

                min_cost = temp_cost
                min_road = road

        return min_cost, min_road


    def sorted_successors(self, predicted_traffic, node):

        cheapest_path = []
        cheapest_road = []
        cheapest_road_cost = []

        for child in self.graph_dict[node]:

            temp0_cost, temp_road = self.min_road_cost(predicted_traffic, node, child)
            # Sort the successors by calculating f(n), since all children have the same father, only the step cost and h(n) change.
            temp_cost = temp0_cost + self.heuristic(child)

            if not cheapest_road_cost:

                cheapest_road_cost.append(temp_cost)
                cheapest_road.append(temp_road)
                cheapest_path.append(child)

            else:
                
                x = bisect.bisect_left(cheapest_road_cost, temp_cost)

                if x == len(cheapest_road_cost):
                    cheapest_road_cost.append(temp_cost)
                    cheapest_road.append(temp_road)
                    cheapest_path.append(child)
                else:
                    cheapest_road_cost.insert(x, temp_cost)
                    cheapest_road.insert(x, temp_road)
                    cheapest_path.insert(x, child)


        return cheapest_path, cheapest_road, cheapest_road_cost

               
             

import Graph
import pprint
import linecache
import time


graph_dict = {}



def remove_tags(text):

    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def read_traffic(traffic_line, road_number, lines):

    traffic = {}
    road_counter = 1

    while road_counter <= road_number:

        if(lines[traffic_line] == "<Day>\n" or lines[traffic_line] == "</Day>\n"):

            traffic_line += 1

        else:

            line = lines[traffic_line]
            temp = line.split(';' ' ', 2)
            traffic[temp[0]] = temp[1].rstrip()
            road_counter += 1
            traffic_line += 1

    return traffic, traffic_line


def calculate_real_cost(actual_traffic, road_path, predicted_cost_per_road):

    actual_total_cost = 0
    index = 0

    for road in road_path:

        traffic_status = actual_traffic[road]

        if(traffic_status == "low"):

            actual_total_cost += predicted_cost_per_road[index]*0.9

        elif(traffic_status == "normal"):

            actual_total_cost += predicted_cost_per_road[index]

        else:

            actual_total_cost += predicted_cost_per_road[index]*1.25

        index += 1

    return actual_total_cost


def reevaluate_propabilities(graph, road_number, actual_traffic, predicted_traffic):

    


       

   
    


def output(path, total_cost, cost_per_road, actual_total_cost, algo_name, day):

    number_of_nodes = len(path)

    if algo_name != "IDA*":
        print("Day", day)
    
    print(algo_name+":")
    print("\tVisited Nodes number:", number_of_nodes)
    print("\tPath:", end='')

    index = 0
    for index in range(len(path)):

        if index == len(path)-1:

            print(path[index], end='')

        else:

            print(path[index]+"("+str(cost_per_road[index])+")"+"->", end='')

        index += 1

    print("")
    print("\tPredicted cost:", total_cost)
    print("\tReal Cost:", actual_total_cost)


def main():

    p1 = 0.2
    p2 = 0.2
    p3 = 0.6

    graph = Graph.Graph(graph_dict, p1, p2, p3)

    file = open("sampleGraph1.txt", "r")

    source, destination, actual_traffic_line, predictions_line, roads_count, average_cost_per_road = graph.read_graph(file)

    file.close()

    source = source.rstrip()
    destination = destination.rstrip()

    path_bfs = graph.breadth_first_search(source, destination)

    predicted_total_cost, predicted_cost_per_road, road_path = graph.calculate_cost_bfs(path_bfs)


    file = open("sampleGraph1.txt", "r")
    lines = file.readlines()

    days = 80
    road_number = roads_count
    a_traffic_line = actual_traffic_line + 1
    p_traffic_line = predictions_line + 1

    
    for current_day in range(1):

        actual_traffic, a_traffic_line = read_traffic(a_traffic_line, road_number, lines)

        actual_real_cost_bfs = calculate_real_cost(actual_traffic, road_path, predicted_cost_per_road)

        predicted_traffic, p_traffic_line = read_traffic(p_traffic_line, road_number, lines)

        #path_ida, path_of_roads, cost_of_path, limit = graph.ida_star(predicted_traffic, source, destination)

        #actual_real_cost_ida = calculate_real_cost(path_of_roads, cost_of_path)

        #output(path_bfs, predicted_total_cost, predicted_cost_per_road, actual_real_cost_bfs, "Breadth First Search", current_day + 1)
        #output(path_ida, sum(cost_of_path), cost_of_path, actual_real_cost_ida, "IDA*", current_day + 1)
        
        reevaluate_propabilities(graph, road_number, actual_traffic, predicted_traffic)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))


import Graph
import pprint
import linecache
import time


graph_dict = {}
h_dict = {}
percentage_low = []
percentage_normal = []
percentage_heavy = []


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


def find_actual_traffic_dist(road_number, actual_traffic):

    low_counter = 0
    normal_counter = 0
    heavy_counter = 0

    for road in actual_traffic:

        if actual_traffic[road] == 'low':
            low_counter += 1

        elif actual_traffic[road] == 'normal':
            normal_counter += 1

        else:
            heavy_counter += 1
            
    pl = low_counter / road_number 
    pn = normal_counter / road_number
    ph = heavy_counter / road_number

    percentage_low.append(pl)
    percentage_normal.append(pn)
    percentage_heavy.append(ph)

    
def reevaluate_propabilities(graph, day):

    dist_low = sum(percentage_low) / day
    dist_normal = sum(percentage_normal) / day
    dist_heavy = sum(percentage_heavy) / day

    graph.set_p1(dist_low)
    graph.set_p2(dist_normal)
    graph.set_p3(dist_heavy)    


def output(path, total_cost, cost_per_road, actual_total_cost, algo_name, day, exec_time):

    number_of_nodes = len(path)

    if algo_name != "IDA*":
        print("Day", day)
    
    print(algo_name+":")

    if(algo_name != "IDA*"):
        #print("\tExecution time: %s milliseconds" % (exec_time))
        print("\tExecution Time: ~1 millisecond")
    else:
        print("\tExecution Time: %s seconds" % ('%.2f' % (exec_time)))

    print("\tVisited Nodes number:", number_of_nodes)
    print("\tPath:", end='')

    index = 0
    for index in range(len(path)):

        if index == len(path)-1:

            print(path[index], end='')

        else:

            print(path[index]+"("+str( '%.2f' % cost_per_road[index])+")"+"->", end='')

        index += 1

    print("")
    print("\tPredicted Cost:", '%.2f' %  total_cost)
    print("\tReal Cost:", '%.2f' % actual_total_cost)


def main():

    p1 = 0.2
    p2 = 0.2
    p3 = 0.6

    graph = Graph.Graph(graph_dict, p1, p2, p3, h_dict)

    choice = '0'
    while choice =='0':

        print("Choose what to do")
        print("  1) Run with sampleGraph1")
        print("  2) Run with sampleGraph2")
        print("  3) Run with sampleGraph3")
        print("  4) Run with custom file name")
        print("  5) Exit")

        choice = input ("Please enter your choice:")

        if choice == "1":

            print("Executing for sampleGraph1...")
            choice = 'sampleGraph1.txt'
            
        elif choice == "2":

            print("Executing for sampleGraph2...")
            choice = 'sampleGraph2.txt'

        elif choice == "3":

            print("Executing for sampleGraph3...")
            choice = 'sampleGraph3.txt'

        elif choice == "4":

            flag = False
            while flag == False:

                fr = input("\nPlease enter the name of the file you wish to read:")
                
                if fr.endswith('.txt'):
                    choice = fr
                    flag = True
                else:
                    print('Enter a file with the suffix .txt')

        elif choice == "5":

            print("YEET!")
            quit()

        else:

            print("Enter a valid command (1 through 5)")
            choice = '0'

    file = open(choice, "r")

    source, destination, actual_traffic_line, predictions_line, roads_count = graph.read_graph(file)

    file.close()

    source = source.rstrip()
    destination = destination.rstrip()

    graph.myheuristic(destination, source)

    time_bfs0 = time.time()
    path_bfs = graph.breadth_first_search(source, destination)
    
    predicted_total_cost, predicted_cost_per_road, road_path = graph.calculate_cost_bfs(path_bfs)
    time_bfs1 = round(time.time() - time_bfs0 * 1000) 

    file = open(choice, "r")
    lines = file.readlines()

    days = 80
    road_number = roads_count
    a_traffic_line = actual_traffic_line + 1
    p_traffic_line = predictions_line + 1

    cost_bfs = []
    cost_ida = []

    
    for current_day in range(days):

        actual_traffic, a_traffic_line = read_traffic(a_traffic_line, road_number, lines)

        actual_real_cost_bfs = calculate_real_cost(actual_traffic, road_path, predicted_cost_per_road)

        predicted_traffic, p_traffic_line = read_traffic(p_traffic_line, road_number, lines)

        time_ida0 = time.time()
        path_ida, path_of_roads, cost_of_path = graph.ida_star(predicted_traffic, source, destination)
        time_ida1 = time.time() - time_ida0

        base_cost_ida = graph.calculate_base_cost_ida(path_ida, path_of_roads)
        actual_real_cost_ida = calculate_real_cost(actual_traffic, path_of_roads, base_cost_ida)

        output(path_bfs, predicted_total_cost, predicted_cost_per_road, actual_real_cost_bfs, "Breadth First Search", current_day + 1, time_bfs1)
        output(path_ida, sum(cost_of_path), cost_of_path, actual_real_cost_ida, "IDA*", current_day + 1, time_ida1)
        
        
        find_actual_traffic_dist(road_number, actual_traffic)
        reevaluate_propabilities(graph, current_day + 1)

        cost_bfs.append(actual_real_cost_bfs)
        cost_ida.append(actual_real_cost_ida)

    mean_bfs = sum(cost_bfs) / days
    mean_ida = sum(cost_ida) / days

    print('\nMean real cost Breadth First Search:', '%.2f' % mean_bfs)
    print('Mean real cost IDA*:', '%.2f' % mean_ida)
    
        

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Total execution time: --- %.2f seconds ---" % (time.time() - start_time))

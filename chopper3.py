import json
import itertools
import googlemaps
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def get_distance_matrix(locations, api_key):
    gmaps = googlemaps.Client(key=api_key)
    matrix = gmaps.distance_matrix(locations, locations, mode='driving')
    
    distance_matrix = []
    for row in matrix['rows']:
        distance_matrix.append([element['distance']['value'] for element in row['elements']])
    
    return distance_matrix

def solve_tsp(distance_matrix):
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)
    
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]
    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    
    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        return [manager.IndexToNode(routing.IndexToNode(i)) for i in range(routing.Size())]
    else:
        return None

def main():
    file_path = 'tour_data.json'  # Replace with actual file path
    api_key = 'YOUR_GOOGLE_MAPS_API_KEY'  # Replace with your API key
    
    data = load_data(file_path)
    locations = [event['location'] for event in data['events']]
    distance_matrix = get_distance_matrix(locations, api_key)
    
    optimal_route = solve_tsp(distance_matrix)
    if optimal_route:
        print("Optimal Tour Route:")
        for index in optimal_route:
            print(locations[index])
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import numpy as np
import pandas as pd
from geopy.distance import geodesic
from itertools import permutations
import json

def optimize_itinerary(locations):
    """Solve TSP for a list of coordinates."""
    # Distance matrix
    distance_matrix = [
        [geodesic(locations[i], locations[j]).kilometers for j in range(len(locations))]
        for i in range(len(locations))
    ]

    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    # Define distance callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(distance_matrix[from_node][to_node])

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Solve the problem
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.time_limit.seconds = 10
    solution = routing.SolveWithParameters(search_parameters)

    # Extract solution
    if solution:
        index = routing.Start(0)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        return route
    else:
        return None

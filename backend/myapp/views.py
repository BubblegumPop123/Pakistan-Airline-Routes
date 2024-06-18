from django.shortcuts import render , HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import random
import math
from haversine import haversine
import os


# Create your views here.

def show(request):
    return HttpResponse("hello world")

@csrf_exempt
def getPath(request):
    if request.method == "POST":
        SourceCity = request.POST.get('SourceCity')
        DestinationCity = request.POST.get('DestinationCity')
        Date = request.POST.get('Date')
        if SourceCity is not None and DestinationCity is not None:
            # Airport class
            class Airport:
                def __init__(self, icao_code, latitude, longitude, city):
                    self.icao_code = icao_code
                    self.latitude = float(latitude)
                    self.longitude = float(longitude)
                    self.city = city


            # Preprocess airport data function
            def preprocess_airport_data(airport_data):
                """
                Preprocesses airport data to ensure latitude and longitude are in the correct range.
                """
                # Assuming a known scaling factor, if any, to convert to the correct range
                # Update these values with the actual scaling factors if available
                latitude_scaling_factor = 0.01
                longitude_scaling_factor = 0.01

                airport_data['Latitude'] = airport_data['Latitude'].astype(float) * latitude_scaling_factor
                airport_data['Longitude'] = airport_data['Longitude'].astype(float) * longitude_scaling_factor

                # Check if any latitude or longitude values are out of range
                if any((airport_data['Latitude'] < -90) | (airport_data['Latitude'] > 90)):
                    raise ValueError("One or more latitude values are out of range after scaling.")
                if any((airport_data['Longitude'] < -180) | (airport_data['Longitude'] > 180)):
                    raise ValueError("One or more longitude values are out of range after scaling.")

                return airport_data

            # Aircraft class
            class Aircraft:
                def __init__(self, aircraft_type, max_range, cruise_speed, fuel_consumption):
                    self.aircraft_type = aircraft_type
                    self.max_range = float(max_range)
                    self.cruise_speed = float(cruise_speed)
                    self.fuel_consumption = float(fuel_consumption)

            # Graph class for representing the network of airports
            class Graph:
                def __init__(self):
                    self.nodes = {}

                def add_edge(self, from_airport, to_airport, distance):
                    if from_airport not in self.nodes:
                        self.nodes[from_airport] = {}
                    self.nodes[from_airport][to_airport] = distance

            # Dijkstra's algorithm for shortest path
            def dijkstra(graph, start, end):
                shortest_paths = {start: (None, 0)}
                current_node = start
                visited = set()

                while current_node != end:
                    visited.add(current_node)
                    destinations = graph.nodes[current_node]
                    weight_to_current_node = shortest_paths[current_node][1]

                    for next_node in destinations:
                        weight = graph.nodes[current_node][next_node] + weight_to_current_node
                        if next_node not in shortest_paths:
                            shortest_paths[next_node] = (current_node, weight)
                        else:
                            current_shortest_weight = shortest_paths[next_node][1]
                            if current_shortest_weight > weight:
                                shortest_paths[next_node] = (current_node, weight)

                    next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
                    if not next_destinations:
                        return "Route Not Possible"

                    current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

                path = []
                while current_node is not None:
                    path.append(current_node)
                    next_node = shortest_paths[current_node][0]
                    current_node = next_node
                path = path[::-1]
                return path

            # Route class representing a potential route
            class Route:
                def __init__(self, stops, airports, aircraft, weather_data):
                    self.stops = stops
                    self.airports = airports
                    self.aircraft = aircraft
                    self.weather_data = weather_data

                def calculate_fitness(self):
                    total_distance = 0
                    total_fuel_consumption = 0

                    for i in range(len(self.stops) - 1):
                        start_airport = self.airports[self.stops[i]]
                        end_airport = self.airports[self.stops[i + 1]]

                        distance = haversine((start_airport.latitude, start_airport.longitude),
                                            (end_airport.latitude, end_airport.longitude))
                        total_distance += distance

                        if total_distance > self.aircraft.max_range:
                            return 0  # Route is not feasible for this aircraft

                        fuel_consumption = distance * self.aircraft.fuel_consumption
                        weather_at_start = self.weather_data.get(start_airport.city)
                        if weather_at_start and self.is_traveling_against_wind(start_airport, end_airport, weather_at_start['Wind Direction']):
                            fuel_consumption *= 1.20

                        total_fuel_consumption += fuel_consumption

                    return 1 / (total_distance + total_fuel_consumption) if total_fuel_consumption > 0 else 0

                def is_traveling_against_wind(self, start_airport, end_airport, wind_direction):
                    if wind_direction is None:
                        return False
                    travel_direction = self.calculate_direction(start_airport.latitude, start_airport.longitude,
                                                                end_airport.latitude, end_airport.longitude)
                    angle_diff = (wind_direction - travel_direction + 360) % 360
                    return 90 < angle_diff < 270

                def calculate_direction(self, lat1, lon1, lat2, lon2):
                    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
                    dLon = lon2 - lon1
                    y = math.sin(dLon) * math.cos(lat2)
                    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
                    bearing = math.atan2(y, x)
                    bearing = (math.degrees(bearing) + 360) % 360
                    return bearing

            # GeneticAlgorithm class
            class GeneticAlgorithm:
                def __init__(self, population_size, airports, aircraft, weather_data, graph):
                    self.population_size = population_size
                    self.airports = airports
                    self.aircraft = aircraft
                    self.weather_data = weather_data
                    self.graph = graph
                    self.population = self.initialize_population()

                def initialize_population(self):
                    routes = []
                    airport_codes = list(self.airports.keys())
                    segment_length = max(2, len(airport_codes) // 3)

                    for _ in range(self.population_size):
                        random.shuffle(airport_codes)
                        route = []
                        for i in range(0, len(airport_codes), segment_length):
                            segment = airport_codes[i:i + segment_length]
                            if len(segment) > 1:
                                dijkstra_route = dijkstra(self.graph, segment[0], segment[-1])
                                if dijkstra_route != "Route Not Possible":
                                    route.extend(dijkstra_route[:-1])
                        route.append(airport_codes[-1])
                        routes.append(Route(route, self.airports, self.aircraft, self.weather_data))

                    return routes

                def mutate(self, route):
                    mutated_route = list(route.stops)
                    mutation_type = random.choice(["shuffle", "insert", "delete"])

                    if mutation_type == "shuffle":
                        start_idx = random.randint(0, len(mutated_route) - 2)
                        end_idx = random.randint(start_idx + 1, len(mutated_route))
                        random.shuffle(mutated_route[start_idx:end_idx])

                    elif mutation_type == "insert":
                        insert_idx = random.randint(1, len(mutated_route) - 1)
                        new_stop = random.choice(list(set(self.airports.keys()) - set(mutated_route)))
                        mutated_route.insert(insert_idx, new_stop)

                    elif mutation_type == "delete":
                        if len(mutated_route) > 3:
                            delete_idx = random.randint(1, len(mutated_route) - 2)
                            del mutated_route[delete_idx]

                    return Route(mutated_route, route.airports, route.aircraft, route.weather_data)

                def evolve(self):
                    for _ in range(10):
                        new_population = []
                        for route in self.population:
                            mutated_route = self.mutate(route)
                            new_population.append(mutated_route)
                        self.population = new_population

            # Main function to run the route optimization
            def run_route_optimization_with_ui(source_city, destination_city, date):
                # Load datasets
                base_dir = os.path.dirname(os.path.abspath(__file__))

                aircraft_data = pd.read_csv(os.path.join(base_dir, 'aircraftDataset.csv'))
                weather_data = pd.read_csv(os.path.join(base_dir, 'weatherDataset.csv'))
                airport_data = pd.read_csv(os.path.join(base_dir, 'airportDataset.csv'))

                # Preprocess airport data to ensure latitude and longitude are in the correct range
                airport_data = preprocess_airport_data(airport_data)

                # Initialize airports
                airports = {row['City']: Airport(row['ICAOCODES'], row['Latitude'], row['Longitude'], row['City'])
                            for index, row in airport_data.iterrows()}


                # Initialize aircraft (example with the first aircraft in the dataset)
                aircraft = Aircraft(aircraft_data.iloc[0]['AircraftType'],
                                    aircraft_data.iloc[0]['MaxRange'],
                                    aircraft_data.iloc[0]['CruiseSpeed'],
                                    aircraft_data.iloc[0]['FuelConsumptionatCruise'])

                # Initialize graph with airports as nodes
                graph = Graph()
                for index, row in airport_data.iterrows():
                    from_airport = row['City']
                    for index2, row2 in airport_data.iterrows():
                        to_airport = row2['City']
                        if from_airport != to_airport:
                            distance = haversine((row['Latitude'], row['Longitude']), (row2['Latitude'], row2['Longitude']))
                            graph.add_edge(from_airport, to_airport, distance)

                # Prepare weather data for the given date
                weather_on_date = {row['City']: {'Wind Speed': row['Wind Speed'], 'Wind Direction': row['Wind Direction']}
                                for index, row in weather_data[weather_data['Date'] == date].iterrows()}

                # Run the Genetic Algorithm
                ga = GeneticAlgorithm(10, airports, aircraft, weather_on_date, graph)
                ga.evolve()

                # Select the best route
                best_route = max(ga.population, key=lambda route: route.calculate_fitness())

                
                # Print the best route
                print(f"Optimal Route on {date} from {source_city} to {destination_city}: {' -> '.join(best_route.stops)}")
                return (f"Optimal Route on {date} from {source_city} to {destination_city}: {' -> '.join(best_route.stops)}")

            # Example usage with user interface
            result = run_route_optimization_with_ui( SourceCity, DestinationCity, Date)
            return HttpResponse(result)
        else:
            return HttpResponse("SourceCity or DestinationCity is missing in the POST request")
    else:
        return HttpResponse("404 Not Found")
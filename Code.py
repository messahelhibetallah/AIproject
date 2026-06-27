import readfromjson as data
import random
import json
import sys
import time
import tracemalloc
import heapq
from collections import deque
from copy import deepcopy
from typing import List

# Class Definitions

class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.depth = 0 if parent is None else parent.depth + 1

    def __hash__(self):
        return hash(tuple((wilaya.name, tuple((crop.name, crop.production, crop.land_size) for crop in wilaya.crops)) for wilaya in self.state))

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        if len(self.state) != len(other.state):
            return False
        for wilaya_self, wilaya_other in zip(self.state, other.state):
            if wilaya_self.name != wilaya_other.name or len(wilaya_self.crops) != len(wilaya_other.crops):
                return False
            for crop_self, crop_other in zip(wilaya_self.crops, wilaya_other.crops):
                if crop_self.name != crop_other.name or crop_self.production != crop_other.production or crop_self.land_size != crop_other.land_size:
                    return False
        return True

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        return "state: %s parent: %s action: %s cost: %s" % (self.state, self.parent, self.action, self.cost)


class Crop:
    def __init__(self, name, production, land_size, price, Type, strategic=True, monthly_weather=None):
        self.name = name
        self.land_size = land_size
        self.production = production
        self.price = price
        self.type = Type
        self.strategic = strategic
        self.monthly_weather = monthly_weather

    def is_strategic(self):
        return self.strategic

    def __eq__(self, other):
        if not isinstance(other, Crop):
            return False
        return (self.name, self.production, self.land_size, self.price, self.type, self.strategic) == (other.name, other.production, other.land_size, other.price, other.type, other.strategic)

    def __hash__(self):
        return hash((self.name, self.production, self.land_size, self.price, self.type, self.strategic))

    def __str__(self):
        weather = ", ".join(str(w) for w in self.monthly_weather) if self.monthly_weather else "No monthly data"
        return "name: %s  production :%i  land size: %i price: %i Type: %s Strategic: %s Weather: [%s]" % (
            self.name, self.production, self.land_size, self.price, self.type, self.strategic, weather
        )


class Wilaya:
    def __init__(self, name, crops: List[Crop], land_size, monthly_weather):
        self.name = name
        self.crops = crops
        self.land_size = land_size
        self.monthly_weather = monthly_weather

    def get_total_production(self):
        return sum(crop.production for crop in self.crops)

    def add_crop(self, crop):
        self.crops.append(crop)

    def __str__(self):
        crop_details = ", ".join(str(crop) for crop in self.crops)
        return "name: %s crops: [%s] land_size: %i Weather: [%s]" % (
            self.name, crop_details, self.land_size, self.monthly_weather)


class Weather:
    def __init__(self, temperature, precipitation):
        self.temperature = temperature
        self.precipitation = precipitation

    def __str__(self):
        return "Temperature: %s°C, Precipitation: %smm" % (self.temperature, self.precipitation)


class AgricultureProblem:
    def __init__(self, products_consumption, state_transition_model, wilayas: List[Wilaya] = None, cost=0, actions=None):
        if wilayas is None:
            wilayas = []
        if actions is None:
            actions = ["swap", "decrease", "increase"]
        self.initial_state = wilayas
        self.products_consumption = products_consumption
        self.state_transition_model = state_transition_model
        self.actions = actions
        self.cost = cost

    def add_wilaya(self, wilaya):
        if wilaya not in self.initial_state:
            self.initial_state.append(wilaya)

    def get_crop_production(self, crop_name, state):
        crop_production = 0
        for wilaya in state:
            for crop in wilaya.crops:
                if crop.name == crop_name:
                    crop_production += crop.production
        return crop_production

    def goal_test(self, state):
        for crop_name, consumption in self.products_consumption.items():
            current_production = self.get_crop_production(crop_name, state)
            # print(f"Checking if production of {crop_name} ({current_production}) meets consumption ({consumption}).")
            if consumption > current_production:
                return False
            else:
                print(f"{crop_name} is sufficient with production {current_production}.")
        return True

    def expanding_nodes(self, node):
        successors = []
        random.seed()
        for i in range(3):
            random.shuffle(node.state)
            random.shuffle(node.state[i].crops)
            for crop in node.state[i].crops:
                index = random.randint(0, len(self.actions) - 1)
                action = self.actions[index]
                new_state = deepcopy(node.state)
                if action == "increase" or action == "decrease":
                    self.apply_action(new_state[i], action, None, crop.name, new_state)
                    if new_state == node.state:
                        print("action not applied")
                    else:
                        successors.append(Node(new_state, parent=node, action=action, cost=node.cost + 1))  # tarif de traspore
                else:
                    j = random.randint(0, len(node.state) - 1)
                    while j == i:
                        j = random.randint(0, len(node.state) - 1)
                    self.apply_action(new_state[i], action, new_state[j], crop.name, new_state)
                    successors.append(Node(new_state, parent=node, action=action, cost=node.cost + 1))
        return successors

    def apply_action(self, wilaya, action, other, crop_name, state):
        # print(f"Applying action {action} on crop {crop_name} in wilaya {wilaya.name}")
        action_applied = False
        if action == "decrease":
            for c in wilaya.crops:
                if c.name == crop_name:
                    land_decrease = c.land_size * 0.10
                    if c.land_size > land_decrease > 0 and self.self_sufficient(c.name, state):
                        old_production = c.production
                        c.production = c.production * (c.land_size - land_decrease) / c.land_size
                        if c.production != 0:
                            price = c.price * old_production / c.production + 1
                            if price != 0:
                                c.price = price
                        c.land_size -= land_decrease
                        action_applied = True
                        break
            if not action_applied:
                action = "increase"

        if action == "increase":
            for c in wilaya.crops:
                if c.name == crop_name and not self.self_sufficient(c.name, state) and c.land_size != 0:
                    land_increase = c.land_size * 0.30
                    old_production = c.production
                    # c.production = c.production * (c.land_size + land_increase) / c.land_size
                    c.production *= 1000000
                    if c.production != 0:
                        price = c.price * old_production / c.production - 1
                        if price != 0:
                            c.price = price
                    c.land_size += land_increase
                    action_applied = True
                    break

        if action == "swap":
            if not self.self_sufficient(crop_name, state):
                self.swap_crops(wilaya, other, crop_name)
                action_applied = True
        # print(f"Action {action} applied: {action_applied}")
        return

    def self_sufficient(self, crop_name, state):
        current_production = self.get_crop_production(crop_name, state)
        is_sufficient = self.products_consumption[crop_name] <= current_production
        return is_sufficient

    def swap_crops(self, wilaya, other, crop_name):
        swapped = False
        for crop in wilaya.crops:
            if crop.name == crop_name:
                for crop1 in other.crops:
                    if crop1.name == crop_name:
                        # print(f"Swapping {crop} from {wilaya.name} with {crop1} from {other.name}")
                        wilaya.crops.remove(crop)
                        other.crops.remove(crop1)
                        wilaya.crops.append(crop1)
                        other.crops.append(crop)
                        # print(f"Swapped {crop.name} between {wilaya.name} and {other.name}")
                        swapped = True
                        break
            if swapped:
                break
        if not swapped:
            print(f"Cannot swap {crop_name} between {wilaya.name} and {other.name}")

    def compare_weather(self, crop, wilaya, month):
        crop_weather = crop.monthly_weather[month]
        wilaya_weather = wilaya.monthly_weather[month]

        if crop_weather is None or wilaya_weather is None:
            return False

        wilaya_temp_lower = wilaya_weather["Temperature"] - 1
        wilaya_temp_upper = wilaya_weather["Temperature"] + 1
        wilaya_precip_lower = wilaya_weather["Precipitation"] - 10
        wilaya_precip_upper = wilaya_weather["Precipitation"] + 10

        if (wilaya_temp_lower <= crop_weather["temperature"] <= wilaya_temp_upper) and \
                (wilaya_precip_lower <= crop_weather["precipitation"] <= wilaya_precip_upper):
            return True
        else:
            return False

    def weather_heuristic(self, state):
        mismatch_count = 0
        month = 0
        for wilaya in state:
            for crop in wilaya.crops:
                if not self.compare_weather(crop, wilaya, month):
                    mismatch_count += 1
        return mismatch_count

# Search Algorithms

def dfs(problem: AgricultureProblem, max_depth=float('inf')):
    initial_node = Node(state=problem.initial_state, parent=None, action=["swap", "increase", "decrease"], cost=0)
    frontier = deque([initial_node])
    visited = set()

    while frontier:
        current_node = frontier.pop()
        print("the depth is : \n")
        print(current_node.depth, "......................................")
        if problem.goal_test(current_node.state):
            path_info = generate_path(current_node)
            path_states = [node['state'] for node in path_info]
            return path_states, current_node.cost, len(visited), current_node.depth
        if current_node.depth <= max_depth:
            visited.add(current_node)
            successors = problem.expanding_nodes(current_node)
            for child in successors:
                if child not in visited and all(child != node for node in frontier):
                    frontier.append(child)
        else:
            print("Reached max depth, not expanding further.")
            sys.exit(1)
    return None

def dls(problem: AgricultureProblem, max_depth):
    return dfs(problem, max_depth=max_depth)

def ids(problem: AgricultureProblem, depth):
    max_depth = 0
    solution = None

    while solution is None:
        solution = dfs(problem, max_depth=max_depth)
        if solution:
            break
        max_depth += 1
    return solution

def ida_star(problem: AgricultureProblem,max_iterations=3):
    initial_node = Node(state=problem.initial_state, parent=None, action=["swap", "increase", "decrease"], cost=0)
    bound = problem.weather_heuristic(initial_node.state)
    iterations = 0

    while True:
        if iterations >= max_iterations:
            print("Reached maximum iterations")
            return None
        print("iteration: ",iterations)
        result = ida_search(problem, initial_node, 0, bound)
        if isinstance(result, Node):
            path_info = generate_path(result)
            path_states = [node['state'] for node in path_info]
            return path_states, result.cost, bound, result.depth
        if result == float('inf'):
            return None
        bound = result
        iterations += 1

def ida_search(problem, node, g, bound):
    f = g + problem.weather_heuristic(node.state)
    if f > bound:
        return f
    if problem.goal_test(node.state):
        return node
    min_bound = float('inf')
    for child in problem.expanding_nodes(node):
        result = ida_search(problem, child, g + 1, bound)
        if isinstance(result, Node):
            return result
        if result < min_bound:
            min_bound = result
    return min_bound

def a_star(problem: AgricultureProblem, cost_limit=float('inf')):
    initial_node = Node(state=problem.initial_state, cost=0)
    frontier = []
    heapq.heappush(frontier, (problem.weather_heuristic(initial_node.state) + initial_node.cost, initial_node))
    explored = set()

    while frontier:
        _, current_node = heapq.heappop(frontier)
        if problem.goal_test(current_node.state):
            path_info = generate_path(current_node)
            path_states = [node['state'] for node in path_info]
            return path_states, current_node.cost, len(explored), current_node.depth
        
        explored.add(current_node)
        for neighbor in problem.expanding_nodes(current_node):
            total_cost = neighbor.cost + problem.weather_heuristic(neighbor.state)
            if neighbor not in explored and total_cost <= cost_limit:
                heapq.heappush(frontier, (total_cost, neighbor))

    return None

def hill_climbing(problem: AgricultureProblem, sample_size=100):
    initial_node = Node(state=problem.initial_state)
    current_node = initial_node
    visited = set()
    depth = 0

    while True:
        visited.add(current_node)
        neighbors = problem.expanding_nodes(current_node)
        neighbors = random.sample(neighbors, min(len(neighbors), sample_size))
        if not neighbors:
            break
        neighbor = max(neighbors, key=lambda node: evaluate_state(node.state))
        if evaluate_state(neighbor.state) <= evaluate_state(current_node.state):
            break
        current_node = neighbor
        depth = current_node.depth
        
    path_info = generate_path(current_node)
    path_states = [node['state'] for node in path_info]
    return path_states, current_node.cost, len(visited), depth

def stochastic_hill_climbing(problem: AgricultureProblem, iterations=3):
    initial_node = Node(state=problem.initial_state)
    current_node = initial_node
    visited = set()
    depth = 0

    for _ in range(iterations):
        visited.add(current_node)
        neighbors = problem.expanding_nodes(current_node)
        if not neighbors:
            break
        neighbor = random.choice(neighbors)
        if evaluate_state(neighbor.state) > evaluate_state(current_node.state):
            current_node = neighbor
            depth = current_node.depth
            
    path_info = generate_path(current_node)
    path_states = [node['state'] for node in path_info]
    return path_states, current_node.cost, len(visited), depth

def generate_path(node: Node):
    path = []
    while node:
        node_details = {
            "state": [str(wilaya) for wilaya in node.state],
            "action": node.action,
            "cost": node.cost,
            "depth": node.depth
        }
        path.append(node_details)
        node = node.parent
    path.reverse()
    return path

def evaluate_state(state):
    # Evaluation function: sum of the production of all crops
    return sum(wilaya.get_total_production() for wilaya in state)


def measure_time_and_space(algorithm, problem, *args):
    # Measure time
    start_time = time.time()
    # Measure space
    tracemalloc.start()
    result = algorithm(problem, *args)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time, current, peak

# Data Loading Functions

def load_consumption_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

def load_prices_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

def calculate_mean_price(data):
    mean_prices = {}
    for item in data['items']:
        name = item['name']
        prices = item['prices']
        mean_prices[name] = sum(prices) / len(prices)
    return mean_prices

def load_wilayas_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def load_crops_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    crops_data = {}
    for crop_info in data["crops"]:
        crop_name = crop_info["name"]
        temperature = crop_info["temperature"]
        precipitation = crop_info["precipitation"]
        crops_data[crop_name] = {"temperature": temperature, "precipitation": precipitation}
    
    return crops_data

def get_wilaya_weather(wilaya, month, wilayas_data):
    month_names = ["June", "August","December","February"]
    month_name = month_names[month]
    if wilaya in wilayas_data and month_name in wilayas_data[wilaya]:
        return wilayas_data[wilaya][month_name]
    else:
        print(f"No weather data for {wilaya} in {month_name}")  # Debug print
        return None

def get_crop_weather(crop, month, crops_data):
    month_names = ["June", "August","December","February"]
    month_name = month_names[month]
    if crop in crops_data and month_name in crops_data[crop]["precipitation"]:
        temperature = crops_data[crop]["temperature"]
        precipitation = crops_data[crop]["precipitation"][month_name]
        return {"temperature": temperature, "precipitation": precipitation}
    print(f"No weather data for {crop} in {month_name}")  # Debug print
    return None


def main():
    consumption_data = load_consumption_data("consumption.json")
    crop_data = data.structure_data()
    prices = load_prices_data("prices.json")
    mean_prices = calculate_mean_price(prices)
    land_size = data.wilaya_land_size()
    
    wilayas = [{"wilaya": land['name'], "land_size": land["size"]} for land in land_size]
    crops = [{"wilaya": element['wilaya_name'], "name": element['name'], "production": element['production'], "land_size": element['land_size'], "Type": element['type'], "strategic": True} for element in crop_data]

    # Load weather data
    wilayas_data = load_wilayas_data("wilayascondition.json")
    crops_data = load_crops_data("cropsconditions.json")

    wl = []
    for wilaya in wilayas:
        monthly_weather = [get_wilaya_weather(wilaya['wilaya'], month, wilayas_data) for month in range(4)]
        
        cr = [Crop(name=crop['name'], production=crop['production'], land_size=crop['land_size'], price=mean_prices[crop['name']], Type=crop['Type'], strategic=True, monthly_weather=[get_crop_weather(crop['name'], month, crops_data) for month in range(4)]) for crop in crops if crop['wilaya'] == wilaya['wilaya']]
        
        wl.append(Wilaya(name=wilaya['wilaya'], crops=cr, land_size=wilaya['land_size'], monthly_weather=monthly_weather))

    problem = AgricultureProblem(
        products_consumption=consumption_data,
        state_transition_model=None,
        wilayas=wl,
        actions=["increase", "swap", "decrease"]
    )

    initial_node = Node(state=problem.initial_state, parent=None, action=["swap", "increase", "decrease"], cost=0)



    print("Measuring time and space for Hill Climbing:")
    hill_climbing_result, hill_climbing_time, current_memory, peak_memory = measure_time_and_space(hill_climbing, problem, 100)
    if hill_climbing_result:
        path, cost, visited, depth = hill_climbing_result
        print("Final Result:")
        #print(f"Path: {path}")
        print(f"Cost: {cost}, Visited: {visited}, Depth: {depth}")
        print(f"Hill Climbing Time Taken: {hill_climbing_time} seconds")
        print(f"Current memory usage: {current_memory / 1024:.2f} KB; Peak: {peak_memory / 1024:.2f} KB")
    else:
        print("No solution found.")
            
    print("Measuring time and space for Stochastic Hill Climbing:")
    stochastic_hill_climbing_result, stochastic_hill_climbing_time, current_memory, peak_memory = measure_time_and_space(stochastic_hill_climbing, problem, 30)
    if stochastic_hill_climbing_result:
        path, cost, visited, depth = stochastic_hill_climbing_result
        print("Final Result:")
        #print(f"Path: {path}")
        print(f"Cost: {cost}, Visited: {visited}, Depth: {depth}")
        print(f"IDA* Time Taken: {stochastic_hill_climbing_time} seconds")
        print(f"Current memory usage: {current_memory / 1024:.2f} KB; Peak: {peak_memory / 1024:.2f} KB")
    else:
        print("No solution found.")
        

    print("Measuring time and space for DLS:")
    dls_result, dls_time, current_memory, peak_memory = measure_time_and_space(dls, problem, 30)
    if dls_result:
        path, cost, visited, depth = dls_result
        print("Final Result:")
        #print(f"Path: {path}")
        print(f"Cost: {cost}, Visited: {visited}, Depth: {depth}")
        print(f"DLS Time Taken: {dls_time} seconds")
        print(f"Current memory usage: {current_memory / 1024:.2f} KB; Peak: {peak_memory / 1024:.2f} KB")
    else:
        print("No solution found.")
        
    print("Measuring time and space for IDA* Search:")
    ida_star_result, ida_star_time, current_memory, peak_memory = measure_time_and_space(ida_star, problem)
    if ida_star_result:
        path, cost, visited, depth = ida_star_result
        print("Final Result:")
        #print(f"Path: {path}")
        print(f"Cost: {cost}")
        #print(f"Visited: {visited}")
        print(f"Depth: {depth}")
        print(f"IDA* Time Taken: {ida_star_time} seconds")
        print(f"Current memory usage: {current_memory / 1024:.2f} KB; Peak: {peak_memory / 1024:.2f} KB")
    else:
        print("No solution found.")
        
        
    print("Measuring time and space for DFS:")
    dfs_result, dfs_time, current_memory, peak_memory = measure_time_and_space(dfs, problem)
    if dfs_result:
        path, cost, visited, depth = dfs_result
        print("Final Result:")
        #print(f"Path: {path}")
        print(f"Cost: {cost}, Visited: {visited}, Depth: {depth}")
        print(f"DFS Time Taken: {dfs_time} seconds")
        print(f"Current memory usage: {current_memory / 1024:.2f} KB; Peak: {peak_memory / 1024:.2f} KB")
    else:
        print("No solution found.")    
        
        
    
        

if __name__ == "__main__":
    main()

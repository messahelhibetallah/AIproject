import random
from collections import deque
from copy import deepcopy
from typing import List, Optional


class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.depth = 0 if parent is None else parent.depth + 1

    def __hash__(self):
        return hash(tuple(self.state))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __str__(self):
        return f"Node(state={self.state}, depth={self.depth})"


class Crop:
    def __init__(self, name, production, land_size, price, Type, strategic=True):
        self.name = name
        self.land_size = land_size
        self.production = production
        self.price = price
        self.type = Type
        self.strategic = strategic

    def is_strategic(self):
        return self.strategic

    def __str__(self):
        return f"Crop(name={self.name}, production={self.production}, land_size={self.land_size}, price={self.price}, type={self.type}, strategic={self.strategic})"


class Wilaya:
    def __init__(self, name, crops: List[Crop], land_size, weather_conditions):
        self.name = name
        self.crops = crops
        self.land_size =land_size
        self.weather_conditions =weather_conditions

    def get_total_production(self):
        return sum(crop.production for crop in self.crops)

    def add_crop(self, crop):
        self.crops.append(crop)

    def __str__(self):  # Providing a more useful string representation
        return f"Wilaya(name={self.name}, crops={self.crops}, land_size={self.land_size}, weather_conditions={self.weather_conditions})"


class AgricultureProblem:
    def __init__(self, products_consumption, state_transition_model, wilayas:List[Wilaya]=None, cost=0,actions=None):
        if wilayas is None:
            wilayas = []
        if actions is None:
            actions = ["swap","decrease","increase"]
        self.initial_state =wilayas
        self.products_consumption =products_consumption
        self.state_transition_model =state_transition_model
        self.actions =actions
        self.cost =cost

    def add_wilaya(self, wilaya):
        if wilaya not in self.initial_state:
            self.initial_state.append(wilaya)

    def get_total_crop_production(self,state):
        total_production = 0
        for wilaya in state:
            total_production += wilaya.get_total_production()
        return total_production

    def get_crop_production(self, crop_name,state):
        crop_production = 0
        for wilaya in state:
            for crop in wilaya.crops:
                if crop.name == crop_name:
                    crop_production += crop.production
        return crop_production

    def goal_test(self, state):
        for crop_name, consumption in self.products_consumption.items():
            print(f"Checking if production of {crop_name} ({self.get_crop_production(crop_name,state)}) meets consumption ({consumption}).")
            if consumption > self.get_crop_production(crop_name,state):
                return False
            else:
                print(f"{crop_name} is done!!!! Don't touch it!!")
        print("allll is done!!!!!!")        
        return True


    def expanding_nodes(self,node):
         successors=[]
         random.seed()
         for i in range(len(node.state)):
            random.shuffle(node.state[i].crops)
            for crop in node.state[i].crops:                
                index=random.randint(0,len(self.actions)-1)
                action=self.actions[index]
                new_state=deepcopy(node.state) 
                if action=="increase" or action=="decrease" :
                    self.apply_action(new_state[i],action,None,crop.name,new_state)
                    if new_state==node.state:
                        print("action not applied")
                    else:
                        successors.append(Node(new_state,parent=node,action=action,cost=node.cost+1)) #tarif de traspore
                else:
                    j=random.randint(0,len(node.state)-1)
                    while j==i:
                        
                        j=random.randint(0,len(node.state)-1)
                    self.apply_action(new_state[i],action,new_state[j],crop.name,new_state)
                    successors.append(Node(new_state,parent=node,action=action,cost=node.cost+1))
                             
         return successors              
                         


    def apply_action(self, wilaya, action, other, crop_name,state):
        action_applied = False
        if action == "increase":
            for c in wilaya.crops:
                if c.name == crop_name and not self.self_sufficient(c.name,state) :  # Ensure there's land to increase
                    land_increase = c.land_size * 0.10  # Example: Increase by 10%                    
                    c.production=c.production*(c.land_size+land_increase)/c.land_size
                    c.land_size += land_increase
                    action_applied = True
                    print("::::::::::::::::::::::::::")
                    break  # Exit after applying the action
            if not action_applied:
                print(f"we could not increase {crop_name}.")

        elif action == "decrease":
            for c in wilaya.crops:
                land_decrease = c.land_size * 0.10  # Decrease by 10%
                if c.name == crop_name and c.land_size >land_decrease and self.self_sufficient(c.name,state):
                    c.production=c.production*(c.land_size-land_decrease)/c.land_size
                    c.land_size -= land_decrease
                    action_applied = True
                    break
            if not action_applied:
                print(f"we could not decrease {crop_name}.")
        else:
            if not self.self_sufficient(crop_name,state):
                self.swap_crops(wilaya,other,crop_name)


    def self_sufficient(self,crop__name,state):
        for crop_name, consumption in self.products_consumption.items():
            if crop_name==crop__name: 
                if consumption > self.get_crop_production(crop_name,state):
                    return False
                else:
                    return True
            
  
    
    def swap_crops(self, wilaya, other, crop_name):
        swapped=False
        for crop in wilaya.crops:
            for crop1 in other.crops:
                if crop.name==crop_name and crop1.name==crop_name:
                    wilaya_crop=deepcopy(crop)
                    other_crop=deepcopy(crop1)
                    wilaya.crops.remove(crop)
                    other.crops.remove(crop1)
                    wilaya.crops.append(other_crop)
                    other.crops.append(wilaya_crop)
                    swapped=True
                    break
            if swapped:
                break
        if not swapped:
            print(f"we can't swap the crops between {wilaya.name} and {other.name}")                
                    


def dfs(problem: AgricultureProblem, max_depth=None):
    initial_node = Node(state=problem.initial_state, parent=None,action=["swap", "increase", "decrease"],cost=0)
    frontier = deque([initial_node])
    visited = set()

    while frontier:
        current_node = frontier.pop()
        if problem.goal_test(current_node.state):
            return (
                [node.state for node in generate_path(current_node)], current_node.cost, len(visited),
                current_node.depth)
            break
        if max_depth is None or current_node.depth < max_depth:
            visited.add(current_node)
            for child in problem.expanding_nodes(current_node):
                if child not in visited and all(child != node for node in frontier):
                    frontier.append(child)
    return None


def generate_path(node):
    path = []
    while node:
        path.append(node)
        node = node.parent
    return list(reversed(path))


def dls(problem: AgricultureProblem, max_depth):
    return dfs(problem, max_depth=max_depth)


def ids(problem: AgricultureProblem):
    max_depth = 0
    solution = None

    while solution is None:
        solution = dfs(problem, max_depth=max_depth)
        if solution:
            break
        max_depth += 1
    return solution


def main():
    crops1 = [
        Crop(name="olives", production=800, land_size=800, price=15, Type="vegetables", strategic=True),
        Crop(name="peach", production=500, land_size=600, price=10, Type="fruits", strategic=False),
        Crop(name="Wheat", production=1000, land_size=500, price=20, Type="Grain", strategic=True),
       
        Crop(name="Corn", production=100, land_size=400, price=5, Type="Grain", strategic=True)
    ]

    crops2 = [
        
        Crop(name="Wheat", production=500, land_size=500, price=20, Type="Grain", strategic=True),
        Crop(name="olives", production=567, land_size=800, price=15, Type="vegetables", strategic=True),
        Crop(name="peach", production=530, land_size=600, price=10, Type="fruits", strategic=False),
        Crop(name="Corn", production=234, land_size=400, price=5, Type="Grain", strategic=True)
    ]

    crops3 = [
        
        Crop(name="Wheat", production=2345, land_size=500, price=20, Type="Grain", strategic=True),
        Crop(name="olives", production=3000, land_size=800, price=15, Type="vegetables", strategic=True),
        Crop(name="peach", production=345, land_size=600, price=10, Type="fruits", strategic=False),
     
        Crop(name="Corn", production=234, land_size=400, price=5, Type="Grain", strategic=True)
    ]

    crops4 = [
        Crop(name="olives", production=678, land_size=800, price=15, Type="vegetables", strategic=True),
        Crop(name="Wheat", production=6788, land_size=500, price=20, Type="Grain", strategic=True),
   
        Crop(name="peach", production=5678, land_size=600, price=10, Type="fruits", strategic=False),
        Crop(name="Corn", production=3456, land_size=400, price=5, Type="Grain", strategic=True)
       
    ]

    wilayas = [
        Wilaya(name="Algiers", crops=crops1, land_size=1000, weather_conditions="Favorable"),
        Wilaya(name="Oran", crops=crops2, land_size=1000, weather_conditions="Favorable"),
        Wilaya(name="Msila", crops=crops3, land_size=1000, weather_conditions="Favorable"),
        Wilaya(name="Mila", crops=crops4, land_size=1000, weather_conditions="Favorable")
    ]

    problem = AgricultureProblem(
        products_consumption={ "Corn": 4000,"Wheat": 9000, "olives": 5087, "peach": 3300},
        state_transition_model=None,  # Assuming you define this elsewhere
        wilayas=wilayas,
        actions=[ "swap","decrease","increase"]
    )

    dfs_result = dfs(problem)
    if dfs_result:
        print("DFS Result:", dfs_result)

    dls_result = dls(problem, max_depth=3)
    if dls_result:
        print("DLS Result:", dls_result)

    ids_result = ids(problem)
    if ids_result:
        print("IDS Result:", ids_result)


if __name__ == "__main__":
    main()

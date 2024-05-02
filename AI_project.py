import random
#hello guys

class agriculture_problem:
    def __init__(self,products_consumption,state_transition_model,wilayas=[],cost=0,actions={}):
        self.initial_state=wilayas
        self.products_consumption=products_consumption
        self.state_transition_model = state_transition_model
        self.actions=actions
        self.cost=cost

        
  #actions are swap,minimize,maximize
      
        def add_wilaya(self,wilaya):
            if wilaya not in self.initial_state:
                self.initial_state.append(wilaya)
            
        def get_total_crop_production(self):
            total_production = 0
            for wilaya in self.initial_state:
                total_production += wilaya.get_total_production()
            return total_production 
        
        def get_crop_production(self,crop):
            crop_production=0
            for wilaya in self.initial_state:
                 for crop in wilaya.crops:
                     if crop.name==crop:
                         crop_production+=crop.production
                     else:
                         continue
                     
        
        def goal_test(self, state):
                for crop,consumption in  self.products_consumption.items():
                    if consumption <=self.get_crop_production(crop):  #test self suffieciency
                        continue
                    else:
                        return False
                return True     
          
   
    def expanding_nodes(self,node):
        successors=[]
        for action in self.actions:
            for i in range(0,48):
                for crop in node.wilayas[i].crops:
                    new_state=node.state
                    if action=="increase" or action=="increase" :
                        self.apply_action(new_state.initial_state[i],action,None,crop)
                        if new_state==node.state:
                            continue
                        else:
                            successors.append(Node(new_state,parent=node, action=action,cost=node.cost+1))
                                        
                    else:
                        index=random.randint(0,48)
                        while index==i:
                            index=random.randint(1,49)
                        second_state=node.state 
                        self.apply_action(new_state.initial_state[i],action,second_state.initial_state[index],crop)
                        successors.append(Node(new_state,parent=node, action=action,cost=node.cost+1))
                        successors.append(Node(second_state,parent=node,action=action,cost=node.cost+1))
                        
                        
                    
    # if self.evaluate_meteo(crop.whether_conditions)==self.evaluate_meteo(node.state[i].whether_conditions): #returns true or false        
    
    def apply_action(self,wilaya,action,other,crop):
        land=0
        if action =='increase':
            for crop in wilaya.crops:
                if crop==crop:
                    land=crop.land_size/10
                    crop.land_size+=crop.land_size/10 
            for crop1 in wilaya.crops:
                if crop1.is_strategic()==False and crop1!=crop and crop1.land_size!=0:
                    crop1.land_size-=land       
                    
        elif action == 'decrease':
            for crop in wilaya.crops:
                if crop==crop and crop.land_size>0:
                    land=crop.land_size/10
                    crop.land_size-=crop.land_size/10
            for crop1 in wilaya.crops:
                if crop1.is_strategic()==True and crop1!=crop:
                    crop1.land_size+=land          
                else:
                    if crop.land_size==0:
                        wilaya.crops.remove(crop)

        else:
            if crop not in other.crops: 
                pass
            else:
                self.swap_crops(wilaya,other,crop)    
                


    def swap_crops(self,wilaya,other,crop):
        for crop1 in other.crops:
            if crop1==crop:
                temp=crop1
                other.crops.remove(crop1)
                other.crops.append(crop)
                wilaya.crops.remove(crop)
                wilaya.crops.append(temp)
            else:
                continue
    
    #return successors  
     
        def evaluate_meteo(self,whether): #temp
            return True
        
        def  get_better_wilaya(self,crop):
            return 1


#____________________________________________________________
class wilaya:
    def __init__(self,name,crops,land_size,whether_conditions):
        self.name=name
        self.crops=crops
        self.land_size=land_size
        self.whether_conditions=whether_conditions
        
    def get_total_production(self):
        total_production=0
        for crop in self.crops:
             total_production+=crop.production
        return total_production
    
    def add_crop(self,crop):
        self.crops.append(crop)
    
    
           
#____________________________________________________________
class crop:
    def __init__(self,name,production,land_size,price,Type,strategic=True):
        self.name=name
        self.land_size=land_size
        self.production=production
        self.price=price
        self.type=Type
        self.strategic=strategic #yes or no
        
    def if_strategic(self):
        return self.strategic=="yes"
 
       
        
class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent # node
        self.action = action # action performed to get to this node
        self.cost = cost # (incremented with each newly expanded node)
        if parent is None: #root node
            self.depth = 0 # level in the graph 0 for the root node
        else:
            self.depth = parent.depth + 1 # parent level + 1
    def __hash__(self):
        return hash(tuple(map(tuple, self.state))) #why??????
       
    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state
    def __gt__(self, other):
        pass #to be done        
        
        
        
        
        
        
        

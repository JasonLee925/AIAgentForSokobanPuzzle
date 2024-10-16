'''
IFN680 Sokoban Assignment

The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

You are not allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the 
interface and triggers to a fail for the test of your code.
'''


import search
import sokoban
import time
from enum import Enum

    
def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    e.g.  [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    '''

    raise NotImplementedError()


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell inside a warehouse is 
    called 'taboo' if whenever a box get pushed on such a cell then the puzzle 
    becomes unsolvable.  
    When determining the taboo cells, you must ignore all the existing boxes, 
    simply consider the walls and the target cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner inside the warehouse and not a target, 
             then it is a taboo cell.
     Rule 2: all the cells between two corners inside the warehouse along a 
             wall are taboo if none of these cells is a target.
    
    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with 
       an '#' and the taboo cells marked with an 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    
    # find taboos 🚷
    solver = SokobanPuzzle(warehouse)
    taboo_cells = solver.find_taboo_cells()
    
    # draw the new puzzle in string presentation 
    string_rep_puzzle = ""
    x = 0
    y = 0
    for cell in str(warehouse):
        if cell == "\n":
            y += 1
            x = 0
            string_rep_puzzle += cell
            continue # skip one cell cause the puzzle has a space gap in every fisrt line
    
        if (x, y) in taboo_cells:
            cell = "X"
        
        # TEST: mark inner cells
        # if (x, y) in inner_cells:
        #     cell = "❤️"
        
        if cell not in [" ", "#", "X", "❤️"]:
            cell = " "

        string_rep_puzzle += cell
        x += 1
    
    # print(string_rep_puzzle)
    return string_rep_puzzle
      

class EAction(Enum):
    Up = ((0,-1), (0, -2))
    Down = ((0,1), (0,2))
    Right = ((1,0), (2,0))
    Left = ((-1,0), (-2,0))
    
    def get_next_coordinates(self, x, y):
        '''
        This funciton returns the next two coordinates based on the action.
        
        Example 1:
            If EAction.Up.get_next_coordinates(x,y), 
            it returns (x,y-1) and (x,y-2)
            
        Example 2:
            If EAction.Right.get_next_coordinates(x,y), 
            it returns (x+1,y) and (x+2,y)
            
        Return:
            - coord1: a coordinate of 1 step from (x,y) towards the direction (action) 
            - coord2: a coordinate of 2 steps from (x,y) towards the direction (action) 
        '''
        one_step = self.value[0]
        two_steps = self.value[1]
        coord1 = (x + one_step[0], y + one_step[1])
        coord2 = (x + two_steps[0], y + two_steps[1])
        return coord1, coord2
    
    
class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. It uses search.Problem as a sub-class. 
    That means, it should have a:
    - self.actions() function
    - self.result() function
    - self.goal_test() function
    See the Problem class in search.py for more details on these functions.
    
    Each instance should have at least the following attributes:
    - self.allow_taboo_push
    - self.macro
    
    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.
    
    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.
    '''
    
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.initial = tuple(self.warehouse.worker), tuple(self.warehouse.boxes) 
        self.taboo_cells = self.find_taboo_cells()
        
        self.allow_taboo_push = False
        self.marco = True
    
    def find_taboo_cells(self): 
        # find the boundaries of the maze
        min_x = min ([x for x,y in self.warehouse.walls])
        max_x = max ([x for x,y in self.warehouse.walls])
        min_y = min ([y for x,y in self.warehouse.walls])
        max_y = max ([y for x,y in self.warehouse.walls])

        # 1. find corners 
        corners = []
        for y in range(max_y+1):
            for x in range(max_x+1): 
                if (x, y) not in set(self.warehouse.walls + self.warehouse.targets):
                    if( ((x-1,y) in self.warehouse.walls and (x,y-1) in self.warehouse.walls) or 
                        ((x-1,y) in self.warehouse.walls and (x,y+1) in self.warehouse.walls) or
                        ((x+1,y) in self.warehouse.walls and (x,y-1) in self.warehouse.walls) or
                        ((x+1,y) in self.warehouse.walls and (x,y+1) in self.warehouse.walls)
                    ):
                        corners.append((x,y))

        # 2. find inner space
        inner_cells = []
        y_cells = []            
        x_cells = []

        for y in range(max_y + 1): # horizontally find cells between min and max wall's coordinates
            min_x_row = min(_x for _x, _y in self.warehouse.walls if y == _y)
            max_x_row = max(_x for _x, _y in self.warehouse.walls if y == _y)
            for x in range(min_x_row + 1, max_x_row):
                cc = (x,y) # checking cell
                if cc not in self.warehouse.walls:
                    x_cells.append(cc)

        for x in range(max_x + 1): # vertically find cells between min and max wall's coordinates
            min_y_row = min(_y for _x, _y in self.warehouse.walls if x == _x)
            max_y_row = max(_y for _x, _y in self.warehouse.walls if x == _x)
            for y in range(min_y_row + 1, max_y_row):
                cc = (x,y) # checking cell
                if cc not in self.warehouse.walls:
                    y_cells.append(cc)

        inner_cells = set(x_cells) & set(y_cells)     


        # 3. find taboos      
        taboo_cells = []
        for corner in corners:
            if corner in inner_cells:
                taboo_cells.append(corner)
                
        return taboo_cells

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        
        (x, y), _ = state
        
        action_list = []
        
        if self.check_legal_move(state, *EAction.Left.get_next_coordinates(x,y)):
            action_list += ['Left']

        if self.check_legal_move(state, *EAction.Up.get_next_coordinates(x,y)):
            action_list += ['Up']

        if self.check_legal_move(state, *EAction.Right.get_next_coordinates(x,y)):
            action_list += ['Right']

        if self.check_legal_move(state, *EAction.Down.get_next_coordinates(x,y)):
            action_list += ['Down']
        
        return action_list
        
    def check_legal_move(self, state, coord1, coord2):
        
        _, box_coords = state
        box_coords = list(box_coords)
        if coord1 in self.warehouse.walls: # bumps into a wall
            return False
        
        if coord1 in box_coords: # bumps into a box 
            if coord2 in set(self.warehouse.walls + box_coords):
                return False 
            if coord2 in self.taboo_cells:
                return False
            
        return True
        
    def result(self, state, action):
        
        (x, y), box_coords = state
        coord1, coord2 = (x,y), (x,y) 
        for e_action in EAction:
             if action == e_action.name:
                coord1, coord2 = e_action.get_next_coordinates(x,y)
                         
                box_coords = list(box_coords)
                
                if coord1 in box_coords: # bumps into a box 
                    box_idx = box_coords.index(coord1) # box index
                    box_coords[box_idx] = coord2 # update box coord
                    
                break
            
        return tuple(coord1), tuple(box_coords)
    
    def goal_test(self, state):
        _, box_coords = state
        return set(box_coords) == set(self.warehouse.targets)
              
    def h(self, state):
        # (x, y), box_coords = state
        h_box = 0
        h_worker = 0
        worker_coord = state.state[0]
        min_worker_distance = None
        for box_coord in state.state[1]:
            worker_distance = self.find_manhattan(box_coord, worker_coord)
            if min_worker_distance == None or worker_distance < min_worker_distance:
                min_worker_distance = worker_distance
            min_box_distance = None                
            for target_coord in self.warehouse.targets:
                box_distance = self.find_manhattan(box_coord, target_coord)
                if min_box_distance == None or box_distance < min_box_distance:
                    min_box_distance = box_distance
            h_box+= min_box_distance 
        h_worker = min_worker_distance

        return h_worker + h_box
    
    def find_manhattan(self, p1, p2):
        return sum(abs(sum1-sum2) for sum1, sum2 in zip(p1,p2))
    
    def print_solution(self, goal_node):
        path = goal_node.path()
        
        print( f"Solution takes {len(path)-1} steps from the initial state to the goal state\n")
        # print( "Below is the sequence of moves\n")
        moves = []
        for node in path:
            if node.action:
                moves += [f"{node.action}"]
       
        return moves
        

#### ---------- ####
 
def check_action_seq_update_wh (warehouse, action_seq, coord1, coord2):
    '''
    @param coord1: a coordinate of "one" step from the original coordinate
    @param coord2: a coordinate of "two" steps from the original coordinate
    '''
    if coord1 in warehouse.walls:
            return 'Failure'
        
    if coord1 in warehouse.boxes: 
        if coord2 in set(warehouse.walls + warehouse.boxes):
            return 'Failure'
        box_idx = warehouse.boxes.index(coord1) # box index
        warehouse.boxes[box_idx] = coord2 # update box

    warehouse.worker = tuple(coord1) # update worker
    return check_action_seq(warehouse, action_seq)

def check_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall, or walk into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    wh = warehouse.copy()
    x, y = wh.worker
    
    if not action_seq:
        return wh.__str__()
        
    action = action_seq.pop(0)
    for e_action in EAction:
        if action == e_action.name:
            coord1, coord2 = e_action.get_next_coordinates(x,y)
            return check_action_seq_update_wh(wh, action_seq, coord1, coord2)
        
    return wh.__str__()


def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using elementary actions 
    the puzzle defined in a file.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    solver = SokobanPuzzle(warehouse)
    t0 = time.time()
    sol_ts = search.breadth_first_graph_search(solver)
    # sol_ts = search.astar_graph_search(solver)
    t1 = time.time()

    print (f"Solver took {1000*(t1-t0):.2f} milli-seconds to find a solution.")
    if sol_ts == None:
        return "Impossible"

    return solver.print_solution(sol_ts)


def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

def solve_sokoban_macro(warehouse):
    '''    
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

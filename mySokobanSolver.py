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
    # find the boundaries of the maze
    min_x = min ([x for x,y in warehouse.walls])
    max_x = max ([x for x,y in warehouse.walls])
    min_y = min ([y for x,y in warehouse.walls])
    max_y = max ([y for x,y in warehouse.walls])
    
    # 1. find corners 
    corners = []
    for y in range(max_y+1):
        for x in range(max_x+1): 
            if (x, y) not in set(warehouse.walls + warehouse.targets):
                if( ((x-1,y) in warehouse.walls and (x,y-1) in warehouse.walls) or 
                    ((x-1,y) in warehouse.walls and (x,y+1) in warehouse.walls) or
                    ((x+1,y) in warehouse.walls and (x,y-1) in warehouse.walls) or
                    ((x+1,y) in warehouse.walls and (x,y+1) in warehouse.walls)
                ):
                    corners.append((x,y))
    
    # 2. find inner space
    inner_cells = []
    y_cells = []            
    x_cells = []
    
    for y in range(max_y + 1): # horizontally find cells between min and max wall's coordinates
        min_x_row = min(_x for _x, _y in warehouse.walls if y == _y)
        max_x_row = max(_x for _x, _y in warehouse.walls if y == _y)
        for x in range(min_x_row + 1, max_x_row):
            cc = (x,y) # checking cell
            if cc not in warehouse.walls:
                x_cells.append(cc)
    
    for x in range(max_x + 1): # vertically find cells between min and max wall's coordinates
        min_y_row = min(_y for _x, _y in warehouse.walls if x == _x)
        max_y_row = max(_y for _x, _y in warehouse.walls if x == _x)
        for y in range(min_y_row + 1, max_y_row):
            cc = (x,y) # checking cell
            if cc not in warehouse.walls:
                y_cells.append(cc)
           
    inner_cells = set(x_cells) & set(y_cells)     
                
                
    # 3. find taboos      
    taboo_cells = []
    for corner in corners:
        if corner in inner_cells:
            taboo_cells.append(corner)
    
    
    # 4. draw the new puzzle in string presentation
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
    
    
    
    print(string_rep_puzzle)
    return string_rep_puzzle
      
    

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
        raise NotImplementedError()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        raise NotImplementedError


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
    # wallsAndBoxes = set(wh.walls + wh.boxes)
    
    if not action_seq:
        return wh.__str__()
        
    action = action_seq.pop(0)
    if action == "Left":
        return check_action_seq_update_wh(wh, action_seq, (x-1,y), (x-2,y))
    elif action == "Right":
        return check_action_seq_update_wh(wh, action_seq, (x+1,y), (x+2,y))
    elif action == "Up":
        return check_action_seq_update_wh(wh, action_seq, (x,y-1), (x,y-2))
    elif action == "Down":
        return check_action_seq_update_wh(wh, action_seq, (x,y+1), (x,y+2))
        
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
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    
    # Convert (y, x) format to (x, y) format for internal use
    start = (warehouse.worker[1], warehouse.worker[0])  # (row, col) to (x, y)
    dst = (dst[1], dst[0])  # (row, col) to (x, y)

    # Obstacles remain in (x, y) format
    obstacles = set((x, y) for x, y in warehouse.walls + warehouse.boxes)
    visited = set()
    queue = deque([start])

    if dst in obstacles:
        return False

    # Dynamically calculate the grid dimensions from the walls
    max_x = max(x for x, y in warehouse.walls)  # maximum column index (width)
    max_y = max(y for x, y in warehouse.walls)  # maximum row index (height)

    # BFS search
    while queue:
        current = queue.popleft()

        if current == dst:
            return True
        
        if current in visited:
            continue
        
        visited.add(current)
        
        # Left, Right, Up, Down (using x, y format)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (current[0] + dx, current[1] + dy)
            
            # Ensure the next position is within grid bounds
            if not (0 <= next_pos[0] <= max_x and 0 <= next_pos[1] <= max_y):
                continue
            
            # Check if the position is not an obstacle and hasn't been visited
            if next_pos not in obstacles and next_pos not in visited:
                queue.append(next_pos)

    return False

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


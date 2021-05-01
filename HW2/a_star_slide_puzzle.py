# A General A* Function and its Application to Slide Puzzles
# CS 470/670 at UMass Boston

import numpy as np

example_1_start = np.array([[2, 8, 3],
                           [1, 6, 4],
                           [7, 0, 5]])

example_1_goal = np.array([[1, 2, 3],
                           [8, 0, 4],
                           [7, 6, 5]])

example_2_start = np.array([[ 2,  6,  4,  8],
                            [ 5, 11,  3, 12],
                            [ 7,  0,  1, 15],
                            [10,  9, 13, 14]])

example_2_goal = np.array([[ 1,  2,  3,  4],
                           [ 5,  6,  7,  8],
                           [ 9, 10, 11, 12],
                           [13, 14, 15,  0]])

class Node:
    def __init__(self, state, prevState=None):
        self.g = 0
        self.h = 0
        self.state = state
        self.prevState = prevState

def isGoal(state, otherState):
    # Apparently np has an array_equal function
    return np.array_equal(state.state, otherState.state)


# For a given current state, move, and goal, compute the new state and its h'-score and return them as a pair. 
def make_node(state, row_from, col_from, row_to, col_to, goal):
    # Create the new state that results from playing the current move. 
    (height, width) = state.shape
    new_state = np.copy(state)
    new_state[row_to, col_to] = new_state[row_from, col_from]
    new_state[row_from, col_from] = 0
    
    # Count the mismatched numbers and use this value as the h'-score (estimated number of moves needed to reach the goal).
    mismatch_count = 0
    for i in range(height):
        for j in range(width):
            if new_state[i, j] > 0 and new_state[i, j] != goal[i, j]:
                mismatch_count += 1
   
    return (new_state, mismatch_count)

# For given current state and goal state, create all states that can be reached from the current state
# (i.e., expand the current node in the search tree) and return a list that contains a pair (state, h'-score)
# for each of these states.   
def slide_expand(state, goal):
    node_list = []
    (height, width) = state.shape
    (empty_row, empty_col) = np.argwhere(state == 0)[0]     # Find the position of the empty tile
    
    # Based on the position of the empty tile, find all possible moves and add a pair (new_state, h'-score)
    # for each of them.
    if empty_row > 0:
        node_list.append(make_node(state, empty_row - 1, empty_col, empty_row, empty_col, goal))
    if empty_row < height - 1:
        node_list.append(make_node(state, empty_row + 1, empty_col, empty_row, empty_col, goal))
    if empty_col > 0:
        node_list.append(make_node(state, empty_row, empty_col - 1, empty_row, empty_col, goal))
    if empty_col < width - 1:
        node_list.append(make_node(state, empty_row, empty_col + 1, empty_row, empty_col, goal))
    
    return node_list

#Copy of the improve
def make_node_improve(state, row_from, col_from, row_to, col_to, goal):
    # Create the new state that results from playing the current move.
    (height, width) = state.shape
    new_state = np.copy(state)
    new_state[row_to, col_to] = new_state[row_from, col_from]
    new_state[row_from, col_from] = 0

    # Count the mismatched numbers and use this value as the h'-score (estimated number of moves needed to reach the goal).
    mismatch_count = 0
    for i in range(height):
        for j in range(width):
            if new_state[i, j] > 0 and new_state[i, j] != goal[i, j]:
                mismatch_count += 1

    return (new_state, mismatch_count)


#Copy of the improve
def slide_expand_improve(state, goal):
    node_list = []
    (height, width) = state.shape
    (empty_row, empty_col) = np.argwhere(state == 0)[0]  # Find the position of the empty tile

    # Based on the position of the empty tile, find all possible moves and add a pair (new_state, h'-score)
    # for each of them.
    if empty_row > 0:
        node_list.append(make_node(state, empty_row - 1, empty_col, empty_row, empty_col, goal))
    if empty_row < height - 1:
        node_list.append(make_node(state, empty_row + 1, empty_col, empty_row, empty_col, goal))
    if empty_col > 0:
        node_list.append(make_node(state, empty_row, empty_col - 1, empty_row, empty_col, goal))
    if empty_col < width - 1:
        node_list.append(make_node(state, empty_row, empty_col + 1, empty_row, empty_col, goal))

    return node_list
  
# TO DO: Return either the solution as a list of states from start to goal or [] if there is no solution.               
def a_star(start, goal, expand):

    init_node = Node(start)
    goal_node = Node(goal)
    openList = []
    closedList = []

    # we add the first init, to start the iterative process
    openList.append(init_node)

    # While the list isn't empty
    while len(openList) != 0:
        cNode = openList.pop() # We take the init Note in the first iteration, and after that the nodes we've added
        closedList.append(cNode) #After predicting the best search, we don't need the node anymore and will check if it appears again

        if isGoal(cNode, goal_node):
            sol = []
            # Starts from the cur node back to start node
            while not isGoal(cNode, init_node):
                sol.insert(0, cNode.state) # We need to add this in the beginning of the solution list
                cNode = cNode.prevState
            return sol

        possibleStates = expand(cNode.state, goal_node.state)
        # we go through all of the possible negihbors
        for potentialState, h in possibleStates:
            state = Node(potentialState, cNode) # Create a node creating the previous node
            state.h = h # We get the calculated score
            state.g = cNode.g + 1

            # now verify if we've checked a previous potentialState
            if state not in closedList:
                openList.append(state)

        openList.sort(key=lambda node: node.g+node.h, reverse=True)

    # No Solution
    return []

# Find and print a solution for a given slide puzzle, i.e., the states we need to go through 
# in order to get from the start state to the goal state.
def slide_puzzle_solver(start, goal):
    solution = a_star(start, goal, slide_expand)
    if len(solution) == 0:
        print('This puzzle has no solution. Please stop trying to fool me.')
        return
        
    (height, width) = start.shape
    if height * width >= 10:            # If numbers can have two digits, more space is needed for printing
        digits = 2
    else:
        digits = 1
    horizLine = ('+' + '-' * (digits + 2)) * width + '+'
    for step in range(len(solution)):
        state = solution[step]
        for row in range(height):
            print(horizLine)
            for col in range(width):
                print('| %*d'%(digits, state[row, col]), end=' ')
            print('|')
        print(horizLine)
        if step < len(solution) - 1:
            space = ' ' * (width * (digits + 3) // 2)
            print(space + '|')
            print(space + 'V')

slide_puzzle_solver(example_1_start, example_1_goal)       # Find solution to example_1

import numpy as np
global num_iterations

def anagram_expand(state, goal):
    node_list = []
    
    for pos in range(1, len(state)):    # Create each possible state that can be created from the current one in a single step
        new_state = state[1:pos + 1] + state[0] + state[pos + 1:]
    
    # Very simple h' function - please improve!
        if new_state == goal:
            score = 0
        else:
            score = 0
            for n in range(1, len(new_state)):
                if new_state[n] == goal[n]:
                    score+= 1

        node_list.append((new_state, score))
    
    return node_list
    
def a_star(start, goal, expand):
    global num_iterations

    open_list = [([start], -1)]
    while open_list:
        num_iterations += 1
        open_list.sort(key = lambda x: len(x[0]) + x[1])
        if open_list[0][1] == 0:
            return open_list[0][0]
        
        ancestors = open_list[0][0]
        open_list = open_list[1:]
        new_nodes = expand(ancestors[-1], goal)
        
        for (new_state, score) in new_nodes:    
            append_new_node = True
            for ancestor in ancestors:
                if np.array_equal(new_state, ancestor):
                    append_new_node = False
                    break
            
            if append_new_node:
                open_list.append((ancestors + [new_state], score))        
    return []

# Finds a solution, i.e., a placement of all rectangles within the given field, for a rectangle puzzle
def anagram_solver(start, goal):
    global num_iterations
    num_iterations = 0

    
    # Add code below to check in advance whether the problem is solvable

    tempStart = sorted(start)
    tempGoal = sorted(goal)

    # We want to verify they atleast have the same letters and length, so I sorted both
    if tempGoal != tempStart:
        print('This is clearly impossible. I am not even trying to solve this.')
        return

    solution = a_star(start, goal, anagram_expand)
    
    if not solution:
        print('No solution found. This is weird, I should have caught this before even trying A*.')
        return
        
    print(str(len(solution) - 1) + ' steps from start to goal:')
    
    for step in solution:
        print(step)
    
    print(str(num_iterations) + ' A* iterations were performed to find this solution.')
    

anagram_solver('TRACE', 'CRATE')

anagram_solver('SECURE', 'RESCUE')

anagram_solver('THECLASSROOM', 'SCHOOLMASTER')


anagram_solver('TEARDROP', 'PREDATOR')


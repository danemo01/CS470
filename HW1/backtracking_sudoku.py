# A General Backtracking Function and its Application to the Sudoku Problem
# CS 470/670 at UMass Boston

import numpy as np

example_1 = np.array([[1, 0, 8, 5, 3, 0, 7, 0, 0],
                      [2, 0, 6, 0, 0, 8, 0, 3, 0],
                      [0, 0, 0, 0, 0, 4, 2, 5, 8],
                      [0, 0, 0, 0, 0, 5, 8, 1, 0],
                      [4, 2, 0, 0, 0, 0, 0, 6, 3],
                      [0, 8, 3, 2, 0, 0, 0, 0, 0],
                      [3, 6, 2, 4, 0, 0, 0, 0, 0],
                      [0, 7, 0, 6, 0, 0, 3, 0, 9],
                      [0, 0, 4, 0, 7, 3, 6, 0, 5]])

example_2 = np.array([[0, 0, 0, 0, 3, 0, 2, 8, 0],
                      [7, 0, 0, 5, 0, 0, 0, 1, 0],
                      [3, 0, 0, 0, 6, 0, 0, 0, 0],
                      [0, 8, 0, 0, 0, 2, 0, 4, 0],
                      [1, 0, 0, 0, 5, 0, 0, 0, 2],
                      [0, 6, 0, 9, 0, 0, 0, 3, 0],
                      [0, 0, 0, 0, 2, 0, 0, 0, 4],
                      [0, 4, 0, 0, 0, 6, 0, 0, 1],
                      [0, 9, 2, 0, 7, 0, 0, 0, 0]])

def rectangle_decider(current_state, decision_info, option):
    #verify that option can be accepted through the row
    l = [] # I tried creating a subsquare on numpy but was impossible
    for a in range(3):
        for b in range(3):
            l.append (current_state[(decision_info[0]//3)*3+a][(decision_info[1]//3)*3+b])

    if option not in current_state[decision_info[0],:]: #check if in row using numpy
        if option not in current_state[:,decision_info[1]]: # check if in column using numpy
            if option not in l: # check if in subsquare
                new_state = np.copy(current_state)
                new_state[decision_info[0]][decision_info[1]] = option
                return new_state

    return [] #f it fails any yes, there's no new state to add.

# Recursive backtracking function that receives the current state of the problem, the list of decisions
# that still need to be made from that point on, and a reference to a decider function for the given problem.
# It returns a solution (final problem state) if there is one, otherwise it returns [].
def backtrack(current_state, remaining_decisions, decider_func):
    if remaining_decisions == []:
        return current_state    # No further decisions to be made -> return the solution

    for next_option in remaining_decisions[0][1]:     # Iterate through decision options
        new_state = decider_func(current_state, remaining_decisions[0][0], next_option)
        if len(new_state) > 0:     
            final_state = backtrack(new_state, remaining_decisions[1:], decider_func)    # Option is valid -> move recursively down in the tree
            if len(final_state) > 0:
                return final_state     # If we reach the bottom level -> solution found! 

    return []   # No valid options exist for the current decision -> backtrack to parent node (= previous state)

def sudoku_solver(puzzle):
    decision_seq = []

    fake_list = [1,2,3,4,5,6,7,8,9]
    for row_index in range(len(puzzle)):
        for col_index in range(len(puzzle)):
            if puzzle[row_index][col_index] == 0:
                decision_seq += [((row_index, col_index), list(fake_list))]

    solution = backtrack(puzzle, decision_seq, rectangle_decider)

    if len(solution) == 0:
        print('Sorry, there is no solution. Someone played a prank on you.')
        return

    for row_index in range(len(puzzle)):
        for col_index in range(len(puzzle)):
            print(solution[row_index, col_index], end=' ')
        print('')



sudoku_solver(example_2)

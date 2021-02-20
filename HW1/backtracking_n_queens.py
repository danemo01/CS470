# A General Backtracking Function and its Application to the n-Queens Problem
# CS 470/670 at UMass Boston

import copy
import numpy as np

# Decider function for the n-queens problem.
# For a given search state, check whether the chosen option for the next decision could possibly lead to a solution.
# If so, return the state that results from this decision. Otherwise, return []. 
def queens_decider(current_state, decision_info, option):
    for column in range(len(current_state)):
        row_distance = abs(current_state[column] - option)
        if row_distance == 0 or row_distance == len(current_state) - column:
            return []  # If the new queen shares its row or a diagonal line with
                       # another queen, the current option is invalid.

    new_state = copy.deepcopy(current_state)
    new_state.append(option)    # Otherwise, create and return a new state by copying 
    return new_state            # the old one and appending the row index of the new queen. 

# Recursive backtracking function that receives the current state of the problem, the list of decisions
# that still need to be made from that point on, and a reference to a decider function for the given problem.
# It returns a solution (final problem state) if there is one, otherwise it returns [].
def backtrack(current_state, remaining_decisions, decider_func):
    if remaining_decisions == []:
        return current_state    # No further decisions to be made -> return the solution

    for next_option in remaining_decisions[0][1]:     # Iterate through decision options
        new_state = decider_func(current_state, remaining_decisions[0][0], next_option)
        # print('  ' * remaining_decisions[0][0] + 'In state ' + str(current_state) + ' trying next option ' + str(next_option) + '-> ' + str(len(new_state) > 0))
        if len(new_state) > 0:     
            final_state = backtrack(new_state, remaining_decisions[1:], decider_func)    # Option is valid -> move recursively down in the tree
            if len(final_state) > 0:
                return final_state     # If we reach the bottom level -> solution found! 

    return []   # No valid options exist for the current decision -> backtrack to parent node (= previous state)

# Finds a solution to the n-queens problem (list of n row indices for queen placement)
def n_queens_solver(n):
    decision_seq = [(i, list(range(1, n + 1))) for i in range(1, n + 1)]
    return backtrack([], decision_seq, queens_decider)

# Solves the n-queens problem and prints the solution in ASCII format 
def n_queens_ascii(n):
    solution = n_queens_solver(n)
    if len(solution) == 0:
        print('Sorry, there is no solution to the %d-queens problem.'%(n))
    else:
        print('Solution: ' + str(solution))
        for y in range(1, n + 1):
            for x in range(0, n):
                if solution[x] == y:
                    print('Q', end=' ')
                else:
                    print('.', end=' ')
            print('')

n_queens_ascii(4)
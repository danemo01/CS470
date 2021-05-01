# A General Backtracking Function and its Application to Serious Halloween Problems
# CS 470/670 at UMass Boston

from copy import deepcopy

def capacity(c):

    if c is []:
        return 0
    return sum(c)

# Decider function for the Halloween problem.
def halloween_decider(current_state, decision_info, option):
    # check viability of option for the current decision and return either [] or new_state

    newState = deepcopy(current_state)

    if option == 'Ella' :
        if capacity(current_state[1][0]) + decision_info > current_state[1][1]:
            return []
        else:
            newState[1][0].append(decision_info)
    else: # should be Kingdston
        if capacity(current_state[0][0]) + decision_info > current_state[0][1]:
            return []
        else:
            newState[0][0].append(decision_info)




    return newState
    
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

# Finds a solution, i.e., a list of decisions, for a given Sudoku puzzle
def halloween_solver(candy_list, capacity_ella, capacity_kingston):
    if sum(candy_list) > capacity_ella + capacity_kingston:
        print('Too much candy to carry for Ella and Kingston! PLease revise treats to avoid tricks.')
        return
    
    # Generate decision_seq for the given problem
    decision_seq = []
    for candy in candy_list:
        decision_seq += [(candy, ['Ella', 'Kingston'])]
    # Decision seq for each options a list of tuple (index(?),options)

    solution = backtrack((([], capacity_ella), ([], capacity_kingston)), decision_seq, halloween_decider)
    
    if len(solution) == 0:
        print('There is no way for Ella and Kingston to divide and carry their candy. What a haunting experience!')
        return
    
    print("Problem solved:")
    print("Candy items in Ella's bag:     " + str(solution[0]))
    print("Candy items in Kingston's bag: " + str(solution[1]))
    print("Happy Halloween!")
 
    
halloween_solver([6.1, 1.3, 0.7, 2.9, 4.1, 2.7, 0.9, 3.6, 0.5, 1.2, 1.0], 15, 10)

# A General Backtracking Function and its Application to the Rectangle Problem
# CS 470/670 at UMass Boston
#
# The problem is to place a set of rectangles in such a way that they fit into a given area (field)
# without overlapping. The example problems are given as a pair of field size (height, width)
# and list of rectangle sizes.
#   
# In this solution code, a decision in the sequence consists of the rectangle index (1..n) and its 
# placement options, i.e., potential coordinates of its corners within the field.
# The solver function first prints (in ASCII) the individual rectangles and then their arrangement 
# in the solution.

import numpy as np

example_1 = ((6, 6), [(2, 4), (2, 4), (2, 4), (2, 4), (2, 2)])

example_2 = ((17, 14), [(1, 4), (1, 4), (1, 6), (1, 8),
                        (2, 2), (2, 4), (2, 5), (2, 5), (2, 9), (2, 11),
                        (3, 3), (3, 3), (3, 4), (3, 4), (3, 5), (3, 5),
                        (4, 5), (4, 6), (4, 7)])


# Decider function for the rectangle problem.
# For a given search state (node), it checks whether the next decision could possibly lead to a solution.
def rectangle_decider(current_state, decision_info, option):
    (top, left, bottom, right) = option
    if np.sum(current_state[top:bottom, left:right]) > 0:
        return []  # If the rectangle to be added overlaps with an existing one, the current option is invalid.

    new_state = np.copy(current_state)
    new_state[top:bottom, left:right] = decision_info
    return new_state  # Otherwise, return the new state (array) that includes the new rectangle


# Recursive backtracking function that receives the current state of the problem, the list of decisions
# that still need to be made from that point on, and a reference to a decider function for the given problem.
# It returns a solution (final problem state) if there is one, otherwise it returns [].
# DO NOT MODIFY THIS CODE AT ALL, IT IS UNNECESSARY
def backtrack(current_state, remaining_decisions, decider_func):
    if remaining_decisions == []:
        return current_state  # No further decisions to be made -> return the solution

    for next_option in remaining_decisions[0][1]:  # Iterate through decision options
        new_state = decider_func(current_state, remaining_decisions[0][0], next_option)
        if len(new_state) > 0:
            final_state = backtrack(new_state, remaining_decisions[1:],
                                    decider_func)  # Option is valid -> move recursively down in the tree
            if len(final_state) > 0:
                return final_state  # If we reach the bottom level -> solution found!

    return []  # No valid options exist for the current decision -> backtrack to parent node (= previous state)


# Finds a solution, i.e., a placement of all rectangles within the given field, for a rectangle puzzle
def rectangle_solver(rect_puzzle):
    rect_puzzle[1].sort(key=lambda item: item[0] * item[1], reverse=True)
    min_val = min(rect_puzzle[1], key=lambda item:item[0])[0]



    (field_height, field_width) = rect_puzzle[0]  # The main rect creates freight_height and field_width
    rectangles = rect_puzzle[1]  # all the Rects we need to add in main rect

    rectangle_area_sum = sum([height * width for (height, width) in rectangles])
    if rectangle_area_sum > field_height * field_width:
        print('Come on now, the rectangles are too big for the given field.')
        return

    symbols = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    decision_seq = []
    rect_index = 0
    for (rect_height, rect_width) in rectangles:  # creates all possible options, adds it into decision Sequence
        options = []
        rect_index += 1

        for row in range(rect_height):
            for column in range(rect_width):
                print(symbols[rect_index], end=' ')
            print('')
        print('')

        for top in range(0,field_height - rect_height + 1,min_val):
            for left in range(0,field_width - rect_width + 1,min_val):
                options.append((top, left, top + rect_height, left + rect_width))

        if rect_height != rect_width:  # Unless it is a square, also try rotating each rectangle by 90 degrees
            for top in range(0,field_height - rect_width + 1,min_val):
                for left in range(0,field_width - rect_height + 1,min_val):
                    options.append((top, left, top + rect_width, left + rect_height))

        decision_seq.append((rect_index, options))

    initial_state = np.zeros((field_height, field_width), dtype=int)
    solution = backtrack(initial_state, decision_seq, rectangle_decider)

    if len(solution) == 0:
        print('Sorry, there is no solution. Someone played a prank on you.')
        return

    symbols = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    for row in range(field_height):
        for column in range(field_width):
            print(symbols[solution[row, column]], end=' ')
        print('')


rectangle_solver(example_1)

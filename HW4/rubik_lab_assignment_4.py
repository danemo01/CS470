import numpy as np
from collections import deque
import bisect
from numpy.core.numeric import array_equal
from graphics import GraphWin, Text, Point, Rectangle, Circle, Line, Polygon, update, color_rgb

#         +-------+
#         | 16 17 |          
#         | 18 19 |          
# +-------+-------+-------+-------+
# | 12 13 |  0  1 |  4  5 |  8  9 |
# | 14 15 |  2  3 |  6  7 | 10 11 |
# +-------+-------+-------+-------+
#         | 20 21 |          
#         | 22 23 |          
#         +-------+
#
#   0 -> blue   1 -> white   2 -> green   3 -> yellow   4 -> red   5 -> orange

CELL_SIZE = 60          # Size in pixels of each square cell in the GUI (20 x 12 cells) 
NUM_CELLS = (20, 12)    # Size of the GUI in terms of cells (columns, rows)

CUBE_COLORS = [color_rgb(0, 0, 200), color_rgb(230, 230, 230), color_rgb(0, 200, 0), 
               color_rgb(255, 255, 50), color_rgb(220, 30, 30), color_rgb(255, 150, 30)]

SQUARE_POS = [(11, 4), (12, 4), (11, 5), (12, 5), (14, 4), (15, 4), (14, 5), (15, 5), (17, 4), (18, 4), (17, 5), (18, 5),
              (8, 4), (9, 4), (8, 5), (9, 5), (11, 1), (12, 1), (11, 2), (12, 2), (11, 7), (12, 7), (11, 8), (12, 8)]

SURFACE_LABELS = ['FRONT', 'RIGHT', 'BACK', 'LEFT', 'TOP', 'BOTTOM']
LABEL_POS = [(11.5, 3.2), (14.5, 3.2), (17.5, 3.2), (8.5, 3.2), (11.5, 0.2), (11.5, 6.2)]

LINE_COLOR = color_rgb(255, 255, 255)
BUTTON_COLOR = color_rgb(70, 70, 70)
HISTORY_COLOR = color_rgb(0, 0, 0)
SCORE_COLOR = color_rgb(200, 200, 200)
HISTORY_ORIGIN_X = 7

MOVE_EFFECTS = np.array([
    [ 2,  0,  3,  1, 18,  5, 19,  7,  8,  9, 10, 11, 12, 20, 14, 21, 16, 17, 15, 13,  6,  4, 22, 23], 
    [ 3,  2,  1,  0, 15,  5, 13,  7,  8,  9, 10, 11, 12,  6, 14,  4, 16, 17, 21, 20, 19, 18, 22, 23],
    [ 1,  3,  0,  2, 21,  5, 20,  7,  8,  9, 10, 11, 12, 19, 14, 18, 16, 17,  4,  6, 13, 15, 22, 23],
    [16,  1, 18,  3,  4,  5,  6,  7,  8, 22, 10, 20, 14, 12, 15, 13, 11, 17,  9, 19,  0, 21,  2, 23],
    [11,  1,  9,  3,  4,  5,  6,  7,  8,  2, 10,  0, 15, 14, 13, 12, 20, 17, 22, 19, 16, 21, 18, 23],
    [20,  1, 22,  3,  4,  5,  6,  7,  8, 18, 10, 16, 13, 15, 12, 14,  0, 17,  2, 19, 11, 21,  9, 23],
    [ 4,  5,  2,  3,  8,  9,  6,  7, 12, 13, 10, 11,  0,  1, 14, 15, 18, 16, 19, 17, 20, 21, 22, 23],
    [ 8,  9,  2,  3, 12, 13,  6,  7,  0,  1, 10, 11,  4,  5, 14, 15, 19, 18, 17, 16, 20, 21, 22, 23],
    [12, 13,  2,  3,  0,  1,  6,  7,  4,  5, 10, 11,  8,  9, 14, 15, 17, 19, 16, 18, 20, 21, 22, 23]], dtype=np.uint8)

AXES = ['FRONT', 'LEFT', 'TOP']
ROTATIONS = ['CW', '180', 'CCW']

MOVE_COLORS = [color_rgb(0, 50, 50), color_rgb(0, 100, 100), color_rgb(0, 150, 150), 
                color_rgb(50, 50, 0), color_rgb(70, 70, 0), color_rgb(90, 90, 0),
                color_rgb(50, 0, 50), color_rgb(100, 0, 100), color_rgb(150, 0, 150)]

OPPOSING_SURFACES = [2, 3, 0, 1, 5, 4]

neighbor_x1 = np.array([0, 2, 8, 10, 16, 18, 20, 22], dtype=np.int)
neighbor_x2 = np.array([1, 3, 9, 11, 17, 19, 21, 23], dtype = np.int)
neighbor_y1 = np.array([0, 1, 4, 5, 8, 9, 12, 13], dtype=np.int)
neighbor_y2 = np.array([2, 3, 6, 7, 10, 11, 14, 15], dtype = np.int)
neighbor_z1 = np.array([4, 6, 12, 14, 16, 17, 20, 21], dtype=np.int)
neighbor_z2 = np.array([5, 7, 13, 15, 18, 19, 22, 23], dtype = np.int)
neighbor1 = np.array([0, 0, 1, 2, 4, 4, 5, 6, 8, 8, 9, 10, 12, 12, 13, 14, 16, 16, 17, 18, 20, 20, 21, 22], dtype=np.int)
neighbor2 = np.array([1, 2, 3, 3, 5, 6, 7, 7, 9, 10, 11, 11, 13, 14, 15, 15, 17, 18, 19, 19, 21, 22, 23, 23], dtype = np.int)

start_state_9_moves = np.array([0, 1, 4, 0, 4, 2, 1, 0, 5, 4, 5, 5, 1, 3, 1, 2, 2, 3, 4, 0, 3, 5, 2, 3], dtype=np.uint8)
start_state_x = np.array([0, 1, 4, 0, 4, 2, 1, 0, 5, 4, 5, 5, 1, 3, 1, 2, 2, 3, 4, 0, 3, 5, 2, 3], dtype=np.uint8)
start_state_easy = np.array([1, 1, 0, 0, 2, 2, 1, 1, 3, 3, 2, 2, 0, 0, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5], dtype=np.uint8)
start_state_11_moves = np.array([0, 0, 0, 0, 3, 3, 3, 1, 2, 2, 2, 2, 3, 1, 1, 1, 4, 5, 5, 5, 4, 4, 4, 5], dtype=np.uint8)
perfect_state = np.array([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5], dtype=np.uint8)

class HistoryEntry(object):
    __slots__ = ['operation', 'new_state', 'new_score']

start_state = perfect_state.copy()
goal_state = []

def coords(x_cell, y_cell, center=False):
    return Point(int(min(NUM_CELLS[0] * CELL_SIZE - 1, (x_cell + 0.5 * center) * CELL_SIZE)), int((y_cell + 0.5 * center) * CELL_SIZE))

def draw_square(x, y, col):
    r = Rectangle(coords(x, y), coords(x + 1, y + 1))
    r.setFill(col)
    r.setWidth(1)
    r.setOutline(LINE_COLOR)
    r.draw(win)

def draw_button(x, y, col=LINE_COLOR, dict_entry=(-1, -1)):
    global button_dict
    button_dict[x, y] = dict_entry
    draw_square(x, y, col)
    
def draw_text(x, y, text, col=LINE_COLOR, text_size = 12):
    t = Text(coords(x, y, center=True), text)
    t.setFace('arial')
    t.setSize(int(CELL_SIZE / 60.0 * text_size))
    t.setTextColor(col)
    t.draw(win)

def draw_transition_button(x, y, operation, draw_in_history=False):
    if draw_in_history:
        button_dict_entry = ('history_jump', x - HISTORY_ORIGIN_X)
    else:
        button_dict_entry = operation

    if operation[0] == 'make_move':
        draw_button(x, y, MOVE_COLORS[operation[1]], button_dict_entry)
        draw_text(x, y - 0.2, AXES[operation[1] // 3])
        draw_text(x, y + 0.2, ROTATIONS[operation[1] % 3])
    elif operation[0] == 'cube_edit':
        draw_button(x, y, BUTTON_COLOR, button_dict_entry)
        draw_text(x, y - 0.2, 'CUBE')
        draw_text(x, y + 0.2, 'EDIT')
    elif operation[0] == 'start_state':
        draw_button(x, y, BUTTON_COLOR, button_dict_entry)
        draw_text(x, y - 0.2, 'START')
        draw_text(x, y + 0.2, 'STATE')
    elif operation[0] == 'perfect_state':
        draw_button(x, y, BUTTON_COLOR, button_dict_entry)
        draw_text(x, y - 0.2, 'PERFECT', text_size=9)
        draw_text(x, y + 0.2, 'STATE')
    else:
        draw_button(x, y, color_rgb(0, 0, 0), button_dict_entry)  

def display_GUI():
    win.delete('all')
    
    for y in range(3):
        for x in range(3):
            draw_transition_button(2 * x + 1, 2 * y + 1, ('make_move', 3 * y + x))
            
    for sq in range(len(SQUARE_POS)):
        draw_button(SQUARE_POS[sq][0], SQUARE_POS[sq][1], CUBE_COLORS[curr_state[sq]], ('cube_edit', sq))

    for i in range(6):
        draw_text(LABEL_POS[i][0], LABEL_POS[i][1], SURFACE_LABELS[i])

    draw_button(1, 8, BUTTON_COLOR, ('solve', 0))
    draw_button(2, 8, BUTTON_COLOR, ('solve', 0))
    draw_button(3, 8, BUTTON_COLOR, ('solve', 0))
    r = Rectangle(coords(1, 8), coords(4, 9))
    r.setFill(BUTTON_COLOR)
    r.setWidth(1)
    r.setOutline(LINE_COLOR)
    r.draw(win)
    draw_text(2, 8, 'SOLVE !', LINE_COLOR, 20)

    draw_button(HISTORY_ORIGIN_X - 1, 8, HISTORY_COLOR, ('history_jump', -1))
    draw_text(HISTORY_ORIGIN_X - 1, 7.7, 'BACK', text_size=8)
    p = Polygon([coords(HISTORY_ORIGIN_X - 0.8, 8.6), coords(HISTORY_ORIGIN_X - 0.2, 8.3), coords(HISTORY_ORIGIN_X - 0.2, 8.9)])
    p.setFill(BUTTON_COLOR)
    p.setWidth(1)
    p.setOutline(LINE_COLOR)
    p.draw(win)

    draw_button(HISTORY_ORIGIN_X, 8, HISTORY_COLOR, ('history_jump', 1))
    draw_text(HISTORY_ORIGIN_X, 7.7, 'FWD', text_size=8)
    p = Polygon([coords(HISTORY_ORIGIN_X + 0.8, 8.6), coords(HISTORY_ORIGIN_X + 0.2, 8.3), coords(HISTORY_ORIGIN_X + 0.2, 8.9)])
    p.setFill(BUTTON_COLOR)
    p.setWidth(1)
    p.setOutline(LINE_COLOR)
    p.draw(win)

    for x in range(NUM_CELLS[0]):
        history_index = history_pointer + x - HISTORY_ORIGIN_X
        if history_index >= 0 and history_index < len(history) - 1:
            operation = history[history_index + 1].operation
        else:
            operation = ('', 0)    
        draw_transition_button(x, 10, operation, draw_in_history=True)

        if history_index >= 0 and history_index < len(history):
            sc = history[history_index].new_score
            sc_color = SCORE_COLOR
            if sc == 0:
                sc_color = LINE_COLOR
            draw_text(x - 0.5, 10.8, '%.1f'%(sc))

    l = Line(coords(HISTORY_ORIGIN_X, 8), coords(HISTORY_ORIGIN_X, 11))
    l.setWidth(3)
    l.setFill(LINE_COLOR)
    l.draw(win)

    draw_transition_button(15, 1, ('start_state', 0))
    draw_transition_button(17, 1, ('perfect_state', 0))
    
    draw_button(15, 8, BUTTON_COLOR, ('random_move', 0))
    draw_text(15, 7.8, 'RANDOM', text_size=10)
    draw_text(15, 8.2, 'MOVE')
    draw_button(17, 8, BUTTON_COLOR, ('quit', 0))
    draw_text(17, 8, 'QUIT')
    update()

# Get cell coordinates of the button clicked by the user
def get_clicked_button():
    while True:
        clickPos = win.getMouse()
        cell_x = int(clickPos.x / CELL_SIZE)
        cell_y = int(clickPos.y / CELL_SIZE)

        if cell_x >= 0 and cell_x < NUM_CELLS[0] and cell_y >= 0 and cell_y < NUM_CELLS[1]:
            return (cell_x, cell_y)

def get_h_prime(state, goal):
    if np.array_equal(state, goal):
        return 0
    else:
        return 1

def expand_rubik(last_move, state, goal):
    if last_move == -1:
        move_range = range(0, 9)
    elif last_move < 3:
        move_range = range(3, 9)
    elif last_move < 6:
        move_range = [0, 1, 2, 6, 7, 8]
    else:
        move_range = range(0, 6)
    
    new_nodes = []
    for move in move_range:
        new_state = state[MOVE_EFFECTS[move]]
        h_prime = get_h_prime(new_state, goal)
        new_nodes += [(move, new_state, h_prime)]
        
    return new_nodes

def a_star(start, goal, expand):
    open_nodes = deque([(-1, start.tobytes())]) # For each node on the OPEN list, keep its f'-score and a key for looking up its path from the start state (root)
    counter = 0
    node_dictionary = {start.tobytes(): []}

    while open_nodes:
        last_score, state_code = open_nodes.popleft()
        move_seq = node_dictionary[state_code]   # Associate every state encountered with the shortest path to reach it (that we have found so far)
        state = np.frombuffer(state_code, dtype=np.uint8)
        if len(move_seq) == 0:
            last_move = -1
        else:
            last_move = move_seq[-1]
        new_nodes = expand(last_move, state, goal)
        new_node_depth = len(move_seq) + 1
        counter += 1
        
        if counter % 1000 == 0:
            print('Iterations: %d, nodes in list: %d, winner node depth: %d, score: %f'%(counter, len(open_nodes), new_node_depth, last_score))

        for (new_move, new_state, h_prime) in new_nodes:
            if h_prime == 0:
                return move_seq + [new_move]
            new_state_code = new_state.tobytes()
            if not (new_state_code in node_dictionary) or len(node_dictionary[new_state_code]) > new_node_depth: 
                node_dictionary[new_state_code] = move_seq + [new_move]
                f_prime = new_node_depth + h_prime    # We now need to keep f' rather than h' on open_node_scores for correct sorting
                bisect.insort_left(open_nodes, (f_prime, new_state_code))
    return []

def rubik_solver():
    set_goal_state(curr_state)
    solution_moves = a_star(curr_state, goal_state, expand_rubik)
    return solution_moves

def set_goal_state(curr_state):
    global goal_state

    goal_state = np.zeros(24, dtype=np.uint8)
    goal_state[4:8] = curr_state[7]
    goal_state[8:12] = curr_state[10]
    goal_state[20:24] = curr_state[23]
    goal_state[12:16] = OPPOSING_SURFACES[curr_state[7]]
    goal_state[0:4] = OPPOSING_SURFACES[curr_state[10]]
    goal_state[16:20] = OPPOSING_SURFACES[curr_state[23]]

win = GraphWin("Rubik's 2x2x2 Cube Lab for Mad Computer Scientists", NUM_CELLS[0] * CELL_SIZE, NUM_CELLS[1] * CELL_SIZE, autoflush=False)
win.setBackground('black')

curr_state = start_state.copy()
set_goal_state(curr_state)
initial_history = HistoryEntry()
initial_history.operation = ('', 0)
initial_history.new_state = start_state.copy()
initial_history.new_score = get_h_prime(start_state, goal_state)
history = [initial_history]
history_pointer = 0
button_dict = dict()

while True:
    display_GUI()
    x, y = get_clicked_button()
    if (x, y) in button_dict:
        expand_history = False
        action = button_dict[(x, y)][0]
        param = button_dict[(x, y)][1]

        if action == 'quit':
            break
        elif action == 'solve':
            if get_h_prime(curr_state, goal_state) > 0:
                solution = rubik_solver()
                expand_history = True
        elif action == 'history_jump':
            if history_pointer + param >= 0 and history_pointer + param < len(history):
                history_pointer += param
                curr_state = history[history_pointer].new_state      
        elif action == 'cube_edit':
            curr_state[param] = (curr_state[param] + 1) % 6
            expand_history = True
        elif action == 'start_state':
            curr_state = start_state.copy()
            expand_history = True
        elif action == 'perfect_state':
            curr_state = perfect_state.copy()
            expand_history = True
        elif action == 'random_move':
            action = 'make_move'
            param = np.random.randint(9)
        if action == 'make_move':
            curr_state = curr_state[MOVE_EFFECTS[param]]
            expand_history = True

        set_goal_state(curr_state)

        if expand_history:
            if history_pointer < len(history) - 1:
                history = history[:history_pointer + 1]

            if action == 'cube_edit' and history[history_pointer].operation[0] == 'cube_edit':
                history[history_pointer].new_state = curr_state.copy()
                history[history_pointer].new_score = get_h_prime(curr_state, goal_state)
            elif action == 'solve':
                temp_state = curr_state.copy()
                for move in solution:
                    temp_state = temp_state[MOVE_EFFECTS[move]]
                    new_entry = HistoryEntry()
                    new_entry.operation = ('make_move', move)
                    new_entry.new_state = temp_state.copy()
                    new_entry.new_score = get_h_prime(temp_state, goal_state)
                    history.append(new_entry)
            else:
                new_entry = HistoryEntry()
                new_entry.operation = (action, param)
                new_entry.new_state = curr_state.copy()
                new_entry.new_score = get_h_prime(curr_state, goal_state)
                history.append(new_entry)
                history_pointer += 1
    
win.close()

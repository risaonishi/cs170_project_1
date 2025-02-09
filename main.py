import heapq

goal_state = [[1, 2, 3], 
              [4, 5, 6], 
              [7, 8, 0]]

# Solvable test cases from instructions
depth_1 = [[1, 2, 3],
           [4, 5, 6],
           [7, 0, 8]]
depth_3 = [[1, 2, 3],
           [0, 5, 6],
           [4, 7, 8]]
depth_4 = [[1, 2, 3],
           [5, 0, 6],
           [4, 7, 8]]
depth_8 = [[1, 3, 6],
           [5, 0, 2],
           [4, 7, 8]]
depth_12 = [[1, 3, 6],
            [5, 0, 7],   
            [4, 8, 2]]
depth_16 = [[1, 6, 7],
            [5, 0, 3],
            [4, 8, 2]]
depth_20 = [[7, 1, 2],
            [4, 8, 5],
            [6, 3, 0]]
depth_24 = [[0, 7, 2],
            [4, 6, 1],
            [3, 5, 8]]
class Node:
    def __init__(self, state, parent=None, cost=0):
        self.state = state
        self.parent = parent
        self.cost = cost

    # Comparison operators for heapq
    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.cost == other.cost

class Problem:
    def __init__(self, initial_state):
        self.initial_state = initial_state

    def goal_test(self, state):
        return state == goal_state
    
    def operators(self, state):
        i, j = find_number(state, 0)
        applicable_operators = []
        if i > 0:  # Up
            applicable_operators.append('Up')
        if i < 2:  # Down
            applicable_operators.append('Down')
        if j > 0:  # Left
            applicable_operators.append('Left')
        if j < 2:  # Right
            applicable_operators.append('Right')
        return applicable_operators

def make_queue(node):
    queue = []
    heapq.heappush(queue, (node.cost, node))
    return queue

def make_node(state, parent=None, cost=0):
    return Node(state, parent, cost)

# Check if queue is empty
def empty(nodes):
    return len(nodes) == 0

# Pop the front of the queue and print the state
def remove_front(nodes):
    print_state(nodes[0][1].state)
    return heapq.heappop(nodes)[1]

def expand(node, operators):
    children = []
    i, j = find_number(node.state, 0)
    for operator in operators(node.state):
        child_state = [row[:] for row in node.state] # Copy the state to create new ones with operators applied
        if operator == 'Up':  # Up
            child_state[i][j], child_state[i-1][j] = child_state[i-1][j], child_state[i][j] # Swapping 0 w/ number above
        if operator == 'Down':  # Down
            child_state[i][j], child_state[i+1][j] = child_state[i+1][j], child_state[i][j] # Swapping 0 w/ number below
        if operator == 'Left':  # Left 
            child_state[i][j], child_state[i][j-1] = child_state[i][j-1], child_state[i][j] # Swapping 0 w/ number left
        if operator == 'Right':  # Right
            child_state[i][j], child_state[i][j+1] = child_state[i][j+1], child_state[i][j] # Swapping 0 w/ number right
        children.append(make_node(child_state, node, node.cost + 1))
    return children

# Find position of given number in the state
def find_number(state, number):
    for i in range(3):
        for j in range(3):
            if state[i][j] == number: # 
                return i, j

def uniform_cost(nodes, children):
    for child in children:
        heapq.heappush(nodes, (child.cost, child))
    return nodes

# Uses misplaced tile heuristic, which counts tiles in the wrong position
def A_star_misplaced(nodes, children):
    for child in children:
        misplaced = 0
        for i in range(3):
            for j in range(3):
                if child.state[i][j] != goal_state[i][j]: # Count all tiles that aren't in the correct position
                    misplaced += 1
        heapq.heappush(nodes, (child.cost + misplaced, child))
    return nodes

# Uses manhattan dist. heuristic, which sums the distances of each tile from their goal positions
def A_star_manhattan(nodes, children):
    for child in children:
        distance = 0
        for i in range(3):
            for j in range(3):
                goal_i, goal_j = find_number(goal_state, child.state[i][j]) # Find where the current number is supposed to be
                distance += abs(i - goal_i) + abs(j - goal_j) # Calculate manhattan distance to that position
        heapq.heappush(nodes, (child.cost + distance, child)) # Push to pq, sorted by min (cost to get to a node + distance to goal)
    return nodes

def print_state(state):
    for i in range(3):
        for j in range(3):
            print(state[i][j], end=' ')
        print()
    print() 

def general_search(problem, queueing_function):
    nodes = make_queue(make_node(problem.initial_state)) # Make queue and add initial state
    visited = [] # Used to prevent repetition
    nodes_expanded =0

    while True:
        if empty(nodes): return None
        node = remove_front(nodes)
        nodes_expanded += 1
        if problem.goal_test(node.state): 
            print("Nodes expanded: ", nodes_expanded)
            return node
        children = expand(node, problem.operators)
        for child in children:
            if child.state not in visited: # Prevent repeated states by appending only if not visited
                visited.append(child.state)
                nodes = queueing_function(nodes, children)
        # nodes = queueing_function(nodes, expand(node, problem.operators))

def main():
    print("Welcome to the 8-puzzle solver!")
    puzzle = depth_8
    solved = general_search(Problem(puzzle), A_star_manhattan)
    if solved:
        print("Solution found!")
        print_state(solved.state)
    else:
        print("No solution found.")
    return 0

if __name__ == "__main__":
    main()

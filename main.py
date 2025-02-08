import heapq

goal_state = [[1, 2, 3], 
              [4, 5, 6], 
              [7, 8, 0]]
class Node:
    def __init__(self, state, parent = None, cost = 0):
        self.state = state
        self.parent = parent
        self.cost = cost

class Problem:
    def __init__(self, initial_state):
        self.initial_state = initial_state

    def goal_test(self, state):
        return state == goal_state
    
    def operators(self, state): # 
        i, j = find_0(state)
        applicable_operators = []
        if i > 0: # Up
            applicable_operators.append('Up')
        if i < 2: # Down
            applicable_operators.append('Down')
        if j > 0: # Left
            applicable_operators.append('Left')
        if j < 2: # Right
            applicable_operators.append('Right')
        return applicable_operators
            

def make_queue(node):
    queue = []
    heapq.heappush(queue, (node.cost, node))
    return queue

def make_node(state, parent = None, cost = 0):
    return Node(state, parent, cost)

def empty(nodes):
    return len(nodes) == 0

def remove_front(nodes):
    return heapq.heappop(nodes)

def expand(node, operators):
    children = []
    i, j = find_0(node.state)
    for operator in operators(node.state):
        if operator == 'Up': # Up
            child_state[i,j] = child_state[i-1,j] # Turn 0 into the number above it
            child_state[i-1,j] = 0 
            children.append(make_node(child_state, node, node.cost + 1))
        if operator == 'Down': # Down
            child_state[i,j] = child_state[i+1,j] # Turn 0 into the number below it
            child_state[i+1,j] = 0
            children.append(make_node(child_state, node, node.cost + 1))
        if operator == 'Left': # Left
            child_state[i,j] = child_state[i,j-1] # Turn 0 into the number to its left
            child_state[i,j-1] = 0
            children.append(make_node(child_state, node, node.cost + 1))
        if operator == 'Right': # Right
            child_state[i,j] = child_state[i,j+1] # Turn 0 into the number to its right 
            child_state[i,j+1] = 0
            children.append(make_node(child_state, node, node.cost + 1))
    return children

def find_0(node):
    for i in range(3):
        for j in range(3):
            if node.state[i][j] == 0:
                return i, j

def heuristic_search(nodes, children):
    for child in children:
        heapq.heappush(nodes, (child.cost, child))
    return nodes



def general_search(problem, queueing_function):
    nodes = make_queue(make_node(problem.initial_state))
    while True:
        if empty(nodes): return None
        node = remove_front(nodes)
        if problem.goal_test(node.state): return node
        nodes = queueing_function(nodes, expand(node, problem.operators))

def main() -> int:
    print("Welcome to the 8-puzzle solver!")
    return 0

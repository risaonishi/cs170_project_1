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
    
    def operators(self, state):
        return 1
    
goal_state = [[1, 2, 3], 
              [4, 5, 6], 
              [7, 8, 0]]

def make_queue(node):
    return [node]

def make_node(state, parent = None, cost = 0):
    return Node(state, parent, cost)

def empty(nodes):
    return len(nodes) == 0

def remove_front(nodes):
    return nodes.pop_front()

def search_driver(problem, queueing_function):
    nodes = make_queue(make_node(problem.initial_state))
    while True:
        if empty(nodes): return None
        node = remove_front(nodes)
        if problem.goal_test(node.state): return node
        nodes = queueing_function(nodes, expand(node, problem.operators))

def main() -> int:
    return 0

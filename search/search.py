# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

#Code by Dylan Sholtes in Collaboration with Bhuvaneshwar Mohan
"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    currentState = problem.getStartState()
    #visitedStates holds every gamestate that dfs has passed through
    visitedStates = []
    visitedStates.append(start)
    frontier = util.Stack()
    #This initializes a tuple to hold our starting position, start is the State, the empty list is the action
    state = (start, [])
    #add initial state to the frontier
    frontier.push(state)
    while not frontier.isEmpty() and not problem.isGoalState(currentState):
        #node holds current position through DFS, action holds the list of actions to reach goal state
        node, action = frontier.pop()
        #add node to the explored set
        visitedStates.append(node)
        #get the successor children from node, add them to frontier if they aren't in frontier already
        children = problem.getSuccessors(node)
        for i in children:
            child = i[0]
            #if the child has not been explored, add it to the frontier
            if child not in visitedStates:
                direction = i[1]
                currentState = child
                frontier.push((child, action + [direction]))
    return action + [direction]
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    #visitedStates holds every gamestate that bfs has passed through
    visitedStates = []
    visitedStates.append(start)
    frontier = util.Queue()
    #This initializes a tuple to hold our starting position, start is the State, the empty list is the action
    state = (start, [])
    #add initial state to the frontier
    frontier.push(state)
    while frontier.isEmpty() is False:
        #node holds current position through BFS, action holds the list of actions to reach goal state
        node, action = frontier.pop()
        #add node to the explored set
        visitedStates.append(node)
        if problem.isGoalState(node):
            return action
        #get the successor children from node, add them to frontier if they aren't in frontier already
        children = problem.getSuccessors(node)
        for i in children:
            child = i[0]
            #if the child has not been explored, add it to the frontier
            if child not in visitedStates:
                direction = i[1]
                frontier.push((child, action + [direction]))
                visitedStates.append(child)
    return action
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    #visitedStates holds every gamestate that UCS has passed through
    visitedStates = []
    #We make the frontier a priority queue so that children  are explored by cost
    frontier = util.PriorityQueue()
    #This initializes a tuple to hold our starting position, start is the State, the empty list is the action
    state = (start, [], 0)
    #add initial state to the frontier
    frontier.push((start, []), 0)
    while frontier.isEmpty() is False:
        #node holds current position through UCS, action holds the list of actions to reach goal state
        node, action = frontier.pop()
        if problem.isGoalState(node):
            return action
        #get the successor children from node, add them to frontier if they aren't in frontier already
        if node not in visitedStates:
            #add node to visitedStates if it is not already part of visitedStates, grab children
            visitedStates.append(node)
            children = problem.getSuccessors(node)
            for i in children:
                child = i[0]
                #if the child has not been explored, add it to the frontier
                if i not in visitedStates:
                    direction = i[1]
                    totalCost = action + [direction]
                    f_n = problem.getCostOfActions(totalCost)
                    #Get Cost of Actions returns the total cost of the actions
                    frontier.push((child, action + [direction]), f_n)
                else:
                    for i in range(0, len(frontier.heap)):
                        if frontier.heap[i][0] > f_n:
                            frontier.heap[i] = (f_n, (child, action + [direction]))
    return action
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    #visitedStates holds every gamestate that UCS has passed through
    visitedStates = []
    #We make the frontier a priority queue so that the states are handled successively
    frontier = util.PriorityQueue()
    #add initial state to the frontier
    frontier.push((start, []), nullHeuristic(start, problem=problem))
    while frontier.isEmpty() is False:
        #node holds current position through A*, action holds the list of actions to reach goal state
        node, action = frontier.pop()
        if problem.isGoalState(node):
            return action
        #get the successor children from node, add them to frontier if they aren't in frontier already
        if node not in visitedStates:
            #add node to visitedStates if it is not already part of visitedStates, grab children
            visitedStates.append(node)
            children = problem.getSuccessors(node)
            for i in children:
                child = i[0]
                direction = i[1]
                f_n = problem.getCostOfActions(action + [direction]) + heuristic(child, problem)
                #if the child has not been explored, add it to the frontier
                if i not in visitedStates:
                    frontier.push((child, action + [direction]), f_n)
                    visitedStates.append(node)
                else:
                    for i in range(0, len(frontier.heap)):
                        if frontier.heap[i][0] > f_n:
                                frontier.heap[i] = (f_n, (child, action + [direction]))


    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

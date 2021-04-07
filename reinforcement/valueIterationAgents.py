# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
#Code by Dylan Sholtes and Bhuvaneshwar Mohan
class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            newVals = self.values.copy()
            #loop through states
            for state in self.mdp.getStates():
                #check if a terminal state has been reached
                if not self.mdp.isTerminal(state):
                    #find best action from the current state
                    bestAction = self.computeActionFromValues(state)
                    #compute a new q value based from bestAction from currentState
                    newVals[state] = self.computeQValueFromValues(state, bestAction)
            #update values with new q values after each iteration
            self.values = newVals




    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #initialize q value to be zero
        qVal = 0
        #loop through transition states and their probabilites
        for transitionState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            #sum the probablity multiplied by the reward plus the discount multiplied by the current value iteration
            qVal += prob * (self.mdp.getReward(state, action, transitionState) + self.discount * self.getValue(transitionState))
        return qVal

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)
        #if no actions are available, terminal state
        if len(actions) == 0:
            return None
        bestAction = 0
        maxVal = 0
        #loop through possible actions
        for action in actions:
            val = 0
            #compute values for each possible transition state
            for transitionState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                val += prob * (self.mdp.getReward(state, action, transitionState) + self.discount * self.getValue(transitionState))
            #if the value from successor is greater than the current max value
            #or if the current maxVal is 0
            #update maxVal and make bestAction to be action
            if val > maxVal or maxVal == 0:
                maxVal = val
                bestAction = action
        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

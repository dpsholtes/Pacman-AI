# multiAgents.py
# --------------
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
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        currPos = currentGameState.getPacmanPosition()
        currFood = currentGameState.getFood()
        #store food as a list, to compare lengths of foodLists to find food score
        foodList = currFood.asList()
        newFoodList = newFood.asList()
        #calculate ghost score, set default ghost score to be zero
        ghostScore = 0
        #get the new ghost positions
        newGhostPositions = successorGameState.getGhostPositions()
        #set the minGhostDistance to be the manhattan distance of the new pacman position to the first ghost
        #we will use this as a basis of comparison to find the closest ghost to pacmans new position
        minGhostDistance = util.manhattanDistance(newPos, newGhostPositions[0])
        for ghost in newGhostPositions:
            if minGhostDistance > util.manhattanDistance(newPos, ghost):
                #if the manhattanPosition of a ghost is less than the current minGhost distance
                #set the minGhost distance to be the manhattanDistance of the new ghost
                    minGhostDistance = util.manhattanDistance(newPos, ghost)
        #check the minimum ghost distance, and assign a negative value accordingly
        #if the ghosts are not scared, being close to a ghost is really bad
        if newScaredTimes == 0:
            # if the ghost is closer, the ghostscore is a more negative number
            # half ghost score for each tile the ghost gets further from the pacman position
            # once ghost distance is larger than 4, ghost distance becomes 0
            # that means the closest ghost is at least five tiles away from pacman, and not currently a problem
            if minGhostDistance <= 2:
                ghostScore = -50
            elif minGhostDistance <= 3:
                ghostScore = -25
            elif minGhostDistance <= 4:
                ghostScore = -12
            else:
                ghostScore = 0
        #if the ghosts are scared, being close to a ghost isnt the worst, but best to not get too close
        else:
            #if pacman is one tile away from a ghost, large negative penalty
            #once pacman is two or 3 tiles away, the penalty decreases, since ghosts are not dangerous when scared
            #once larger than 3 tiles away, ghosts are not a threat while scared, so no penalty occurs
            if minGhostDistance == 1:
                ghostScore = -25
            elif minGhostDistance <=3:
                ghostScore = -5
            else:
                ghostScore = 0

        foodScore = 0
        #if the length of the newFoodList is less than the length of the currentFoodList
        #pacman has collected food in his new state
        #if pacman has collected no food, the lengths of both lists will be the same
        #in that case, foodScore will be 1/ the minimum manhattan distance to the closest food
        #this allows foodScore to increase the closer pacman is to food
        #without giving too mucn incentive into the food to where pacman runs himself into ghosts
        if len(foodList) - len(newFoodList) != 0:
            foodScore = 1 * len(foodList) - len(newFoodList)
        else:
            minFoodDistance = manhattanDistance(newPos, newFoodList[0])
            for food in newFoodList:
                if minFoodDistance > manhattanDistance(newPos, food):
                    minFoodDistance = manhattanDistance(newPos, food)
            foodScore = 1 /float(minFoodDistance)
        #pacman is penalized for taking actions that does not decrease the amount of food left on the board
        remainingFoodPenalty = len(newFoodList)

        #total the ghostScore, foodScore, and the penalty for remainingFood
        return ghostScore + foodScore - remainingFoodPenalty

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def maxValue(state, depth, agentIndex):
            #if terminal tests return utility
            if depth == self.depth or state.isLose() or state.isWin():
                return self.evaluationFunction(state)
            #initializing v to be -infinity
            v = float('-inf')
            #loop through actions and find max score
            for action in state.getLegalActions(agentIndex):
                successorState = state.generateSuccessor(agentIndex, action)
                #this finds the max of the minimum values
                v = max(v, minValue(successorState, depth, 1))
            return v


        def minValue(state, depth, agentIndex):
            #if terminal tests, return utility
            if depth == self.depth or state.isLose() or state.isWin():
                return self.evaluationFunction(state)
            v = float('inf')
            #loop through actions for agentIndex
            for action in state.getLegalActions(agentIndex):
                #if the agentIndex is a ghost agent, continue to call minValue
                if agentIndex < state.getNumAgents() - 1:
                    successorState = state.generateSuccessor(agentIndex, action)
                    v = min(v, minValue(successorState, depth, agentIndex + 1))
                #once minValue of all ghost agents has been found, increase depth, and find the maxValue of pacman
                else:
                    successorState = state.generateSuccessor(agentIndex, action)
                    #this will return the smallest maxValue
                    v = min(v, maxValue(successorState, depth + 1, 0))
            return v

        def minimaxDecision():
            #initialize v to be -infinity
            v = float('-inf')
            #loop through pacman's legal actions
            for action in gameState.getLegalActions(0):
                #find successor pacman state based on action
                successorState = gameState.generateSuccessor(0, action)
                #find the action with the highest min value
                score = minValue(successorState, 0, 1)
                # if an action has a higher minValue, update v to be score of the new action
                #update bestAction to be the new highest min value
                if score > v:
                    v = score
                    bestAction = action
            return bestAction
        return minimaxDecision()

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(state, alpha, beta, depth, agentIndex):
            v = float('-inf')
            #if terminal tests return utility
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            #loop through pacmans actions
            for action in state.getLegalActions():
                successorState = state.generateSuccessor(agentIndex, action)
                #find the largest minValue
                v = max(v, minValue(successorState, alpha, beta, depth, 1))
                #stop searching tree early if value is greater than beta
                if v > beta:
                    return v
                #update alpha to be the max of v and alpha
                alpha = max(alpha, v)
            return v
        def minValue(state, alpha, beta,depth, agentIndex):
            v = float('inf')
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            #loop through current agents actions
            for action in state.getLegalActions(agentIndex):
                successorState = state.generateSuccessor(agentIndex, action)
                #if agent is a ghost, get smallest minValue
                if agentIndex < state.getNumAgents() - 1:
                    v = min(v, minValue(successorState, alpha, beta, depth, agentIndex + 1))
                #once all of the minValues for the ghosts have been found
                #find the smallest maxValue for pacman
                else:
                    v = min(v, maxValue(successorState, alpha, beta, depth + 1, 0))
                #stop searching tree early is value is less than alpha
                if v < alpha:
                    return v
                #update beta to be the min of v and beta
                beta = min(beta, v)
            return v
        def alphabetadecision():
            v = float('-inf')
            alpha = float('-inf')
            beta = float('inf')
            for action in gameState.getLegalActions():
                successorState = gameState.generateSuccessor(0, action)
                score = minValue(successorState, alpha, beta, 0 , 1)
                #if an action has a higher min score, update v to be score
                #update bestAction to be action
                if score > v:
                    v = score
                    bestAction = action
                #update alpha to be the max of v and alpha
                alpha = max(alpha, v)
            return bestAction
        return alphabetadecision()





class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        def value(depth, agent, state):
            # run evaluation function if terminal state or max depth has been reached
            if state.isWin() or state.isLose() or depth == self.depth:
                return (self.evaluationFunction(state), Directions.STOP)

            # Max val will only accept pacman
            if agent == 0:
                return max_val(depth, agent, state)
            else:
                # Run expectimax on all ghost agents
                return exp_val(depth, agent, state)

        def max_val(depth, agent, state):
            """Evaluates max node similar to minimax"""
            v = (float("-inf"), None)  # initialize max score

            # get all legal actions for pacman
            actions = state.getLegalActions(agent)

            # increment index for successive states
            successorIndex = agent + 1
            # if legal actions exist
            if actions:
                # iterate through actions
                for action in actions:
                    # generate successor state
                    successorState = state.generateSuccessor(agent, action)
                    # pass to value to run expectimax on the ghosts
                    successorVal = value(depth, successorIndex, successorState)
                    # replace existing value if expectimax returns a larger value
                    v = max([v, (successorVal[0], action)], key=lambda x: x[0])
            else:
                # if no available actions, run evaluationfucntion
                return value(self.depth, 0, state)

            return v

        def exp_val(depth, agent, state):
            """Evaluates chance nodes with uncertain outcomes using weighted average of succesive nodes"""
            v = (0, None)  # initialize expectimax value for ghosts
            #grab legal actions for ghost
            actions = state.getLegalActions(agent)

            successorIndex = agent + 1
            # if the index reaches the number of agents, pacman is next agent
            #this will only occur after expectimax runs on all ghosts
            if gameState.getNumAgents() == successorIndex:
                successorIndex = 0
                depth += 1

            num_actions = len(actions)
            if actions:
                for action in actions:
                    #generate successor to agent
                    successorState = state.generateSuccessor(agent, action)
                    #find the value of the successor
                    successorVal = value(depth, successorIndex, successorState)
                    # running total of children's expectimax values
                    v_sum = v[0] + successorVal[0]
                    v = (v_sum, action)
                # weight the sum of expected values
                # with the probablity of an action occuring over all available actions (uniform distribution)
                v = (v[0] / float(num_actions), None)
            else:
                # if no available actions, run evaluationfucntion
                return value(self.depth, 0, state)

            return v

        # return expectimax action
        return value(0, 0, gameState)[1]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # State data
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # GHOSTS
    #if ghosts are close and scared, or far away add points, if ghosts are not scared and close, lose points
    sumGhostDist = 0
    minGhostDist = (float("inf"), None)
    scaredBonus = 0
    for ghost in newGhostStates:
        ghostPos = ghost.getPosition()
        ghostDist = manhattanDistance(newPos, ghostPos)
        # finding the minimum ghost position from the current position in order to determine contingencies
        minGhostDist = min(minGhostDist, (ghostDist, ghostPos), key=lambda x: x[0])
        #if ghosts are scared, no penalties for being close to a ghost will occur
        #give incentive for pacman to eat ghosts while they are scared
        if ghost.scaredTimer > 0:
            scaredBonus += 30 * len(newGhostStates)
        else:
            #If ghost is further than one tile away, don't worry about ghost
            #Increase score by small amount
            if ghostDist > 1:
                sumGhostDist += 1 / float(ghostDist)  # 1/ghost_dist to increment sum relative to the current ghost
            # if at 1 place or closer decrease score, not a valid move for the current state
            elif ghostDist > 0:
                sumGhostDist -= 60 * 1 / float(ghostDist)  # DANGER - decrement by a LARGE and relative value
        # Final ghost metric for game score
        ghostScore = scaredBonus + sumGhostDist
    # FOOD
    """Food is usually abundant and is clustered next to other food nodes so pacman tries to 
    follow a trail or clear a majority of the nodes in an area before moving on"""
    foodList = newFood.asList()
    minFoodDist = (float("inf"), None)
    foodScore = 0
    for foodPos in foodList:
        foodDist = manhattanDistance(newPos, foodPos)
        #find the closest food to pacman by using smallest manhattan distance
        minFoodDist = min(minFoodDist, (foodDist, foodPos), key=lambda x: x[0])
    foodScore = 0
    # check if there is a food node stranded in the farther end of the board
    # and move towards the node if a ghost is not obstructing the path
    if minGhostDist and minFoodDist[1]:
        if minFoodDist[0] > minGhostDist[0] and not ( \
                        newPos[0] < minGhostDist[1][0] < minFoodDist[1][0] and newPos[1] < minGhostDist[1][1] <
                        minFoodDist[1][1] and \
                        newPos[0] > minGhostDist[1][0] > minFoodDist[1][0] and newPos[1] > minGhostDist[1][1] >
                        minFoodDist[1][1]):
            foodScore += 15
    # if a food node exists right next to pacman, add a large number to make pacman eat food
    #decrease foodScore bonus as min distance becomes further away
    if minFoodDist <= 1:
        foodScore += 40
    elif minFoodDist <= 2:
        foodScore += 25
    elif minFoodDist <= 3:
        foodScore += 15

    foodScore += 10 / float(minFoodDist[0])
    foodPenalty = -len(foodList)
    foodScore += foodPenalty
    # PELLET
    powerPellets = currentGameState.getCapsules()
    powerPelletProximityBonus = 0
    minPowerPelletDist = float("-inf")
    if powerPellets:
        for pelletPos in powerPellets:
            # get distance to closest power pellet
            minPowerPelletDist = min(minPowerPelletDist, manhattanDistance(newPos, pelletPos))
            #if ghosts are not already scared
            #and a power pellet is closer than the min ghost distance
            #give incentive for pacman to grab powerpellet
        if abs(minGhostDist[0] - minPowerPelletDist) < 2 and newScaredTimes == 0:
            powerPelletProximityBonus += 20
        powerPelletProximityBonus +=  (
                    10 / float(minPowerPelletDist if minPowerPelletDist > 0 else 10))

    # total gameState score, foodScore, ghostScore, and the powerPellet bonus to get final score
    finalScore = currentGameState.getScore() + foodScore + ghostScore + powerPelletProximityBonus

    return finalScore
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction


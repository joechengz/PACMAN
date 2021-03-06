# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    from util import manhattanDistance
    if successorGameState.isWin():
        return 99999
    #score for food distance
    res = scoreEvaluationFunction(successorGameState)
    minFoodDistance = 99999
    for food in newFood.asList():
        minFoodDistance = min(minFoodDistance,manhattanDistance(newPos,food))
    #score for scared-ghost
    for newghost in newGhostStates:
        ghostdist = manhattanDistance(newPos,newghost.getPosition())
        if newghost.scaredTimer>ghostdist:
            res+=newghost.scaredTimer-ghostdist
    #score for ghost
    minGhostDistance = 99999
    for ghost in newGhostStates:
        if ghost.scaredTimer==0:
            minGhostDistance = min(minGhostDistance,manhattanDistance(newPos,ghost.getPosition()))
    #if there are all scared ghost
    if minGhostDistance==99999:
        minGhostDistance=0
    #score for walls
    walls = currentGameState.getWalls()       
    x,y = newPos
    if walls[x][y]:
        res-=100;
    #score for eating food
    newleftfood = successorGameState.getNumFood()
    return res+minGhostDistance-minFoodDistance-10*newleftfood

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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    res=self.getaction_helper(0, gameState)
    return res[0]

  def getaction_helper(self,depth,gameState):
    if depth==self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
        return (None,self.evaluationFunction(gameState))
    if depth%gameState.getNumAgents()==0:
        return self.maxFunction(gameState,depth)
    else:
        return self.minFunction(gameState,depth)
    
  def maxFunction(self,gameState,depth):
    if depth ==self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
    actions = gameState.getLegalActions(0)
    if len(actions)==0:
        return (None,self.evaluationFunction(gameState))
    maxval = (None,-99999)
    for action in actions:
        successor = gameState.generateSuccessor(0, action)
        tmpval = self.getaction_helper(depth+1,successor)
        if tmpval[1]>maxval[1]:
            maxval = (action,tmpval[1])
    return maxval
    
  def minFunction(self,gameState,depth):
    if depth==self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
    actions = gameState.getLegalActions(depth%gameState.getNumAgents())
    if len(actions)==0:
        return (None,self.evaluationFunction(gameState))
    minval = (None,99999)
    for action in actions:
        successor = gameState.generateSuccessor(depth%gameState.getNumAgents(),action)
        tmpval = self.getaction_helper(depth+1,successor)
        if tmpval[1]<minval[1]:
            minval = (action,tmpval[1])
    return minval

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    res = self.getaction_helper(0,gameState,-99999,99999)
    return res[0]
  
  def getaction_helper(self,depth,gameState,alpha,beta):
    if depth==self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
        return (None,self.evaluationFunction(gameState))
    if depth%gameState.getNumAgents()==0:
        return self.maxFunction(gameState,depth,alpha,beta)
    else:
        return self.minFunction(gameState,depth,alpha,beta)
      
      
  def maxFunction(self,gameState,depth,alpha,beta):
    if depth==self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
        return (None,self.evaluationFunction(gameState))
    actions = gameState.getLegalActions(0)
    if len(actions)==0:
        return (None, self.evaluationFunction(gameState))
    maxval = (None,-99999)
    for action in actions:
        successor = gameState.generateSuccessor(0,action)
        tmpval = self.getaction_helper(depth+1, successor, alpha, beta)
        if tmpval[1]>maxval[1]:
            maxval=(action,tmpval[1])
        if maxval[1]>beta:
            return maxval
        alpha = max(alpha,maxval[1])
    return maxval
      
  def minFunction(self,gameState,depth,alpha,beta):
    if depth==self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
        return (None,self.evaluationFunction(gameState))
    actions = gameState.getLegalActions(depth%gameState.getNumAgents())
    if len(actions)==0:
        return (None,self.evaluationFunction(gameState))
    minval = (None,99999)
    for action in actions:
        successor = gameState.generateSuccessor(depth%gameState.getNumAgents(),action)
        tmpval = self.getaction_helper(depth+1, successor, alpha, beta)
        if tmpval[1]<minval[1]:
            minval = (action,tmpval[1])
        if minval[1]<alpha:
            beta = min(beta,minval[1])
    return minval

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
    res = self.getaction_helper(0, gameState)
    return res[0]
  def getaction_helper(self,depth,gameState):
    if depth==self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
        return (None,self.evaluationFunction(gameState))
    if depth%gameState.getNumAgents()==0:
        return self.maxFunction(gameState,depth)
    else:
        return self.expFunction(gameState,depth)
    
  def maxFunction(self,gameState,depth):
    actions = gameState.getLegalActions(0)
    if len(actions)==0:
        return (None, self.evaluationFunction(gameState))
    
    maxval = (None,-99999)
    for action in actions:
        successor = gameState.generateSuccessor(0,action)
        tmpval = self.getaction_helper(depth+1, successor)
        if tmpval[1]>maxval[1]:
            maxval = (action,tmpval[1])
    return maxval

  def expFunction(self,gameState,depth):
    actions = gameState.getLegalActions(depth%gameState.getNumAgents())
    if len(actions)==0:
        return (None,self.evaluationFunction(gameState))
    
    pro = 1.0/len(actions)
    expval = 0
    for action in actions:
        successor = gameState.generateSuccessor(depth%gameState.getNumAgents(),action)
        tmpval = self.getaction_helper(depth+1, successor)
        expval =expval+tmpval[1]*pro
    return (None,expval)

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  #util.raiseNotDefined()
  from util import manhattanDistance
  newPos = currentGameState.getPacmanPosition()
  newFood = currentGameState.getFood()
  newGhostStates = currentGameState.getGhostStates()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
  
  
  score = currentGameState.getScore()
  ghostDistances = [manhattanDistance(newPos,newghost.getPosition()) for newghost in newGhostStates]
  
  oldfoodnum = currentGameState.getNumFood()
  
  #score for going to near foods
  nearFoodDist = 100
  for i, item in enumerate(newFood):
      for j, foodItem in enumerate(item):
          nearFoodDist = min(nearFoodDist, manhattanDistance(newPos, (i, j)) if foodItem else 100)
  nearfoodscore = 1.0/nearFoodDist       
  #score for ghost
  ghostscore = 0
  for index in range(len(ghostDistances)):
      if newScaredTimes[index]<1:
          if ghostDistances[index]<3:
              ghostscore+=-20+ghostDistances[index]**4
          else:
              ghostscore+=-1.0/ghostDistances[index]
  
  #score for pelets
  pelets = currentGameState.getCapsules()
  nearpeletedist = min(100,[manhattanDistance(newPos,pelet) for pelet in pelets])
  nearpeletescore = 1.0/nearpeletedist
  peletenum = len(pelets)
  
  if all((t>0 for t in newScaredTimes)):
      return score+nearfoodscore-2*ghostscore +3*nearpeletescore -1.5*oldfoodnum
  else:
      return score+nearfoodscore+2*ghostscore +3*nearpeletescore -1.5*oldfoodnum-8*peletenum

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


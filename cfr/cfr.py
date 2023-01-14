import bloodRiverGame
import numpy as np
from copy import deepcopy


class bloodyStream:

    def __init__(self):
        self.strategy = {}
        self.nodeMap = {}


    def createNode(self,):
        '''Creates a node for the infoset if it doesn't exist'''
        



    def lcfr(self, infoset, π_i={}, i=0, t=0):
        '''Linear Counterfactual Regret Minimization'''

        #get the gamestate node if it exists
        #if it doesn't exist, create it
        gameState = None
        if infoset in self.nodeMap: gameState = self.nodeMap[infoset]
        else:
            self.nodeMap[infoset] = bloodRiverGame.bloodRiver()
            gameState = self.nodeMap[infoset]


        #base case?
        if gameState.isTerminal():
            return gameState.getPayout()
        
        #we should consider the chance node case if performance is unsatisfactory
        #note that chance node outcomes can be precomputed
        
        I = gameState.infoSet()

        #σ[t][I] = regret_matching(R[t][I])
        strategy = gameState.getStrategy()
        
          
        #game instance should have a strategy field
        #when the regrets are added, we should make sure that the strategy is updated
        #this is covered in the thesis somewhere

        if gameState.currentPlayer == i:
            # traverse all available actions, to illiminate influence of σ_i
            v[I] = {a: lcfr(h + [a], {**π_i, P(h): π_i[P(h)] * σ[t][I][a]}, i, t) 
                                    for a in A[I]}
        else:
            # sample one a from A[I]
            a = sample(A[I], σ[t][I])
            v[I][a] = lcfr(h + [a], {**π_i, P(h): π_i[P(h)] * σ[t][I][a]})
        
        #Here, we need to compute the expected regret over the available actions
        #regret = some function

        #then for each action, add to the regret for the next iteration
        #and then update the strategy * probability of reaching that action

        return regret


    
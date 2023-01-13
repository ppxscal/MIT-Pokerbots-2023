import bloodRiverGame
import numpy as np

class node:
    pass

class bloodyStream:

    def __init__(self):
        self.strategy = {}

    def regretMatch(self):
        pass

    def mccfr(self, gameState=bloodRiverGame.Game(), π_i={}, i=0, t=0):
        '''Monte Carlo Counterfactual Regret Minimization'''

        #base case?
        if gameState.isTerminal():
            return gameState.getPayout()
        
        I = gameState.infoSet()

        #σ[t][I] = regret_matching(R[t][I]) 
        #game instance should have a strategy field
        #when the regrets are added, we should make sure that the strategy is updated
        #this is covered in the thesis somewhere

        if gameState.currentPlayer == i:
            # traverse all available actions, to illiminate influence of σ_i
            v[I] = {a: mccfr(h + [a], {**π_i, P(h): π_i[P(h)] * σ[t][I][a]}, i, t) 
                                    for a in A[I]}
        else:
            # sample one a from A[I]
            a = sample(A[I], σ[t][I])
            v[I][a] = mccfr(h + [a], {**π_i, P(h): π_i[P(h)] * σ[t][I][a]})
        
        #Here, we need to compute the expected regret over the available actions
        #regret = some function

        #then for each action, add to the regret for the next iteration
        #and then update the strategy * probability of reaching that action

        return regret


    
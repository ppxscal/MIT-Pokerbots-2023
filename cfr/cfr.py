from bloodRiverGame import bloodRiver
import numpy as np
from copy import deepcopy


class bloodyStream:

    def __init__(self):
        #access via dic[infoset][action]
        #We define the action strategy/regret indices as follows:
        #['FOLD', 'CALL', 'RAISE', 'CHECK', 'BET']
        #[ 0,      1,      2,       3,       4]
        self.regretSum = {}
        self.strategySum = {}
        self.strategy = {}


    def get_strategy(self, infoset, action):
        '''Returns the strategy for the current player via regret matching'''

        normalizingSum = 0

        for i in range(len(self.regretSum)):
            self.strategy[i] = self.regretSum[i] if self.regretSum[i] > 0 else 0
            normalizingSum += self.strategy[i]

        if normalizingSum > 0: 
            for i in range(len(self.strategy)): 
                self.strategy[i] = self.strategy[i]/normalizingSum
        else: self.strategy = np.full((1,len(self.strategy)), 1/len(self.strategy))

        self.strategySum += self.strategy

        return self.strategy


    def lcfr(self, game, probabilities):
        '''Linear Counterfactual Regret Minimization
        probabilities is a vector of probabilities that the ith player will reach the current node
        '''

        #base case
        if gameState.isTerminal():
            return gameState.getPayout()
        
        #we should consider the chance node case if performance is unsatisfactory
        #note that chance node outcomes can be precomputed
        infoset = game.infoSet()
        actions = gameState.getActions()
        player = infoset['player']

        #create the node if it doesn't exist
        if infoset not in self.strategySum[player]:
            self.strategySum[player][infoset] = np.zeros(len(actions))
            self.regretSum[player][infoset] = np.zeros(len(actions))

        #get the strategy for the current player
        strategy = game.getStrategy()
        actionUtilities = np.zeros(shape = (len(actions), 2))
        nodeUtilities = np.zeros(2)
          
        #for each action, recursively call lcfr
        for i in range(len(actions)):
            gameCopy = deepcopy(game)
            gameCopy.makeMove(actions[i])
            probabilityCopy = np.copy(probabilities)
            probabilityCopy[player] *= strategy[i]
            actionUtilities[i] = self.lcfr(copy, probabilityCopy)

            for player in range(2):
                nodeUtilities[player] += actionUtilities[actions[i], player] * strategy[action]

        #from here collect the counterfactual regrets
        for i in range(len(actions)):
            counterfacProb = 1
            for i in range(2):
                if i != player: counterfacProb *= probabilities[i]
        
            #update the regrets
            regret = actionUtilities[actions[i], player] - nodeUtilities[player]
            self.regretSum[player][infoset][actions[i]] += counterfacProb * regret
            self.strategySum[player][infoset][actions[i]] += counterfacProb * strategy[actions[i]]

        return nodeUtilities


    def train(self, iterations):
        '''Trains the CFR algorithm for the given number of iterations'''

        for i in range(iterations):
            game = bloodRiver()
            game.beginGame()
            self.lcfr(game, [1, 1])

        #compute the average strategy
        for player in range(2):
            for infoset in self.strategySum[player]:
                normalizingSum = 0
                for i in range(len(self.strategySum[player][infoset])):
                    normalizingSum += self.strategySum[player][infoset][i]
                for i in range(len(self.strategySum[player][infoset])):
                    if normalizingSum > 0:
                        self.strategySum[player][infoset][i] /= normalizingSum
                    else:
                        self.strategySum[player][infoset][i] = 1/len(self.strategySum[player][infoset])

        return self.strategySum


if __name__ == '__main__':
    cfr = bloodyStream()
    cfr.train(100000)
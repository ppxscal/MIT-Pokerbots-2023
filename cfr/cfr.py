from bloodRiverGame import bloodRiver
import numpy as np
from copy import deepcopy
from bloodRiverGame import hashabledict
import eval7


class bloodyStream:

    def __init__(self):
        #access via dic[infoset][action]
        #We define the action strategy/regret indices as follows:
        #['FOLD', 'CALL', 'RAISE', 'CHECK', 'BET']
        #[ 0,      1,      2,       3,       4]
        self.regretSum = {0: {}, 1: {}}
        self.strategySum = {0: {}, 1: {}}
        self.strategy = {0: {}, 1: {}}
        self.actionIndex = {'FOLD': 0, 'CALL': 1, 'RAISE': 2, 'CHECK': 3, 'BET': 4}
    

    def getStrategy(self, infohash, currentPlayer):
        '''Returns the strategy for the current player via regret matching'''

        normalizingSum = 0
        #print(self.regretSum, 'hiiiiiiiiiiiiiii')

        for i in range(5):
            self.strategy[currentPlayer][infohash] = self.regretSum[currentPlayer][infohash] if sum(self.regretSum[currentPlayer][infohash]) > 0 else 0
            normalizingSum += self.strategy[currentPlayer][infohash]

        if normalizingSum > 0: 
            for i in range(5): 
                self.strategy[currentPlayer][infohash] = self.strategy[currentPlayer][infohash]/normalizingSum
        else: self.strategy[currentPlayer][infohash] = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

        self.strategySum[currentPlayer][infohash] += self.strategy[currentPlayer][infohash]

        return self.strategy
    
    def copyGame(self, game):
        '''Copies an intance of the game object'''

        gameCopy = bloodRiver()
        attributes = vars(game)
        eval7Copy = lambda lst: [eval7.Card(str(card)) for card in lst]

        #hard coding since I can't find a way to reference the attributes iteratively
        gameCopy.deck = eval7Copy(game.deck)
        gameCopy.history = list(game.history)
        gameCopy.stack = np.copy(game.stack)
        gameCopy.currentPlayer = game.currentPlayer
        gameCopy.dealer = game.dealer
        gameCopy.winner = game.winner
        gameCopy.isTerminal = game.isTerminal
        gameCopy.cards = [eval7Copy(game.cards[0]), eval7Copy(game.cards[1])]
        gameCopy.board = eval7Copy(game.board)
        gameCopy.street = game.street
        gameCopy.firstMove = game.firstMove

        return gameCopy


    def lcfr(self, game, probabilities):
        '''Linear Counterfactual Regret Minimization
        probabilities is a vector of probabilities that the ith player will reach the current node
        '''

        #base case
        if game.isTerminal:
            return game.getPayout()
        
        #we should consider the chance node case if performance is unsatisfactory
        #note that chance node outcomes can be precomputed
        infoset = game.infoSet()
        infohash = hash(infoset)
        actions = game.getActions()
        player = infoset['player']

        #create the node if it doesn't exist
        if infohash not in self.strategySum.get(player, {}):
            self.strategySum[player][infohash] = np.zeros(5)
            self.regretSum[player][infohash] = np.zeros(5)
            self.strategy[player][infohash] = np.zeros(5)

        #get the strategy for the current player
        strategy = self.getStrategy(infohash, player)
        actionUtilities = np.array([[0,0,0,0,0],[0,0,0,0,0]])
        nodeUtilities = np.zeros(2)
          
        #for each action, recursively call lcfr
        for action in actions:
            gameCopy = self.copyGame(game)
            actIndx = self.actionIndex[action]
            print(gameCopy.infoSet())
            gameCopy.makeMove(action)
            print(gameCopy.infoSet(), '\n')
            probabilityCopy = np.copy(probabilities)
            probabilityCopy[player] *= strategy[player][infohash][actIndx]
            actionUtilities[actIndx] = self.lcfr(gameCopy, probabilityCopy)

            for playerIndex in range(2):
                nodeUtilities[playerIndex] += actionUtilities[playerIndex][actIndx] * strategy[player][infohash][actIndx]

        #from here collect the counterfactual regrets
        for i in range(5):
            counterfacProb = 1
            for i in range(2):
                if i != player: counterfacProb *= probabilities[i]
        
            #update the regrets
            regret = actionUtilities[actIndx][actions[i]] - nodeUtilities[player]
            self.regretSum[player][infoset][actions[i]] += counterfacProb * regret
            self.strategySum[player][infoset][actions[i]] += counterfacProb * strategy[actions[i]]

        return nodeUtilities


    def train(self, iterations):
        '''Trains the CFR algorithm for the given number of iterations'''

        for i in range(iterations):
            game = bloodRiver()
            game.beginGame(i%2)
            self.lcfr(game, np.array([1, 1]))

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
    trainer = bloodyStream()
    trainer.train(1)
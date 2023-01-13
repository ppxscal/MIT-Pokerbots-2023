from game import Game
import eval7
from types import MappingProxyType
import numpy as np

class bloodRiver(Game):
    
    def __init__(self):
        self.deck = eval7.Deck()
        self.deck.shuffle()
        self.history = []
        self.stack = np.array([400,400])
        self.pot = np.array([0,0])
        self.currentPlayer = 0
        self.dealer = 0
        self.winner = -1
        self.isTerminal = False
        self.cards = [self.deck.deal(2), self.deck.deal(2)]
        self.board = self.deck.deal(5)
        self.street = 0
        self.firstMove = True
        #We define the action strategy/regret indices as follows:
        #['FOLD', 'CALL', 'RAISE', 'CHECK', 'BET']
        #[ 0,      1,      2,       3,       4]

        self.regretSum = np.zeros(5)
        self.strategySum = np.zeros(5)
        self.strategy = np.zeros(5)

    def get_strategy(self, ):
        '''Returns the strategy for the current player'''
        normalizingSum = 0
        for i in range(len(self.regretSum)):
            self.strategy[i] = self.regretSum[i] if self.regretSum[i] > 0 else 0
            normalizingSum += self.strategy[i]

        if normalizingSum > 0: 
            for i in range(len(self.strategy)): 
                self.strategy[i] = self.strategy[i]/normalizingSum
        else: self.strategy = np.full((1,len(self.strategy)), 1/len(self.strategy))

        #self.strategySum += self.strategy
        #mccfr calls for a different way ofupdating the strategy
        #http://mlanctot.info/files/papers/PhD_Thesis_MarcLanctot.pdf 
        
        return self.strategy

    
    def beginGame(self, dealer):
        '''Start the game'''
        #play blinds
        self.dealer = dealer
        self.stack[self.dealer] -= 1
        self.stack[1-self.dealer] -= 2
        self.pot[self.dealer] += 1
        self.pot[1-self.dealer] += 2
        self.history.append(('BLIND', -1))
        self.street +=1

    def infoSet(self):
        '''Returns the information set hash for the current player. It is all the availble information for that player'''

        infoset = MappingProxyType({'player' : self.currentPlayer, 
                'dealer' : self.dealer,
                'history' : self.history, 
                'cards' : self.cards[self.currentPlayer],
                'actions' : self.getActions(),
                'street': self.street,
                'terminal': self.isTerminal,
                'pot': self.pot,
                'stack': self.stack,}
                )
        print(infoset, '\n')
        return infoset
        
    def getActions(self):
        '''Returns a set of all possible actions for the current player'''
        #Make sure logic is correct TODO

        if self.isTerminal:
            return({})

        if self.street == 0: return frozenset({'BLIND'})

        if self.street <= 5:
            if self.firstMove:
                if self.street == 1 and self.currentPlayer == self.dealer:
                    return frozenset({'FOLD', 'CALL', 'RAISE'})
                if self.street > 1 and self.currentPlayer != self.dealer:
                    return frozenset({'CHECK', "BET"})
            
            if self.street == 1 and self.history[-1] == 'CALL' and self.currentPlayer == self.dealer:
                return frozenset({'CHECK', 'RAISE'})

            if self.history[-1][0] in {'BET', 'RAISE'}:
                return frozenset({'CHECK', 'RAISE', 'CALL', 'FOLD'})
        
            return frozenset({'BET', 'FOLD', 'CHECK'})
        else:
            self.isTerminal = True
            #the expected number of additional rounds after the river is 1 we can handle the other cases manually
            print('Game is terminal after 5 streets')
            return frozenset({})
        

    def getWinner(self):
        '''Returns the winning player'''
        player0HS = eval7.evaluate(self.player0Cards + self.board)
        player1HS = eval7.evaluate(self.player1Cards + self.board)
        self.winner = 0 if player0HS > player1HS else 1
        return self.winner

    def makeMove(self, action):
        '''Updates the game state based on the action taken'''

        if self.isTerminal:
            raise Exception('Game is already terminal')
        
        actions = self.getActions()

        if action[0] not in actions:
            raise Exception('Invalid action', action, actions)
        
        print('Making move: ', action, '\n')

        if action[0] == 'FOLD':
            self.isTerminal = True
            self.winner = 1-self.currentPlayer
            self.history.append(('FOLD', -1))
        
        elif action[0] == 'CHECK':
            self.currentPlayer = 1-self.currentPlayer     
            if self.history[-1][0] == 'CHECK' and not self.firstMove:
                self.firstMove = True
                self.street += 1
                self.history.append(('CHECK', -1))
                return
            self.history.append(('CHECK', -1))
        
        elif action[0] == 'CALL':
            callValue = abs(self.pot[0]-self.pot[1])
            self.stack[self.currentPlayer] -= callValue
            self.pot[self.currentPlayer] += callValue
            self.firstMove = True
            self.currentPlayer = 1-self.dealer
            if not(self.street == 1 and self.currentPlayer == self.dealer and len(self.history) == 0):
                self.street += 1
            self.history.append(('CALL', -1))
            return
        
        elif action[0] == 'RAISE':
            if self.history[-1][0] != 'BET' and self.history[-1][0] != 'RAISE':
                raise Exception('Not allowed to Raise')

            #if responding to a bet or raise
            if self.history[-1][0] in {'BET', 'RAISE'}:
                if action[1] <= self.history[-1][1]:
                    if self.history[-1][1] > self.stack[self.currentPlayer]:
                        print('The only raise should be all in')
                        action = ('RAISE', self.stack[self.currentPlayer])
                    else:
                        raise Exception('Raise must be larger than previous bet or raise')
                if action[1] > self.stack[1 - self.currentPlayer]:
                    raise Exception('Cannot raise more than what opponent is able to call')           

            deficit = abs(self.pot[0]-self.pot[1])
            contribAmt = deficit + action[1]

            self.stack[self.currentPlayer] -= contribAmt
            self.pot[self.currentPlayer] += contribAmt
            self.currentPlayer = 1-self.currentPlayer
            self.history.append(('RAISE ', action[1]))
            return
        
        elif action[0] == 'BET':
            if action[1] < 2:
                raise Exception('Minimum bet is 2')
            if action[1] > max(self.stack):
                raise Exception('Cannot bet more than stack')
            self.stack[self.currentPlayer] -= action[1]
            self.pot[self.currentPlayer] += action[1]
            self.history.append(('BET', action[1]))
            self.currentPlayer = 1-self.currentPlayer
        
        if self.firstMove: self.firstMove = False

    def getPayout(self):
        '''Returns the payout for the winner'''
        if not self.isTerminal:
            raise Exception('Game is not terminal')
        return sum(self.pot)


game = bloodRiver()
game.beginGame(0)
game.infoSet()
game.makeMove(('CALL', -1))
game.infoSet()
game.makeMove(('CHECK', -1))
game.infoSet()
game.makeMove(('CHECK', -1))
game.infoSet()
game.makeMove(('CHECK', -1))
game.infoSet()
game.makeMove(('BET', 200))
game.infoSet()
game.makeMove(('CALL', -1))
game.infoSet()
game.makeMove(('BET', 70))
game.infoSet()
game.makeMove(('RAISE', 71))
game.infoSet()
game.makeMove(('FOLD', -1))
print(game.getPayout())


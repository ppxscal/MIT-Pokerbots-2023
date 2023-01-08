from game import Game
import random
import copy

class KuhnGame(Game):
    '''Kuhn Poker Game Class'''

    def __init__(self):
        self.cards = []
        self.history = ''
        self.pot = [0,0]
        self.currentPlayer = 0
        self.winner = -1
        self.isTerminal = False

    def beginGame(self):
        '''Begins a new Game'''
        
        #deal cards 
        self.cards = ['K', 'Q', 'J']
        #by convention, player 0 has card in index 0 and player 1 has card in index 1
        random.shuffle(self.cards)

        history = ''
        pot = [0,0]
        currentPlayer = 0
        winner = -1
        isTerminal = False

    def infoSet(self):
        '''Returns the information set hash for the current player. It is all the availble information for that player'''
        
        return {'Player:' : self.currentPlayer, 
                'History:' : self.history, 
                'Cards:' : self.cards[self.currentPlayer],
                'Actions:' : self.getActions(),
                'cards:' : self.cards}

    def getActions(self):
        '''Returns a set of all possible actions for the current player'''

        if self.history != '' and self.history[-1] == 'BET':
            return {'CALL', 'FOLD'}
        return {'BET', 'CHECK'}
    
    def getWinner(self):
        '''Returns the winner of the game'''
        if self.cards[0] == 'K': winner = 0
        elif self.cards[1] == 'K': winner = 1
        elif self.cards[0] == 'Q': winner = 0
        else: winner = 1
        return winner

    def makeMove(self, action):
        '''Makes a move for the current player'''

        if self.isTerminal:
            raise ValueError('Game is finished')
        
        if len(self.history) >= 4:
            raise ValueError('Game is finished')
        
        if action not in self.getActions():
            raise ValueError('Invalid Action')
    
        if action == 'BET':
            self.pot[self.currentPlayer] += 1
        elif action == 'CHECK':
            if len(self.history) == 1:
                assert(self.history[0] == 'CHECK')
                self.winner = 0
                self.isTerminal = True
        elif action == 'FOLD':
            self.winner = 1 - self.currentPlayer
            self.isTerminal = True
        elif action == 'CALL':
            self.pot[self.currentPlayer] += 1
            self.winner = 0
            self.isTerminal = True
        else:
            raise ValueError('Invalid Action')

        self.history += action
        self.currentPlayer = 1 - self.currentPlayer

    def getPayout(self):
        '''Return a payout vector for a finished game'''
        if not self.isTerminal:
            raise ValueError('Game is not finished')
        if self.winner == -1:
            return [0,0]
        
        monies = sum(self.pot)
        if self.winner == 0:
            return [monies - self.pot[self.winner], self.pot[self.winner]]
        return [monies - self.pot[self.winner], self.pot[self.winner]]
    
# game = KuhnGame()
# game.beginGame()
# print(game.infoSet())


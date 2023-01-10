from game import Game
import eval7

class bloodRiver(Game):
    
    def __init__(self):
        self.deck = eval7.Deck()
        self.deck.shuffle()
        self.history = []
        self.pot = [400,400]
        self.currentPlayer = 0
        self.dealer = 0
        self.winner = -1
        self.isTerminal = False
        self.player0Cards = deck.deal(2)
        self.player1Cards = deck.deal(2)
        self.board = deck.deal(3)
        self.street = 0
        self.firstBet = True

    def infoSet(self):
        pass    
        
    def getActions(self):
        '''Returns a set of all possible actions for the current player'''
        #Make sure logic is correct TODO

        if self.street == 0: return frozenset({'BLIND'})

        if self.firstBet:
            if self.street == 1 and self.currentPlayer == self.dealer:
                return frozenset({'FOLD', 'CALL', 'RAISE'})
            if self.street > 1 and self.currentPlayer != self.dealer:
                return frozenset({'CHECK', "BET"})

        if self.history[-1] in {'BET', 'RAISE'}:
            return frozenset({'CHECK', 'BET', 'RAISE', 'CALL', 'FOLD'})
        
        return frozenset({'CALL', 'BET', 'FOLD', 'CHECK'})
        

    def getWinner(self):
        '''Returns the winning player'''
        player0HS = eval7.evaluate(self.player0Cards + self.board)
        player1HS = eval7.evaluate(self.player1Cards + self.board)
        self.winner = 0 if player0HS > player1HS else 1
        return self.winner

    def makeMove(self, action):
        pass    

    def getPayout(self):
        pass    

    

    

game = bloodRiver()
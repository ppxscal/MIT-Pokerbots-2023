from game import Game
import eval7

class bloodRiver(Game):
    
    def __init__(self):
        self.deck = eval7.Deck()
        self.deck.shuffle()
        self.history = []
        self.stack = [400,400]
        self.pot = []
        self.currentPlayer = 0
        self.dealer = 0
        self.winner = -1
        self.isTerminal = False
        self.player0Cards = deck.deal(2)
        self.player1Cards = deck.deal(2)
        self.board = deck.deal(3)
        self.street = 0
        self.firstBet = True
    
    def beginGame(dealer):
        '''Start the game'''
        #play blinds
        self.dealer = dealer
        self.stack[self.dealer] -= 1
        self.stack[1-self.dealer] -= 2
        self.pot += 3
        self.history.append('BLIND')
        self.currentPlayer = 1-self.dealer
        self.street +=1

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
        
        if self.street == 1 and self.history[-1] == 'CALL' and self.currentPlayer == self.dealer:
            return frozenset({'CHECK', 'RAISE'})

        if self.history[-1] in {'BET', 'RAISE'}:
            return frozenset({'CHECK', 'BET', 'RAISE', 'CALL', 'FOLD'})
        
        return frozenset({'CALL', 'BET', 'FOLD', 'CHECK'})
        

    def getWinner(self):
        '''Returns the winning player'''
        player0HS = eval7.evaluate(self.player0Cards + self.board)
        player1HS = eval7.evaluate(self.player1Cards + self.board)
        self.winner = 0 if player0HS > player1HS else 1
        return self.winner

    def makeMove(self, action, value=0):
        '''Updates the game state based on the action taken'''

        if self.isTerminal:
            raise Exception('Game is already terminal')
        
        #the expected number of additional rounds after the river is 1 we can handle the other cases manually

        if self.street > 5:
            self.isTerminal = True
            print('Game is terminal after 5 streets')
        
        actions = self.getActions()

        if action not in actions:
            raise Exception('Invalid action')
        
        self.street += 1

        if action == 'FOLD':
            self.isTerminal = True
            self.winner = 1-self.currentPlayer
            self.history.append('FOLD')
            return
        
        if action == 'CHECK':
            self.currentPlayer = 1-self.currentPlayer     
            self.history.append('CHECK')
            if self.history[-1] == 'CHECK':
                self.firstBet = True
                self.winner = self.getWinner()
            return
        
        if action == 'CALL':
            callValue = abs(pot[0]-pot[1])
            self.stack[self.currentPlayer] -= callValue
            self.pot[self.currentPlayer] += callValue
            self.firstBet = True
            if not(self.street == 1 and self.currentPlayer == self.dealer and len(self.history) == 0):
                self.street += 1
            return
        
        if action == 'RAISE':
            if self.history[-1] != 'BET' and self.history[-1] != 'RAISE':
                raise Exception('Not allowed to Raise')
            self.stack[self.currentPlayer] -= value
            self.pot[self.currentPlayer] += value
            self.currentPlayer = 1-self.currentPlayer
            self.firstBet = False
            self.history.append('RAISE ' + str(value))
            return
        
        if action == 'BET':
            if value < 2:
                raise Exception('Minimum bet is 2')
        
            self.stack[self.currentPlayer] -= value
            self.pot[self.currentPlayer] += value
            self.firstBet = False
            self.history.append('BET ' + str(value))

        



    def getPayout(self):
        pass    

    

    

game = bloodRiver()
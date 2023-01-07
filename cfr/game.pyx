import cython

cdef class Game():

    cpdef beginGame():
        '''Start a new game'''
        return 0
    
    cpdef makeMove(int move):
        '''Make a move'''
        return 0
    
    cpdef getPayouts():
        '''Returns a vector with payouts for the ith player'''
        return 0
    
    cpdef deepCopy():
        '''Returns a deep copy of the game'''
        return 0 
    
    cpdef infoSet():
        '''Returns the information set of the current player'''
        return 0
    
    cpdef isTerminal():
        '''Returns true if the game is over'''
        return 0
    
    cpdef getNumPlayers():
        '''Returns the number of players'''
        return 0
    
    cpdef playerToAct():
        '''Returns the player to act 0 based indexing'''
        return 0
    
    cpdef actions():
        '''Returns a vector of actions available to the current player'''
        return 0

    

    



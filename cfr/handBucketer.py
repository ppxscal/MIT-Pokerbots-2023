
import eval7
from eval7 import Card
import random
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
import pickle

# ranks = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
# suits = ('c', 'd', 'h', 's')

class bucketer():
    '''
    takes in a hand and returns a bucket
    '''

    def __init__(self):
        pass


    def calc_strength(self, cards, iterations):
        '''method to calculate hand strength of a given hand of greater than 1 card'''

        deck = eval7.Deck()
        eval7Cards = [Card(str(card)) for card in cards]
        score = 0

        for card in eval7Cards:
            deck.cards.remove(card)

        for _ in range(iterations):
            deck.shuffle()

            _COMM = 5
            _OPP = 2

            draw = deck.peek(_COMM + _OPP)

            opp_hole = draw[:_OPP]
            community = draw[_OPP:]

            rivCard = str(community[-1])[1]
            bloodyRound = False if reduce(lambda x,y: x or (rivCard in {'h', 'd'}) , community) else True

            our_hand = eval7Cards +  community
            opp_hand = opp_hole +  community

            if bloodyRound:
                community += deck.peek(1)
                our_value = eval7.evaluate(our_hand + community[:-1])+eval7.evaluate(opp_hand + community[:-1]) * .5
                opp_value = eval7.evaluate(our_hand + community[1:])+eval7.evaluate(opp_hand + community[1:]) * .5
            
            else:
                our_value = eval7.evaluate(our_hand)
                opp_value = eval7.evaluate(opp_hand)

            if our_value > opp_value:
                score += 2
            
            elif our_value == opp_value:
                score += 1

            else:
                score += 0

        hand_strength = score / (2 * iterations)

        print(hand_strength, our_value, opp_value)

        return hand_strength
    
    def equiyDist(self, hole, epochs):
        '''returns the equiy distribution of a given hand for some epocs'''
        
        vals = np.array([])

        for i in range(epochs):
            vals = np.append(vals, self.calc_strength(hole, 25))

        plt.hist(vals, bins=100)
        plt.show()
    
    def preflopAbstraction(self, hole):
        '''returns the preflop abstraction of a given hand in a dictionary'''

        
        #169 ranges -> compute their equity distributions -> bucket them based on relative distance 
        
        



    

if __name__ == '__main__':
    hole = input('Enter hand: ')
    hole = hole.split(',')
    iterations = int(input('Enter iterations: '))
    hole = [Card(hole[0]), Card(hole[1])]
    calcObj = bucketer()
    calcObj.equiyDist(hole, iterations)
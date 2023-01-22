import eval7
from eval7 import Card
import random
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from itertools import combinations
from tqdm import tqdm
from progress.bar import Bar
import pickle
import os




class computer():

    def __init__(self):
        self.ranks = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
        self.suits = ('c', 'd', 'h', 's')
        self.cards = set()
        for rank in self.ranks:
            for suit in self.suits:
                self.cards.add(rank + suit)

    def calc_strength(self, cards, iterations):
        """method to calculate hand strength of a given hand of greater than 1 card"""

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
            bloodyRound = (
                False
                if reduce(lambda x, y: x or (rivCard in {"h", "d"}), community)
                else True
            )

            if bloodyRound:
                community += deck.peek(1)

            our_hand = eval7Cards + community
            opp_hand = opp_hole + community

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

    def allBoards(self, street):
        """returns all possible boards as an iterable""" 
        seen = set()
        for board in combinations(self.cards, 2 + street):
            board = tuple(sorted(list(board)))
            if board not in seen:
                #yield board
                seen.add(board)
        return seen
    
    def lookupGenerator(self):
        
        streets = [('preflop', 0), ('flop', 3), ('turn', 4), ('river', 5)]
        for street in streets:
            print("Generating lookup for " + street[0])
            lookup = {}  

            with Bar('Generating: ' + street[0] + ' lookup', max=len(self.allBoards(street[1]))) as bar:
                for board in self.allBoards(street[1]):
                    lookup[board] = self.calc_strength(board, 1000)
                    bar.next()
                

            if not os.path.exists(street[0] + "Lookup.pkl"):
                with open(street[0] + "Lookup.pkl", "wb") as file:
                    
                    pickle.dump(lookup, file)
                
  



if __name__ == "__main__":
    # hole = input('Enter hand: ')
    # hole = hole.split(',')
    # iterations = int(input('Enter iterations: '))
    # hole = [Card(hole[0]), Card(hole[1])]
    calcObj =computer()
    calcObj.lookupGenerator()

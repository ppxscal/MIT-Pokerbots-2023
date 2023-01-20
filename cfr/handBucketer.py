import eval7
from eval7 import Card
import random
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from itertools import combinations
from alive_progress import alive_bar
import pickle
import os

# ranks = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
# suits = ('c', 'd', 'h', 's')


class bucketer:
    """
    takes in a hand and returns a bucket
    """

    def __init__(self):
        self.ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
        self.suits = ("c", "d", "h", "s")
        self.rankVals = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "T": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14,
        }
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

            _COMM = 6
            _OPP = 2

            draw = deck.peek(_COMM + _OPP)

            opp_hole = draw[:_OPP]
            community = draw[_OPP:]
            numBloody = 0

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

    def equiyDist(self, hand, epochs):
        """returns the equiy distribution of a given hand for some epocs"""

        vals = np.array([])

        for i in range(epochs):
            vals = np.append(vals, self.calc_strength(hand, 50))

        return vals

    def postFlopAbstraction(self):
        """creates the postflop abstraction 7 card hands
           https://upswingpoker.com/board-texture-tips/"""

        boardTextures = {
            "paired",
            "rainbowDisc",
            "rainbowConec",
            "twoToneDisc",
            "twoToneConec",
            "monotoneBlack",
            "monotoneRed"
        }

        def connected(rankCounter):
                vals = self.rankVals
                ranks = sorted([rank for rank in rankCounter])
                if len(ranks) == 2: return False
                if len(ranks) == 1 or vals[ranks[2]] - vals[ranks[1]] == vals[ranks[1]] - vals[ranks[0]]:
                    return True
                else:
                    return False

        def getTexture(board):
            """return the board's texture"""

            board = [str(card) for card in board]
            suitCounter = {}
            rankCounter = {}
            traits = set()

            for card in board:
                for i, counter in enumerate([rankCounter, suitCounter]):
                    if card[i] not in counter:
                        counter[card[i]] = 0
                    counter[card[i]] += 1

            isConec = connected(rankCounter)
            if len(suitCounter) == 3 and not isConec: return "rainbowDisc"
            elif len(rankCounter) == 2: return 'paired'
            elif len(suitCounter) == 3 and isConec: return "rainbowConec"
            elif len(suitCounter) == 2:
                if isConec:return "twoToneConec"
                else: return "twoToneDisc"
            else:
                if 'h' in suitCounter or 'd' in suitCounter: return "monotoneRed"
                else: return "monotoneBlack"
        
        def allBoards(hole):
            """returns all possible boards as a generator"""
            newDeck = set(self.cards)
            newDeck = newDeck - hole
            seen = set()
            for board in combinations(newDeck, 3):
                board = tuple(sorted(list(board)))
                if board not in seen:
                    yield board
                    seen.add(board)
    
        def flopAbstractor():
            '''Iterate through possible flops, 
            for each group - calculate equity distribution,
            use emd to create points in 4d space against flopLookups
            100 k-means clusters which are the buckets
            '''
            equities = {}
            preflops = set()

            for cards in combinations(self.cards, 2):
                preflops.add(tuple(sorted(cards)))
            
            for preflop in preflops:
                hole ={card for card in preflop}
                equities[preflop] = {}
                for board in allBoards(hole):
                    hand = [Card(str(card)) for card in preflop+board]
                    distribution = self.equiyDist(hand, 100)
                    equities[preflop][board] = distribution
                    plt.hist(equities[preflop][board], bins=100)
                    plt.show()
                    break
                break
                
            
            # with alive_bar() as bar:
            #     for preflop in preflops:
            #         equities[preflop] = {}

        flopAbstractor()
                     
        def preflopDistribututions():
            
            with open("data/flopLookup.pkl", "rb") as file:
                flopLookup = pickle.load(file)

        def turnAbstractor():
            '''Iterate through possible turn cards, 
            for each group - calculate equity distribution,
            use emd to create points in 4d space against flopLookups
            100 k-means clusters which are the buckets
            '''
            pass
            
        # flopAbstractor()
        



if __name__ == "__main__":
    calcObj = bucketer()
    calcObj.postFlopAbstraction()
    

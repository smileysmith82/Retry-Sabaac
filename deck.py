#No Adjustments Needed Here
#Ready to Use

import random
import copy
import time
from cards import Card

class Deck():
    def __init__(self):
        self.deck = []
        self.suits = ["C", "S", "T"]
        for suit in self.suits:
            for rank in range (1,11):
                self.deck.append(Card(rank,suit))
                self.deck.append(Card(-rank,suit))
        for i in range (2):
            self.deck.append(Card(0, ''))
        self.shuffled_deck = []
        
    def debug_print_deck(self):       
        for card in self.shuffled_deck:
            print(card)
            
    def get_deck_length(self):
        return len(self.shuffled_deck)
    
    def shuffle(self):
        self.shuffled_deck = copy.deepcopy(self.deck)
        random.shuffle(self.shuffled_deck)
        return self.shuffled_deck  

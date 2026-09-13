#No Adjustments Needed Here
#Ready to Use

class Card():
    def __init__(self, rank, suit):
        self.rank = int(rank)
        self.suit = suit

        if self.suit == 'C':
            self.suit_name = 'Circle'
        elif self.suit == 'S':
            self.suit_name = 'Square'
        elif self.suit == 'T':
            self.suit_name = 'Triangle'

    @property
    def file_name(self):
        if self.rank == 0:
            return "sylops.png"
        elif self.rank > 0:
            return f"g_{self.rank}_{self.suit.lower()}.png"
        elif self.rank < 0: 
            return f"r_{abs(self.rank)}_{self.suit.lower()}.png"

        
    def __str__(self):
        if self.rank == 0:
            return "Sylops"
        elif self.rank > 0:
            return f"Green +{self.rank} of {self.suit_name}"
        elif self.rank < 0: 
            return f"Red {abs(self.rank)} of {self.suit_name}"
  
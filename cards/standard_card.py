from card import Card

class StandardCard(Card):

    def __init__(self, strength, alliance):
        super().__init__(alliance)
        
        self.strength = strength


    
from cards.card import Card


class StandardCard(Card):
    
    strength = 0

    def __init__(self, alliance, card_type):
        super().__init__(alliance, card_type)

        self.strength = card_type.value


    def to_string(self):
        return str(self.strength)

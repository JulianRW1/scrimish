from cards.card import Card


class StandardCard(Card):

    def __init__(self, alliance, card_type):
        super().__init__(alliance, card_type)

        self.strength = card_type.value

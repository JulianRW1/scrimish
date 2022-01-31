from cards.card_type import CardType


# NOTE: I may not need to subclass for any cards bc everything is based on CardType
class Card:
    alliance = None
    card_type = None

    def __init__(self, card_alliance, card_type):
        self.alliance = card_alliance
        self.card_type = card_type

    
    def to_string(self):
        return ''



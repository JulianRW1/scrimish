from cards.card_type import CardType
from cards.specials.special_card import SpecialCard


class Shield(SpecialCard):
    def __init__(self, card_alliance):
        super().__init__(card_alliance, CardType.SHIELD)


    def to_string(self):
        return 'S'

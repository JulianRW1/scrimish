from cards.card_type import CardType
from cards.specials.special_card import SpecialCard


class Archer(SpecialCard):
    def __init__(self, card_alliance):
        super().__init__(card_alliance, CardType.ARCHER)


    def to_string(self):
        return 'A'
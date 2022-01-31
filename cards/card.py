from alliance import Alliance
from cards.card_type import CardType


class Card:
    alliance = None
    card_type = None

    def __init__(self, card_alliance, card_type):
        self.alliance = card_alliance
        self.cardType = card_type

    # TODO: Make a card_factory module
    def get_instance(card_alliance: Alliance, card_type: CardType):
        if card_type == CardType.standard_card:
            from cards.standard_card import StandardCard
            return StandardCard(card_alliance, card_type)
        elif card_type == CardType.ARCHER:
            from cards.specials.archer import Archer
            return Archer(card_alliance)
        elif card_type == CardType.SHIELD:
            from cards.specials.shield import Shield
            return Shield(card_alliance)
        elif card_type == CardType.CROWN:
            from cards.specials.crown import Crown
            return Crown(card_alliance)

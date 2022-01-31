from alliance import Alliance
from cards.card_type import CardType


class CardFactory:
    
    def make_card(card_alliance: Alliance, card_type: CardType):
        if CardType.is_standard(card_type):
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

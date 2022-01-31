from alliance import Alliance
from cards import card_methods
from cards.card_factory import CardFactory
from cards.card_type import CardType


REALM_SIZE = 5


def get_standard_card_set(alliance: Alliance):

    standard_cards_quantities = {
        CardType.DAGGER: 5,
        CardType.SWORD: 5,
        CardType.MORNING_STAR: 3,
        CardType.WAR_AXE: 3, 
        CardType.HALBERD: 2,
        CardType.LONGSWORD: 2,
        CardType.ARCHER: 2,
        CardType.SHIELD: 2, 
        CardType.CROWN: 1
    }

    card_set = []
    
    for type in standard_cards_quantities:
        for i in range(standard_cards_quantities[type]):
            card_set.append(CardFactory.make_card(alliance, type))

    return card_set


RED_STANDARD_CARD_SET = get_standard_card_set(Alliance.RED)
BLUE_STANDARD_CARD_SET = get_standard_card_set(Alliance.BLUE)

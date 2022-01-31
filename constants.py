from alliance import Alliance
from cards.card_factory import CardFactory
from cards.card_type import CardType


STANDARD_REALM_SIZE = 5
STANDARD_PILE_SIZE = 5

TOP_PILE_INDEX = -1
BOTTOM_PILE_INDEX = 0


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

    standard_cards = []
    
    for type in standard_cards_quantities:
        for i in range(standard_cards_quantities[type]):
            standard_cards.append(CardFactory.make_card(alliance, type))
    
    # Turn the standard card array into a 2D array
    card_set_2D = []
    for pile in range(STANDARD_REALM_SIZE):
        card_set_2D.append([])
        for index in range(STANDARD_PILE_SIZE):
            # loop through the piles
            card_set_2D[pile].append(standard_cards[(pile * 5) + index])

    return card_set_2D


RED_STANDARD_CARD_SET = get_standard_card_set(Alliance.RED)
BLUE_STANDARD_CARD_SET = get_standard_card_set(Alliance.BLUE)

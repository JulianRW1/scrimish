from random import Random
from alliance import Alliance
import constants


# TODO: bury the crown
def randomize_standard_set(alliance: Alliance, bury_crown: bool):
    cards = []
    standard_set = constants.BLUE_STANDARD_CARD_SET.copy()
    for row in range(constants.REALM_SIZE):
        cards.append([])
        for col in range(5):
            rand_card = Random().choice(standard_set)
            standard_set.remove(rand_card)
            cards[row].append(rand_card)
    
    return cards



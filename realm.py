import random
from cards.card import Card
from cards.card_type import CardType
import constants


class Realm():

    _data = []

    def __init__(self, cards):
        super().__init__()
        
        self._data = cards
    

    def print(self):
        for pile in self._data:
            output = '['
            for index in range(0, len(pile) - 1):
                output += pile[(len(pile) - 1) - index].to_string() + ', '

            print(output + pile[0].to_string() + ']')


    # location should be (pile, index)
    def place(self, pile_index: int, card_index:int, card: Card) -> None:

        self._data[pile_index][card_index] = card

    
    def push(self, pile: int, card):
        self._data[pile].append(card)


    def remove_top(self, pile: int) -> Card:
        top = self._data[pile][constants.TOP_PILE_INDEX]
        self._data[pile].remove(top)
        return top
    
    def get(self, pile: int, index: int) -> Card:
        if index < len(self._data[pile]):
            return self._data[pile][index]
        else:
            return None
    

    def get_top(self, pile: int) -> Card:
        if len(self._data[pile]) > 0:
            return self._data[pile][-1]
        else:
            return None


    def get_pile(self, target_card: Card) -> int:
        for pile_index in range(len(self._data)):
            for card in self._data[pile_index]:
                if card == target_card:
                    return pile_index
        return -1


    def shuffle(self):
        all_cards = []

        # get list of cards in realm
        for pile in self._data:
            for card in pile:
                all_cards.append(card)

        for pile in self._data:
            for card in range(len(self._data)):
                rand_card = random.Random().choice(all_cards)
                all_cards.remove(rand_card)
                pile[card] = rand_card
    

    # Swap the crown with the last card in its pile
    def bury_crown(self):
        crown_pile = None
        crown_index = 100

        for pile in self._data:
            for card in range(len(pile)):
                if pile[card].card_type == CardType.CROWN:
                    crown_pile = pile
                    crown_index = card

        if crown_index != constants.BOTTOM_PILE_INDEX:
            #swap crown with last card in crown pile
            temp = crown_pile[constants.BOTTOM_PILE_INDEX]
            crown_pile[constants.BOTTOM_PILE_INDEX] = crown_pile[crown_index]
            crown_pile[crown_index] = temp

    
    def get_realm(self):
        return self._data

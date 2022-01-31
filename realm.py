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
    def place(self, location: tuple, card):

        self._data[location[0]][location[1]] = card

    
    def push(self, pile: int, card):
        self._data[pile].append(card)


    def remove_top(self, pile: int) -> Card:
        top = self._data[pile][constants.TOP_PILE_INDEX]
        self._data[pile].remove(top)
        return top
    
    def get(self, pile: int, index: int) -> Card:
        return self._data[pile][index]

    def shuffle(self):
        all_cards = []

        # get list of cards in realm
        for pile in self._data:
            for card in pile:
                all_cards.append(card)


        un_shuffled = self._data
        for pile in self._data:
            for card in range(len(self._data)):
                rand_card = random.Random().choice(all_cards)
                all_cards.remove(rand_card)
                pile[card] = rand_card
    

    # Swap the crown with the last card in its pile
    def bury_crown(self):
        crown_pile = 100
        crown_index = 100

        for pile in self._data:
            for card in range(len(pile)):
                if pile[card].card_type == CardType.CROWN:
                    crown_pile = pile
                    crown_index = card
                    print(f'crown pile: {self._data.index(crown_pile)}, crown index: {crown_index}')
        
        if crown_pile[crown_index] != crown_pile[constants.BOTTOM_PILE_INDEX]:
            #swap crown with last card in crown pile
            temp = crown_pile[constants.BOTTOM_PILE_INDEX]
            crown_pile[constants.BOTTOM_PILE_INDEX] = crown_pile[crown_index]
            crown_pile[crown_index] = temp

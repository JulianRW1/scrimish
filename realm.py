from pip import List


class Realm(List):

    _piles = []
    
    def __init__(self, piles) -> None:

        for i in range(piles):
            self._piles.append([])


    def put(self, pile_index, card):
        self._piles 

    
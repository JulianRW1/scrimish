from cmath import pi


class Realm():

    def __init__(self, cards):
        super().__init__()
        
        self._data = cards
    

    def print(self):
        for index in range(len(self._data)):
            output = '|'
            for pile in range(len(self._data[index])):
                output += ' ' + self._data[pile][index].to_string() + ' |'
            
            print(output)


    # location should be (pile, index)
    def place(self, location: tuple, card):

        self._data[location[0]][location[1]] = card

    
    def push(self, pile: int, card):
        self._data[pile].append(card)


    def pop(self, pile: int):
        return self._data[pile].pop()

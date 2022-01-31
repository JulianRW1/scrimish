


class Player:

    realm = []

    def __init__(self, alliance, realm_size):
        self.alliance = alliance
        
        for i in range(realm_size):
            self.realm.append([])


    def make_move(self, card_used, target):
        pass
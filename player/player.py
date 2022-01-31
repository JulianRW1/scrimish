import constants
from realm import Realm


class Player:

    realm = None

    def __init__(self, alliance, realm):
        self.alliance = alliance
        
        if (realm == None):
            realm = Realm(constants.REALM_SIZE)
        else:
            self.realm = Realm(realm)


    def make_move(self, card_used, target):
        pass
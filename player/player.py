from alliance import Alliance
import constants
from moves.attack import Attack
from moves.attack_result import AttackResult
from realm import Realm


class Player:

    realm = None
    color = ''

    def __init__(self, alliance, realm=None):
        self.alliance = alliance

        if alliance == Alliance.BLUE:
            self.color = 'BLUE'
        elif alliance == Alliance.RED:
            self.color = 'RED'
        
        if realm == None:
            if alliance == Alliance.BLUE:
                self.realm = Realm(constants.BLUE_STANDARD_CARD_SET.copy())
            elif alliance == Alliance.RED:
                self.realm = Realm(constants.RED_STANDARD_CARD_SET.copy())
            self.realm.shuffle()
            self.realm.bury_crown()
        else:
            self.realm = Realm(realm)


    # returns the cards that lost
    def make_attack(self, defender_realm: Realm, attacker_pile: int, defender_pile: int):
        attack = Attack(self.realm, defender_realm, attacker_pile, defender_pile)

        attack_result = attack.resolve_attack()

        losing_cards = ()

        if attack_result == AttackResult.ATTACKER_WINS:
            losing_cards = [defender_realm.remove_top(defender_pile)]
        elif attack_result == AttackResult.DEFENDER_WINS:
            losing_cards = [self.realm.remove_top(attacker_pile)]
        elif attack_result == AttackResult.BOTH_LOSE:
            losing_cards = [self.realm.remove_top(attacker_pile), defender_realm.remove_top(defender_pile)]
        elif attack_result == AttackResult.BOTH_SURVIVE:
            losing_cards = []
        
        return losing_cards


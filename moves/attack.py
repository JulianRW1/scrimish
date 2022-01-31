from cards.card_type import CardType
import constants
from moves.attack_result import AttackResult
from realm import Realm


class Attack:

    attacker_realm = None
    attack_pile = 100

    defender_realm = None
    defense_pile = 100

    def __init__(self, attacker_realm: Realm, defender_realm: Realm, attack_pile: int, defense_pile: int):
        self.attacker_realm = attacker_realm
        self.attack_pile = attack_pile

        self.defender_realm = defender_realm
        self.defense_pile = defense_pile

    
    # Returns the winner of the attack
    # Returns and
    def resolve_attack(self) -> AttackResult:
        atk_type = self.attacker_realm.get(self.attack_pile, constants.TOP_PILE_INDEX).card_type
        def_type = self.defender_realm.get(self.defense_pile, constants.TOP_PILE_INDEX).card_type

        if CardType.is_standard(atk_type):

            if CardType.is_standard(def_type):
                # Compares strength of cards
                if  atk_type.value > def_type.value:
                    return AttackResult.ATTACKER_WINS
                elif atk_type.value < def_type.value:
                    return AttackResult.DEFENDER_WINS
                else:
                    return AttackResult.BOTH_LOSE

            elif def_type == CardType.ARCHER or def_type == CardType.CROWN :
                return AttackResult.ATTACKER_WINS

            elif def_type == CardType.SHIELD:
                return AttackResult.BOTH_LOSE

        elif atk_type == CardType.ARCHER:

            if def_type == CardType.SHIELD:
                return AttackResult.BOTH_SURVIVE
            
            else:
                return AttackResult.ATTACKER_WINS
            
        elif atk_type == CardType.CROWN:

            if def_type == CardType.CROWN:
                return AttackResult.ATTACKER_WINS

            else:
                return AttackResult.DEFENDER_WINS

        elif atk_type == CardType.SHIELD:
            raise Exception('Shields Cannot Attack')

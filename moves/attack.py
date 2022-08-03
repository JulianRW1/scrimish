from cards.card_type import CardType
import constants
from moves.attack_result import AttackResult
from realm import Realm


class Attack:

    pile:int

    defender = None
    defense_pile:int

    def __init__(self, attacking_player, defending_player, attack_pile: int, defense_pile: int):
        self.player = attacking_player
        self.pile = attack_pile

        self.defender = defending_player
        self.defense_pile = defense_pile

    
    # Returns the winner of the attack
    # Returns and
    def resolve_attack(self) -> AttackResult:
        atk_type = self.player.realm.get(self.pile, constants.TOP_PILE_INDEX).card_type
        def_type = self.defender.realm.get(self.defense_pile, constants.TOP_PILE_INDEX).card_type

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

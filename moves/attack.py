from cards.card_type import CardType
from cards.card import Card
from moves.attack_result import AttackResult


class Attack:

    attacker = None
    defender = None

    def __init__(self, attacker: Card, defender: Card):
        self.attacker = attacker
        self.defender = defender

    
    # Returns the winner of the attack
    # Returns and
    def resolve_attack(self) -> AttackResult:
        atk_type = self.attacker.card_type
        def_type = self.defender.card_type

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

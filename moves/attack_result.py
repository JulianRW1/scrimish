from enum import Enum


class AttackResult(Enum):
    BOTH_LOSE = 0
    ATTACKER_WINS = 1
    DEFENDER_WINS = 2
    BOTH_SURVIVE = 3

from enum import Enum


class CardType(Enum):
    DAGGER = 1
    SWORD = 2
    MORNING_STAR = 3
    WAR_AXE = 4
    HALBERD = 5
    LONGSWORD = 6

    ARCHER = 7
    SHIELD = 8
    CROWN = 9

    def is_standard(card_type):
        return (card_type == CardType.DAGGER or 
                card_type == CardType.SWORD or 
                card_type == CardType.MORNING_STAR or 
                card_type == CardType.WAR_AXE or
                card_type == CardType.HALBERD or 
                card_type == CardType.LONGSWORD)

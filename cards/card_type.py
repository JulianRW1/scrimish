from enum import Flag


class CardType(Flag):
    DAGGER = 1
    SWORD = 2
    MORNING_STAR = 3
    WAR_AXE = 4
    HALBERD = 5
    LONGSWORD = 6

    ARCHER = 7
    SHIELD = 8
    CROWN = 9

    standard_card = DAGGER | SWORD | MORNING_STAR | WAR_AXE | HALBERD | LONGSWORD

# from alliance import Alliance
# from gui.table import Table
# from player.player import Player


# blue_player = Player(Alliance.BLUE)
# red_player = Player(Alliance.RED)

# print('Blue Realm')
# blue_player.realm.print()
# print('Red Realm')
# red_player.realm.print()

# Table(blue_player, red_player).set_up()

from alliance import Alliance
from moves.move import Move
from player.player import Player


class Scrimish:
    red_player = Player
    blue_player = Player
    move_list = [Move]
    last_defender_lost = False
    winner = None

    realms = []

    
    def __init__(self, id: str, level:str, speed:str) -> None:
        self.id = id
        self.level = level
        self.speed = speed
        self.blue_player = Player(Alliance.BLUE)
        self.red_player = Player(Alliance.RED)

    
    def get_current_player(self):
        last_move = self.move_list[len(self.move_list) - 1]
        if last_move.player.alliance == Alliance.BLUE:
            return self.red_player
        else:
            return self.blue_player

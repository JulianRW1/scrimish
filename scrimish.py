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

import json
from alliance import Alliance
from moves.attack import Attack
from moves.move import Move
from player.player import Player


class Scrimish:
    red_player = Player
    blue_player = Player
    move_list = []
    last_defender_lost = False
    winner = None

    realms = []

    
    def __init__(self, id: str, level:str, speed:str) -> None:
        self.id = id
        self.level = level
        self.speed = speed
        self.blue_player = Player(Alliance.BLUE)
        self.red_player = Player(Alliance.RED)


    def play_attack(self, player_color, attack_pile, defense_pile):

        active_player: Player
        inactive_player: Player

        if player_color == 'b':
            active_player = self.blue_player
            inactive_player = self.red_player
        elif player_color == 'r':
            active_player = self.red_player
            inactive_player = self.blue_player
        else:
            raise RuntimeError('in Scrimish.play_move(): invalid player_color')
        
        losers = active_player.make_attack(inactive_player, attack_pile, defense_pile)

        self.move_list.append(Attack(active_player, inactive_player, attack_pile, defense_pile))

        return losers
        
        
    
    def get_current_player(self):
        """
        returns a letter representing the current player
        """

        if len(self.move_list) == 0:
            return 'b'
            # TODO - make first player the player who finishes setting up first

        print(len(self.move_list))
        last_move = self.move_list[len(self.move_list) - 1]
        if last_move.player.alliance == Alliance.BLUE:
            return 'r'
        else:
            return 'b'

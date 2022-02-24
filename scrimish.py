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

        self.create_random_realms()


    def create_random_realms(self):
        standard_realm = [
            '1', '1', '1', '1', '1', 
            '2', '2', '2', '2', '2', 
            '3', '3', '3', 
            '4', '4', '4', 
            '5', '5', 
            '6', '6', 
            'A', 'A', 
            'S', 'S',
            'C'
        ]
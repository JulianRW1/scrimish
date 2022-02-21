from alliance import Alliance
from gui.table import Table
from player.player import Player


blue_player = Player(Alliance.BLUE)
red_player = Player(Alliance.RED)

print('Blue Realm')
blue_player.realm.print()
print('Red Realm')
red_player.realm.print()

Table(blue_player, red_player).set_up()
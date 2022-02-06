import constants
from cards.card_factory import CardFactory
from cards.card_type import CardType
from alliance import Alliance
from gui.table import Table
from moves.attack import Attack
from player.player import Player
from realm import Realm


blue_player = Player(Alliance.BLUE)
red_player = Player(Alliance.RED)

print('Blue Realm')
blue_player.realm.print()
print('Red Realm')
red_player.realm.print()

Table(blue_player, red_player).set_up()
import constants
from cards.card_factory import CardFactory
from cards.card_type import CardType
from alliance import Alliance
from gui.table import Table
from moves.attack import Attack
from player.player import Player
from realm import Realm


# attack tests
blue_player = Player(Alliance.BLUE)
red_player = Player(Alliance.RED)

print('Blue Realm')
blue_player.realm.print()
print('Red Realm')
red_player.realm.print()

losers = blue_player.make_attack(red_player.realm, attacker_pile=0, defender_pile= 0)

if (isinstance(losers, tuple)):
    for card in losers:
        print(card.to_string())
elif(losers == None):
    print('NO CARD LOST')
else:
    print(losers.to_string())

print('Blue Realm')
blue_player.realm.print()
print('Red Realm')
red_player.realm.print()

# attack = Attack(attacker_realm=blue_player.realm, defender_realm=red_player.realm, attack_pile=0, defense_pile=0)
# result = attack.resolve_attack()
# print(result)

Table(blue_player, red_player).set_up()
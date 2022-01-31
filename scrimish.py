import constants
from cards.card_factory import CardFactory
from cards.card_type import CardType
from alliance import Alliance
from moves.attack import Attack
from player.player import Player
from realm import Realm


realm = Realm(constants.BLUE_STANDARD_CARD_SET.copy())

realm.shuffle()
realm.bury_crown()

test_card = CardFactory.make_card(Alliance.RED, CardType.HALBERD)

print(f'''
Alliance: {test_card.alliance}
CardType: {test_card.card_type}
Strength: {test_card.strength}
''')

# attack tests
blue_player = Player(Alliance.BLUE)
red_player = Player(Alliance.RED)

print('Blue Realm')
blue_player.realm.print()
print('Red Realm')
red_player.realm.print()

losers = red_player.make_attack(blue_player.realm, attacker_pile=0, defender_pile= 1)

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

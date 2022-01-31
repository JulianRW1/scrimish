
from cards.card_type import CardType
from cards.card import Card
from player.player import Player
from alliance import Alliance
import constants


player = Player(Alliance.BLUE, constants.REALM_SIZE)

player.realm = [
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5]
]

print(player.realm)

blue_archer = Card.get_instance(Alliance.BLUE, CardType.ARCHER)

print(f'''
Alliance: {blue_archer.alliance}
CardType: {blue_archer.card_type}
''')

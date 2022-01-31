from random import Random
from re import A
from cards import card_methods
from cards.card_factory import CardFactory
from cards.card_type import CardType
from alliance import Alliance
from moves.attack import Attack
from realm import Realm
import constants


cards = card_methods.randomize_standard_set(Alliance.BLUE, False)
realm = Realm(cards)

realm.print()

test_card = CardFactory.make_card(Alliance.RED, CardType.HALBERD)

print(f'''
Alliance: {test_card.alliance}
CardType: {test_card.card_type}
Strength: {test_card.strength}
''')


attacker = CardFactory.make_card(Alliance.BLUE, CardType.ARCHER)
defender = CardFactory.make_card(Alliance.RED, CardType.LONGSWORD)


result = Attack(attacker, defender).resolve_attack()

print(result)

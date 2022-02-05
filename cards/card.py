from PIL import Image
from alliance import Alliance
from cards.card_type import CardType


# NOTE: I may not need to subclass for any cards bc everything is based on CardType
class Card:
    alliance = None
    card_type = None

    def __init__(self, card_alliance: Alliance, card_type: CardType):
        self.alliance = card_alliance
        self.card_type = card_type

    
    def to_string(self):
        return ''


    def get_image_path(self):
        file_name = ''
        if self.alliance == Alliance.RED:
            file_name = 'images/red_'
        else:
            file_name = 'images/blue_'
        
        if self.card_type == CardType.DAGGER:
            file_name += 'dagger'
        elif self.card_type == CardType.SWORD:
            file_name += 'sword'
        elif self.card_type == CardType.MORNING_STAR:
            file_name += 'morning_star'
        elif self.card_type == CardType.WAR_AXE:
            file_name += 'war_axe'
        elif self.card_type == CardType.HALBERD:
            file_name += 'halberd'
        elif self.card_type == CardType.LONGSWORD:
            file_name += 'longsword'
        elif self.card_type == CardType.ARCHER:
            file_name += 'archer'
        elif self.card_type == CardType.SHIELD:
            file_name += 'shield'
        elif self.card_type == CardType.CROWN:
            file_name += 'crown'
        
        file_name += '.png'
        return file_name
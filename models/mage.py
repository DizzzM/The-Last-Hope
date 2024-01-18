from models.entity import Entity
from models.models_config import mage


class Mage(Entity):
    def __init__(self, room=0, floor=0, enemy=False):
        if enemy:
            super().__init__(mage['hp'] + (room - 1 + (floor - 1) * 10), mage['def'] * floor, mage['atk'], mage['luck'], mage['cd'], mage['duration'],
                             'sprites/mage.png', True)
        else:
            super().__init__(mage['hp'], mage['def'], mage['atk'], mage['luck'], mage['cd'], mage['duration'],
                             'sprites/mage.png', False)

    def cast(self):
        self.cast_current_cd = self.cast_cd
        self.defence += round(self.defence * 0.5)
        self.heal(self.hp / 10)
        self.atk_multiplier += 0.5
        self.luck = 10
        self.cast_current_duration = self.cast_duration

        return 'used Almighty Power'

    def remove_cast_effects(self):
        self.atk_multiplier -= 0.5
        self.defence = self.base_defence
        self.luck = self.base_luck
        return 'Almighty Power effect disappears'

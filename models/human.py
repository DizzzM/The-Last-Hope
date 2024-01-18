from models.entity import Entity
from models.models_config import human


class Human(Entity):
    def __init__(self, room=0, floor=0, enemy=False):
        if enemy:
            super().__init__(human['hp'] + (room - 1 + (floor - 1) * 10), human['def'] * floor, human['atk'], human['luck'], human['cd'], human['duration'],
                             'sprites/human.png', True)
        else:
            super().__init__(human['hp'], human['def'], human['atk'], human['luck'], human['cd'], human['duration'],
                         'sprites/human.png', False)

    def cast(self):
        self.cast_current_cd = self.cast_cd
        self.heal(self.hp/10)
        self.atk_multiplier += 0.5
        self.cast_current_duration = self.cast_duration
        return 'used Divine Blessing'

    def remove_cast_effects(self):
        self.atk_multiplier -= 0.5
        return 'Divine Blessing effect disappears'

from models.entity import Entity
from models.models_config import elf


class Elf(Entity):
    def __init__(self, room=0, floor=0, enemy=False):
        if enemy:
            super().__init__(elf['hp'] + (room - 1 + (floor - 1) * 10), elf['def'] * floor, elf['atk'],
                             elf['luck'], elf['cd'], elf['duration'],
                             'sprites/elf.png', True)
        else:
            super().__init__(elf['hp'], elf['def'], elf['atk'], elf['luck'], elf['cd'], elf['duration'],
                             'sprites/elf.png', False)

    def cast(self):
        self.cast_current_cd = self.cast_cd
        self.luck = 10
        self.cast_current_duration = self.cast_duration
        return 'used Shadow Realm'

    def remove_cast_effects(self):
        self.luck = self.base_luck
        return 'Shadow Realm effect disappears'

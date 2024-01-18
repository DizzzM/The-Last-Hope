from models.entity import Entity
from models.models_config import dwarf


class Dwarf(Entity):
    def __init__(self, room=0, floor=0, enemy=False):
        if enemy:
            super().__init__(dwarf['hp'] + (room - 1 + (floor - 1) * 10), dwarf['def'] * floor, dwarf['atk'], dwarf['luck'], dwarf['cd'], dwarf['duration'],
                             'sprites/dwarf.png', True)
        else:
            super().__init__(dwarf['hp'], dwarf['def'], dwarf['atk'], dwarf['luck'], dwarf['cd'], dwarf['duration'],
                             'sprites/dwarf.png', False)

    def cast(self):
        self.cast_current_cd = self.cast_cd
        self.defence += round(self.defence * 0.5)
        self.atk_multiplier += 0.25
        self.cast_current_duration = self.cast_duration

        return 'used Rage'

    def remove_cast_effects(self):
        self.atk_multiplier -= 0.25
        self.defence = self.base_defence
        return 'Rage effect disappears'

import random
from models import human, dwarf, elf


def generate_enemy(room, floor):
    enemy_class = random.choice([human.Human, dwarf.Dwarf, elf.Elf])
    enemy = enemy_class(room=room, floor=floor, enemy=True)
    enemy.base_defence *= floor
    return enemy

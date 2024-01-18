import numpy as np
from PIL import ImageTk, Image, ImageOps
import tkinter as tk


def import_img(path, mirror):
    img = Image.open(path)
    img = img.convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    if mirror:
        img = ImageOps.mirror(img)
    return img


class Entity:
    def __init__(self, hp, defence, atk, luck, cd, cast_duration, sprite, enemy):
        self.hp = hp
        self.current_hp = self.hp
        self.base_defence = defence
        self.defence = self.base_defence
        self.atk = atk
        self.base_luck = luck
        self.luck = self.base_luck
        self.cast_cd = cd
        self.cast_current_cd = 0
        self.cast_duration = cast_duration
        self.cast_current_duration = 0
        self.atk_multiplier = 1
        self.dead = False
        self.enemy = enemy
        self.sprite = import_img(sprite, self.enemy)

    def draw(self, canvas, hp, defence=None, atk=None, luck=None, cd=None):
        if self.enemy:
            hp.configure(text=f'{self.current_hp}/{self.hp}')
        else:
            hp.configure(text=f'{self.current_hp}/{self.hp}')
            defence.configure(text=f'{self.defence}')
            atk.configure(text=f'{round(self.atk * self.atk_multiplier)}-{round(self.atk * self.atk_multiplier * 2)}')
            luck.configure(text=f'{self.luck}')
            cd.configure(text=f'{self.cast_current_cd}')

        img = ImageTk.PhotoImage(self.sprite)
        canvas.background = img
        canvas.create_image(0, 0, anchor=tk.NW, image=img)

    def quick_attack(self, enemy):
        miss_chance = (30 + self.luck) / 40
        missed = np.random.choice([0, 1], 1, p=[1 - miss_chance, miss_chance])[0]
        damage = self.atk_multiplier * self.atk + np.random.randint(1,7)
        damage_dealt = enemy.take_damage(
                round(damage * missed))
        return f'quick attacked for {damage_dealt} damage'

    def power_attack(self, enemy):
        miss_chance = (30 + self.luck) / 40
        missed = np.random.choice([0, 1], 1, p=[1 - miss_chance, miss_chance])[0]
        damage = 2 * self.atk_multiplier * self.atk + np.random.randint(1,7)
        damage_dealt = enemy.take_damage(
                round(damage * missed))
        return f'power attacked for {damage_dealt} damage'

    def cast(self):
        pass

    def take_damage(self, dmg):
        evasion = min(self.luck-2, 1) / 10
        evaded = np.random.choice([0, 1], 1, p=[evasion, 1 - evasion])[0]
        dmg = max(dmg - self.defence // 2, 0) * evaded
        self.current_hp = max(0, self.current_hp - dmg)
        if self.current_hp == 0:
            self.dead = True
        return dmg

    def heal(self, amount):
        self.current_hp = round(min(self.current_hp + amount, self.hp))

    def add_hp(self, amount):
        self.hp += round(amount)
        self.heal(self.hp/2)

    def add_def(self, amount):
        self.base_defence += amount
        self.defence = self.base_defence

    def add_atk(self, amount):
        self.atk += amount

    def add_luck(self, amount):
        self.luck = min(self.luck + amount, 10)


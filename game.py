import random
import tkinter as tk
import config
from models import human, dwarf, elf, enemy, mage


class Game:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('The Last Hope')
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.geometry(f'600x800+{self.screen_width // 2 - 300}+{self.screen_height // 2 - 400}')
        self.window.wm_minsize(600, 800)
        self.window.wm_maxsize(600, 800)
        self.floor = 1
        self.room = 1

    def init_ui(self):
        # general layout setup
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=5)
        self.window.grid_rowconfigure(2, weight=3)

        header = tk.Frame(self.window, bg=config.BG)
        game_screen = tk.Frame(self.window, bg=config.SCENE_BG)
        footer = tk.Frame(self.window, bg=config.BG)
        header.grid(row=0, column=0, sticky=tk.NSEW)
        game_screen.grid(row=1, column=0, sticky=tk.NSEW)
        footer.grid(row=2, column=0, sticky=tk.NSEW)

        # header setup
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=1, uniform='header')
        header.grid_columnconfigure(2, weight=1)
        header.grid_columnconfigure(3, weight=1, uniform='header')
        header.grid_columnconfigure(4, weight=1)
        header.grid_rowconfigure(0, weight=1)
        header.grid_rowconfigure(1, weight=1)

        floor_label = tk.Label(header, anchor=tk.W, text='Floor', font=config.FONT, bg=config.BG)
        room_label = tk.Label(header, anchor=tk.W, text='Room', font=config.FONT, bg=config.BG)
        floor_label.grid(row=0, column=0, sticky=tk.W, padx=5)
        room_label.grid(row=1, column=0, sticky=tk.W, padx=5)
        self.floor_value = tk.Label(header, anchor=tk.E, text=f'{self.floor}', font=config.FONT, bg=config.BG)
        self.room_value = tk.Label(header, anchor=tk.E, text=f'{self.room}', font=config.FONT, bg=config.BG)
        self.floor_value.grid(row=0, column=1, sticky=tk.E, padx=5)
        self.room_value.grid(row=1, column=1, sticky=tk.E, padx=5)
        enemy_hp_label = tk.Label(header, anchor=tk.W, text='Enemy HP', font=config.FONT, bg=config.BG)
        self.enemy_hp_value = tk.Label(header, anchor=tk.E, text='00/00', font=config.FONT, bg=config.BG)
        enemy_hp_label.grid(row=1, column=3, sticky=tk.W, padx=5)
        self.enemy_hp_value.grid(row=1, column=4, sticky=tk.E, padx=5)

        # game_screen setup
        game_screen.grid_rowconfigure(0, weight=1)
        game_screen.grid_rowconfigure(1, weight=2)
        game_screen.grid_rowconfigure(2, weight=1)
        game_screen.grid_columnconfigure(0, weight=1)
        game_screen.grid_columnconfigure(1, weight=1)
        game_screen.grid_columnconfigure(2, weight=1)
        self.player_sprite = tk.Canvas(game_screen, width=200, height=200, bg=config.SCENE_BG, highlightthickness=0)
        self.enemy_sprite = tk.Canvas(game_screen, width=200, height=200, bg=config.SCENE_BG, highlightthickness=0)
        self.log = tk.Label(game_screen, anchor=tk.CENTER, font=config.FONT, bg=config.SCENE_BG, fg='#ffffff')

        self.player_sprite.grid(row=1, column=0, sticky=tk.S)
        self.enemy_sprite.grid(row=1, column=2, sticky=tk.S)
        self.log.grid(row=0, column=0, columnspan=3)
        # footer setup
        footer.grid_rowconfigure(0, weight=1)
        footer.grid_columnconfigure(0, weight=1)
        footer.grid_columnconfigure(1, weight=3)
        stats = tk.Frame(footer, bg=config.BG)
        buttons = tk.Frame(footer, bg=config.BG)
        stats.grid(row=0, column=0, sticky=tk.NSEW)
        buttons.grid(row=0, column=1, sticky=tk.NSEW)

        # buttons setup
        buttons.grid_columnconfigure(0, weight=1)
        buttons.grid_columnconfigure(1, weight=2)
        buttons.grid_columnconfigure(2, weight=1)
        buttons.grid_rowconfigure(0, weight=1)
        buttons.grid_rowconfigure(1, weight=2)
        buttons.grid_rowconfigure(2, weight=2)
        buttons.grid_rowconfigure(3, weight=2)
        buttons.grid_rowconfigure(4, weight=2)
        buttons.grid_rowconfigure(5, weight=2)
        buttons.grid_rowconfigure(6, weight=1)
        self.quick_attack_button = tk.Button(buttons, text='Quick Attack', font=config.FONT,
                                             command=lambda: self.button_click('quick'), bg=config.BG,
                                             highlightthickness=0)
        self.power_attack_button = tk.Button(buttons, text='Power Attack', font=config.FONT,
                                             command=lambda: self.button_click('power'), bg=config.BG,
                                             highlightthickness=0)
        self.cast_button = tk.Button(buttons, text='Cast', font=config.FONT,
                                     command=lambda: self.button_click('cast'), bg=config.BG,
                                     highlightthickness=0)
        self.quick_attack_button.grid(row=1, column=1, sticky=tk.NSEW)
        self.power_attack_button.grid(row=3, column=1, sticky=tk.NSEW)
        self.cast_button.grid(row=5, column=1, sticky=tk.NSEW)

        # stats setup
        stats.grid_columnconfigure(0, weight=1)
        stats.grid_columnconfigure(1, weight=1)
        stats.grid_rowconfigure(0, weight=1)
        stats.grid_rowconfigure(1, weight=1)
        stats.grid_rowconfigure(2, weight=1)
        stats.grid_rowconfigure(3, weight=1)
        stats.grid_rowconfigure(4, weight=1)
        hp_label = tk.Label(stats, anchor=tk.W, text='HP', font=config.FONT, bg=config.BG)
        def_label = tk.Label(stats, anchor=tk.W, text='DEF', font=config.FONT, bg=config.BG)
        atk_label = tk.Label(stats, anchor=tk.W, text='ATK', font=config.FONT, bg=config.BG)
        luck_label = tk.Label(stats, anchor=tk.W, text='LUCK', font=config.FONT, bg=config.BG)
        cd_label = tk.Label(stats, anchor=tk.W, text='CAST CD', font=config.FONT, bg=config.BG)
        hp_label.grid(row=0, column=0, sticky=tk.W, padx=10)
        def_label.grid(row=1, column=0, sticky=tk.W, padx=10)
        atk_label.grid(row=2, column=0, sticky=tk.W, padx=10)
        luck_label.grid(row=3, column=0, sticky=tk.W, padx=10)
        cd_label.grid(row=4, column=0, sticky=tk.W, padx=10)

        self.hp_value = tk.Label(stats, anchor=tk.E, text=f'00/00', font=config.FONT, bg=config.BG)
        self.def_value = tk.Label(stats, anchor=tk.E, text='00', font=config.FONT, bg=config.BG)
        self.atk_value = tk.Label(stats, anchor=tk.E, text='00-00', font=config.FONT, bg=config.BG)
        self.luck_value = tk.Label(stats, anchor=tk.E, text='00', font=config.FONT, bg=config.BG)
        self.cd_value = tk.Label(stats, anchor=tk.E, text='0', font=config.FONT, bg=config.BG)
        self.hp_value.grid(row=0, column=1, sticky=tk.E, padx=10)
        self.def_value.grid(row=1, column=1, sticky=tk.E, padx=10)
        self.atk_value.grid(row=2, column=1, sticky=tk.E, padx=10)
        self.luck_value.grid(row=3, column=1, sticky=tk.E, padx=10)
        self.cd_value.grid(row=4, column=1, sticky=tk.E, padx=10)

    def update_ui(self):
        self.player.draw(self.player_sprite, self.hp_value, self.def_value, self.atk_value, self.luck_value,
                         self.cd_value)
        self.current_enemy.draw(self.enemy_sprite, self.enemy_hp_value)
        self.room_value.configure(text=f'{self.room}')
        self.floor_value.configure(text=f'{self.floor}')

    def update_cd(self, entity):
        log = ''
        if entity.cast_current_cd > 0:
            if entity == self.player:
                self.cast_button.configure(state='disabled')
            entity.cast_current_cd -= 1
        else:
            if entity == self.player:
                self.cast_button.configure(state='normal')
        if entity.cast_current_duration > 0:
            if entity.cast_current_duration == 1:
                log = entity.remove_cast_effects()
            entity.cast_current_duration -= 1
        return log

    def enemy_death(self):
        self.player.heal(self.player.hp / 4)
        if len(self.enemies) > 1:
            self.enemies.pop(0)
            self.current_enemy = self.enemies[0]
            self.window.after(2000, self.enemy_turn)
        else:
            self.choose_room_reward()
            self.room += 1
            if self.room > config.ROOMS:
                self.choose_floor_reward()
                self.room = 1
                self.floor += 1
            if not (self.room == config.ROOMS and self.floor == config.FLOORS):
                self.generate_enemies()
            else:
                self.boss_fight()
        if self.floor == 4:
            self.win()

    def enemy_turn(self):
        log = ''
        cd_result = self.update_cd(self.current_enemy)
        if not cd_result == '':
            log += f'Enemy`s {cd_result}\n'

        if self.current_enemy.cast_current_cd > 0:
            actions = [0, 1]
        else:
            actions = [0, 1, 2]
        action = random.choice(actions)
        if action == 0:
            result = self.current_enemy.quick_attack(self.player)
        elif action == 1:
            result = self.current_enemy.power_attack(self.player)
        else:
            result = self.current_enemy.cast()

        if self.player.dead:
            self.death()
        log += f'Enemy {result}'
        self.log.configure(text=log)
        self.update_ui()
        self.window.after(2000, self.player_turn)

    def player_turn(self):
        log = ''
        cd_result = self.update_cd(self.player)
        if not cd_result == '':
            log += f'Your {cd_result}\n'
        self.log.configure(text=log)
        self.quick_attack_button.configure(state='normal')
        self.power_attack_button.configure(state='normal')

    def button_click(self, action):
        log = ''
        if action == 'quick':
            result = self.player.quick_attack(self.current_enemy)
        elif action == 'power':
            result = self.player.power_attack(self.current_enemy)
        else:
            result = self.player.cast()

        log += f'You {result}'
        if self.current_enemy.dead:
            self.enemy_death()
            log += '\nYou killed enemy'
        else:
            self.window.after(2000, self.enemy_turn)

        self.log.configure(text=log)

        self.quick_attack_button.configure(state='disabled')
        self.power_attack_button.configure(state='disabled')
        self.cast_button.configure(state='disabled')
        self.update_ui()

    def generate_enemies(self):
        enemies_count = random.randint(1, config.ENEMIES)
        self.enemies = []
        for _ in range(enemies_count):
            self.enemies.append(enemy.generate_enemy(self.room, self.floor))

        self.current_enemy = self.enemies[0]

    def start_game(self):
        self.generate_enemies()
        self.player_turn()
        self.update_ui()

    def choose_race_util(self, race):
        self.player = race
        self.start_game()
        self.window.deiconify()
        self.race_window.destroy()

    def choose_race(self):
        self.window.withdraw()
        self.race_window = tk.Toplevel(self.window)
        self.race_window.title("Choose your race")

        self.race_window.geometry(f'600x800+{self.screen_width // 2 - 300}+{self.screen_height // 2 - 400}')

        self.race_window.configure(bg=config.BG)
        self.race_window.grid_columnconfigure(0, weight=1)
        self.race_window.grid_rowconfigure(0, weight=1)
        self.race_window.grid_rowconfigure(1, weight=3)

        header = tk.Frame(self.race_window,
                          bg=config.BG)
        header.grid(row=0, column=0, sticky=tk.NSEW)
        tk.Label(self.race_window, text='Click on the button with\nrace name to choose it', font=config.FONT,
                 bg=config.BG).grid(
                row=0, column=0, sticky=tk.NSEW)

        main = tk.Frame(self.race_window,
                        bg=config.BG)
        main.grid(row=1, column=0, sticky=tk.NSEW)
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_columnconfigure(2, weight=1)
        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)
        main.grid_rowconfigure(2, weight=1)
        main.grid_rowconfigure(3, weight=1)

        tk.Button(main, text='Human', font=config.FONT,
                  command=lambda: self.choose_race_util(human.Human()), bg=config.BG).grid(row=0, column=0,
                                                                                           sticky=tk.NSEW,
                                                                                           padx=5, pady=5)
        tk.Label(main, text='Mid HP', font=config.FONT, bg=config.BG).grid(row=1, column=0, sticky=tk.NSEW, padx=5,
                                                                           pady=5)
        tk.Label(main, text='High DEF', font=config.FONT, bg=config.BG).grid(row=2, column=0, sticky=tk.NSEW, padx=5,
                                                                             pady=5)
        tk.Label(main, text='Low ATK', font=config.FONT, bg=config.BG).grid(row=3, column=0, sticky=tk.NSEW, padx=5,
                                                                            pady=5)

        tk.Button(main, text='Dwarf', font=config.FONT,
                  command=lambda: self.choose_race_util(dwarf.Dwarf()), bg=config.BG).grid(row=0, column=1,
                                                                                           sticky=tk.NSEW,
                                                                                           padx=5, pady=5)
        tk.Label(main, text='High HP', font=config.FONT, bg=config.BG).grid(row=1, column=1, sticky=tk.NSEW, padx=5,
                                                                            pady=5)
        tk.Label(main, text='Low DEF', font=config.FONT, bg=config.BG).grid(row=2, column=1, sticky=tk.NSEW, padx=5,
                                                                            pady=5)
        tk.Label(main, text='Mid ATK', font=config.FONT, bg=config.BG).grid(row=3, column=1, sticky=tk.NSEW, padx=5,
                                                                            pady=5)

        tk.Button(main, text='Elf', font=config.FONT,
                  command=lambda: self.choose_race_util(elf.Elf()), bg=config.BG).grid(row=0, column=2,
                                                                                       sticky=tk.NSEW,
                                                                                       padx=5, pady=5)
        tk.Label(main, text='Low HP', font=config.FONT, bg=config.BG).grid(row=1, column=2, sticky=tk.NSEW, padx=5,
                                                                           pady=5)
        tk.Label(main, text='Mid DEF', font=config.FONT, bg=config.BG).grid(row=2, column=2, sticky=tk.NSEW, padx=5,
                                                                            pady=5)
        tk.Label(main, text='High ATK', font=config.FONT, bg=config.BG).grid(row=3, column=2, sticky=tk.NSEW, padx=5,
                                                                             pady=5)

    def room_util(self, action, value):
        action(value)
        self.window.after(2000, self.enemy_turn)
        self.update_ui()
        self.window.deiconify()
        self.room_window.destroy()

    def choose_room_reward(self):
        self.window.withdraw()
        self.room_window = tk.Toplevel(self.window)
        self.room_window.geometry(f'600x800+{self.screen_width // 2 - 300}+{self.screen_height // 2 - 400}')
        self.room_window.configure(bg=config.BG)
        self.room_window.grid_rowconfigure(0, weight=1)
        self.room_window.grid_rowconfigure(1, weight=2)
        self.room_window.grid_rowconfigure(2, weight=2)
        self.room_window.grid_columnconfigure(0, weight=1, uniform="buttons")
        self.room_window.grid_columnconfigure(1, weight=1, uniform="buttons")
        self.room_window.grid_columnconfigure(2, weight=1, uniform="buttons")

        hp = (tk.Button(self.room_window, text='+ HP', font=config.FONT,
                        command=lambda: self.room_util(self.player.add_hp, 10), bg=config.BG),
              tk.Label(self.room_window, text='+ 10 HP\nRestore 50% of HP', font=config.FONT, anchor=tk.CENTER,
                       bg=config.BG))
        defence = (tk.Button(self.room_window, text='+ DEF', font=config.FONT,
                             command=lambda: self.room_util(self.player.add_def, 2), bg=config.BG),
                   tk.Label(self.room_window, text='+ 2 DEF', font=config.FONT, anchor=tk.CENTER, bg=config.BG))
        atk = (tk.Button(self.room_window, text='+ ATK', font=config.FONT,
                         command=lambda: self.room_util(self.player.add_atk, 2), bg=config.BG),
               tk.Label(self.room_window, text='+ 2 ATK', font=config.FONT, anchor=tk.CENTER, bg=config.BG))
        luck = (tk.Button(self.room_window, text='+ LUCK', font=config.FONT,
                          command=lambda: self.room_util(self.player.add_luck, 1), bg=config.BG),
                tk.Label(self.room_window, text='+ 1 LUCK', font=config.FONT, anchor=tk.CENTER, bg=config.BG))

        buffs = [hp, defence, atk, luck]
        chosen = random.sample(buffs, 3)
        for i, j in zip(chosen, range(3)):
            i[0].grid(row=1, column=j, sticky=tk.NSEW, padx=5, pady=5)
            i[1].grid(row=2, column=j, sticky=tk.N, padx=5, pady=5)
        tk.Label(self.room_window, text='Choose your room reward', font=config.FONT, anchor=tk.CENTER,
                 bg=config.BG).grid(row=0,
                                    column=0,
                                    columnspan=3,
                                    sticky=tk.NSEW)

    def floor_util(self, action, value):
        action(value)
        self.window.after(2000, self.enemy_turn)
        self.update_ui()
        self.window.deiconify()
        self.floor_window.destroy()

    def choose_floor_reward(self):
        self.window.withdraw()
        self.floor_window = tk.Toplevel(self.window)
        self.floor_window.geometry(f'600x800+{self.screen_width // 2 - 300}+{self.screen_height // 2 - 400}')
        self.floor_window.configure(bg=config.BG)
        self.floor_window.grid_rowconfigure(0, weight=1)
        self.floor_window.grid_rowconfigure(1, weight=2)
        self.floor_window.grid_rowconfigure(2, weight=2)
        self.floor_window.grid_columnconfigure(0, weight=1, uniform="buttons")
        self.floor_window.grid_columnconfigure(1, weight=1, uniform="buttons")
        self.floor_window.grid_columnconfigure(2, weight=1, uniform="buttons")

        tk.Button(self.floor_window, text='+ HP', font=config.FONT,
                  command=lambda: self.floor_util(self.player.add_hp, self.player.hp / 2), bg=config.BG).grid(row=1,
                                                                                                              column=0,
                                                                                                              sticky=tk.NSEW,
                                                                                                              padx=5,
                                                                                                              pady=5)
        tk.Label(self.floor_window, text='+ 50% HP\nRestore 50% of HP', font=config.FONT, anchor=tk.CENTER,
                 bg=config.BG).grid(row=2,
                                    column=0,
                                    sticky=tk.N,
                                    padx=5,
                                    pady=5)
        tk.Button(self.floor_window, text='+ DEF', font=config.FONT,
                  command=lambda: self.floor_util(self.player.add_def, 10), bg=config.BG).grid(row=1, column=1,
                                                                                               sticky=tk.NSEW,
                                                                                               padx=5, pady=5)
        tk.Label(self.floor_window, text='+ 10 DEF', font=config.FONT, anchor=tk.CENTER, bg=config.BG).grid(row=2,
                                                                                                            column=1,
                                                                                                            sticky=tk.N,
                                                                                                            padx=5,
                                                                                                            pady=5)
        tk.Button(self.floor_window, text='+ ATK', font=config.FONT,
                  command=lambda: self.floor_util(self.player.add_atk, 5), bg=config.BG).grid(row=1, column=2,
                                                                                              sticky=tk.NSEW, padx=5,
                                                                                              pady=5)
        tk.Label(self.floor_window, text='+ 5 ATK', font=config.FONT, anchor=tk.CENTER, bg=config.BG).grid(row=2,
                                                                                                           column=2,
                                                                                                           sticky=tk.N,
                                                                                                           padx=5,
                                                                                                           pady=5)

        tk.Label(self.floor_window, text='Choose your floor reward', font=config.FONT, anchor=tk.CENTER,
                 bg=config.BG).grid(row=0,
                                    column=0,
                                    columnspan=3,
                                    sticky=tk.NSEW)

    def boss_fight(self):
        self.player.heal(self.player.hp)
        self.current_enemy = mage.Mage(room=self.room, floor=self.floor, enemy=True)

    def death(self):
        self.window.withdraw()
        self.death_window = tk.Toplevel(self.window)
        self.death_window.geometry(f'600x800+{self.screen_width // 2 - 300}+{self.screen_height // 2 - 400}')
        self.death_window.configure(bg=config.BG)
        tk.Label(self.death_window, text='You are dead', font=config.FONT, anchor=tk.CENTER, bg=config.BG).pack(
            anchor=tk.CENTER)

    def win(self):
        self.window.withdraw()
        self.win_window = tk.Toplevel(self.window)
        self.win_window.geometry(f'600x800+{self.screen_width // 2 - 300}+{self.screen_height // 2 - 400}')
        self.win_window.configure(bg=config.BG)
        tk.Label(self.win_window, text='Congratulations!\n You have beaten this game!', font=config.FONT,
                 anchor=tk.CENTER, bg=config.BG).pack(anchor=tk.CENTER)

    def start(self):
        self.choose_race()
        self.init_ui()
        self.window.mainloop()


game = Game()
game.start()

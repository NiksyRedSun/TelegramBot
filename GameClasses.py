class Unit:
    def __init__(self, s_name: str, s_story: str, s_hp: int, s_attack: int, s_defense: int, s_initiative: int):
        self.name = s_name
        self.story = s_story
        self.hp = s_hp
        self.max_hp = self.hp
        self.attack = s_attack
        self.defense = s_defense
        self.initiative = s_initiative
        self.alive = True


    def check_alive(self):
        if self.hp <= 0:
            self.hp = 0
            self.alive = False


    def reset(self):
        self.alive = True
        self.hp = self.max_hp



class Character(Unit):
    def __init__(self, s_name: str, s_story: str, s_hp: int, s_attack: int, s_defense: int, s_initiative: int):
        super().__init__(s_name, s_story, s_hp, s_attack, s_defense, s_initiative)
        self.money = 0
        self.level = 1
        self.exp = 0
        self.next_level_exp = 100


    def presentation(self):

        def str_to_deathstr(string: str):
            new_string = map(lambda x: '/', string)
            return ''.join(new_string)

        pres_name = "+" + self.name.center(50, "-") + "+"
        pres_level = "+" + ("Уровень: " + str(self.level)).center(46 + len(self.name) - 3, "-") + "+"
        text = [
                f"{pres_name}",
                f"{self.story}",
                f"Здоровье: ".ljust(20) + f"{self.hp}/{self.max_hp}",
                f"Атака: ".ljust(24) + f"{self.attack}",
                f"Защита: ".ljust(22) + f"{self.defense}",
                f"Инициатива: ".ljust(17) + f"{self.initiative}",
                f"Золото: ".ljust(23) + f"{self.money}",
                f"Опыт: ".ljust(24) + f"{self.exp}/{self.next_level_exp}",
                f"{pres_level}"
                ]
        if self.alive:
            return '\n'.join(text)
        else:
            pres_name = "+" + ("Дух " + self.name).center(56, "-") + "+"
            text = [str_to_deathstr(text[i]) if i != 2 else text[i] for i in range(len(text))]
            text[0] = pres_name
            return '\n'.join(text)



    def fight_presentation(self):
        pres_name = "+" + self.name.center(29, "-") + "+"
        text = [
                f"{pres_name}",
                f"Здоровье: {self.hp}/{self.max_hp}".center(27),
                f"Атака: {self.attack}",
                f"Защита: {self.defense}",
                f"Инициатива: {self.initiative}"]
        return '\n'.join(text)


    def next_level(self):
        while self.exp > self.next_level_exp:
            self.next_level_exp = self.next_level_exp * 2 ** self.level
            self.level += 1
            self.max_hp += 3
            self.hp = self.max_hp
            self.initiative += 1
            self.attack += 1
            self.defense += 1



class Villian(Unit):
    def __init__(self, s_name: str, s_story: str, s_hp: int, s_attack: int, s_defense: int, s_initiative: int):
        super().__init__(s_name, s_story, s_hp, s_attack, s_defense, s_initiative)
        self.money = 250
        self.exp = 1000

    def presentation(self):
        text = [f"Ваш противник: {self.name}", f"{self.story}"]
        return '\n'.join(text)

    def fight_presentation(self):
        pres_name = "+" + self.name.center(29, "-") + "+"
        text = [f"{pres_name}", f"Здоровье: {self.hp}/{self.max_hp}".center(27)]
        return '\n'.join(text)
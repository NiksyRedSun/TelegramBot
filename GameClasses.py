
class Unit:
    def __init__(self, s_name: str, s_story: str, s_hp: int, s_attack: int, s_initiative: int):
        self.name = s_name
        self.story = s_story
        self.hp = s_hp
        self.max_hp = self.hp
        self.attack = s_attack
        self.initiative = s_initiative
        self.alive = True


    def check_alive(self):
        if self.hp <= 0:
            self.alive = False


    def reset(self):
        self.alive = True
        self.hp = self.max_hp



class Character(Unit):
    def __init__(self, s_name: str, s_story: str, s_hp: int, s_attack: int, s_initiative: int):
        super().__init__(s_name, s_story, s_hp, s_attack, s_initiative)
        self.money = 0
        self.level = 1
        self.exp = 0
        self.next_level_exp = 100


    def presentation(self):
        pres_name = "+" + self.name.center(60, "-") + "+"
        pres_level = "+" + ("Уровень: " + str(self.level)).center(55, "-") + "+"
        text = [f"{pres_name}", f"{self.story}", f"Ваше здоровье: {self.hp}/{self.max_hp}",
                f"Ваш коэффициент урона: {self.attack}", f"Ваша инициатива: {self.initiative}", f"Ваше золото: {self.money}",
                f"Ваш опыт: {self.exp}/{self.next_level_exp}",
                f"{pres_level}"]
        return '\n'.join(text)


    def fight_presentation(self):
        text = [f"+------{self.name}------+", f"Ваше здоровье: {self.hp}/{self.max_hp}",
                f"Ваш коэффициент урона {self.attack}", f"Ваша инициатива {self.initiative}"]
        return '\n'.join(text)


    def next_level(self):
        while self.exp > self.next_level_exp:
            self.next_level_exp = self.next_level_exp * 2 ** self.level
            self.level += 1
            self.max_hp += 3
            self.hp = self.max_hp
            self.initiative += 1
            self.attack += 1





class Villian(Unit):
    def __init__(self, s_name: str, s_story: str, s_hp: int, s_attack: int, s_initiative: int):
        super().__init__(s_name, s_story, s_hp, s_attack, s_initiative)
        self.money = 250

    def presentation(self):
        text = [f"Ваш противник: {self.name}", f"{self.story}"]
        return '\n'.join(text)

    def fight_presentation(self):
        text = [f"+-{self.name}-+", f"Его здоровье: {self.hp}/{self.max_hp}"]
        return '\n'.join(text)
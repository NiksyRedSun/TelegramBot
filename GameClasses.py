
class Unit:
    def __init__(self, s_name: str, s_story: str, s_hp: int, s_attack: int, s_initiative: int):
        self.name = s_name
        self.story = s_story
        self.hp = s_hp
        self.max_hp = self.hp
        self.attack = s_attack
        self.initiative = s_initiative
        self.alive = True


    def presentation(self):
        text = [f"Ваше имя: {self.name}", f"{self.story}", f"Ваше максимальное здоровье {self.hp}",
                f"Ваш коэффициент урона {self.attack}", f"Ваша инициатива {self.initiative}"]

        return '\n'.join(text)

    def fight_presentation(self):
        text = [f"+------{self.name}------+", f"Ваше здоровье: {self.hp}/{self.max_hp}",
                f"Ваш коэффициент урона {self.attack}", f"Ваша инициатива {self.initiative}"]

        return '\n'.join(text)

    def check_alive(self):
        if self.hp <= 0:
            self.alive = False



class Villian(Unit):

    def presentation(self):
        text = [f"Ваш противник: {self.name}", f"{self.story}"]
        return '\n'.join(text)

    def fight_presentation(self):
        text = [f"+-{self.name}-+", f"Его здоровье: {self.hp}/{self.max_hp}",]

        return '\n'.join(text)
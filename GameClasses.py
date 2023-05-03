import random
import asyncio
from EasyGameLoader import bot



def double_dices():
    return random.randint(1, 6) + random.randint(1, 6)


def dice():
    return random.randint(1, 6)



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


    async def attack_func(self, villian: Unit, message):
        await message.answer(text = f"{self.name} замахивается на противника")
        await asyncio.sleep(0.5)
        hero_init = double_dices() + self.initiative
        villian_init = double_dices() + villian.initiative
        if hero_init > villian_init:


            crit = random.randint(1, 100)
            if crit in range(1, self.initiative * 6):
                hit_damage = self.attack * 2
                await message.answer(text=f"*<b>КРИТИЧЕСКИЙ УДАР</b>*", parse_mode="HTML")
            else:
                hit_damage = self.attack


            damage = hit_damage + dice() - villian.defense
            if damage <= 0:
                await message.answer(text=f"Изловчившись {self.name} попадает по противнику, но тот остается невредим")
            else:
                villian.hp -= damage
                await message.answer(text=f"{self.name} наносит удар, который попадает прямо в цель, нанеся {damage} урона")
                villian.check_alive()

        else:
            await message.answer(text=f"Однако его удар пролетает мимо врага")




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


class DragonVillian(Villian):
    def __init__(self):
        self.name = "Красный дракон"
        self.story = "Его чешуя отливает бордово-винным цветом, но все почему-то говорят, что он красный"
        self.hp = 230
        self.max_hp = self.hp
        self.attack = 8
        self.defense = 4
        self.initiative = 5
        self.alive = True
        self.money = 250
        self.exp = 1000


    async def attack_one_func(self, players: dict, char, bot, quouteIndex):
        if char.alive:
            pos_quotes = [f"{char.name} успевает уклониться от хвоста", f"{char.name} успевает уклониться от столба пламени",
                            f"{char.name} вовремя закрывает уши", f"{char.name} избегает действия порыва ветра"]
            villian_init = double_dices() + self.initiative
            char_init = double_dices() + char.initiative
            if villian_init > char_init:
                damage = self.attack + dice() - char.defense
                # if critical_hit:
                #     neg_quotes = [f"{char.name} подлетает вверх на 5 метров, а потом получает {damage} урона от падения",
                #                   f"{char.name} получает {damage} единиц урона от горения, задержавшись в пламени на две секунды",
                #                   f"{char.name} роняет барабанные перепонки и теряет {damage} hp",
                #                   f"{char.name} теряет равновесие, и оказавшись в когтях дракона теряет {damage} hp"]

                neg_quotes = [f"{char.name} получает {damage} урона от удара хвостом",
                              f"{char.name} получает {damage} единиц урона от ожогов, задержавшись в пламени на пол секунды",
                              f"{char.name} теряет кровь из ушей и {damage} hp",
                              f"{char.name} отлетает от дракона и теряет {damage} hp"]
                if damage <= 0:
                    for player in players:
                        await bot.send_message(chat_id=player, text=pos_quotes[quouteIndex])
                else:
                    char.hp -= damage
                    char.check_alive()
                    for player in players:
                        await bot.send_message(chat_id=player, text=neg_quotes[quouteIndex])
            else:
                for player in players:
                    await bot.send_message(chat_id=player, text=pos_quotes[quouteIndex])




    async def attack_func(self, players: dict, bot):
        quoteIndex = random.randint(0, 3)
        quotes = [f"{self.name} замахивается своим хвостом", f"{self.name} готовится залить все огнем",
                  f"{self.name} издает пронзительный рев", f"{self.name} хлопает крыльями"]
        for player in players:
            text = random.choice(quotes)
            await bot.send_message(chat_id=player, text=quotes[quoteIndex])
        await asyncio.sleep(1.5)
        for player in players:
            await self.attack_one_func(players, players[player], bot, quoteIndex)

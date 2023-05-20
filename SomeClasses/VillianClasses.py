import random
import asyncio
from EasyGameLoader import bot
from SomeClasses.BasicClasses import Unit, dice, double_dices
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from SomeKeyboards import attack_menu_keyb, death_menu_keyb, end_menu_keyb


class Villian(Unit):
    def __init__(self):
        self.money = None
        self.exp = None


    def presentation(self):
        text = [f"Ваш противник: {self.name}", f"{self.story}"]
        return '\n'.join(text)

    def fight_presentation(self):
        pres_name = "+" + self.name.center(22, "-") + "+"
        text = [f"<code>{pres_name}</code>", f"Здоровье: {self.hp}/{self.max_hp}".center(35)]
        return '\n'.join(text)

    def reset(self):
        self.__init__()

    async def boss_money_exp_dealing(self, all_players: dict, players: dict, bot):
        cur_money = int(self.money / len(all_players))
        cur_exp = int(self.exp / len(all_players))
        text = ["<code>+" + "Результаты".center(28, "-") + "+</code>",
                "<b><code>" + "Рейд-босс мертв".center(30, " ") + "</code></b>\n",
                "Урон игроков:"]

        for id in sorted(players.items(), key=lambda x: x[1]["damage"], reverse=True):
            text.append(f"{id[1]['char'].name} - {id[1]['damage']} урона")


        if sorted(players.keys()) != sorted(all_players.keys()):
            text.append(f"\nПали в бою:")
            for player in all_players:
                if player not in players:
                    text.append(f"{all_players[player].name}")

        text.append(f"\nКаждый из участников битвы получил по {cur_money} монет")
        text.append(f"Каждый из участников битвы получил по {cur_exp} опыта")

        for player in all_players.copy():
            all_players[player].money += cur_money
            all_players[player].exp += cur_exp
            all_players[player].next_level()
            await bot.send_message(chat_id=player,
                                   text='\n'.join(text),
                                   parse_mode="HTML",
                                   reply_markup=end_menu_keyb)




class DragonVillian(Villian):
    def __init__(self):
        self.name = "Красный дракон"
        self.story = "Чешуя отливает бордово-винным, но все почему-то говорят, что он красный"
        self.hp = 230
        self.max_hp = self.hp
        self.attack = 8
        self.defense = 4
        self.initiative = 5
        self.alive = True
        self.money = random.randint(250, 1000)
        self.exp = random.randint(850, 1350)
        self.quoteIndex = 0
        self.dead_quotes = [f"Это был последний взмах хвоста Красного дракона",
                      f"{self.name} больше никого не зальет огнем",
                      f"Теперь {self.name} уж точно никогда не будет рычать",
                      f"{self.name} схлапывается сам",
                      f"{self.name} упал, вытянув ноги"]



    def attack_one_func(self, char, text: list):
        if char.alive:
            pos_quotes = [f"{char.name} успевает уклониться от хвоста Красного дракона",
                          f"{char.name} успевает уклониться от столба пламени Красного дракона",
                            f"{char.name} вовремя закрывает уши и не слышит рева Красного дракона",
                          f"{char.name} избегает действия порыва ветра созданного Красным драконом",
                          f"{char.name} уворачивается от когтей Красного дракона"]
            villian_init = double_dices() + self.initiative
            char_init = double_dices() + char.initiative

            if villian_init > char_init:
                damage = self.attack + dice() - char.defense
                neg_quotes = [f"{char.name} получает {damage} урона от удара хвостом, устояв на ногах",
                              f"{char.name} получает {damage} единиц урона от ожогов, задержавшись в пламени на пол секунды",
                              f"{char.name} ловит головную боль, теряя {damage} hp",
                              f"От порыва ветра {char.name} падает на землю теряя {damage} hp",
                              f"{char.name} не успевает увернуться от когтей теряя {damage} hp"]

                really_neg_quotes = [f"{char.name} отлетает от хвоста дракона на 10 метров и получает {damage} урона",
                              f"{char.name} получает {damage} единиц урона от горения, задержавшись в пламени на полторы секунды",
                              f"{char.name} теряет кровь из ушей и {damage} hp",
                              f"{char.name} прижат к земле порывом ветра и теряет {damage} hp",
                              f"{char.name} поднят когтями и сброшен, потеряв {damage} hp"]

                if damage <= 0:
                    text.append(pos_quotes[self.quoteIndex])
                else:
                    char.hp -= damage
                    if damage > 10:
                        text.append(really_neg_quotes[self.quoteIndex])
                    else:
                        text.append(neg_quotes[self.quoteIndex])
                    char.check_alive()
                    if not char.alive:
                        text.append(f"<b>{char.name} отъезжает в ходе битвы</b>\n")
                    else:
                        text.append("")
            else:
                text.append(pos_quotes[self.quoteIndex])


    async def attack_func(self, players: dict, bot):
        if not self.alive:
            return None
        self.quoteIndex = random.randint(0, 4)
        quotes = [f"{self.name} замахивается своим хвостом",
                  f"{self.name} готовится залить все огнем",
                  f"{self.name} издает пронзительный рев",
                  f"{self.name} хлопает крыльями",
                  f"{self.name} взлетел и приготовил когти для атаки"]
        for player in players.copy():
            await bot.send_message(chat_id=player, text=quotes[self.quoteIndex])
        await asyncio.sleep(2)

        self.check_alive()
        if not self.alive:
            return None

        message_text = []
        for player in players:
            self.attack_one_func(players[player]["char"], message_text)
        for player in players.copy():
            await bot.send_message(chat_id=player, text="\n".join(message_text), parse_mode="HTML")
        self.quoteIndex = None


class SpiderVillian(Villian):
    def __init__(self):
        self.name = "Огромный паук"
        self.story = "Представьте паука размером с медведя"
        self.hp = 250
        self.max_hp = self.hp
        self.attack = 6
        self.defense = 3
        self.initiative = 6
        self.alive = True
        self.money = random.randint(250, 1000)
        self.exp = random.randint(850, 1350)
        self.quoteIndex = 0
        self.dead_quotes = [f"{self.name} упал замертво",
                  f"{self.name} больше никогда не будет плевать кислотой",
                  f"Теперь {self.name} склеил лапы",
                  f"{self.name} подавился собственными жвалами"]



    def attack_one_func(self, char, text: list):
        if char.alive:
            pos_quotes = [f"{char.name} успевает уклониться от сетки паука",
                          f"{char.name} успевает увернуться от кислоты",
                            f"{char.name} уворачивается от лап паука",
                          f"{char.name} избежал жвал паука"]
            villian_init = double_dices() + self.initiative
            char_init = double_dices() + char.initiative
            if villian_init > char_init:
                damage = self.attack + dice() - char.defense

                neg_quotes = [f"{char.name} падает на пол запутавшись в паутине и получает {damage} урона",
                              f"{char.name} получает {damage} урона кислотой",
                              f"{char.name} проткнут передней лапой паука на {damage} hp",
                              f"{char.name} зацеплен жвалами паука на {damage} hp"]

                really_neg_quotes = [f"{char.name} падает на пол запутавшись в паутине, ударяется головой и получает {damage} урона",
                              f"{char.name} получает {damage} урона кислотой до костей",
                              f"{char.name} проткнут передней лапой паука насквозь на {damage} hp",
                              f"{char.name} застрял в жвалах паука на {damage} hp"]

                if damage <= 0:
                    text.append(pos_quotes[self.quoteIndex])
                else:
                    char.hp -= damage
                    if damage > 10:
                        text.append(really_neg_quotes[self.quoteIndex])
                    else:
                        text.append(neg_quotes[self.quoteIndex])
                    char.check_alive()
                    if not char.alive:
                        text.append(f"<b>{char.name} отъезжает в ходе битвы</b>\n")
                    else:
                        text.append("")
            else:
                text.append(pos_quotes[self.quoteIndex])


    async def attack_func(self, players: dict, bot):
        if not self.alive:
            return None
        self.quoteIndex = random.randint(0, 3)
        quotes = [f"{self.name} выстреливает сеткой из паутины",
                  f"{self.name} плюется кислотой",
                  f"{self.name} замахивается передними лапами",
                  f"{self.name} готовится пустить в ход жвалы"]
        for player in players.copy():
            await bot.send_message(chat_id=player, text=quotes[self.quoteIndex])
        await asyncio.sleep(2)

        self.check_alive()
        if not self.alive:
            return None

        message_text = []
        for player in players:
            self.attack_one_func(players[player]["char"], message_text)
        for player in players.copy():
            await bot.send_message(chat_id=player, text="\n".join(message_text), parse_mode="HTML")
        self.quoteIndex = None


class GolemVillian(Villian):
    def __init__(self):
        self.name = "Железный голем"
        self.story = "Цельнометалический парень высотой в 2,5 метра, размахивает кулаком-молотом"
        self.hp = 300
        self.max_hp = self.hp
        self.attack = 8
        self.defense = 5
        self.initiative = 4
        self.alive = True
        self.money = random.randint(700, 1500)
        self.exp = random.randint(1000, 1550)
        self.quoteIndex = 0
        self.dead_quotes = [f"{self.name} теряет равновесие и разливает масло",
                      f"{self.name} теряет свое кипящее масло",
                      f"Это были последние колышки, которыми он планировал выстрелить",
                      f"{self.name} падает на бегу"]



    def attack_one_func(self, char, text: list):
        if char.alive:
            pos_quotes = [f"{char.name} успевает уклониться от кулака-молота",
                          f"{char.name} успевает увернуться от кипящего масла",
                            f"{char.name} уворачивается от колышков",
                          f"{char.name} избегает столкновения с Големом"]
            villian_init = double_dices() + self.initiative
            char_init = double_dices() + char.initiative
            if villian_init > char_init:
                damage = self.attack + dice() - char.defense
                neg_quotes = [f"{char.name} теряет зубы и {damage} hp от кулака-молота",
                              f"{char.name} получает {damage} урона будучи залит потоком масла",
                              f"{char.name} обнаруживает в себе стальной колышек на {damage} hp",
                              f"{char.name} получает головой Голема в свою и теряет {damage} hp"]

                really_neg_quotes = [f"{char.name} теряет лицо и {damage} hp от кулака-молота",
                              f"{char.name} получает {damage} урона упав в кипящее масло",
                              f"{char.name} обнаруживает в себе два стальных колышка на {damage} hp",
                              f"{char.name} получает головой Голема в свою и падая на пол, теряет {damage} hp"]

                if damage <= 0:
                    text.append(pos_quotes[self.quoteIndex])
                else:
                    char.hp -= damage
                    if damage > 10:
                        text.append(really_neg_quotes[self.quoteIndex])
                    else:
                        text.append(neg_quotes[self.quoteIndex])
                    char.check_alive()
                    if not char.alive:
                        text.append(f"<b>{char.name} отъезжает в ходе битвы</b>\n")
                    else:
                        text.append("")
            else:
                text.append(pos_quotes[self.quoteIndex])


    async def attack_func(self, players: dict, bot):
        if not self.alive:
            return None
        self.quoteIndex = random.randint(0, 3)
        quotes = [f"{self.name} замахивается кулаком-молотом",
                  f"{self.name} пускает в ход кипящее масло",
                  f"{self.name} готовится выстрелить стальными колышками",
                  f"{self.name} разгоняется для удара"]
        for player in players.copy():
            await bot.send_message(chat_id=player, text=quotes[self.quoteIndex])
        await asyncio.sleep(2)

        self.check_alive()
        if not self.alive:
            return None

        message_text = []
        for player in players:
            self.attack_one_func(players[player]["char"], message_text)
        for player in players.copy():
            await bot.send_message(chat_id=player, text="\n".join(message_text), parse_mode="HTML")
        self.quoteIndex = None



class TreeVillian(Villian):
    def __init__(self):
        self.name = "Гнилое дерево"
        self.story = "Это дерево... Оно живое и похоже не радо, что кто-то заглянул на его болото"
        self.hp = 270
        self.max_hp = self.hp
        self.attack = 7
        self.defense = 4
        self.initiative = 5
        self.alive = True
        self.money = random.randint(700, 1300)
        self.exp = random.randint(1000, 1550)
        self.quoteIndex = 0
        self.dead_quotes = [f"{self.name} роняет ветки",
                      f"{self.name} переворачивается корнями вверх",
                      f"{self.name} тонет в собственной гнили",
                      f"{self.name} перераскрыло свой потенциал"]



    def attack_one_func(self, char, text: list):
        if char.alive:
            pos_quotes = [f"{char.name} успевает уклониться от веток",
                          f"{char.name} успевает увернуться от корней",
                            f"{char.name} уклоняется от гнилых плодов",
                          f"{char.name} успевает отвернуться от вылетающих насекомых"]
            villian_init = double_dices() + self.initiative
            char_init = double_dices() + char.initiative
            if villian_init > char_init:
                damage = self.attack + dice() - char.defense
                neg_quotes = [f"{char.name} получает удар ветками по лицу и {damage} урона",
                              f"{char.name} получил корнем в живот и теряет {damage} hp",
                              f"{char.name} обнаруживает на себе химические ожоги от гнилых плодов и потерю {damage} hp",
                              f"{char.name} окружен, вылетающими из кроны дерева насекомыми, откусывающими от него {damage} hp"]

                really_neg_quotes = [f"{char.name} получает удар ветками в глаза и {damage} урона",
                              f"{char.name} сбит с ног корнями Дерева, теряет {damage} hp",
                              f"{char.name} обнаруживает на себе химические ожоги до кости от гнилых плодов и потерю {damage} hp",
                              f"{char.name} оказывается заперт в кроне дерева с ульем, проедающим ему лицо на {damage} hp"]

                if damage <= 0:
                    text.append(pos_quotes[self.quoteIndex])
                else:
                    char.hp -= damage
                    if damage > 10:
                        text.append(really_neg_quotes[self.quoteIndex])
                    else:
                        text.append(neg_quotes[self.quoteIndex])
                    char.check_alive()
                    if not char.alive:
                        text.append(f"<b>{char.name} отъезжает в ходе битвы</b>\n")
                    else:
                        text.append("")
            else:
                text.append(pos_quotes[self.quoteIndex])


    async def attack_func(self, players: dict, bot):
        if not self.alive:
            return None
        self.quoteIndex = random.randint(0, 3)
        quotes = [f"{self.name} замахивается ветками",
                  f"{self.name} пускает в ход свои корни",
                  f"{self.name} роняет гнилые плоды",
                  f"{self.name} приподнимает свои листья, раскрывая крону"]
        for player in players.copy():
            await bot.send_message(chat_id=player, text=quotes[self.quoteIndex])
        await asyncio.sleep(2)

        self.check_alive()
        if not self.alive:
            return None

        message_text = []
        for player in players:
            self.attack_one_func(players[player]["char"], message_text)
        for player in players.copy():
            await bot.send_message(chat_id=player, text="\n".join(message_text), parse_mode="HTML")
        self.quoteIndex = None



class WyvernVillian(Villian):
    def __init__(self):
        self.name = "Виверна"
        self.story = "Знаете чем отличается виверна от дракона? Одной парой лап, жалом на конце хвоста и отсутствием огненного дыхания"
        self.hp = 300
        self.max_hp = self.hp
        self.attack = 8
        self.defense = 4
        self.initiative = 6
        self.alive = True
        self.money = random.randint(1000, 1800)
        self.exp = random.randint(1200, 1800)
        self.quoteIndex = 0
        self.dead_quotes = [f"Виверна роняет своё жало",
                      f"Пикирование виверны переходит в падение",
                      f"Из пасти Виверны вырывается кровь, орошая поле боя"]



    def attack_one_func(self, char, text: list):
        if char.alive:
            pos_quotes = [f"{char.name} успевает уклониться от жала",
                          f"{char.name} уворачивается от когтей",
                            f"{char.name} уклоняется от зубов"]
            villian_init = double_dices() + self.initiative
            char_init = double_dices() + char.initiative
            if villian_init > char_init:
                damage = self.attack + dice() - char.defense
                neg_quotes = [f"{char.name} проткнут жалом Виверны на {damage} урона",
                              f"{char.name} не успевает уклониться от когтей Виверны получив {damage} урона ",
                              f"{char.name} зацеплен зубами Виверны на {damage} урона"]

                really_neg_quotes = [f"{char.name} проткнут жалом Виверны и обильно снабжен ядом на {damage} урона",
                              f"{char.name} отлетает на несколько метров от когтей Виверны получив {damage} урона ",
                              f"{char.name} оказывается в зубах Виверны и взлетает с ней ввысь, с последующим падением на {damage} урона"]

                if damage <= 0:
                    text.append(pos_quotes[self.quoteIndex])
                else:
                    char.hp -= damage
                    if damage > 10:
                        text.append(really_neg_quotes[self.quoteIndex])
                    else:
                        text.append(neg_quotes[self.quoteIndex])
                    char.check_alive()
                    if not char.alive:
                        text.append(f"<b>{char.name} отъезжает в ходе битвы</b>\n")
                    else:
                        text.append("")
            else:
                text.append(pos_quotes[self.quoteIndex])


    async def attack_func(self, players: dict, bot):
        if not self.alive:
            return None
        self.quoteIndex = random.randint(0, 2)
        quotes = [f"{self.name} приготовила своё жало",
                  f"{self.name} пикирует, выставив вперед когти",
                  f"{self.name} готовит свои зубы для захвата"]
        for player in players.copy():
            await bot.send_message(chat_id=player, text=quotes[self.quoteIndex])
        await asyncio.sleep(2)

        self.check_alive()
        if not self.alive:
            return None

        message_text = []
        for player in players:
            self.attack_one_func(players[player]["char"], message_text)
        for player in players.copy():
            await bot.send_message(chat_id=player, text="\n".join(message_text), parse_mode="HTML")
        self.quoteIndex = None




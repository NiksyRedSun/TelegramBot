import random
import asyncio
from EasyGameLoader import bot
from SomeClasses.BasicClasses import Unit, dice, double_dices



class Villian(Unit):
    def __init__(self):
        self.money = None
        self.exp = None


    def presentation(self):
        text = [f"Ваш противник: {self.name}", f"{self.story}"]
        return '\n'.join(text)

    def fight_presentation(self):
        pres_name = "+" + self.name.center(29, "-") + "+"
        text = [f"<code>{pres_name}</code>", f"Здоровье: {self.hp}/{self.max_hp}".center(54)]
        return '\n'.join(text)

    def reset(self):
        self.__init__()

    async def boss_money_exp_dealing(self, players: dict, message):
        cur_money = int(self.money / len(players))
        cur_exp = int(self.exp / len(players))
        for i in players:
            players[i].money += cur_money
            players[i].exp += cur_exp
        text = [f"Каждый из участников битвы получил по {cur_money} монет", f"Каждый из участников битвы получил по {cur_exp} опыта"]
        await message.answer(text='\n'.join((text)))



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



    def attack_one_func(self, char, quouteIndex, text: list):
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
                neg_quotes = [f"{char.name} получает {damage} урона от удара хвостом",
                              f"{char.name} получает {damage} единиц урона от ожогов, задержавшись в пламени на пол секунды",
                              f"{char.name} теряет кровь из ушей и {damage} hp",
                              f"От порыва ветра {char.name} падает на землю теряя {damage} hp",
                              f"{char.name} не успевает увернуться от когтей теряя {damage} hp"]
                if damage <= 0:
                    text.append(pos_quotes[quouteIndex])
                else:
                    char.hp -= damage
                    text.append(neg_quotes[quouteIndex])
                    char.check_alive()
                    if not char.alive:
                        text.append(f"<b>{char.name} отъезжает в ходе битвы</b>")
            else:
                text.append(pos_quotes[quouteIndex])




    async def attack_func(self, players: dict, bot):
        quoteIndex = random.randint(0, 4)
        quotes = [f"{self.name} замахивается своим хвостом",
                  f"{self.name} готовится залить все огнем",
                  f"{self.name} издает пронзительный рев",
                  f"{self.name} хлопает крыльями",
                  f"{self.name} взлетел и приготовил когти для атаки"]
        for player in players:
            await bot.send_message(chat_id=player, text=quotes[quoteIndex])
        await asyncio.sleep(2)
        message_text = []
        for player in players:
            self.attack_one_func(players[player], quoteIndex, message_text)
        for player in players:
            await bot.send_message(chat_id=player, text="\n".join(message_text), parse_mode="HTML")


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



    def attack_one_func(self, char, quouteIndex, text: list):
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
                              f"{char.name} застрял в жвалах паука на {damage} hp"]
                if damage <= 0:
                    text.append(pos_quotes[quouteIndex])
                else:
                    char.hp -= damage
                    text.append(neg_quotes[quouteIndex])
                    char.check_alive()
                    if not char.alive:
                        text.append(f"<b>{char.name} отъезжает в ходе битвы</b>")
            else:
                text.append(pos_quotes[quouteIndex])


    async def attack_func(self, players: dict, bot):
        quoteIndex = random.randint(0, 3)
        quotes = [f"{self.name} выстреливает сеткой из паутины",
                  f"{self.name} плюется кислотой",
                  f"{self.name} замахивается передними лапами",
                  f"{self.name} готовится пустить в ход жвалы"]
        for player in players:
            await bot.send_message(chat_id=player, text=quotes[quoteIndex])
        await asyncio.sleep(2)
        message_text = []
        for player in players:
            self.attack_one_func(players[player], quoteIndex, message_text)
        for player in players:
            await bot.send_message(chat_id=player, text="\n".join(message_text), parse_mode="HTML")


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



    def attack_one_func(self, char, quouteIndex, text: list):
        if char.alive:
            pos_quotes = [f"{char.name} успевает уклониться от кулака-молота",
                          f"{char.name} успевает увернуться от кипящего масла",
                            f"{char.name} уворачивается от колышков",
                          f"{char.name} избегает столкновения с Големом"]
            villian_init = double_dices() + self.initiative
            char_init = double_dices() + char.initiative
            if villian_init > char_init:
                damage = self.attack + dice() - char.defense
                neg_quotes = [f"{char.name} теряет зубы и {damage} урона от кулака-молота",
                              f"{char.name} получает {damage} урона кипящим маслом",
                              f"{char.name} обнаруживает в себе стальной колышек на {damage} hp",
                              f"{char.name} получает головой Голема в свою и терает {damage} hp"]
                if damage <= 0:
                    text.append(pos_quotes[quouteIndex])
                else:
                    char.hp -= damage
                    text.append(neg_quotes[quouteIndex])
                    char.check_alive()
                    if not char.alive:
                        text.append(f"<b>{char.name} отъезжает в ходе битвы</b>")
            else:
                text.append(pos_quotes[quouteIndex])


    async def attack_func(self, players: dict, bot):
        quoteIndex = random.randint(0, 3)
        quotes = [f"{self.name} замахивается кулаком-молотом",
                  f"{self.name} пускает в ход кипящее масло",
                  f"{self.name} готовится выстрелить стальными колышками",
                  f"{self.name} разгоняется для удара"]
        for player in players:
            await bot.send_message(chat_id=player, text=quotes[quoteIndex])
        await asyncio.sleep(2)
        message_text = []
        for player in players:
            self.attack_one_func(players[player], quoteIndex, message_text)
        for player in players:
            await bot.send_message(chat_id=player, text="\n".join(message_text), parse_mode="HTML")



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



    def attack_one_func(self, char, quouteIndex, text: list):
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
                              f"{char.name} сбит с ног корнями Дерева, теряет {damage} урона ",
                              f"{char.name} обнаруживает на себе химические ожоги и потерю  {damage} hp после разрыва гнилого плода рядом",
                              f"{char.name} окружен, вылетающими из кроны дерева насекомыми, откусывающими от него {damage} hp"]
                if damage <= 0:
                    text.append(pos_quotes[quouteIndex])
                else:
                    char.hp -= damage
                    text.append(neg_quotes[quouteIndex])
                    char.check_alive()
                    if not char.alive:
                        text.append(f"<b>{char.name} отъезжает в ходе битвы</b>")
            else:
                text.append(pos_quotes[quouteIndex])


    async def attack_func(self, players: dict, bot):
        quoteIndex = random.randint(0, 3)
        quotes = [f"{self.name} замахивается ветками",
                  f"{self.name} пускает в ход свои корни",
                  f"{self.name} роняет гнилые плоды",
                  f"{self.name} приподнимает свои листья"]
        for player in players:
            await bot.send_message(chat_id=player, text=quotes[quoteIndex])
        await asyncio.sleep(2)
        message_text = []
        for player in players:
            self.attack_one_func(players[player], quoteIndex, message_text)
        for player in players:
            await bot.send_message(chat_id=player, text="\n".join(message_text), parse_mode="HTML")



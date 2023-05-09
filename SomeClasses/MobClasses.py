from SomeClasses.BasicClasses import Unit, dice, double_dices
import random
import asyncio
from EasyGameLoader import bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType



class Mob(Unit):
    def __init__(self):
        self.money = None
        self.exp = None
        self.quoteIndex = 0
        self.dead_quotes = []


    def presentation(self):
        text = [f"Ваш противник: {self.name}", f"{self.story}"]
        return '\n'.join(text)

    def fight_presentation(self):
        pres_name = "+" + self.name.center(29, "-") + "+"
        text = [f"<code>{pres_name}</code>", f"Здоровье: {self.hp}/{self.max_hp}".center(54)]
        return '\n'.join(text)


    def reset(self):
        self.__init__()

    async def money_exp_having(self, player, message):
        player.money += self.money
        player.exp += self.exp
        player.next_level()
        menu = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Продолжить убивать")], [KeyboardButton(text="К выбору моба")]],
            resize_keyboard=True)
        await message.answer(text=f"{player.name} получает {self.money} монет и {self.exp} опыта за убийство", reply_markup=menu)



class SceletonMob(Mob):
    def __init__(self):
        self.name = "Скелет обыкновенный"
        self.story = "Можно разобрать парочку таких, чисто для разминки"
        self.hp = 30
        self.max_hp = self.hp
        self.attack = 6
        self.defense = 2
        self.initiative = 4
        self.alive = True
        self.money = random.randint(100, 350)
        self.exp = random.randint(100, 350)
        self.link = "/SceletonMob"
        self.quoteIndex = 0
        self.dead_quotes = [f"{self.name} разваливается на части",
                            f"{self.name}  роняет грудную клетку, оставив ноги стоять",
                            f"{self.name} пролетает вперед и разбивается о стену"]


    async def attack_func(self, char, message):
        if not self.alive or not char.alive:
            return None
        self.quoteIndex = random.randint(0, 2)
        quotes = [f"{self.name} замахивается мечом слева",
                  f"{self.name} замахивается мечом справа",
                  f"{self.name} замахивается мечом сверху"]


        await message.answer(text=quotes[self.quoteIndex], reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Атаковать")], [KeyboardButton(text="Соскочить")]], resize_keyboard=True))
        await asyncio.sleep(2)

        self.check_alive()
        if not self.alive:
            return None


        pos_quotes = [f"Вы отходите назад, успевая уклониться от меча скелета",
                      f"Вы проходите под лезвием меча скелета, не задев его",
                      f"Вы успеваете отойти в бок от летящего меча"]


        villian_init = double_dices() + self.initiative
        char_init = double_dices() + char.initiative
        if villian_init > char_init:
            damage = self.attack + dice() - char.defense
            neg_quotes = [f"Вы получаете {damage} урона от попадания меча между ребер",
                          f"Вы получаете {damage} урона от резаной раны живота",
                          f"Вы получаете скользящий удар по груди и теряете {damage} hp"]

            killed_quotes = [f"Скелет просто уходит оставляя вас умирать, оставив свой меч в ваших ребрах на прощание",
                          f"Ваши кишки начинают выпадывать наружу, вы тревожно пытаетесь засунуть их обратно, пока не понимаете, что это безнадежно. Сразу после этого вы теряете сознание",
                          f"Кажется кусок вашего легкого оказался на соседней стенке. Вам ничего не остается кроме как наблюдать за тем, как оно медленно скользит по стене. Вы теряете много крови"]

            if damage <= 0:
                await message.answer(text=pos_quotes[self.quoteIndex])
            else:
                char.hp -= damage
                await message.answer(text=neg_quotes[self.quoteIndex])
                char.check_alive()
                if not char.alive:
                    await message.answer(text=killed_quotes[self.quoteIndex], reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="Продолжить")]], resize_keyboard=True))
        else:
            await message.answer(text=pos_quotes[self.quoteIndex])




class LittleDragonMob(Mob):
    def __init__(self):
        self.name = "Молодой дракон"
        self.story = "Помните рейд-босса Красного дракона? У него есть куча детей ростом в 2 метра." \
                     "Правда, по какой-то причине - они синие"
        self.hp = 40
        self.max_hp = self.hp
        self.attack = 8
        self.defense = 3
        self.initiative = 5
        self.alive = True
        self.money = random.randint(200, 450)
        self.exp = random.randint(200, 450)
        self.link = "/LittleDragonMob"
        self.quoteIndex = 0
        self.dead_quotes = [f"{self.name} от вашего удара роняет голову",
                            f"{self.name} вопит еще в течение 3х секунд, прежде чем отдать концы",
                            f"{self.name} падает лапами вверх"]


    async def attack_func(self, char, message):
        if not self.alive or not char.alive:
            return None
        self.quoteIndex = random.randint(0, 2)
        quotes = [f"{self.name} хочет укусить вас",
                  f"{self.name} начинает пронзительно вопить",
                  f"{self.name} замахивается на вас лапами"]

        await message.answer(text=quotes[self.quoteIndex], reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Атаковать")], [KeyboardButton(text="Соскочить")]], resize_keyboard=True))
        await asyncio.sleep(2)


        self.check_alive()
        if not self.alive:
            return None

        pos_quotes = [f"Вы отходите назад, успевая уклониться зубов Молодого дракона",
                      f"Вы успеваете закрыть уши",
                      f"Вы успеваете отойти в бок от летящих в вас когтей Дракоши"]

        villian_init = double_dices() + self.initiative
        char_init = double_dices() + char.initiative
        if villian_init > char_init:
            damage = self.attack + dice() - char.defense
            neg_quotes = [f"Вы получаете {damage} урона от укуса Молодого дракона",
                          f"Вы получаете {damage} очков головной боли от пронзительного вопля дракона",
                          f"Вы находите на своем теле следы от когтей дракона на {damage} урона"]

            killed_quotes = [f"Падая на колени вы чувствуйте сильный укус на своем теле, разрывая рубашку вы видите следы зубов дракона, из которых обильно сочится кровь, вы начинаете терять сознание",
                          f"Будучи неспособным думать ни о чем кроме шума в голове и крови из ушей вы начинаете терять сознание",
                          f"Лёжа на холодном полу, вы ощущаете как дракон пытается полакомиться вашей селезенкой"]
            if damage <= 0:
                await message.answer(text=pos_quotes[self.quoteIndex])
            else:
                char.hp -= damage
                await message.answer(text=neg_quotes[self.quoteIndex])
                char.check_alive()
                if not char.alive:
                    await message.answer(text=killed_quotes[self.quoteIndex], reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="Продолжить")]], resize_keyboard=True))
        else:
            await message.answer(text=pos_quotes[self.quoteIndex])
        self.quoteIndex = None
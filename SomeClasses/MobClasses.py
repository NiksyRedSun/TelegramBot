from SomeClasses.BasicClasses import Unit, dice, double_dices
import random
import asyncio
from EasyGameLoader import bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from SomeKeyboards import next_keyb, end_menu_keyb, attack_menu_keyb, menu_keyb, mob_next_keyb



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
        await message.answer(text=f"{player.name} получает {self.money} монет и {self.exp} опыта за убийство", reply_markup=mob_next_keyb)



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


        await message.answer(text=quotes[self.quoteIndex], reply_markup=attack_menu_keyb)
        await asyncio.sleep(2)

        char.check_alive()
        self.check_alive()
        if not self.alive or not char.alive:
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
                    if char.in_attack:
                        await message.answer(text=random.choice(char.dead_quotes), reply_markup=next_keyb)
                    else:
                        await message.answer(text=killed_quotes[self.quoteIndex], reply_markup=next_keyb)
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

        await message.answer(text=quotes[self.quoteIndex], reply_markup=attack_menu_keyb)
        await asyncio.sleep(2)

        char.check_alive()
        self.check_alive()
        if not self.alive or not char.alive:
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
                    if char.in_attack:
                        await message.answer(text=random.choice(char.dead_quotes), reply_markup=next_keyb)
                    else:
                        await message.answer(text=killed_quotes[self.quoteIndex], reply_markup=next_keyb)
        else:
            await message.answer(text=pos_quotes[self.quoteIndex])
        self.quoteIndex = None



class OrcMob(Mob):
    def __init__(self):
        self.name = "Орк"
        self.story = "Типичный злой орчина. Выше вас на пол-головы, шире на половину груди. В каком-либо племени не состоит"
        self.hp = 45
        self.max_hp = self.hp
        self.attack = 9
        self.defense = 4
        self.initiative = 6
        self.alive = True
        self.money = random.randint(400, 650)
        self.exp = random.randint(400, 650)
        self.link = "/OrcMob"
        self.quoteIndex = 0
        self.dead_quotes = [f"Из Орка сыплются кишки, но кажется, что его это совсем не интересует",
                            f'"Спасибо за славную смерть", - его последние слова',
                            f"Орк встречает свою смерть, падая спокойным лицом вверх"]


    async def attack_func(self, char, message):
        if not self.alive or not char.alive:
            return None
        self.quoteIndex = random.randint(0, 2)
        quotes = [f"{self.name} замахивается на вас сверху",
                  f"{self.name} хочет ударить вас эфесом своего меча",
                  f"{self.name} готовит ногу для удара"]

        await message.answer(text=quotes[self.quoteIndex], reply_markup=attack_menu_keyb)
        await asyncio.sleep(2)


        char.check_alive()
        self.check_alive()
        if not self.alive or not char.alive:
            return None

        pos_quotes = [f"Вы отходите вбок, пропуская удар мимо себя",
                      f"Вы отводите голову вбок на пару сантиметров и этого достаточно",
                      f"Вы поворачиваете свое тело на 90 градусов по часовой стрелке и пропускаете ногу орка мимо себя"]

        villian_init = double_dices() + self.initiative
        char_init = double_dices() + char.initiative
        if villian_init > char_init:
            damage = self.attack + dice() - char.defense
            neg_quotes = [f"Вы получаете {damage} урона от рассечения груди, не успевая довернуться",
                          f"Вы недостаточно отводите голову в бок, и теряете лицо на {damage} hp",
                          f"Вы не до конца разворачиваете свое тело и получаете пяткой орка в бедро на {damage} урона"]

            killed_quotes = [f"Мгновение назад, вы отвлеклись на боль от ранения. А теперь "
                             f"вы чувствуете как вам в шею сзади помещается кинжал. Спазм шейных мышц заставляет вас еще раз посмотреть на небо перед смертью",
                          f"Последнее, что вы видите, падая на землю, это пятку забивающего вас до смерти Орка",
                          f"После небольшой потери равновесия вы теряете врага из виду, и находите кинжал у себя в пояснице. Отнявшиеся ноги не позволяют вам двигаться"
                          f"и Орк оставляет вас на съедение стервятникам"]
            if damage <= 0:
                await message.answer(text=pos_quotes[self.quoteIndex])
            else:
                char.hp -= damage
                await message.answer(text=neg_quotes[self.quoteIndex])
                char.check_alive()
                if not char.alive:
                    if char.in_attack:
                        await message.answer(text=random.choice(char.dead_quotes), reply_markup=next_keyb)
                    else:
                        await message.answer(text=killed_quotes[self.quoteIndex], reply_markup=next_keyb)
        else:
            await message.answer(text=pos_quotes[self.quoteIndex])
        self.quoteIndex = None
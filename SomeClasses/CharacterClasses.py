from SomeClasses.BasicClasses import Unit, dice, double_dices
from SomeClasses.VillianClasses import Villian
import random
import asyncio
from EasyGameLoader import bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType




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

        pres_name = "<code>" + "+" + self.name.center(30, "-") + "+" + "</code>"
        pres_level = "<code>" + "+" + ("Уровень: " + str(self.level)).center(30, "-") + "+" + "</code>"
        text = [
                f"{pres_name}",
                f" {self.story}",
                f" <code>Здоровье: ".ljust(20) + f"{self.hp}/{self.max_hp}</code>",
                f" <code>Атака: ".ljust(20) + f"{self.attack}</code>",
                f" <code>Защита: ".ljust(20) + f"{self.defense}</code>",
                f" <code>Ловкость: ".ljust(20) + f"{self.initiative}</code>",
                f" <code>Золото: ".ljust(20) + f"{self.money}</code>",
                f" <code>Опыт: ".ljust(20) + f"{self.exp}/{self.next_level_exp}</code>",
                f"{pres_level}"
                ]
        if self.alive:
            return '\n'.join(text)
        else:
            pres_name = "<code>+" + ("Дух " + self.name).center(30, "-") + "+</code>"
            text = [str_to_deathstr(text[i]) if i != 2 else text[i] for i in range(len(text))]
            text[0] = pres_name
            return '\n'.join(text)



    def fight_presentation(self):
        pres_name = "+" + self.name.center(29, "-") + "+"
        text = [
                f"<code>{pres_name}</code>",
                f"Здоровье: {self.hp}/{self.max_hp}".center(54)]
                # f"Атака: {self.attack}",
                # f"Защита: {self.defense}",
                # f"Инициатива: {self.initiative}"]
        return '\n'.join(text)


    def next_level(self):
        while self.exp > self.next_level_exp:
            self.next_level_exp = int(100 * 2 ** self.level)
            self.level += 1
            if self.level % 2 == 0:
                self.max_hp += 3
            if self.level % 3 == 0:
                self.attack += 1
                self.defense += 1
            if self.level % 4 == 0:
                self.initiative += 1
            self.hp = self.max_hp


    async def attack_boss_func(self, villian: Villian, message, bot, players):
        quoteIndex = random.randint(0, 5)
        quotes = [f"Вы замахиваетесь слева",
                  f"Вы замахиваетесь справа",
                  f"Вы замахиваетесь для рубящего, нисходящего сверху удара",
                  f"Вы замахиваетесь для рубящего, восходящего снизу удара",
                  f"Вы готовите руку для колющего удара над верхней конечностью противника",
                  f"Вы готовите руку для колющего удара под верхней конечностью противника"]

        critical_hit = False
        text = []
        await message.answer(text=quotes[quoteIndex])
        await asyncio.sleep(0.7)

        self.check_alive()
        villian.check_alive()
        if not self.alive:
            dead_quotes = [f"Вы роняете свое оружие захлебываясь кровью",
                      f"Оружие выпадывает из ваших рук, но вас гораздо больше интересует кровь, которая льется фонтаном из вашей шеи. Вы медленно теряете сознание",
                      f"Ваши внутренности выпадывают наружу, приключение больше не кажется интересным",
                      f"Ваше оружие падает, вы чувствуете как одежда начинает прилипать к телу из-за многочисленных источников кровотечения под ней. Вам стоило остаться дома",
                      f"Стоя на коленях и готовясь уйти лбом в землю, вы начинаете забывать о том как оказались здесь и медленно теряете сознание",
                      f"В последний раз взглянув на свои окровавленные руки, вы начинаете думать о том, была ли эта смерть славной. Вас погружает в вечный сон"]
            await message.answer(text=random.choice(dead_quotes), parse_mode="HTML")
            return None

        if not villian.alive:
            await message.answer(text=f"Вы опускаете свой меч, опомнившись от ярости", parse_mode="HTML",
                                 reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Закончить")]], resize_keyboard=True))
            return None

        hero_init = double_dices() + self.initiative
        villian_init = double_dices() + villian.initiative
        if hero_init > villian_init:

            crit = random.randint(1, 100)
            if crit in range(1, self.initiative * 6):
                hit_damage = int(self.attack * 2.5)
                text.append(f"*<b>КРИТИЧЕСКИЙ УДАР</b>*")
                critical_hit = True
            else:
                hit_damage = self.attack


            damage = hit_damage + dice() - villian.defense
            if damage <= 0:
                text.append(f"Изловчившись вы попадаете по противнику, но тот остается невредим")
            else:

                hit_quotes = [f"Ваш меч скользит противнику по боку нанося {damage} урона",
                          f"Ваш меч на пол секунды застревает в теле противника, затем вы силой вытаскиваете его, вытягивая из противника {damage} hp",
                          f"Вы едва касаетесь лезвием тела противника, снимая ему {damage} hp",
                          f"Ваш удар проходиться вскользь по поясу противника нанося {damage} урона",
                          f"Ваш меч входит в грудь противнику на два сантиметра, тот теряет {damage} урона",
                          f"Ваш меч скользит по телу противника, снося ему {damage} hp"]


                critical_hit_quotes = [f"Ваш меч сбоку залетает в грудь противнику на десять сантиметров и {damage} урона",
                          f"Вы срезаете противнику кусок тела, нанося {damage} урона",
                          f"Рубящим ударом вы попадаете в то место, где обычно находятся ключицы, снося {damage} hp",
                          f"Ваш меч застревает у противника в нижней конечности, силой вырывая его от туда, вы сносите {damage} hp",
                          f"Колящим ударом ваш меч заходит противнику в грудную клетку на 10 см оставляя там рану на {damage} урона",
                          f"Ваш удар протыкает нижнюю конечность противника насквозь, при выемке меча противник теряет {damage} hp"]

                villian.hp -= damage
                if critical_hit:
                    text.append(critical_hit_quotes[quoteIndex])
                else:
                    text.append(hit_quotes[quoteIndex])
                players[message.chat.id]["damage"] += damage
                if critical_hit:
                    text.append(f"*<b>КРИТИЧЕСКИЙ УДАР</b>*")
            await message.answer(text="\n".join(text), parse_mode="HTML")
            villian.check_alive()
            if not villian.alive:
                for player in players:
                    await bot.send_message(chat_id=player, text=f"{self.name} наносит последний удар")
                    if villian.quoteIndex is not None:
                        await bot.send_message(chat_id=player, text=villian.dead_quotes[villian.quoteIndex])
                    await bot.send_message(chat_id=player, text=f"<b>Рейд-босс мертв</b>", parse_mode="HTML")

        else:
            text.append(f"Вы промахиваетесь")
            await message.answer(text="\n".join(text), parse_mode="HTML")


    def ressurecting(self):
        self.hp = int(self.max_hp * random.random())
        self.alive = True


    async def fountain_healing(self, heal_hp, message):
        if heal_hp + self.hp < self.max_hp:
            self.hp += heal_hp
            await message.answer(text=f"Живительная влага восстановила вам {heal_hp} hp")
        else:
            self.hp = self.max_hp
            await message.answer(text=f"Фонтан залечил каждую рану на вашем теле")



    async def leave_boss_fight(self, players: dict, villian, bot, message, player_id):
        hero_init = double_dices() + self.initiative
        villian_init = double_dices() + villian.initiative
        if hero_init - villian_init > 2:
            for player in players:
                if player_id != player:
                    await bot.send_message(chat_id=player, text=f"{self.name} удачно соскочил с битвы", parse_mode="HTML")
            return True
        else:
            init = dice()
            if init > 3:
                await message.answer(text="У вас не получилось соскочить с битвы")
                for player in players:
                    if player_id != player:
                        await bot.send_message(chat_id=player, text=f"{self.name} пытался соскочить с битвы, но облажался",
                                           parse_mode="HTML")
                return False
            else:
                damage = villian.attack + dice()
                self.hp -= damage
                self.check_alive()
                if not self.alive:
                    await message.answer(text=f"У вас не получилось соскочить с битвы, {villian.name} ударил вас в спину при попытке к бегству, вы потеряли {damage} hp\n"
                                              f"Спешу сообщить, что этот удар был для вас последним", reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="Продолжить")]], resize_keyboard=True))
                    for player in players:
                        if player_id != player:
                            await bot.send_message(chat_id=player, text=f"{self.name} пытался соскочить с битвы, мало того что получил ударом в спину, так еще и отъехал",
                                               parse_mode="HTML")
                else:
                    await message.answer(text=f"У вас не получилось соскочить с битвы, {villian.name} ударил вас в спину при попытке к бегству, вы потеряли {damage} hp")
                    for player in players:
                        if player_id != player:
                            await bot.send_message(chat_id=player, text=f"{self.name} пытался соскочить с битвы, но {villian.name} был инициативнее и снёс герою {damage} ударом в спину",
                                               parse_mode="HTML")

                return False






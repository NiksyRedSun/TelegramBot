from SomeClasses.BasicClasses import Unit, dice, double_dices, DeathCounter
from SomeClasses.VillianClasses import Villian
from SomeClasses.MobClasses import Mob
from SomeClasses.ItemsClasses import HealingPotion, LiqPotion
import random
import asyncio
from EasyGameLoader import bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from SomeKeyboards import next_keyb, end_menu_keyb, attack_menu_keyb, menu_keyb, mob_next_keyb
from SomeAttributes import all_items, all_items_dict_cost
import SomeRepos.sqlaORM
from SomeClasses.StatisticsClasses import Statistics
from SomeClasses.EquipmentClasses import Equipment
import Functions



class Character(Unit):
    def __init__(self, s_name: str, s_story: str, s_hp=5, s_max_hp=5, s_attack=0, s_defense=0, s_initiative=0,
                 s_points=30, s_money=0, s_level=0, s_exp=0, s_next_lvl_exp=100, s_autosave=False):
        super().__init__(s_name, s_story, s_max_hp, s_attack, s_defense, s_initiative)
        self.hp = s_hp
        self.points = s_points
        self.money = s_money
        self.level = s_level
        self.exp = s_exp
        self.next_level_exp = s_next_lvl_exp
        self.quoteIndex = None
        self.in_dead_quote = None
        self.deathCounter = None
        self.fury = 0
        self.dead_quotes = [f"Вы роняете свое оружие захлебываясь кровью",
                      f"Оружие выпадывает из ваших рук, но вас гораздо больше интересует кровь, которая льется фонтаном из вашей шеи. Вы медленно теряете сознание",
                      f"Ваши внутренности выпадывают наружу, приключение больше не кажется интересным",
                      f"Ваше оружие падает, вы чувствуете как одежда начинает прилипать к телу из-за многочисленных источников кровотечения под ней. Вам стоило остаться дома",
                      f"Стоя на коленях и готовясь уйти лбом в землю, вы начинаете забывать о том как оказались здесь и медленно теряете сознание",
                      f"В последний раз взглянув на свои окровавленные руки, вы начинаете думать о том, была ли эта смерть славной. Вас погружает в вечный сон"]

        self.effects = {item().name: None for item in all_items}
        self.inventory = []
        self.in_avoid = False
        self.autosave = s_autosave
        self.stat = Statistics()
        self.equipment = []




    def put_on_eqp_on_load(self, its):
        if its:
            for it in its:
                if it.itemName is not None:
                    self.equipment.append(Equipment(it.itemName, it.itemMaxHp, it.itemAttack, it.itemDefense, it.itemInitiative, it.forAttack))
        self.put_on_eqp()



    def put_on_eqp(self):
        for eq in self.equipment:
            self.max_hp += eq.itemMaxHp
            self.attack += eq.itemAttack
            self.defense += eq.itemDefense
            self.initiative += eq.itemInitiative


    def put_off_eqp(self):
        for eq in self.equipment:
            self.max_hp -= eq.itemMaxHp
            self.attack -= eq.itemAttack
            self.defense -= eq.itemDefense
            self.initiative -= eq.itemInitiative


    def show_equipment(self):
        if self.equipment:
            text = ["На вас надето:"]
            for eq in self.equipment:
                text.extend(eq.info())
            return '\n'.join(text)
        else:
            return "На вас ничего не надето"


    async def autosave_switch(self, message):
        if self.autosave:
            self.autosave = False
            await message.answer(text="Автосохранение выключено", parse_mode="HTML")
        else:
            self.autosave = True
            await message.answer(text="Автосохранение включено", parse_mode="HTML")


    async def do_autosave(self, message):
        if self.autosave:
            self.put_off_eqp()
            await message.answer(text=f"Автосохранение, не выключайте телефон")
            await Functions.check_and_save(self, message)
            await Functions.check_and_save_stat(self.stat, message)
            self.stat = Statistics()
            self.put_on_eqp()


    def count_objects(self, lst, obj_type):
        count = 0
        for obj in lst:
            if isinstance(obj, obj_type):
                count += 1
        return count


    def for_saving(self):
        return [self.name, self.story, self.max_hp, self.attack, self.defense, self.initiative, self.points, self.money, self.level, self.exp]



    async def show_inv(self, message):
        message_text = []
        for item in all_items:
            count = self.count_objects(self.inventory, item)
            if count > 0:
                message_text.append(item().show_in_inv(count))

        if message_text:
            message_text.insert(0, "Ваши расходные материалы:")
            await message.answer(text='\n'.join(message_text))
        else:
            await message.answer(text="У вас нет никаких расходных материалов")


    async def show_inv_in_fight(self, message):
        items = all_items
        message_text = []
        for item in items:
            count = self.count_objects(self.inventory, item)
            if count > 0:
                message_text.append(item().show_in_fight())

        if message_text:
            await message.answer(text='\n'.join(message_text))
        else:
            await message.answer(text="Ваш инвентарь пуст")


    def presentation(self):

        def make_short_string(string: str, long: int):
            result = ' '
            word_list = string.split()
            count = 0
            for i in word_list:
                if count + len(i) > long:
                    result += '\n '
                    count = 0
                result += i + " "
                count += len(i)
            return result


        def str_to_deathstr(string: str):
            new_string = map(lambda x: '/', string)
            return ''.join(new_string)

        pres_name = "<code>" + "+" + self.name.center(28, "-") + "+" + "</code>"
        pres_level = "<code>" + "+" + ("Уровень: " + str(self.level)).center(28, "-") + "+" + "</code>"
        text = [
                f"{pres_name}",
                make_short_string(self.story, 26),
                f"",
                f" <code>Здоровье: ".ljust(20) + f"{self.hp}/{self.max_hp}</code>",
                f" <code>Атака: ".ljust(20) + f"{self.attack}</code>",
                f" <code>Защита: ".ljust(20) + f"{self.defense}</code>",
                f" <code>Ловкость: ".ljust(20) + f"{self.initiative}</code>",
                f" <code>Золото: ".ljust(20) + f"{self.money}</code>",
                f" <code>Опыт: ".ljust(20) + f"{self.exp}/{self.next_level_exp}</code>",
                f"",
                f"{pres_level}"
                ]
        if self.alive:
            return '\n'.join(text)
        else:
            pres_name = "<code>+" + ("Дух " + self.name).center(28, "-") + "+</code>"
            text = [str_to_deathstr(text[i]) if i != 3 else text[i] for i in range(len(text))]
            text[0] = pres_name
            return '\n'.join(text)

    def in_menu_presentation(self):

        def make_short_string(string: str, long: int):
            result = ' '
            word_list = string.split()
            count = 0
            for i in word_list:
                if count + len(i) > long:
                    result += '\n '
                    count = 0
                result += i + " "
                count += len(i)
            return result

        pres_name = "<code>" + "+" + self.name.center(28, "-") + "+" + "</code>"
        pres_level = "<code>" + "+" + ("Уровень: " + str(self.level)).center(28, "-") + "+" + "</code>"
        text = [
            f"{pres_name}",
            make_short_string(self.story, 26),
            f"",
            f"{pres_level}"
        ]
        return '\n'.join(text)


    def give_effects_info(self):
        effects_text = []
        for effect in self.effects:
            if self.effects[effect] is not None:
                if not self.effects[effect].done():
                    effects_text.append(all_items_dict_cost[effect]().status)
        if effects_text:
            return effects_text
        else:
            return None

    def fight_presentation(self):
        pres_name = "+" + self.name.center(22, "-") + "+"
        text = [f"<code>{pres_name}</code>",
                f"Здоровье: {self.hp}/{self.max_hp}".center(40),
                f"Ярость: {self.fury} %".center(43)]
        for effect in self.effects:
            if self.effects[effect] is not None:
                if not self.effects[effect].done():
                    text.append(" "*12 + all_items_dict_cost[effect]().status())
        return '\n'.join(text)

    def get_death_counter(self):
        if self.in_dead_quote is not None:
            self.deathCounter = DeathCounter(self.in_dead_quote)
        else:
            self.deathCounter = DeathCounter(random.choice(self.dead_quotes))

    def next_level(self):
        while self.exp > self.next_level_exp:
            if self.level < 8:
                self.next_level_exp = int(100 * 2 ** self.level)
            elif self.level < 11:
                self.next_level_exp = int(100 * (1.85 - (self.level*0.0115)) ** self.level)
            else:
                self.next_level_exp += 10000 + 750 * (self.level - 12)
            self.level += 1
            if self.level % 2 == 0:
                self.points += 1
            self.hp = self.max_hp

    def points_distr(self, skill: str):
        match skill:
            case "attack":
                if self.points > 0:
                    self.points -= 1
                    self.attack += 1
                    return "Вы увеличили атаку на 1 единицу"
                else:
                    return "Вам не хватает очков умений"
            case "defense":
                if self.points > 0:
                    self.points -= 1
                    self.defense += 1
                    return "Вы увеличили защиту на 1 единицу"
                else:
                    return "Вам не хватает очков умений"
            case "initiative":
                if self.points >= 3:
                    self.points -= 3
                    self.initiative += 1
                    return "Вы увеличили ловкость на 1 единицу"
                else:
                    return "Вам не хватает очков умений"
            case "hp":
                if self.points > 0:
                    self.points -= 1
                    self.max_hp += 5
                    return "Вы увеличили здоровье на 5 единиц"
                else:
                    return "Вам не хватает очков умений"
            case "reload":
                    self.put_off_eqp()
                    self.points += int((self.max_hp - 5)/5 + self.attack + self.defense + self.initiative*3)
                    self.max_hp = 5
                    self.hp = 5
                    self.attack = 0
                    self.defense = 0
                    self.initiative = 0
                    self.put_on_eqp()
                    return f"Вы обнулили очки умений\nКоличество очков умений теперь: {self.points} "


    def critical_hit_text(self, text: list):
        text.insert(0, "<b>" + "КРИТИЧЕСКИЙ УДАР".center(34, "*") + "</b>")
        text.append("<b>" + "КРИТИЧЕСКИЙ УДАР".center(34, "*") + "</b>")
        return text


    async def attack_boss_func(self, villian: Villian, message, bot, players):

        self.quoteIndex = random.randint(0, 5)
        quotes = [f"Вы замахиваетесь слева",
                  f"Вы замахиваетесь справа",
                  f"Вы замахиваетесь для рубящего, нисходящего сверху удара",
                  f"Вы замахиваетесь для рубящего, восходящего снизу удара",
                  f"Вы выставляете меч для колющего удара над верхней конечностью противника",
                  f"Вы выставляете меч для колющего удара под верхней конечностью противника"]

        critical_hit = False
        text = []
        await message.answer(text=quotes[self.quoteIndex])
        await asyncio.sleep(0.7)

        self.check_alive()
        villian.check_alive()
        if not self.alive:
            # self.quoteIndex = None
            # self.in_dead_quote = random.choice(self.dead_quotes)
            # await message.answer(text=self.in_dead_quote, reply_markup=next_keyb)
            return None

        if not villian.alive:
            await message.answer(text=f"Вы опускаете свой меч, опомнившись от ярости", parse_mode="HTML",
                                 reply_markup=ReplyKeyboardMarkup(keyboard=end_menu_keyb))
            self.quoteIndex = None
            return None

        hero_init = double_dices() + self.initiative
        villian_init = double_dices() + villian.initiative
        if hero_init > villian_init:
            self.stat.hits += 1

            crit = random.randint(1, 100)
            if crit in range(1, self.initiative * 6):
                hit_damage = int(self.attack * 2.5) + int(self.fury*0.05*2.5)
                critical_hit = True
                self.stat.criticalHits += 1
            else:
                hit_damage = self.attack + int(self.fury * 0.05)


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
                          f"Колящим ударом ваш меч заходит противнику в грудную клетку на 10 см оставляя там {damage} урона",
                          f"Ваш удар протыкает нижнюю конечность противника насквозь, при выемке меча противник теряет {damage} hp"]


                critical_hit_quotes_team = [f"<b>КРИТИЧЕСКИЙ УДАР</b> by {self.name}\n"
                                            f"{self.name} залетает мечом в грудную клетку противника сбоку снося {damage} hp",
                                            f"<b>КРИТИЧЕСКИЙ УДАР</b> by {self.name}\n"
                                            f"{self.name} срезает противнику кусок тела нанеся {damage} урона",
                                            f"<b>КРИТИЧЕСКИЙ УДАР</b> by {self.name}\n"
                                            f"{self.name} попадает противнику в анатомические ключицы и сносит противнику {damage} hp",
                                            f"<b>КРИТИЧЕСКИЙ УДАР</b> by {self.name}\n"
                                            f"{self.name} наносит глубокий рубящий удар в нижнюю конечность снимая противнику {damage} hp",
                                            f"<b>КРИТИЧЕСКИЙ УДАР</b> by {self.name}\n"
                                            f"{self.name} протыкает грудную клетку снося  противнику {damage} hp",
                                            f"<b>КРИТИЧЕСКИЙ УДАР</b> by {self.name}\n"
                                            f"{self.name} протыкает противнику нижнюю конечность насквозь на {damage} урона",
                                            ]

                villian.hp -= damage
                self.fury_up(int(damage * 0.5))
                try:
                    if critical_hit:
                        text.append(critical_hit_quotes[self.quoteIndex])
                    else:
                        text.append(hit_quotes[self.quoteIndex])
                    players[message.chat.id]["damage"] += damage
                except:
                    print(f"{self.name} отправил сообщение в будущее")
                    await message.answer(text="В противника летит шквал ударов")
                    return None

                if critical_hit:
                    text = self.critical_hit_text(text)

                if critical_hit:
                    for player in players.copy():
                        if message.chat.id != player:
                            await bot.send_message(chat_id=player, text=critical_hit_quotes_team[self.quoteIndex], parse_mode="HTML")

            await message.answer(text="\n".join(text), parse_mode="HTML")
            villian.check_alive()
            if not villian.alive:
                for player in players.copy():
                    await bot.send_message(chat_id=player, text=f"{self.name} наносит последний удар")
                    if villian.quoteIndex is not None:
                        await bot.send_message(chat_id=player, text=villian.dead_quotes[villian.quoteIndex])
                    await bot.send_message(chat_id=player, text=f"<b>Рейд-босс мертв</b>", parse_mode="HTML", reply_markup=end_menu_keyb)
                self.in_avoid = False

        else:
            text.append(f"Вы промахиваетесь")
            await message.answer(text="\n".join(text), parse_mode="HTML")
        self.quoteIndex = None


    async def attack_mob_func(self, mob: Mob, message, mob_fighters: dict):
        if not self.alive:
            return None
        self.quoteIndex = random.randint(0, 5)
        quotes = [f"Вы замахиваетесь слева",
                  f"Вы замахиваетесь справа",
                  f"Вы замахиваетесь для рубящего, нисходящего сверху удара",
                  f"Вы замахиваетесь для рубящего, восходящего снизу удара",
                  f"Вы выставляете меч для колющего удара над верхней конечностью противника",
                  f"Вы выставляете меч для колющего удара под верхней конечностью противника"]

        critical_hit = False
        text = []
        await message.answer(text=quotes[self.quoteIndex])
        await asyncio.sleep(0.7)

        self.check_alive()
        mob.check_alive()

        if not self.alive:
            self.quoteIndex = None
            return None

        if not mob.alive:
            await message.answer(text=f"Вы опускаете свой меч, опомнившись от ярости", parse_mode="HTML")
            return None

        hero_init = double_dices() + self.initiative
        mob_init = double_dices() + mob.initiative

        if hero_init > mob_init:
            self.stat.hits += 1

            crit = random.randint(1, 100)
            if crit in range(1, self.initiative * 6):
                hit_damage = int(self.attack * 2.5) + int(self.fury*0.05*2.5)
                critical_hit = True
                self.stat.criticalHits += 1
            else:
                hit_damage = self.attack + int(self.fury * 0.05)


            damage = hit_damage + dice() - mob.defense
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

                mob.hp -= damage
                self.fury_up(int(damage * 0.5))
                if self.quoteIndex is None:
                    return None

                if critical_hit:
                    text.append(critical_hit_quotes[self.quoteIndex])
                else:
                    text.append(hit_quotes[self.quoteIndex])

                if critical_hit:
                    text = self.critical_hit_text(text)

            await message.answer(text="\n".join(text), parse_mode="HTML")
            mob.check_alive()
            if not mob.alive:
                if mob.quoteIndex is not None:
                    await message.answer(text=mob.dead_quotes[mob.quoteIndex], reply_markup=mob_next_keyb)
                else:
                    await message.answer(text=random.choice(mob.dead_quotes), reply_markup=mob_next_keyb)
                mob_fighters[message.chat.id]['death_mobs'] += 1
                self.in_avoid = False
        else:
            text.append(f"Вы промахиваетесь")
            await message.answer(text="\n".join(text), parse_mode="HTML")
        self.quoteIndex = None


    def ressurecting(self):
        self.hp = int(self.max_hp * random.random())
        self.alive = True
        self.in_dead_quote = None
        self.deathCounter = None


    def check_alive(self):
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.in_avoid = False
            self.fury = 0
            for effect in self.effects:
                if self.effects[effect] is not None:
                    if not self.effects[self.name].done():
                        all_items_dict_cost[effect]().char_ret_stat(self)
                        self.effects[self.name].cancel()
                        self.effects[effect] = None
                    else:
                        self.effects[effect] = None
            self.stat.death += 1


    def remove_effects(self):
        for effect in self.effects:
            if self.effects[effect] is not None:
                if not self.effects[self.name].done():
                    all_items_dict_cost[effect]().char_ret_stat(self)
                    self.effects[self.name].cancel()
                    self.effects[effect] = None
                else:
                    all_items_dict_cost[effect]().char_ret_stat(self)
                    self.effects[effect] = None


    async def fountain_healing(self, heal_hp, message):
        if heal_hp + self.hp < self.max_hp:
            self.hp += heal_hp
            await message.answer(text=f"Живительная влага восстановила вам {heal_hp} hp")
        else:
            self.hp = self.max_hp
            await message.answer(text=f"Фонтан залечил каждую рану на вашем теле")
        self.stat.fountainHealing += 1


    def five_second_healing(self):
        if self.hp == self.max_hp:
            pass
        else:
            self.hp += 1


    def fury_down(self):
        if self.fury > 80:
            self.fury -= 5
        elif self.fury > 60:
            self.fury -= 4
        elif self.fury > 40:
            self.fury -= 3
        elif self.fury > 20:
            self.fury -=2
        elif self.fury > 0:
            self.fury -= 1
        else:
            pass


    def fury_up(self, for_up: int):
        if self.fury + for_up >= 100:
            self.fury = 100
        else:
            self.fury += for_up


    async def leave_boss_fight(self, players: dict, villian, bot, message):
        self.in_avoid = False
        hero_init = double_dices() + self.initiative
        villian_init = double_dices() + villian.initiative
        if hero_init - villian_init > 2:
            self.stat.leavingBossFights += 1
            for player in players.copy():
                if message.chat.id != player:
                    await bot.send_message(chat_id=player, text=f"{self.name} удачно соскочил с битвы", parse_mode="HTML")
            return True
        else:
            init = dice()
            if init > 3:
                await message.answer(text="У вас не получилось соскочить с битвы")
                for player in players.copy():
                    if message.chat.id != player:
                        await bot.send_message(chat_id=player, text=f"{self.name} пытался соскочить с битвы, но облажался",
                                           parse_mode="HTML")
                return False
            else:
                damage = villian.attack + dice()
                self.hp -= damage
                self.check_alive()
                if not self.alive:
                    self.in_dead_quote = villian.give_in_dead_quotes_for_player()
                    await message.answer(text=self.in_dead_quote, reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="Продолжить")]], resize_keyboard=True))
                    for player in players.copy():
                        if message.chat.id != player:
                            await bot.send_message(chat_id=player, text=villian.give_in_dead_quotes_for_team(self),
                                               parse_mode="HTML")
                else:
                    await message.answer(text=f"У вас не получилось соскочить с битвы, {villian.name} ударил вас в спину при попытке к бегству, вы потеряли {damage} hp")
                    for player in players.copy():
                        if message.chat.id != player:
                            await bot.send_message(chat_id=player, text=f"{self.name} пытался соскочить с битвы, но {villian.name} был инициативнее и снёс герою {damage} ударом в спину",
                                               parse_mode="HTML")

                return False


    async def leave_mob_fight(self, mob, message):
        self.in_avoid = False
        hero_init = double_dices() + self.initiative
        mob_init = double_dices() + mob.initiative
        if hero_init - mob_init > 2:
            self.stat.leavingMobFights += 1
            return True
        else:
            init = dice()
            if init > 3:
                await message.answer(text="У вас не получилось соскочить с битвы")
                return False
            else:
                damage = mob.attack + dice()
                self.hp -= damage
                self.check_alive()
                if not self.alive:
                    self.in_dead_quote = mob.give_in_dead_quotes_for_player()
                    await message.answer(text=self.in_dead_quote, reply_markup=next_keyb)
                else:
                    await message.answer(text=f"У вас не получилось соскочить с битвы, {mob.name} ударил вас в спину при попытке к бегству, вы потеряли {damage} hp")
                return False


    async def avoid_enemy(self, message, enemy):
        if enemy.quoteIndex is not None:
            await message.answer(text=f"Вы пытаетесь совершить уклонение")
            self.in_avoid = True
        else:
            await message.answer(text=f"Враг не атакует")








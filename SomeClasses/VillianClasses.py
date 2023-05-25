import random
import asyncio
from EasyGameLoader import bot
from SomeClasses.BasicClasses import Unit, dice, double_dices
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from SomeKeyboards import attack_menu_keyb, death_menu_keyb, end_menu_keyb



class Villian(Unit):
    def __init__(self):
        self.name = None
        self.story = None
        self.hp = None
        self.max_hp = None
        self.attack = None
        self.defense = None
        self.initiative = None
        self.alive = True
        self.money = None
        self.exp = None
        self.quoteIndex = None

        self.quotes = []
        self.dead_quotes = []

        self.maxQuoteIndex = len(self.quotes) - 1



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


        cur_money = int(self.money / len(all_players))
        cur_exp = int(self.exp / len(all_players))
        text = ["<code>+" + "Результаты".center(28, "-") + "+</code>",
                "<b><code>" + "Рейд-босс мертв".center(30, " ") + "</code></b>\n",
                " Урон игроков:"]

        for id in sorted(players.items(), key=lambda x: x[1]["damage"], reverse=True):
            text.append(f" {id[1]['char'].name} - {id[1]['damage']} урона")


        if sorted(players.keys()) != sorted(all_players.keys()):
            text.append(f"\n Пали в бою:")
            for player in all_players:
                if player not in players:
                    text.append(f" {all_players[player].name}")

        text.append("")
        text.append(make_short_string(f"Каждый из участников битвы получил по {cur_money} монет", 26))
        text.append(make_short_string(f"Каждый из участников битвы получил по {cur_exp} опыта", 26))


        for player in all_players.copy():
            all_players[player].money += cur_money
            all_players[player].exp += cur_exp
            all_players[player].next_level()
            await bot.send_message(chat_id=player,
                                   text='\n'.join(text),
                                   parse_mode="HTML",
                                   reply_markup=end_menu_keyb)




    def give_pos_quotes(self, char):
        pos_quotes = []
        return pos_quotes[self.quoteIndex]


    def give_neg_quotes(self, char, damage):
        neg_quotes = []
        return neg_quotes[self.quoteIndex]


    def give_really_neg_quotes(self, char, damage):
        really_neg_quotes = []
        return really_neg_quotes[self.quoteIndex]


    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = []
        not_in_attack_quote = ''
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote


    def give_in_dead_quotes_for_team(self, char):
        in_attack_quotes = []
        not_in_attack_quote = ''
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote



    def attack_one_func(self, char, text: list):
        if char.alive:

            villian_init = double_dices() + self.initiative
            char_init = double_dices() + char.initiative

            if villian_init > char_init:
                damage = self.attack + dice() - char.defense

                if damage <= 0:
                    text.append(self.give_pos_quotes(char))
                else:
                    char.hp -= damage
                    if damage > 10:
                        text.append(self.give_really_neg_quotes(char, damage))
                    else:
                        text.append(self.give_neg_quotes(char, damage))
                    char.check_alive()
                    if not char.alive:
                        text.append(f"<b>{char.name} отъезжает в ходе битвы</b>\n")
                    else:
                        text.append("")
            else:
                text.append(self.give_pos_quotes(char))




    async def attack_func(self, players: dict, bot):
        if not self.alive:
            return None
        self.quoteIndex = random.randint(0, self.maxQuoteIndex)

        for player in players.copy():
            await bot.send_message(chat_id=player, text=self.quotes[self.quoteIndex])
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

        self.quotes = [f"{self.name} замахивается своим хвостом",
                  f"{self.name} готовится залить все огнем",
                  f"{self.name} издает пронзительный рев",
                  f"{self.name} хлопает крыльями",
                  f"{self.name} взлетел и приготовил когти для атаки"]

        self.dead_quotes = [f"Это был последний взмах хвоста Красного дракона",
                      f"{self.name} больше никого не зальет огнем",
                      f"Теперь {self.name} уж точно никогда не будет рычать",
                      f"{self.name} схлапывается сам",
                      f"{self.name} упал, вытянув ноги"]

        self.maxQuoteIndex = len(self.quotes) - 1



    def give_pos_quotes(self, char):
        pos_quotes = [f"{char.name} успевает уклониться от хвоста Красного дракона",
                      f"{char.name} успевает уклониться от столба пламени Красного дракона",
                      f"{char.name} вовремя закрывает уши и не слышит рева Красного дракона",
                      f"{char.name} избегает действия порыва ветра созданного Красным драконом",
                      f"{char.name} уворачивается от когтей Красного дракона"]
        return pos_quotes[self.quoteIndex]


    def give_neg_quotes(self, char, damage):
        neg_quotes = [f"{char.name} получает {damage} урона от удара хвостом, устояв на ногах",
                      f"{char.name} получает {damage} единиц урона от ожогов, задержавшись в пламени на пол секунды",
                      f"{char.name} ловит головную боль, теряя {damage} hp",
                      f"От порыва ветра {char.name} падает на землю теряя {damage} hp",
                      f"{char.name} не успевает увернуться от когтей теряя {damage} hp"]
        return neg_quotes[self.quoteIndex]



    def give_really_neg_quotes(self, char, damage):
        really_neg_quotes = [f"{char.name} отлетает от хвоста дракона на 10 метров и получает {damage} урона",
                             f"{char.name} получает {damage} единиц урона от горения, задержавшись в пламени на полторы секунды",
                             f"{char.name} теряет кровь из ушей и {damage} hp",
                             f"{char.name} прижат к земле порывом ветра и теряет {damage} hp",
                             f"{char.name} поднят когтями и сброшен, потеряв {damage} hp"]
        return really_neg_quotes[self.quoteIndex]


    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"Вы пытаетесь бежать, но вас сносит ударом хвоста в спину, при падении вы разбиваете голову. Пытаясь ползти, вы медленно теряете сознание",
                  f"Вы пытаетесь бежать, но чувствуете, как пламя Дракона настигает вас в спину, быстрее чем вы успеваете вскрикнуть от горячей боли",
                  f"Сделав несколько шагов назад, вы глохнете от рева Дракона и падаете на землю. Пытаясь ползти, вы медленно теряете сознание",
                  f"Не успев развернуться, вас сносит порывом ветра от крыльев Красного дракона, при падении вы разбиваете голову. Пытаясь ползти, вы медленно теряете сознание",
                  f"Развернувшись, вы не успеваете одуматься и когти Дракона подхватывают вас в небо. При падении вы разбиваете голову. Пытаясь ползти, вы медленно теряете сознание"]

        not_in_attack_quote = 'Дракон прочитал ваши мысли быстрее, чем вы успели сдвинуться с места. Своими зубами, он прокусил вам обе ноги разом. От обильной кровопотери вы начинаете терять сознание'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote


    def give_in_dead_quotes_for_team(self, char):
        in_attack_quotes = [f"{char.name} попытался бежать, но отлетел от удара хвоста в спину, разбив голову при падении",
                  f"{char.name} попытался бежать, но был испепелен огнем дракона в спину",
                  f"{char.name} попытался бежать, но упал после оглушения ревом",
                  f"{char.name} попытался бежать, но был снесен порывом ветра, разбив голову при падении",
                  f"{char.name} попытался бежать, но был подброшен в небо когтями дракона. Тело упало слишком далеко, чтобы его можно было рассмотреть"]

        not_in_attack_quote = f'{char.name} пытался сбежать, но Дракон раскусил ему ноги. Герой умирает от обильной кровопотери'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote





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

        self.quotes = [f"{self.name} выстреливает сеткой из паутины",
                  f"{self.name} плюется кислотой",
                  f"{self.name} замахивается передними лапами",
                  f"{self.name} готовится пустить в ход жвалы"]

        self.dead_quotes = [f"{self.name} упал замертво",
                  f"{self.name} больше никогда не будет плевать кислотой",
                  f"Теперь {self.name} склеил лапы",
                  f"{self.name} подавился собственными жвалами"]

        self.maxQuoteIndex = len(self.quotes) - 1



    def give_pos_quotes(self, char):
        pos_quotes = [f"{char.name} успевает уклониться от сетки паука",
                      f"{char.name} успевает увернуться от кислоты",
                      f"{char.name} уворачивается от лап паука",
                      f"{char.name} увернулся от жвал паука"]
        return pos_quotes[self.quoteIndex]



    def give_neg_quotes(self, char, damage):
        neg_quotes = [f"{char.name} падает на пол запутавшись в паутине и получает {damage} урона",
                      f"{char.name} получает {damage} урона кислотой",
                      f"{char.name} проткнут передней лапой паука на {damage} hp",
                      f"{char.name} зацеплен жвалами паука на {damage} hp"]
        return neg_quotes[self.quoteIndex]



    def give_really_neg_quotes(self, char, damage):
        really_neg_quotes = [
            f"{char.name} падает на пол запутавшись в паутине, ударяется головой и получает {damage} урона",
            f"{char.name} получает {damage} урона кислотой до костей",
            f"{char.name} проткнут передней лапой паука насквозь на {damage} hp",
            f"{char.name} застрял в жвалах паука на {damage} hp"]
        return really_neg_quotes[self.quoteIndex]



    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"Вы попытались сбежать, но были прибиты сеткой из паутины к стене. Из вашей головы начинает течь кровь, но вы ничего не можете сделать, поскольку ваши руки связаны паутиной",
                  f"Вы попытались бежать, но были настигнуты попаданием кислоты в спину. Последнее что вы чувствуете, как кости оголяются после излишнего окисления мышц",
                  f"Вы попытались бежать, но были проткнуты лапой паука в поясницу. Ваши дальнейшие попытки двигать ногами были обречены на неудачу. Вам ничего не остается, кроме как умереть от потери крови",
                  f"Вы успели развернуться, но жвалы паука добрались до вашего бедра быстрее, чем вы сделали шаг. Сложно будет бежать с одной ногой"]

        not_in_attack_quote = 'Паук прочитал ваши мысли быстрее, чем вы успели сдвинуться с места. Своими жвалами, он прокусил вам правую ногу. От обильной кровопотери вы начинаете терять сознание'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote


    def give_in_dead_quotes_for_team(self, char):
        in_attack_quotes = [f"{char.name} прибит сеткой из паутины к стене. При влете в стену, его черепная коробка раскрывается",
                  f"{char.name} роняет куски окисленного мяса со своей спины, переходя с бега в падение",
                  f"{char.name} проткнут лапой паука в поясницу. Его дальнейшие попытки двигать ногами обречены на неудачу",
                  f"{char.name} получает укус жвалами в бедро, быстрее чем успевает сделать несколько шагов при попытке к бегству. Ему будет сложно бежать с одной ногой"]

        not_in_attack_quote = f'{char.name} пытался сбежать, но Паук раскусил ему ноги. Герой умирает от обильной кровопотери'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote




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

        self.quotes = [f"{self.name} замахивается кулаком-молотом",
                  f"{self.name} пускает в ход кипящее масло",
                  f"{self.name} готовится выстрелить стальными колышками",
                  f"{self.name} разгоняется для удара"]

        self.dead_quotes = [f"{self.name} теряет равновесие и разливает масло",
                      f"{self.name} теряет свое кипящее масло",
                      f"Это были последние колышки, которыми он планировал выстрелить",
                      f"{self.name} падает на бегу"]

        self.maxQuoteIndex = len(self.quotes) - 1



    def give_pos_quotes(self, char):
        pos_quotes = [f"{char.name} успевает уклониться от кулака-молота",
                      f"{char.name} успевает увернуться от кипящего масла",
                      f"{char.name} уворачивается от колышков",
                      f"{char.name} избегает столкновения с Големом"]
        return pos_quotes[self.quoteIndex]



    def give_neg_quotes(self, char, damage):
        neg_quotes = [f"{char.name} теряет зубы и {damage} hp от кулака-молота",
                      f"{char.name} получает {damage} урона будучи залит потоком масла",
                      f"{char.name} обнаруживает в себе стальной колышек на {damage} hp",
                      f"{char.name} получает головой Голема в свою и теряет {damage} hp"]
        return neg_quotes[self.quoteIndex]



    def give_really_neg_quotes(self, char, damage):
        really_neg_quotes = [f"{char.name} теряет лицо и {damage} hp от кулака-молота",
                             f"{char.name} получает {damage} урона упав в кипящее масло",
                             f"{char.name} обнаруживает в себе два стальных колышка на {damage} hp",
                             f"{char.name} получает головой Голема в свою и падая на пол, теряет {damage} hp"]
        return really_neg_quotes[self.quoteIndex]



    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"При попытке к бегству вы получаете удар кулаком-молотом в затылок. Перед тем как потерять сознание, вы видите кусок мозга летящим перед вами",
                  f"При попытке к бегству вас заливает сзади кипящим маслом. По ощущениям - гораздо хуже, чем в джакузи",
                  f"При попытке к бегству, вы не совсем понимаете что происходит, пока не проводите ладонью по передней поверхности шеи и не осознаете, что ощущаете два острия",
                  f"Вы пытаетесь бежать, но оказывайтесь на траектории пробежки Голема, и втаптываетесь его ногой в пол. Поднимая голову, вы понимаете, что растеряли все зубы. Прежде, чем забыться, вы успеваете увидеть отблескивающую железную ногу голема"]

        not_in_attack_quote = 'Голем прочитал ваши мысли быстрее, чем вы успели сделать хотя бы пару шагов. Вы получаете выстрелом колышка прямо в сердце. Будучи не способным сказать что-нибудь, вы начинаете терять сознание'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote

    def give_in_dead_quotes_for_team(self, char):
        in_attack_quotes = [f"{char.name} получил удар кулаком-молотом в затылок и растерял свой мозг по полу",
                  f"{char.name} залит кипящим маслом при попытке к бегству",
                  f"{char.name} получил два колышка в шею, при попытке к бегству",
                  f"{char.name} попытался бежать, но был затоптан Големом, растеряв остатки лица по полу"]

        not_in_attack_quote = f'{char.name} пытался сбежать, но получил выстрелом колышка прямо в сердце'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote





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

        self.quotes = [f"{self.name} замахивается ветками",
                  f"{self.name} пускает в ход свои корни",
                  f"{self.name} роняет гнилые плоды",
                  f"{self.name} приподнимает свои листья, раскрывая крону"]

        self.dead_quotes = [f"{self.name} роняет ветки",
                      f"{self.name} переворачивается корнями вверх",
                      f"{self.name} тонет в собственной гнили",
                      f"{self.name} перераскрыло свой потенциал"]

        self.maxQuoteIndex = len(self.quotes) - 1


    def give_pos_quotes(self, char):
        pos_quotes = [f"{char.name} успевает уклониться от веток",
                      f"{char.name} успевает увернуться от корней",
                      f"{char.name} уклоняется от гнилых плодов",
                      f"{char.name} успевает отвернуться от вылетающих насекомых"]
        return pos_quotes[self.quoteIndex]



    def give_neg_quotes(self, char, damage):
        neg_quotes = [f"{char.name} получает удар ветками по лицу и {damage} урона",
                      f"{char.name} получил корнем в живот и теряет {damage} hp",
                      f"{char.name} обнаруживает на себе химические ожоги от гнилых плодов и потерю {damage} hp",
                      f"{char.name} окружен, вылетающими из кроны дерева насекомыми, откусывающими от него {damage} hp"]
        return neg_quotes[self.quoteIndex]



    def give_really_neg_quotes(self, char, damage):
        really_neg_quotes = [f"{char.name} получает удар ветками в глаза и {damage} урона",
                             f"{char.name} сбит с ног корнями Дерева, теряет {damage} hp",
                             f"{char.name} обнаруживает на себе химические ожоги до кости от гнилых плодов и потерю {damage} hp",
                             f"{char.name} оказывается заперт в кроне дерева с ульем, проедающим ему лицо на {damage} hp"]
        return really_neg_quotes[self.quoteIndex]




    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"Вы пытаетесь бежать, но получаете ветками в затылок. Потеря сознания делает вас неспособным драться",
                  f"Вы пытаетесь бежать, но Дерево оплетает корнями ваши ноги. Сила корней настолько велика, что в какой-то момент кости в ваших ногах начинают ломаться и вы теряете сознание от болевого шока",
                  f"Вы пытаетесь бежать, но чувствуете, как на голову падает гнилой плод. Идя вперед и пытаясь вытереть глаза от кислоты, вы падаете в объятия встречающих вас корней Гнилого дерева. Они прижимают вас к земле и начинают медленно перемалывать",
                  f"Вы пытаетесь бежать, но вылетающие из кроны насекомые начинают обильно жалить вас в ваше лицо. Будучи неспособным видеть из-за возникшего отека, вы падаете в объятия встречающих вас корней Гнилого дерева. Они прижимают вас к земле и начинают медленно перемалывать"]

        not_in_attack_quote = 'Гнилое дерево прочитало ваши мысли быстрее, чем вы успели сделать хотя бы пару шагов. Вы проткнуты насквозь залетевшими в вашу спину ветками. Вам думается, что стоило остаться дома.'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote

    def give_in_dead_quotes_for_team(self, char):
        in_attack_quotes = [f"{char.name} пытается бежать, но получает ветками в затылок и падает замертво",
                  f"{char.name} пытается бежать, но оказывается опутан корнями деревьев. Сила корней настолько велика, что в какой-то момент кости в его ногах начинают ломаться и он теряете сознание от болевого шока",
                  f"{char.name} пытается бежать, но получает гнилым плодом в затылок и падает, пытаясь вытереть глаза от кислоты",
                  f"{char.name} пытается бежать, но оказывается настигнут вылетевшими из кроны насекомыми. Будучи неспособным видеть, он падает в корни Гнилого дерева"]

        not_in_attack_quote = f'{char.name} пытался сбежать, но был насквкозь проткнут в спину ветками гнилого дерева'
        if char.quoteIndex is not None:
            return in_attack_quotes[char.quoteIndex]
        else:
            return not_in_attack_quote



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

        self.quotes = [f"{self.name} приготовила своё жало",
                  f"{self.name} пикирует, выставив вперед когти",
                  f"{self.name} готовит свои зубы для захвата"]

        self.dead_quotes = [f"Виверна роняет своё жало",
                      f"Пикирование виверны переходит в падение",
                      f"Из пасти Виверны вырывается кровь, орошая поле боя"]

        self.maxQuoteIndex = len(self.quotes) - 1



    def give_pos_quotes(self, char):
        pos_quotes = [f"{char.name} успевает уклониться от жала",
                      f"{char.name} уворачивается от когтей",
                      f"{char.name} уклоняется от зубов"]
        return pos_quotes[self.quoteIndex]



    def give_neg_quotes(self, char, damage):
        neg_quotes = [f"{char.name} проткнут жалом Виверны на {damage} урона",
                      f"{char.name} не успевает уклониться от когтей Виверны получив {damage} урона ",
                      f"{char.name} зацеплен зубами Виверны на {damage} урона"]
        return neg_quotes[self.quoteIndex]



    def give_really_neg_quotes(self, char, damage):
        really_neg_quotes = [f"{char.name} проткнут жалом Виверны и обильно снабжен ядом на {damage} урона",
                             f"{char.name} отлетает на несколько метров от когтей Виверны получив {damage} урона ",
                             f"{char.name} оказывается в зубах Виверны и взлетает с ней ввысь, с последующим падением на {damage} урона"]
        return really_neg_quotes[self.quoteIndex]


    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"Вы пытаетесь бежать, но оказыватесь проткнутым жалом Виверны насквозь. Перед тем, как она вытаскивает его из вас, вы видите на его острие свое сердце. Вам стоило оставаться дома.",
                  f"Вы пытаетесь бежать, но оказываетесь схвачены когтями виверны и отброшены на землю. При падении вы разбиваете голову. Как только поднимаетесь, чувствуете как ваши глаза закрываются и опрокидываетесь на спину",
                  f"Вы пытаетесь бежать, но ваш бок оказывается в цепкой хватке Виверны. Как только она отпускает, со следов её зубов в боку начинает обильно сочиться кровь. Успевая отбежать на пару метров, вы теряете сознание от кровопотери."]

        not_in_attack_quote = 'Виверна прочитала ваши мысли быстрее, чем вы успели сделать разворот. Из-за скорости её движений, вы даже не заметили как потеряли ступню в её зубах. Следующим укусом, она вцепилась в вашу шею. Вы даже не успели вскрикнуть'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote


    def give_in_dead_quotes_for_team(self, char):
        in_attack_quotes = [f"{char.name} проткнут жалом Виверны насквозь при попытке к бегству",
                  f"{char.name} пытается бежать но оказывается в когтях Виверны и отброшен за пределы поля боя",
                  f"{char.name} пытается бежать, но находит свой бок в цепкой хватке Виверны. После того, как Виверна отпускает, он успевает пробежать пару метов, прежде чем падает замертво"]

        not_in_attack_quote = f'{char.name} пытался сбежать, но потерял свою ступню в зубах Виверны. Следующий её укус пришелся на его горло'
        if char.quoteIndex is not None:
            return in_attack_quotes[char.quoteIndex]
        else:
            return not_in_attack_quote



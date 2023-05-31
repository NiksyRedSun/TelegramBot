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


    def give_player_dead_quotes(self):
        player_dead_quotes = []
        return player_dead_quotes[self.quoteIndex]


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



    async def attack_one_func(self, char, text: list, bot, id):
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
                        text.append(f"<b>{char.name} отъезжает в ходе битвы</b>")
                        if char.quoteIndex is not None:
                            char.in_dead_quote = random.choice(char.dead_quotes)
                            await bot.send_message(chat_id=id, text=char.in_dead_quote)
                            char.quoteIndex = None
                        else:
                            char.in_dead_quote = self.give_player_dead_quotes()
                            await bot.send_message(chat_id=id, text=char.in_dead_quote)

            else:
                text.append(self.give_pos_quotes(char))
            text.append("")




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
            await self.attack_one_func(players[player]["char"], message_text, bot, player)
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
        self.exp = random.randint(2500, 3500)
        self.quoteIndex = 0

        self.quotes = [f"{self.name} замахивается своим хвостом",
                  f"{self.name} готовится залить все огнем",
                  f"{self.name} издает пронзительный рев",
                  f"{self.name} широко взмахивает крыльями",
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
                      f"{char.name} уклоняется от порыва ветра",
                      f"{char.name} уворачивается от когтей Красного дракона"]
        return pos_quotes[self.quoteIndex]


    def give_neg_quotes(self, char, damage):
        neg_quotes = [f"{char.name} получает {damage} урона от удара хвостом, устояв на ногах",
                      f"{char.name} получает {damage}  урона от ожогов, задержавшись в пламени на пол секунды",
                      f"{char.name} ловит звон в ушах и головную боль, теряя {damage} hp",
                      f"{char.name} падает на землю от порыва ветра, теряя {damage} hp",
                      f"{char.name} зацеплен когтями дракона на {damage} урона"]
        return neg_quotes[self.quoteIndex]



    def give_really_neg_quotes(self, char, damage):
        really_neg_quotes = [f"{char.name} отлетает от хвоста дракона на 10 метров и получает {damage} урона",
                             f"{char.name} получает {damage} единиц урона от горения, задержавшись в пламени на полторы секунды",
                             f"{char.name} теряет кровь из ушей и {damage} hp",
                             f"{char.name} прижат к земле порывом ветра и теряет {damage} hp",
                             f"{char.name} небрежно отброшен в сторону когтями Дракона, потеряв {damage} hp"]
        return really_neg_quotes[self.quoteIndex]


    def give_player_dead_quotes(self):
        player_dead_quotes = [f"Неудачное падение, после удара хвостом сулит вам сломанную шею. Сознание все еще при вас, но двигаться вы уже не можете, остается только ждать смерти",
                             f"Последнее, что вы помните, это пасть Красного дракона, и вылетающее от туда пламе",
                             f"Шум, звон, головная боль и кровь из ушей роняют вас на землю. Судя по тому что вы не можете пошевелить ровно половиной своего тела, вас хватил удар. Эта ужасная мысль сопровождает вас до скоронаступающей смерти",
                             f"При попытке встать после падения, вы сразу же падаете из-за сильнейшего головокружения. Пытаясь встать, вы замечаете струю крови, спускающуюся по телу. Пара капель попадает вам на ладонь и вы падаете без сил",
                             f"Неудачное падение, после отброса когтями сулит вам сломанную шею. Сознание все еще при вас, но двигаться вы уже не можете, остается только ждать смерти"]
        return player_dead_quotes[self.quoteIndex]


    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"Вы пытаетесь бежать, но вас сносит ударом хвоста в спину, при падении вы разбиваете голову. Пытаясь ползти, вы начинаете медленно терять сознание",
                  f"Вы пытаетесь бежать, но чувствуете, как пламя Дракона настигает вас в спину, быстрее чем вы успеваете вскрикнуть от горячей боли",
                  f"Сделав несколько шагов назад, вы глохнете от рева Дракона и падаете на землю. Пытаясь ползти, вы медленно теряете сознание",
                  f"Не успев развернуться, вас сносит порывом ветра от крыльев Красного дракона, при падении вы разбиваете голову. Пытаясь ползти, вы медленно теряете сознание",
                  f"Развернувшись, вы не успеваете одуматься, как когти Дракона подхватывают вас в небо. При последующем падении вы разбиваете голову. Пытаясь ползти, вы медленно теряете сознание. Перевернувшись на живот перед смертью, вы видите полосу собственно крови на земле"]

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
        self.exp = random.randint(2750, 3750)
        self.quoteIndex = 0

        self.quotes = [f"{self.name} выстреливает сеткой из паутины",
                  f"{self.name} плюется кислотой",
                  f"{self.name} замахивается передними лапами",
                  f"{self.name} готовится пустить в ход жвалы"]

        self.dead_quotes = [f"{self.name} упал замертво",
                  f"{self.name} больше никогда не будет плевать кислотой",
                  f"{self.name} склеил лапы",
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
                      f"{char.name} получает {damage} урона кислотой, прожигающей кожный покров",
                      f"{char.name} зацеплен передней лапой паука на {damage} hp",
                      f"{char.name} зацеплен жвалами паука на {damage} hp"]
        return neg_quotes[self.quoteIndex]



    def give_really_neg_quotes(self, char, damage):
        really_neg_quotes = [
            f"{char.name} падает на пол запутавшись в паутине, ударяется головой и получает {damage} урона",
            f"{char.name} получает {damage} урона кислотой, прожигающей мышечную ткань",
            f"{char.name} проткнут передней лапой паука насквозь на {damage} hp",
            f"{char.name} застрял в жвалах паука на {damage} hp"]
        return really_neg_quotes[self.quoteIndex]


    def give_player_dead_quotes(self):
        player_dead_quotes = [
            f"От удара при падении, из вашей головы начинает течь кровь, но вы ничего не можете сделать, поскольку ваши руки связаны паутиной. Вам остается только терять сознание, наблюдая за ручейком крови, спешащим по вашему телу вниз",
            f"Вы пытаетесь стереть с себя кислоту. Но все что у вас получается - тереть окисленными пальцами по окисленному лицу. Осознание вашей текущей уродливости прерывается потерей сознания от болевого шока",
            f"Думали ли вы когда-нибудь о жизни, после того, как Паук проткнет вам грудную клетку своей лапой насквозь? Ранение не сопоставимое с жизнью, не позволяет вам подумать об этом и теперь и вы медленно теряете сознание",
            f"Находясь в жвалах паука, вы пытаетесь вспомнить хоть какую-нибудь уловку, которая может освободиться, но безуспешно. Вы смотрите в его ужасные глаза и теряете сознание, больше от страха, чем от ранений."]
        return player_dead_quotes[self.quoteIndex]



    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"Вы попытались сбежать, но были прибиты сетью к стене. От удара, из вашей головы начинает течь кровь, но вы ничего не можете сделать, поскольку ваши руки связаны паутиной. Вам остается только терять сознание, наблюдая за ручейком крови, спешащим по вашему телу вниз",
                  f"Вы попытались бежать, но были настигнуты попаданием кислоты в спину. Последнее что вы чувствуете, как кости оголяются после излишнего окисления мышц",
                  f"Вы попытались бежать, но были проткнуты лапой паука в поясницу. Ваши дальнейшие попытки двигать ногами были обречены на неудачу, но вас это не слишком беспокоит, поскольку вы начинаете терять сознание от болевого шока",
                  f"Вы успели развернуться, но жвалы паука добрались до вашего бедра быстрее, чем вы сделали шаг. Думали ли вы когда-нибудь, что вам придется лицезреть обрубок собственной ноги перед тем как умереть?"]

        not_in_attack_quote = 'Паук прочитал ваши мысли быстрее, чем вы успели сдвинуться с места. Своими жвалами, он прокусил вам правую ногу. От обильной потери крови и болевого шока вы начинаете терять сознание'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote


    def give_in_dead_quotes_for_team(self, char):
        in_attack_quotes = [f"{char.name} прибит сеткой из паутины к стене. При влете в стену, его черепная коробка раскрывается",
                  f"{char.name} роняет куски окисленного мяса со своей спины, переходя с бега в падение, а затем и в отключение",
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
        self.exp = random.randint(4500, 5550)
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



    def give_player_dead_quotes(self):
        player_dead_quotes = [f"Последнее, что вы помните - кулак молот, летящий вам в лицо. Поврежденные глаза, не дают вам увидеть картину поля боя. Но это не важно. Вы теряете сознание, сразу после падения на землю",
                             f"Вас заливает кипящим маслом. Открыв рот, в попытках вскрикнуть, вы захлебываетесь им до самой смерти",
                             f"Слишком много ранений не позволяют вам продолжить бой. Последние два колышка становятся причиной сильной потери крови. Сознание медленно улетучивается",
                             f"Последнее, что вы помните - лоб Голема, летящий вам в лицо. Судя по невозможности сохранять равновесие - у вас сотрясение мозга. Вы теряете сознание, сразу после падения на землю"]
        return player_dead_quotes[self.quoteIndex]



    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"При попытке к бегству вы получаете удар кулаком-молотом в затылок. Перед тем как потерять сознание, вы наблюдаете кусок вашего мозга летящим вперед вас самого",
                  f"При попытке к бегству вас заливает сзади кипящим маслом. Открыв рот, в попытках вскрикнуть, вы захлебываетесь им до самой смерти",
                  f"При попытке к бегству, вы не совсем понимаете что происходит, пока не проводите ладонью по передней поверхности шеи и не осознаете, что ощущаете два острия. Разорванная сонная артерия усыпляет лучше чем сказка матери на ночь",
                  f"Вы пытаетесь бежать, но оказывайтесь на траектории пробежки Голема, и втаптываетесь его ногой в пол. Вам тяжело дается осознание того, что большая часть добычи может уйти на зубного. Прежде, чем забыться, вы успеваете увидеть отблескивающую железную ногу"]

        not_in_attack_quote = 'Голем прочитал ваши мысли быстрее, чем вы успели сделать хотя бы поворот в направлении побега. Возникшей темноте предшествовало направление Големом пушки в ваше лицо'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote

    def give_in_dead_quotes_for_team(self, char):
        in_attack_quotes = [f"{char.name} получил удар кулаком-молотом в затылок и растерял свой мозг по полу",
                  f"{char.name} залит кипящим маслом при попытке к бегству",
                  f"{char.name} получил два колышка в шею, при попытке к бегству",
                  f"{char.name} попытался бежать, но был затоптан Големом, растеряв остатки лица по полу"]

        not_in_attack_quote = f'{char.name} пытался сбежать, но получил выстрелом колышка в лицо и зажмурился'
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
        self.exp = random.randint(4000, 4750)
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
        really_neg_quotes = [f"{char.name} получает удар ветками прямо в глаза и {damage} урона",
                             f"{char.name} сбит с ног корнями Дерева, теряя {damage} hp",
                             f"{char.name} обнаруживает на себе химические ожоги до кости от гнилых плодов и потерю {damage} hp",
                             f"{char.name} оказывается заперт в кроне дерева с ульем, проедающим ему лицо на {damage} hp"]
        return really_neg_quotes[self.quoteIndex]


    def give_player_dead_quotes(self):
        player_dead_quotes = [f"Вы чувствуете, как ветки проникают ваш рот, нос и горло, не успевая вскрикнуть, вы понимаете что дерево уже даже в ваших кишках",
                             f"Дерево начинает оплетать вас корнями. Сила корней настолько велика, что в какой-то момент кости в вашем теле начинают ломаться и вы теряете сознание от болевого шока",
                             f"Вы пытаетесь стереть с себя кислоту. Но все что у вас получается - тереть окисленными пальцами по окисленному лицу. Осознание вашей текущей уродливости прерывается потерей сознания от болевого шока",
                             f"Вас заживо съедает улей неизвестных насекомых. Ваших криков не слышно из-за их пронзительного жужжания."]
        return player_dead_quotes[self.quoteIndex]




    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"Вы пытаетесь бежать, но получаете ветками в затылок. Потеря сознания делает вас неспособным драться",
                  f"Вы пытаетесь бежать, но Дерево оплетает корнями ваши ноги. Сила корней настолько велика, что в какой-то момент кости в ваших ногах начинают ломаться и вы теряете сознание от болевого шока",
                  f"Вы пытаетесь бежать, но чувствуете, как на голову падает гнилой плод. Идя вперед и пытаясь вытереть глаза от кислоты, вы падаете в объятия встречающих вас корней Гнилого дерева. Они прижимают вас к земле и начинают медленно перемалывать. Ваш крик никто не слышит, потому что первым делом они добираются до вашей шеи",
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
        self.exp = random.randint(5000, 5790)

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


    def give_player_dead_quotes(self):
        player_dead_quotes = [f"Вы оказались проткнутым жалом Виверны насквозь. Перед тем, как она вытаскивает его из вас, вы видите на его острие то что осталось от вашего сердца. От увиденного, вам не хватает сил даже вскрикнуть",
                             f"Вы оказываетесь схвачены когтями виверны и отброшены за пределы поля боя. При падении вы разбиваете голову. Как только поднимаетесь, чувствуете как ваши глаза закрываются и опрокидываетесь на спину",
                             f"Ваш бок оказывается в цепкой хватке Виверны. Как только она отпускает, со следов её зубов в боку начинает обильно сочиться кровь. Вам не хватает сил остановить кровь и пройдя пару шагов от места падения вы проваливаетесь в вечный сон."]
        return player_dead_quotes[self.quoteIndex]


    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"Вы пытаетесь бежать, но оказыватесь проткнутым жалом Виверны насквозь. Перед тем, как она вытаскивает его из вас, вы видите на его острие то что осталось от вашего сердца. От увиденного, вам не хватает сил даже вскрикнуть",
                  f"Вы пытаетесь бежать, но оказываетесь схвачены когтями виверны и отброшены за пределы поля боя. При падении вы разбиваете голову. Как только поднимаетесь, чувствуете как ваши глаза закрываются и опрокидываетесь на спину",
                  f"Вы пытаетесь бежать, но ваш бок оказывается в цепкой хватке Виверны. Как только она отпускает, со следов её зубов в боку начинает обильно сочиться кровь. Вам не хватает сил остановить кровь, пройдя пару шагов от места падения вы проваливаетесь в вечный сон."]

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




class ToadVillian(Villian):
    def __init__(self):
        self.name = "Гигантский жаб"
        self.story = "Тот парень из террариума, но в человеческий рост. Может проглотить за один раз."
        self.hp = 400
        self.max_hp = self.hp
        self.attack = 9
        self.defense = 4
        self.initiative = 7
        self.alive = True
        self.money = random.randint(1500, 1500)
        self.exp = random.randint(6000, 6750)
        self.quoteIndex = 0

        self.quotes = [f"{self.name} выпускает свой язык",
                  f"{self.name} замахивается лапой",
                  f"{self.name} делает разрушительный *КВА*"]

        self.dead_quotes = [f"Теряет свой длинный язык",
                      f"{self.name} опрокидывается в замахе",
                      f"Теперь {self.name} заканчивает свой *КВА* и жизнь вместе с ним"]

        self.maxQuoteIndex = len(self.quotes) - 1



    def give_pos_quotes(self, char):
        pos_quotes = [f"{char.name} успевает уклониться от языка Жабы",
                      f"{char.name} успевает уклониться от лабы Жабика",
                      f"{char.name} закрывает уши и не слышит разрушительного *КВА*"]
        return pos_quotes[self.quoteIndex]


    def give_neg_quotes(self, char, damage):
        neg_quotes = [f"{char.name} получает {damage} урона от удара языком Жабчика в лицо",
                      f"{char.name} получает {damage}  урона от удара лапы Жабчика по лицу",
                      f"{char.name} ловит звон в ушах и головную боль, теряя {damage} hp"]
        return neg_quotes[self.quoteIndex]



    def give_really_neg_quotes(self, char, damage):
        really_neg_quotes = [f"{char.name} втянут в живот Жабчика и задерживается там на {damage} урона",
                             f"{char.name} откинут лапой Жабчика в близлежащее дерево",
                             f"{char.name} теряет кровь из ушей и {damage} hp"]
        return really_neg_quotes[self.quoteIndex]


    def give_player_dead_quotes(self):
        player_dead_quotes = [f"Попадание в живот Жабеса сулит вам скорую смерть. Содержимое желудка уже занимается вашим перевариванием. Снизу вверх, вы прожигаетесь кислотой и испускаете дух",
                             f"Удар Жабеса настолько сильный, что пробивает вашу голову, отправляя вас к праотцам",
                             f"Будучи оглушенным, вы падаете на землю. Последующий наскок Жабы, придавливает вас. Думали ли вы когда-нибудь, что увидите свои внутренности, выходящие изо рта"]
        return player_dead_quotes[self.quoteIndex]


    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"Вы пытаетесь бежать, но вас сносит ударом языка в спину, при падении вы разбиваете голову. Пытаясь ползти, вы начинаете медленно терять сознание",
                  f"Вы пытаетесь бежать, но не успеваете сделать и шагу, как оказываетесь придавлены Жабесом. Думали ли вы когда-нибудь, что увидите свои внутренности, выходящие изо рта",
                  f"Сделав несколько шагов назад, вы глохнете от Кваканья Жабчика и падаете на землю. Пытаясь ползти, вы медленно теряете сознание"]

        not_in_attack_quote = 'Жабчик прочитал ваши мысли быстрее, чем вы успели сдвинуться с места. Своим языком, он пригвоздил вас к дереву и проглотил целиком.'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote


    def give_in_dead_quotes_for_team(self, char):
        in_attack_quotes = [f"{char.name} попытался бежать, но отлетел от удара языка Жабчика в спину, разбив голову при падении",
                  f"{char.name} попытался бежать, но был придавлен Жабчиком, оставив внутренности на земле",
                  f"{char.name} попытался бежать, но упал после оглушения Кваком"]

        not_in_attack_quote = f'{char.name} пытался сбежать, но Жабес пригвоздил к дереву с последующим проглатыванием'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote
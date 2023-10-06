from SomeClasses.BasicClasses import Unit, dice, double_dices
import random
import asyncio
from EasyGameLoader import bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from SomeKeyboards import next_keyb, end_menu_keyb, attack_menu_keyb, menu_keyb, mob_next_keyb



class Mob(Unit):
    def __init__(self):
        self.name = None
        self.story = None
        self.hp = None
        self.max_hp = None
        self.attack = None
        self.defense = None
        self.initiative = None
        self.alive = None
        self.money = None
        self.exp = None
        self.link = None
        self.quoteIndex = None

        self.quotes = []
        self.pos_quotes = []
        self.dead_quotes = []
        self.char_killed_quotes = []

        self.maxQuoteIndex = len(self.quotes)-1


    def presentation(self):
        text = [f"Ваш противник: {self.name}", f"{self.story}"]
        return '\n'.join(text)

    def fight_presentation(self):
        pres_name = "+" + self.name.center(22, "-") + "+"
        text = [f"<code>{pres_name}</code>", f"Здоровье: {self.hp}/{self.max_hp}".center(40)]
        return '\n'.join(text)


    def reset(self):
        self.__init__()


    async def money_exp_having(self, player, message):
        player.money += self.money
        player.exp += self.exp
        player.next_level()
        await message.answer(text=f"{player.name} получает {self.money} монет и {self.exp} опыта за убийство", reply_markup=mob_next_keyb)


    def give_neg_quotes(self, damage):
        neg_quotes = []
        return neg_quotes[self.quoteIndex]


    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = []
        not_in_attack_quote = ''
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote



    async def attack_func(self, char, message):
        if not self.alive or not char.alive:
            return None
        self.quoteIndex = random.randint(0, self.maxQuoteIndex)

        await message.answer(text=self.quotes[self.quoteIndex], reply_markup=attack_menu_keyb)
        await asyncio.sleep(2)

        char.check_alive()
        self.check_alive()
        if not self.alive or not char.alive:
            return None

        villian_init = double_dices() + self.initiative
        if char.in_avoid:
            char_init = double_dices() + char.initiative
        else:
            char_init = double_dices() + dice()

        if villian_init > char_init:
            damage = self.attack + dice() - char.defense

            if damage <= 0:
                await message.answer(text="Противник попадает по вам, но не наносит урона")
            else:
                if char.in_avoid:
                    await message.answer(text="Уклонение безуспешно")
                char.hp -= damage
                await message.answer(text=self.give_neg_quotes(damage))
                char.check_alive()
                if not char.alive:
                    if char.quoteIndex is not None:
                        char.in_dead_quote = char.dead_quotes[char.quoteIndex]
                        await message.answer(text=char.in_dead_quote, reply_markup=next_keyb)
                    else:
                        char.in_dead_quote = random.choice(self.char_killed_quotes)
                        await message.answer(text=char.in_dead_quote, reply_markup=next_keyb)
        else:
            if char.in_avoid:
                await message.answer(text="Уклонение успешно")
                char.stat.successAvoiding += 1
            await message.answer(text=self.pos_quotes[self.quoteIndex])
        self.quoteIndex = None
        char.in_avoid = False





class SceletonMob(Mob):
    def __init__(self):
        self.name = "Скелет"
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
        self.quoteIndex = None

        self.quotes = [f"{self.name} замахивается мечом слева",
                  f"{self.name} замахивается мечом справа",
                  f"{self.name} замахивается мечом сверху"]

        self.pos_quotes = [f"Вы отходите назад, успевая уклониться от меча скелета",
                      f"Вы проходите под лезвием меча скелета, не задев его",
                      f"Вы успеваете отойти в бок от летящего меча"]

        self.dead_quotes = [f"{self.name} разваливается на части",
                            f"{self.name}  роняет грудную клетку, оставив ноги стоять",
                            f"{self.name} пролетает вперед и разбивается о стену"]

        self.char_killed_quotes = [f"Скелет просто уходит оставляя вас умирать, оставив свой меч в ваших ребрах на прощание",
                          f"Ваши кишки начинают выпадывать наружу, вы тревожно пытаетесь засунуть их обратно, пока не "
                          f"понимаете, что это безнадежно. Сразу после этого вы теряете сознание",
                          f"Кажется кусок вашего легкого оказался на соседней стенке. Вам ничего не остается кроме как "
                          f"наблюдать за тем, как оно медленно скользит по стене. Вы теряете много крови"]

        self.maxQuoteIndex = len(self.quotes)-1


    def give_neg_quotes(self, damage):
        neg_quotes = [f"Вы получаете {damage} урона от попадания меча между ребер",
                          f"Вы получаете {damage} урона от резаной раны живота",
                          f"Вы получаете скользящий удар по груди и теряете {damage} hp"]
        return neg_quotes[self.quoteIndex]


    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"Вы пытаетесь бежать, но скелет протыкает вас мечом под лопатку. Судя по его виду, ему нет дела до меча, оставшегося у вас в спине. Вы начинаете терять сознание",
                  f"Вы разворачиваетесь, но не успевая сделать и шагу, обнаруживаете меч скелета заходящим сбоку в левую половину грудной клетки. Ваши попытки вытащить его заканчиваются тем, что вы окончательно теряете силы и сознание",
                  f"Не успевая сделать и шагу назад, вы получаете удар меча в затылок и забытье"]
        not_in_attack_quote = 'Казалось бы, что может быть проще, чем убежать от скелета. Вы тоже так думали, до того момента, как он метнул вам в спину меч при попытке к бегству. Падая, ваше тело опирается на лезвие меча, торчащее из вашей груди. Ваше тело медленно соскальзывает на нем к полу'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote






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
        self.exp = random.randint(450, 750)
        self.link = "/LittleDragonMob"
        self.quoteIndex = None

        self.quotes = [f"{self.name} хочет укусить вас",
                  f"{self.name} начинает пронзительно вопить",
                  f"{self.name} замахивается на вас лапами"]

        self.pos_quotes = [f"Вы отходите назад, успевая уклониться зубов Молодого дракона",
                      f"Вы успеваете закрыть уши",
                      f"Вы успеваете отойти в бок от летящих в вас когтей Дракоши"]

        self.dead_quotes = [f"{self.name} от вашего попадания роняет голову",
                            f"{self.name} вопит еще в течение 3х секунд, прежде чем отдать концы",
                            f"{self.name} падает лапами вверх"]

        self.char_killed_quotes = [f"Падая на колени вы чувствуйте сильный укус на своем теле, разрывая рубашку вы видите следы зубов дракона,"
                              f" из которых обильно сочится кровь, вы начинаете терять сознание",
                             f"Будучи неспособным думать ни о чем кроме шума в голове и крови из ушей вы начинаете терять сознание",
                            f"Лёжа на холодном полу, вы ощущаете как дракон пытается полакомиться вашей селезенкой"]

        self.maxQuoteIndex = len(self.quotes) - 1

    def give_neg_quotes(self, damage):
        neg_quotes = [f"Вы получаете {damage} урона от укуса Молодого дракона",
                      f"Вы получаете {damage} очков головной боли от пронзительного вопля дракона",
                      f"Вы находите на своем теле следы от когтей дракона на {damage} урона"]
        return neg_quotes[self.quoteIndex]


    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"Развернувшись вы понимаете, что дракон успел добраться своими зубами до вашей шеи, быстрее чем вы успели сделать шаг. Будучи не способным сказать хоть слово, вы падаете на землю и пытаетесь остановить кровотечение. Следующий укус дракона приходится на ваше лицо",
                  f"Вы пытаетесь бежать, но падаете, будучи оглушенным воем дракоши. Следующее, что вы видите - зубы дракона, летящие в ваши глаза",
                  f"Сразу после разворота вас отбрасывает лапами дракоши на соседние камни. Кровь обильно вытекает из вашего затылка. Поэтому вы теряете сознание быстрее, чем дракоша успевает добраться своими зубами до вашей печени"]
        not_in_attack_quote = 'Сразу после разворота вашу голень пробивает сильнейшей болью, земля выпадает у вас из под ног. Следующий укус дракоши приходится на вашу шею'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote






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
        self.exp = random.randint(750, 950)
        self.link = "/OrcMob"
        self.quoteIndex = None

        self.quotes = [f"{self.name} замахивается на вас сверху",
                  f"{self.name} хочет ударить вас эфесом своего меча",
                  f"{self.name} пытается замахнуться ногой для удара"]

        self.pos_quotes = [f"Вы отходите вбок, пропуская удар мимо себя",
                      f"Вы отводите голову вбок на пару сантиметров и этого достаточно",
                      f"Вы делаете шаг назад и оказываетесь недостижимы для ноги Орка"]

        self.dead_quotes = [f"Из Орка сыплются кишки, но кажется, что его это совсем не интересует",
                            f'"Спасибо за славную смерть", - его последние слова',
                            f"Орк встречает свою смерть, падая спокойным лицом вверх"]

        self.char_killed_quotes = [f"Мгновение назад, вы отвлеклись на боль от ранения. А теперь вы чувствуете как вам в шею сзади помещается кинжал. Спазм шейных мышц заставляет вас еще раз посмотреть на небо перед смертью",
                                f"Последнее, что вы видите, падая на землю, это пятку забивающего вас до смерти Орка",
                                f"После небольшой потери равновесия вы теряете врага из виду, и находите кинжал у себя в пояснице. Отнявшиеся ноги не позволяют вам двигаться и Орк оставляет вас на съедение стервятникам"]

        self.maxQuoteIndex = len(self.quotes) - 1

    def give_neg_quotes(self, damage):
        neg_quotes = [f"Вы получаете {damage} урона от рассечения груди, не успевая довернуться",
                      f"Вы недостаточно отводите голову в бок, и теряете лицо на {damage} hp",
                      f"Вы не успеваете сделать шаг назад и получаете пяткой орка под дых на {damage} урона"]
        return neg_quotes[self.quoteIndex]


    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"Сразу после разворота на ваш затылок опускается орочий меч. Последнее, что вы видите - орка, уходящего вдаль, без желания добивать своего врага",
                  f"Сразу после разворота на ваш затылок опускается эфес орочего меча. Последнее, что вы видите - орка, уходящего вдаль, без желания добивать своего врага",
                  f"Развернувшись вы падаете, после удара орка ногой вам в крестец. Перевернув вас на спину, он вставляет вам меч в грудь. Ваших сил недостаточно, чтобы попытаться вытащить лезвие и вы теряете сознание."]
        not_in_attack_quote = 'Сразу после разворота ваше колено пробивает сильнейшей болью сзади наперед, земля выпадает у вас из под ног. Прежде чем нанести заключительный удар, орк презрительно смотрит на вас'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote






class ElvenWizardMob(Mob):
    def __init__(self):
        self.name = "Лесной эльф маг"
        self.story = "Очередной приверженец эльфийской лесной культуры. Такие контролируют и отстаивают 50% местных чащоб"
        self.hp = 65
        self.max_hp = self.hp
        self.attack = 9
        self.defense = 3
        self.initiative = 8
        self.alive = True
        self.money = random.randint(600, 800)
        self.exp = random.randint(950, 1250)
        self.link = "/ElvenWizardMob"
        self.quoteIndex = None

        self.quotes = [f"{self.name} поднимает столбы воды из недр земли",
                  f"{self.name} пускает в вас осколками льда",
                  f"{self.name} стреляет в вас молнией из своего посоха"]

        self.pos_quotes = [f"Вы уворачиваетесь от поднимающихся вверх столбов воды",
                      f"Вы уворачиваетесь от осколков льда",
                      f"В кувырке вы уворачиваетесь от молнии"]

        self.dead_quotes = [f"Каким бы эльфийским он не был, умирает прямо как среднестатистический человек. От полученных ран.",
                            f"Вы перерезаете очередную глотку эльфа очередным ударом меча",
                            f"Судя по его предсмертному лицу, парень был не против умереть за этот лес"]

        self.char_killed_quotes = [f"Падая на землю, вы понимаете, что корни окутывают ваши конечности, не давая вам пошевелиться. Эльф, управляя корнями поднимает вас в воздух и разворачивает к себе лицом. Последнее, что вы помните - летящий в ваше лицо ледяной колышек",
                                f"Из-за полученных ран, вы подпускаете эльфийского мага слишком близко и он разрезает вам глотку заточенной обратной стороной посоха. Падая на колени, вы пытаетесь кричать, но вас уже никто не услышит",
                                f"Ледяной дробью вам простреливает в грудь и брюхо. Вы падаете на колени и видите, как из многочисленных ранений на теле торчат кусочки льда. Эльф оставляет вас на лесной опушке терять кровь"]

        self.maxQuoteIndex = len(self.quotes) - 1

    def give_neg_quotes(self, damage):
        neg_quotes = [f"Вас подбрасывает вверх на 4 метра, столбом воды. Падая лицом в землю вы теряете {damage} hp",
                      f"Вы находите колышек льда в правой подвздошной области, и теряете {damage} hp",
                      f"Вы чувствуете полноценную прожарку, в том числе и внутренних органов на {damage} урона"]
        return neg_quotes[self.quoteIndex]


    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"Сразу после разворота в ваш копчик влетает столб воды. Переламывая вам кости таза, он надежно гвоздит вас к земле. Вы провожаете глазами уходящего вдаль эльфа",
                  f"Сразу после разворота ваше колено сзади наперед простреливает колышком льда. Второй колышек маг отправляет вам в ступню, надежно пригвоздя к земле. Последний удар он наносит кинжалом, вскрывая вам глотку",
                  f"Сразу после разворота вас пробирает током. Из-за неожиданности вы не можете пошевелиться и чувствуете как прожариваются ваши внутренние органы. В какой-то момент вы начинаете понимать, что сознание накрывается из-за гипертермии"]
        not_in_attack_quote = 'Сразу после разворота вас простреливает ледяной дробью в спину. Вас прижимает к земле количеством льда в вашем организме. Вы еще долго лежа смотрите в бок, прежде чем теряете сознание'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote




class ElvenArcherMob(Mob):
    def __init__(self):
        self.name = "Лесной эльф лучник"
        self.story = "Еще один лесной эльф. Этот из местного спецназа, который отправили, чтобы устранить тех, кто наустранял эльфиских магов"
        self.hp = 75
        self.max_hp = self.hp
        self.attack = 10
        self.defense = 6
        self.initiative = 9
        self.alive = True
        self.money = random.randint(900, 1000)
        self.exp = random.randint(1250, 1450)
        self.link = "/ElvenArcherMob"
        self.quoteIndex = None

        self.quotes = [f"{self.name} целится в вас луком",
                  f"{self.name} отправляет в вас метательным кинжалом",
                  f"{self.name} пытается ударить кулаком с кастетом"]

        self.pos_quotes = [f"Вы уворачиваетесь от пролетающей в сантиметрах от вас стрелы",
                      f"Кинжал попадает в соседнее дерево, но не в вас",
                      f"Успеваете пригнуться от кастета"]

        self.dead_quotes = [f"Каким бы эльфийским он не был, умирает прямо как среднестатистический человек. От полученных ран.",
                            f"Говорят, что эти парни не даются живыми. Обильная кровопотеря убивает его слишком быстро, чтобы это узнать",
                            f"Теряющий кровь изо рта не такой уж и спецназ падает перед вами на колени, а потом и на лицо"]

        self.char_killed_quotes = [f"Падая на землю от стрелы в подколенной ямке вы не успеваете вскрикнуть, как вам перезают горло. Эти ребята никому не позволяют кричать в своем лесу",
                                f"Вы получаете кинжалом в самое сердце. Эльф вытаскивает кинжал, оставляя вас истекать кровью на опушке леса",
                                f"Вы получаете ударом кастета в лицо. А потом еще одним и еще. Постепенно эта цепочка затягивается и вы понимаете, что уже не можете ей противостоять. На 25 ударе, ваше лицо превращается в месево. Взмахом кинжала эльф перерезает вам сухожилия под коленкой и оставляет умирать"]

        self.maxQuoteIndex = len(self.quotes) - 1

    def give_neg_quotes(self, damage):
        neg_quotes = [f"Вы получаете стрелой в бедро, теряя при этом {damage} hp",
                      f"Вы получаете метательный нож в плечо и {damage} урона",
                      f"Вы получаете удар кастета в лицо на {damage} урона"]
        return neg_quotes[self.quoteIndex]


    def give_in_dead_quotes_for_player(self):
        in_attack_quotes = [f"Сразу после разворота ваше зрение выключается, а ноги подкашивает. В какой-то момент, вы начинаете понимать что вам прилетело стрелой в затылок и больше ничего не остается кроме как умереть",
                  f"Сразу после разворота ваше колено сзади наперед простреливает метателным кинжалом. Второй кинжал эльф отправляет вам в ступню, надежно пригвоздя к земле. Кинжал он использует и для последнего удара, вскрывая вам глотку",
                  f"Сразу после разворота ваш затылок пробирает кастетом. Вы получаете несколько ударов в затылок и последний пяткой, после которого теряете сознание"]
        not_in_attack_quote = 'Сразу после разворота вас простреливает луком в поясницу. Следующую стрелу эльф отправляет вам в шею'
        if self.quoteIndex is not None:
            return in_attack_quotes[self.quoteIndex]
        else:
            return not_in_attack_quote
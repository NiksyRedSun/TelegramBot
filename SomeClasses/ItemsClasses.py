import asyncio


class Item:
    def __init__(self):
        self.name = None
        self.tname = None
        self.cost = None
        self.info = None



    def shop_info(self):
        return f"{self.tname} - {self.name}. Стоимость: {self.cost} монет\n{self.info}"


    def show_in_inv(self, count):
        return f"{self.name} - {count} штук"


    def show_in_fight(self):
        return f"{self.tname} - {self.name}"



class HealingPotion(Item):
    def __init__(self):
        self.name = "Зелье восстановления здоровья"
        self.tname = "/healingPotion"
        self.info = "Восстанавливает два hp раз в две секунды, в течение 10и секунду "
        self.time = 5
        self.cost = 500
        self.quote = "Вас поправляет..."


    def remove_object(self, lst, obj_type):
        for obj in lst:
            if isinstance(obj, obj_type):
                lst.remove(obj)
                return True
        return False



    async def healing(self, char):
        while self.time > 0:
            if char.alive:
                if char.hp + 2 >= char.max_hp:
                    char.hp = char.max_hp
                else:
                    char.hp += 2
            else:
                break
            self.time -= 1
            await asyncio.sleep(2)
        char.effects[self.name] = None

    def char_ret_stat(self, char):
        pass


    async def item_task(self, message, char):
        if char.effects[self.name] is not None:
            char.effects[self.name].cancel()
            await asyncio.sleep(0.3)
        if self.remove_object(char.inventory, HealingPotion):
            char.effects[self.name] = asyncio.create_task(self.healing(char))
            await message.answer(text="Зелье лечения использовано")
        else:
            await message.answer(text="У вас нет зелья лечения в инвентаре")

    def status(self):
        return self.quote





class LiqPotion(Item):
    def __init__(self):
        self.name = "Наливка из местного *РОСКОМНАДЗОР* ресторана"
        self.tname = "/liqPotion"
        self.info = "Поднимает ваш уровень агрессии до заоблачных высот"
        self.time = 5
        self.cost = 1000
        self.quote = "Эх, наливочка..."


    def remove_object(self, lst, obj_type):
        for obj in lst:
            if isinstance(obj, obj_type):
                lst.remove(obj)
                return True
        return False


    async def inqreasing(self, char):
        while self.time > 0:
            if char.alive:
                if char.fury + 10 >= 100:
                    char.fury = 100
                else:
                    char.fury += 10
            else:
                break
            self.time -= 1
            await asyncio.sleep(2)
        await asyncio.sleep(20)
        char.effects[self.name] = None


    async def item_task(self, message, char):
        if char.effects[self.name] is not None:
            if not char.effects[self.name].done():
                await message.answer(text="Предыдущая наливочка еще не исчепрала свой эффект")
                return None
        if self.remove_object(char.inventory, LiqPotion):
            char.effects[self.name] = asyncio.create_task(self.inqreasing(char))
            await message.answer(text="Вы глотнули наливочки")
        else:
            await message.answer(text="У вас нет наливочки")

    def char_ret_stat(self, char):
        pass


    def status(self):
        return self.quote






class ConcentreationScroll(Item):
    def __init__(self):
        self.name = "Свиток концентрации"
        self.tname = '/conScroll'
        self.info = "Всем уже давно пора приобрести такие"
        self.cost = 1000
        self.quote = "Концентрация!"


    def remove_object(self, lst, obj_type):
        for obj in lst:
            if isinstance(obj, obj_type):
                lst.remove(obj)
                return True
        return False


    async def concentrating(self, char):
        char.initiative += 1
        await asyncio.sleep(10)
        char.initiative -= 1
        char.effects[self.name] = None


    async def item_task(self, message, char):
        if char.effects[self.name] is not None:
            if not char.effects[self.name].done():
                await message.answer(text="Предыдущий свиток концентрации еще действует")
                return None
        if self.remove_object(char.inventory, LiqPotion):
            char.effects[self.name] = asyncio.create_task(self.concentrating(char))
            await message.answer(text="Вы прочитывайте свиток концентрации")
        else:
            await message.answer(text="У вас нет свитка концентрации")

    def char_ret_stat(self, char):
        char.initiative -= 1


    def status(self):
        return self.quote



class Poison(Item):
    def __init__(self):
        self.name = "Яд на оружие"
        self.tname = '/poison'
        self.info = "Свежее поступление. Наносить на начищенный до блеска меч, до 3х раз в день"
        self.cost = 1500
        self.quote = "Оружие отравлено"


    def remove_object(self, lst, obj_type):
        for obj in lst:
            if isinstance(obj, obj_type):
                lst.remove(obj)
                return True
        return False


    async def concentrating(self, char):
        char.attack += 3
        await asyncio.sleep(15)
        char.attack -= 3
        char.effects[self.name] = None


    async def item_task(self, message, char):
        if char.effects[self.name] is not None:
            if not char.effects[self.name].done():
                await message.answer(text="Предыдущая порция яда еще не смылась")
                return None
        if self.remove_object(char.inventory, LiqPotion):
            char.effects[self.name] = asyncio.create_task(self.concentrating(char))
            await message.answer(text="Вы смазываете свое оружие ядом")
        else:
            await message.answer(text="У вас нет яда")

    def char_ret_stat(self, char):
        char.attack -= 3


    def status(self):
        return self.quote
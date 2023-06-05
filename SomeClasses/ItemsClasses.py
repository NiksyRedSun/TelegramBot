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


    async def item_task(self, message, char):
        if char.effects[self.name] is not None:
            char.effects[self.name].cancel()
            await asyncio.sleep(0.3)
        if self.remove_object(char.inventory, HealingPotion):
            char.effects[self.name] = asyncio.create_task(self.healing(char))
            await message.answer(text="Зелье лечения использовано")
        else:
            await message.answer(text="У вас нет зелья лечения в инвентаре")





class LiqPotion(Item):
    def __init__(self):
        self.name = "Наливка из местного *РОСКОМНАДЗОР* ресторана"
        self.tname = "/liqPotion"
        self.info = "Поднимает ваш уровень агрессии до заоблачных высот"
        self.time = 5
        self.cost = 1000


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




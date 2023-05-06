from SomeClasses.BasicClasses import Unit, dice, double_dices
import random
import asyncio
from EasyGameLoader import bot


class Mob(Unit):
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

    async def money_exp_having(self, player, message):
        player.money += self.money
        player.exp += self.exp
        await message.answer(text=f"{player.name} получает {self.money} монет и {self.exp} опыта за убийство")
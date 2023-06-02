import asyncio


class Item:
    def __init__(self):
        self.name = None
        self.tname = None



class HealingPotion(Item):
    def __init__(self):
        self.name = "Зелье восстановления здоровья"
        self.tname = "/healingPotion"
        self.info = "Восстанавливает 2 hp раз в секунду, в течение 5и секунду "
        self.time = 5
        self.cost = 500


    async def healing(self, char):
        while self.time > 0:
            if char.alive:
                if char.hp + 3 >= char.max_hp:
                    char.hp = char.max_hp
                else:
                    char.hp += 3
            else:
                break
            self.time -= 1
            await asyncio.sleep(1)


    def shop_info(self):
        return f"{self.tname} - {self.name}. Стоимость: {self.cost} монет\n{self.info}"


    def show_in_inv(self, count):
        return f"{self.name} - {count} штук"


    def show_in_fight(self, count):
        return f"{self.tname} - {self.name} - {count} штук"


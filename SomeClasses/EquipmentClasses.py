import asyncio


class Equipment:
    def __init__(self, itemName, itemMaxHp, itemAttack, itemDefense, itemInitiative, forAttack):
        self.itemName = itemName
        self.itemMaxHp = itemMaxHp
        self.itemAttack = itemAttack
        self.itemDefense = itemDefense
        self.itemInitiative = itemInitiative
        self.forAttack = forAttack

    def info(self):
        text = ["",
                f"{self.itemName}",
                f"<code>Подъем здоровья: ".ljust(20) + f"{self.itemMaxHp}</code>",
                f"<code>Подъем атаки: ".ljust(20) + f"{self.itemAttack}</code>",
                f"<code>Подъем защиты: ".ljust(20) + f"{self.itemDefense}</code>",
                f"<code>Подъем ловкости: ".ljust(20) + f"{self.itemInitiative}</code>",
                f"<code>Используется в бою: ".ljust(20) + f"{self.forAttack}</code>",
                ""
                ]
        return text
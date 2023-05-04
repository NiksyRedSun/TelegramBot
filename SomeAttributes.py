from GameClasses import Character, DragonVillian
from Functions import give_villian

villian = give_villian()



pirate = Character("Черная борода", "Как вы уже догадались, вы пират", 35, 7, 2, 5)
tatarin = Character("Айзулбек", "Вы тут за татарина с луком", 25, 7, 3, 5)
viking = Character("Сигурд", "Вы тут за викинга, вам ничего не остается кроме как махать мечом", 60, 10, 4, 3)
elf = Character("Дарриан", "Вы тут за эльфа, наемного убийцу", 20, 8, 1, 6)
khajiit = Character("Рисаад", "Опция для тех, кто хочет играть за каджита", 30, 7, 2, 5)
gnom = Character("Эдукан", "Никакой команде не обойтись без гнома, на вас - размахивать топором", 50, 10, 4, 4)
testChar = Character("SomePers", "Используем этого перса для тестирования", 100, 100, 100, 1000)

ids = []

units_dict = {"/pirate": pirate, "/tatarin": tatarin, "/viking": viking, "/elf": elf, "/khajiit": khajiit,
              "/gnom": gnom, "/testChar": testChar}

boss_fight_is_on = False

players_dict = {}

current_boss_fight_team = {}
boss_fight_team = {}


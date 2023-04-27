from GameClasses import Unit, Villian, Character

villian = Villian("Красный дракон", "Его чешуя отливает бордово-винным цветом, но все почему-то говорят, что он красный", 300, 8, 4, 5)


pirate = Character("Черная борода", "Как вы уже догадались, вы пират", 45, 5, 2, 4)
tatarin = Character("Айзулбек", "Вы тут за татарина с луком", 25, 8, 2, 4)
viking = Character("Сигурд", "Вы тут за викинга, вам ничего не остается кроме как махать мечом", 60, 10, 4, 2)
elf = Character("Дарриан", "Вы тут за эльфа, наемного убийцу", 20, 8, 1, 6)
khajiit = Character("Рисаад", "Опция для тех, кто хочет играть за каджита", 30, 7, 1, 5)
gnom = Character("Эдукан", "Никакой команде не обойтись без гнома, на вас - размахивать топором", 50, 8, 3, 3)
testChar = Character("SomePers", "Используем этого перса для тестирования", 1, 1, 1, 1)

ids = []

units_dict = {"/pirate": pirate, "/tatarin": tatarin, "/viking": viking, "/elf": elf, "/khajiit": khajiit,
              "/gnom": gnom, "/testChar": testChar}

players_dict = {}

current_boss_fight_team = []


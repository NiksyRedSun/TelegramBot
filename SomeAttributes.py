from GameClasses import Unit, Villian

villian = Villian("Груда костей", "Несколько тысяч костей, по прикидкам в нем человек 10, не меньше", 200, 7, 4)
pirate = Unit("Черная борода", "Как вы уже догадались, вы пират", 45, 5, 4)
tatarin = Unit("Айзулбек", "Вы тут за татарина с луком", 25, 8, 4)
viking = Unit("Сигурд", "Вы тут за викинга, вам ничего не остается кроме как махать мечом", 60, 10, 2)
elf = Unit("Дарриан", "Вы тут за эльфа, наемного убийцу", 20, 8, 6)
khajiit = Unit("Рисаад", "Опция для тех, кто хочет играть за каджита", 30, 7, 5)
gnom = Unit("Эдукан", "Никакой команде не обойтись без гнома, на вас - размахивать топором", 50, 8, 3)

ids = []

units_dict = {"/pirate": pirate, "/tatarin": tatarin, "/viking": viking, "/elf": elf, "/khajiit": khajiit,
              "/gnom": gnom}

alive_players = []
death_players = []
players = 0

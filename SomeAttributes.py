import SomeClasses
from Functions import give_villian
from SomeClasses.ItemsClasses import HealingPotion, LiqPotion, ConcentreationScroll, Poison


players_dict = {}

#boss_fighting
current_boss_fight_team = {}
boss_fight_team = {}

boss_fight_is_on = False
boss_fight_is_over = False



#mob_fighting
mob_fight_dict = {}


#death
death_tasks_dict = {}

#Items
all_items = [HealingPotion, LiqPotion, ConcentreationScroll, Poison]
all_items.sort(key=lambda item: item().name)
all_items_tnames = list(map(lambda item: item().tname, all_items))
all_items_dict = {item().tname: item for item in all_items}
all_items_dict_cost = {item().name: item for item in all_items}



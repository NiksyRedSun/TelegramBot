import random
from GameClasses import Unit, Villian


def round(hero: Unit, vilian: Unit):
    text = []
    hero_init = random.randint(1, 6) + hero.initiative
    villian_init = random.randint(1, 6) + vilian.initiative
    if villian_init > hero_init:
        text.append(f"В этом раунде перехватывает инициативу и атакует {vilian.name}")
        hero_init = random.randint(1, 6) + hero.initiative
        villian_init = random.randint(1, 6) + vilian.initiative
        if villian_init > hero_init:
            damage = vilian.attack + random.randint(1, 6)
            hero.hp -= damage
            text.append(f"Его удар попадает прямо в цель, нанеся {damage} урона")
        else:
            text.append(f"Однако его удар не попадает по цели")
    else:
        text.append(f"В этом раунде перехватывает инициативу и атакует {hero.name}")
        hero_init = random.randint(1, 6) + hero.initiative
        villian_init = random.randint(1, 6) + vilian.initiative
        if hero_init > villian_init:
            damage = hero.attack + random.randint(1, 6)
            vilian.hp -= damage
            text.append(f"Его удар попадает прямо в цель, нанеся {damage} урона")
        else:
            text.append(f"Однако его удар не попадает по цели")
    return "\n".join(text)
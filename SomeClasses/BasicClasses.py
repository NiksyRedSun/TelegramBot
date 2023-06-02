import random
import asyncio
from EasyGameLoader import bot
import asyncio



def double_dices():
    return random.randint(1, 6) + random.randint(1, 6)


def dice():
    return random.randint(1, 6)


class Unit:
    def __init__(self, s_name: str, s_story: str, s_max_hp: int, s_attack: int, s_defense: int, s_initiative: int):
        self.name = s_name
        self.story = s_story
        self.hp = s_max_hp
        self.max_hp = s_max_hp
        self.attack = s_attack
        self.defense = s_defense
        self.initiative = s_initiative
        self.alive = True


    def check_alive(self):
        if self.hp <= 0:
            self.hp = 0
            self.alive = False


    def reset(self):
        self.alive = True
        self.hp = self.max_hp




class DeathCounter:
    def __init__(self, words: str):
        self.word_list = []
        word_list = list(map(lambda line: line.capitalize(), words.split()))
        for word in word_list:
            result_word = ''
            trash_list = '.,!?'
            for symbol in word:
                if symbol not in trash_list:
                    result_word += symbol
            self.word_list.append(result_word)
        self.len = len(self.word_list)
        self.cur_ind = 0
        self.good_words = 0


    def __iter__(self):
        return self


    def __next__(self):
        if self.cur_ind == self.len:
            raise StopIteration
        else:
            self.cur_ind += 1
            return self.word_list[self.cur_ind-1]


    def check_word(self, word):
        if word == self.word_list[self.cur_ind-1]:
            self.good_words += 1


    def check_words(self):
        if self.good_words > self.len/1.5:
            return True
        else:
            return False



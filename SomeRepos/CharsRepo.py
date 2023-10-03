import sqlite3
from SomeClasses.CharacterClasses import Character


char = Character("Дарриан", "Вы тут за эльфа, наемного убийцу", 20, 8, 1, 6)


con = sqlite3.connect("C:\\repos\\tg_bot\SomeRepos\Chars.db")


def get_char(id):
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM Characters WHERE id={id}")
        row = cur.fetchone()
        return Character(*row[1:])



def post_char(id: int, char: Character):
    try:
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO Characters (id, name, story, hp, attack, defense, initiative, points, money, level, exp, next_level_exp)"
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, char.name, char.story, char.max_hp, char.attack,
                                                                     char.defense, char.initiative, char.points, char.money, char.level, char.exp, char.next_level_exp))
            con.commit()
            return "Ваш персонаж успешно сохранен"
    except:
        return "Что-то пошло не так"




def put_char(id: int, char: Character):
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Characters SET name=?, story=?, hp=?, attack=?, defense=?, initiative=?, points=?, money=?, level=?, exp=?, next_level_exp=?"
                    "WHERE id=?", (char.name, char.story, char.hp, char.attack,
                                                                 char.defense, char.initiative, char.points, char.money, char.level, char.exp, char.next_level_exp, id))
        con.commit()


def delete_char(id: int):
    with con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM Characters WHERE id={id}")
        con.commit()


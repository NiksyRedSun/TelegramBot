from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey, Text, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from SomeClasses.CharacterClasses import Character



#создание декларативной базы данных
Base = declarative_base()


class Characters(Base):
    __tablename__ = "Characters"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(50))
    story = Column("story", Text)
    hp = Column("hp", Integer)
    attack = Column("attack", Integer)
    defense = Column("defense", Integer)
    initiative = Column("initiative", Integer)
    points = Column("points", Integer)
    money = Column("money", Integer)
    level = Column("level", Integer)
    exp = Column("exp", Integer)
    next_level_exp = Column("next_level_exp", Integer)


    def __init__(self, id, name, story, hp, attack, defense, initiative, points, money, level, exp, next_level_exp):
        self.id = id
        self.name = name
        self.story = story
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.initiative = initiative
        self.points = points
        self.money = money
        self.level = level
        self.exp = exp
        self.next_level_exp = next_level_exp


    def __repr__(self):
        return f"Имя персонажа:{self.name}, уровень: {self.level}"


#движок
engine = create_engine("sqlite:///C:\\repos\\tg_bot\\SomeRepos\\TgBotdb.db", echo=True)

#следующая строка берет все классы сверху, унаследованные от Base и делает из них таблицы
# Base.metadata.create_all(bind=engine)

#создание сешнемейкера
Session = sessionmaker(bind=engine)



def get_char(id):
    with Session() as session:
        try:
            char = session.query(Characters).filter(Characters.id==id).first()
            return Character(char.name, char.story, char.hp, char.attack, char.defense, char.initiative, char.points,
                             char.money, char.level, char.exp, char.next_level_exp)
        except Exception as e:
            # return "Что-то пошло не так при загрузке персонажа"
            print(e)


def post_char(id: int, char: Character):
        with Session() as session:
            try:
                char = Characters(id=id, name=char.name, story=char.story, hp=char.max_hp, attack=char.attack,
                 defense=char.defense, initiative=char.initiative, points=char.points, money=char.money, level=char.level, exp=char.exp,
                                  next_level_exp=char.next_level_exp)
                session.add(char)
                session.commit()
                return "Ваш персонаж успешно сохранен"
            except:
                session.rollback()
                return "Что-то пошло не так"


def put_char(id: int, char: Character):
    with Session() as session:
        try:
            ch = session.query(Characters).filter(Characters.id==id).first()
            ch.name = char.name
            ch.story = char.story
            ch.hp = char.max_hp
            ch.attack = char.attack
            ch.defense = char.defense
            ch.initiative = char.initiative
            ch.points = char.points
            ch.money = char.money
            ch.level = char.level
            ch.exp = char.exp
            session.commit()
            return "Ваш персонаж успешно обновлен"
        except:
            session.rollback()
            return "Что-то пошло не так"


def delete_char(id: int):
    with Session() as session:
        try:
            ch = session.query(Characters).filter(Characters.id==id).first()
            session.delete(ch)
            session.commit()
            return "Ваш персонаж успешно сохранен"
        except:
            session.rollback()
            return "Что-то пошло не так"


# print(get_char(218656239))
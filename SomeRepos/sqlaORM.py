from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey, Text, CHAR, Boolean, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import SomeClasses.CharacterClasses
import SomeClasses.StatisticsClasses




#создание декларативной базы данных
Base = declarative_base()


class Characters(Base):
    __tablename__ = "Characters"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(50))
    story = Column("story", Text)
    hp = Column("hp", Integer)
    max_hp = Column("max_hp", Integer)
    attack = Column("attack", Integer)
    defense = Column("defense", Integer)
    initiative = Column("initiative", Integer)
    points = Column("points", Integer)
    money = Column("money", Integer)
    level = Column("level", Integer)
    exp = Column("exp", Integer)
    next_level_exp = Column("next_level_exp", Integer)
    autosave = Column("autosave", Boolean)
    items_available = Column("items_available", Integer)
    user_id = Column("user_id", Integer, nullable=True)


    def __init__(self, id, name, story, hp, max_hp, attack, defense, initiative, points, money, level, exp, next_level_exp, autosave):
        self.id = id
        self.name = name
        self.story = story
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.initiative = initiative
        self.points = points
        self.money = money
        self.level = level
        self.exp = exp
        self.next_level_exp = next_level_exp
        self.autosave = autosave


    def __repr__(self):
        return f"Имя персонажа:{self.name}, уровень: {self.level}"



class Statistics(Base):
    __tablename__ = "Statistics"


    id = Column("id", Integer, primary_key=True)
    mobKill = Column("mobKill", Integer)
    bossKill = Column("bossKill", Integer)
    death = Column("death", Integer)
    itemsUsed = Column("itemsUsed", Integer)
    moneySpend = Column("moneySpend", Integer)
    fountainHealing = Column("fountainHealing", Integer)
    hits = Column("hits", Integer)
    criticalHits = Column("criticalHits", Integer)
    successAvoiding = Column("successAvoiding", Integer)
    leavingBossFights = Column("leavingBossFights", Integer)
    leavingMobFights = Column("leavingMobFights", Integer)
    char_id = Column("char_id", Integer, ForeignKey("Characters.id"), nullable=True)



    def __init__(self, mobKill, bossKill, death, itemsUsed, moneySpend, fountainHealing, hits, criticalHits,
                 successAvoiding, leavingBossFights, leavingMobFights, char_id):
        self.mobKill = mobKill
        self.bossKill = bossKill
        self.death = death
        self.itemsUsed = itemsUsed
        self.moneySpend = moneySpend
        self.fountainHealing = fountainHealing
        self.hits = hits
        self.criticalHits = criticalHits
        self.successAvoiding = successAvoiding
        self.leavingBossFights = leavingBossFights
        self.leavingMobFights = leavingMobFights
        self.char_id = char_id


    def __repr__(self):
        return f"Stat id: {self.id}, char id: {self.char_id}"




class Items(Base):
    __tablename__ = "Items"


    id = Column("id", Integer, primary_key=True)
    itemName = Column("itemName", String(50))
    itemMaxHp = Column("itemMaxHp", Integer)
    itemAttack = Column("itemAttack", Integer)
    itemDefense = Column("itemDefense", Integer)
    itemInitiative = Column("itemInitiative", Integer)
    forAttack = Column("forAttack", Boolean)
    char_id = Column("char_id", Integer, ForeignKey("Characters.id"), nullable=True)


    def __init__(self, itemName, itemMaxHp, itemAttack, itemDefense, itemInitiative, forAttack, char_id):
        self.itemName = itemName
        self.itemMaxHp = itemMaxHp
        self.itemAttack = itemAttack
        self.itemDefense = itemDefense
        self.itemInitiative = itemInitiative
        self.forAttack = forAttack
        self.char_id = char_id


    def __repr__(self):
        return f"Stat id: {self.id}, char id: {self.char_id}"




#движок
# engine = create_engine("sqlite:///C:\\repos\\tg_bot\\SomeRepos\\TgBotdb.db", echo=True)
engine = create_engine("sqlite:///C:\\repos\\AutoBlog\\instance\\blog.db", echo=True)

#следующая строка берет все классы сверху, унаследованные от Base и делает из них таблицы
# Base.metadata.create_all(bind=engine)

#создание сешнемейкера
Session = sessionmaker(bind=engine)



def get_items(char_id):
    with Session() as session:
        try:
            its = session.query(Items).filter(Items.char_id == char_id).all()
            return its
        except:
            return "Что-то пошло не так при загрузке вещей"



def get_char(id):
    with Session() as session:
        try:
            char = session.query(Characters).filter(Characters.id==id).first()
            return SomeClasses.CharacterClasses.Character(char.name, char.story, char.max_hp, char.max_hp, char.attack, char.defense, char.initiative, char.points,
                                                          char.money, char.level, char.exp, char.next_level_exp, char.autosave)
        except:
            return "Что-то пошло не так при загрузке персонажа"



def post_char(id: int, char):
        char.remove_effects()
        with Session() as session:
            try:
                char = Characters(id=id, name=char.name, story=char.story, hp=char.max_hp, max_hp=char.max_hp, attack=char.attack,
                                  defense=char.defense, initiative=char.initiative, points=char.points, money=char.money, level=char.level, exp=char.exp,
                                  next_level_exp=char.next_level_exp, autosave=char.autosave)
                session.add(char)
                session.commit()
                return "Ваш персонаж успешно сохранен"
            except:
                session.rollback()
                return "Что-то пошло не так"


def put_char(id: int, char):
    char.remove_effects()
    with Session() as session:
        try:
            ch = session.query(Characters).filter(Characters.id==id).first()
            ch.name = char.name
            ch.story = char.story
            ch.hp = char.max_hp
            ch.max_hp = char.max_hp
            ch.attack = char.attack
            ch.defense = char.defense
            ch.initiative = char.initiative
            ch.points = char.points
            ch.money = char.money
            ch.level = char.level
            ch.exp = char.exp
            ch.autosave = char.autosave
            session.commit()
            return "Ваш персонаж успешно обновлен"
        except:
            session.rollback()
            return "Что-то пошло не так при обновлении статистики"


def delete_char(id: int):
    with Session() as session:
        try:
            ch = session.query(Characters).filter(Characters.id==id).first()
            session.delete(ch)
            session.commit()
            return "Ваш персонаж успешно удален"
        except:
            session.rollback()
            return "Что-то пошло не так"



def get_stat(id):
    with Session() as session:
        try:
            stat = session.query(Statistics).filter(Statistics.char_id==id).first()
            if not stat:
                print("Статистика не обнаружена")
                return False
            return stat
        except:
            return "Что-то пошло не так при загрузке статистики"



def post_stat(id: int, stat):
    with Session() as session:
        try:
            dbStat = Statistics(mobKill=stat.mobKill, bossKill=stat.bossKill, death=stat.death,
                            itemsUsed=stat.itemsUsed, moneySpend=stat.moneySpend, fountainHealing=stat.fountainHealing,
                            hits=stat.hits, criticalHits=stat.criticalHits, successAvoiding=stat.successAvoiding,
                              leavingBossFights=stat.leavingBossFights, leavingMobFights=stat.leavingMobFights, char_id=id)

            session.add(dbStat)
            session.commit()
            return "Статистика успешно сохранена"
        except Exception as e:
            print(e)
            session.rollback()
            return "Что-то пошло не так при сохранении статистики"



def put_stat(id: int, gamestat):
    with Session() as session:
        try:
            bdstat = session.query(Statistics).filter(Statistics.char_id==id).first()
            bdstat.mobKill += gamestat.mobKill
            bdstat.bossKill += gamestat.bossKill
            bdstat.death += gamestat.death
            bdstat.itemsUsed += gamestat.itemsUsed
            bdstat.moneySpend += gamestat.moneySpend
            bdstat.fountainHealing += gamestat.fountainHealing
            bdstat.hits += gamestat.hits
            bdstat.criticalHits += gamestat.criticalHits
            bdstat.successAvoiding += gamestat.successAvoiding
            bdstat.leavingBossFights += gamestat.leavingBossFights
            bdstat.leavingMobFights += gamestat.leavingMobFights
            session.commit()
            return "Статистика успешно обновлена"
        except Exception as e:
            print(e)
            session.rollback()
            return "Что-то пошло не так при обновлении статистики"

def delete_stat(id: int):
    with Session() as session:
        try:
            st = session.query(Statistics).filter(Statistics.char_id==id).first()
            session.delete(st)
            session.commit()
            return "Ваша статистика успешно удалена"
        except:
            session.rollback()
            return "Что-то пошло не так"



# print(get_char(218656239))

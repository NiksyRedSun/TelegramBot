from SomeClasses.CharacterClasses import Character
from SomeAttributes import players_dict
import asyncio






async def five_second_healing(players: dict):
    while True:
        if players:
            for player in players:
                if players[player] is None or not players[player].alive:
                    continue
                else:
                    players[player].five_second_healing()
        await asyncio.sleep(5)




async def all_fury_down(players: dict):
    while True:
        if players:
            for player in players:
                if players[player] is None or not players[player].alive:
                    continue
                else:
                    players[player].fury_down()
        await asyncio.sleep(1)


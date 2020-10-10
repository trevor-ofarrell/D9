import os
import discord
import json
import random
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

triv = []
reacted = []

async def play_trivia(new_msg, ctx, bot, users):
    with open("trivia_questions.json", 'r') as f:
        trivia = json.load(f)
    data = trivia['items']
    random.shuffle(data)
    flag = 0
    winners = {}
    for item in data:
        q = item['q']
        a = item['a']
        if flag < 1:
            flag += 1
            await new_msg.edit(content=q)
            global triv, reacted
            triv = a
            reacted = users
            msg = await bot.wait_for('message', check=check)
            if msg:
                await msg.add_reaction("\N{SPORTS MEDAL}")
                await ctx.send(str(msg.author.name) + "wins this one!")
                winner = msg.author.name
                try:
                    if winners[winner]:
                        winners[winner] += 1
                except KeyError:
                    winners.update({winner : 1})

            await asyncio.sleep(2)
        else:
            flag += 1
            await ctx.send(q)
            triv = a
            msg = await bot.wait_for('message', check=check)
            if msg:
                await msg.add_reaction("\N{SPORTS MEDAL}")
                await ctx.send(str(msg.author.name) + "wins this one!")
            winner = msg.author.name
            if winners[msg.author.name]:
                winners[msg.author.name] += 1
            else:
                winners.update({winner : 1})
            await asyncio.sleep(2)
    
    champ = max(winners, key= lambda x: winners[x])
    await ctx.send(str(champ) + "Wins the Game! Congrats! :trophy:")


def check(message):
    content = message.content.lower()
    if message.author in reacted:
        if content in triv: 
            return True
        else:
            return False

async def start_quiz(ctx, cache_msg, bot):
    for reaction in cache_msg.reactions:
            async for user in reaction.users():
                users = []
                users.append(user)
    new_msg = await ctx.send(":books: :books: :books: :books: :books: :books: :books: :books: :books: :books:")
    await asyncio.sleep(1)
    await new_msg.edit(content=":books: :books: :books: :books: :books: :books: :books: :books: :books:")
    await asyncio.sleep(1)
    await new_msg.edit(content=":books: :books: :books: :books: :books: :books: :books: :books:")
    await asyncio.sleep(1)
    await new_msg.edit(content=":books: :books: :books: :books: :books: :books: :books:")
    await asyncio.sleep(1)
    await new_msg.edit(content=":books: :books: :books: :books: :books: :books:")
    await asyncio.sleep(1)
    await new_msg.edit(content=":books: :books: :books: :books: :books:")
    await asyncio.sleep(1)
    await new_msg.edit(content=":books: :books: :books: :books:")
    await asyncio.sleep(1)
    await new_msg.edit(content=":books: :books: :books:")
    await asyncio.sleep(1)
    await new_msg.edit(content=":books: :books:")
    await asyncio.sleep(1)
    await new_msg.edit(content=":books:")
    await asyncio.sleep(1)
    await new_msg.edit(content=":confetti_ball: Game Starting!! :confetti_ball:")
    await asyncio.sleep(1)
    await play_trivia(new_msg, ctx, bot, users)
    
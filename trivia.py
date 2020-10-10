import os
import discord
import json
import random
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

global triv
triv = set([])

async def play_trivia(new_msg, ctx):
    with open("trivia_questions.json", 'r') as f:
        trivia = json.load(f)
    data = trivia['items']
    random.shuffle(data)
    for item in data:
        for key in item:
            k = item[key]
            v = item.values()
            flag = 0
            if flag == 0:
                await new_msg.edit(content=v)
                triv += v
                msg = await bot.wait_for('message', check=check)
                if msg:
                    await msg.add_reaction('✅')
                    await ctx.send(str(msg.author.name) + "wins this one")
                await asyncio.sleep(2)
                flag += 1
            else:
                await ctx.send(k)
                triv += v
                msg = await bot.wait_for('message', check=check)
                if msg:
                    await msg.add_reaction('✅')
                    await ctx.send(str(msg.author.name) + "wins this one")
                await asyncio.sleep(2)
                flag += 1

def obama_check(message):
    obama = ['Barack Obama', 'barack obama']
    content = message.content.lower()
    return any(t in content for t in obama)

def check(message):
    content = message.content.lower()
    return any(t in content for t in trivia)

async def quiz(ctx, cache_msg, bot):
    for reaction in cache_msg.reactions:
            async for user in reaction.users():
                users = []
                users.append(user)
    new_msg = await ctx.send(":books: :books: :books: :books: :books: :books: :books: :books: :books:")
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
    await play_trivia(new_msg, ctx)
    
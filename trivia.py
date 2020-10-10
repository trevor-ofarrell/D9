import os
import discord
import json
import random
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

triv = []

async def play_trivia(new_msg, ctx, bot):
    with open("trivia_questions.json", 'r') as f:
        trivia = json.load(f)
    data = trivia['items']
    random.shuffle(data)
    for item in data:
        flag = 0
        for key in item:
            q = item['q']
            a = item['a']
            if flag < 1:
                flag += 1
                await new_msg.edit(content=q)
                global triv
                triv = a
                msg = await bot.wait_for('message', check=check)
                if msg:
                    await msg.add_reaction('✅')
                    await ctx.send(str(msg.author.name) + "wins this one")
                await asyncio.sleep(2)
            else:
                flag += 1
                await ctx.send(q)
                triv = a
                msg = await bot.wait_for('message', check=check)
                if msg:
                    await msg.add_reaction('✅')
                    await ctx.send(str(msg.author.name) + "wins this one!!")
                await asyncio.sleep(2)

def obama_check(message):
    obama = ['Barack Obama', 'barack obama']
    content = message.content.lower()
    return any(t in content for t in obama)

def check(message):
    content = message.content.lower()
    return any(t in content for t in triv)

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
    await play_trivia(new_msg, ctx, bot)
    
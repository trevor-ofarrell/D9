import os
import discord
import json
import random
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import requests
import pprint
from parser import parser
from w3lib.html import replace_entities

triv = []
triv_str = ""
reacted = []

def get_trivia():
    r = requests.get('https://opentdb.com/api.php?amount=10')
    with open("trivia_questions.json", 'r') as f:
        trivia = json.load(f)
    qs = trivia["items"]
    new_list = r.json()['results']
    ret = new_list + random.sample(qs, 10)
    random.shuffle(ret)
    print(ret, flush=True)
    return ret

async def play_trivia(new_msg, ctx, bot, users):
    global triv, reacted, triv_str
    data = get_trivia()
    random.shuffle(data)
    flag = 0
    winners = {}
    for item in data:
        if flag < 1:
            try:
                if item['type']:
                    q = item['question']
                    a = item['correct_answer']
                    ia = item['incorrect_answers']
                    cat = item["type"]
                    if cat == "multiple":
                        flag += 1
                        processed_question = replace_entities(q)
                        await new_msg.edit(content=processed_question)
                        ia += [a]
                        random.shuffle(ia)
                        em = discord.Embed(title = 'Multiple Choice! Type one answer in chat!', color=discord.Color.green())
                        em.add_field(name="Answers:", value="1) {} 2) {} 3) {} 4) {}".format(ia[0], ia[1], ia[2], ia[3]))
                        await ctx.send(embed=em)
                        triv_str = a.lower()
                        reacted = users
                        msg = await bot.wait_for('message', check=check_str)
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
                    elif cat == "boolean":
                        flag += 1
                        processed_question = replace_entities(q)
                        await new_msg.edit(content=processed_question)
                        em = discord.Embed(title = 'True or false! type your selection in the chat!', color=discord.Color.green())
                        await ctx.send(embed=em)
                        triv_str = a.lower()
                        print(triv_str, flush=True)
                        msg = await bot.wait_for('message', check=check_str)
                        print("waiting.......", flush=True)
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
            except KeyError:
                q = item['q']
                a = item['a']
                flag += 1
                await new_msg.edit(content=q)
                reacted = users
                triv = [x.lower() for x in a]
                print(triv, flush=True)
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
            try:
                if item['type']:
                    q = item['question']
                    a = item['correct_answer']
                    ia = item['incorrect_answers']
                    cat = item["type"]
                    if cat == "multiple":
                        flag += 1
                        processed_question = replace_entities(q)
                        await ctx.send(processed_question)
                        ia += [a]
                        random.shuffle(ia)
                        em = discord.Embed(title = 'Multiple Choice! Type one answer in chat!', color=discord.Color.green())
                        em.add_field(name="Answers:", value="1) {} 2) {} 3) {} 4) {}".format(ia[0], ia[1], ia[2], ia[3]))
                        await ctx.send(embed=em)
                        triv_str = a.lower()
                        reacted = users
                        print(triv_str, flush=True)
                        msg = await bot.wait_for('message', check=check_str)
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
                    elif cat == "boolean":
                        flag += 1
                        processed_question = replace_entities(q)
                        await ctx.send(processed_question)
                        em = discord.Embed(title = 'True or false! type your selection in the chat!', color=discord.Color.green())
                        await ctx.send(embed=em)
                        triv_str = a.lower()
                        print(triv_str, flush=True)
                        msg = await bot.wait_for('message', check=check_str)
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
            except KeyError:
                q = item['q']
                a = item['a']
                flag += 1
                await ctx.send(q)
                reacted = users
                triv = [x.lower() for x in a]
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
        print(triv, flush=True)
        if content in triv: 
            return True
        elif content == triv[0]:
            print(triv, flush=True)
            return True
        return False

def check_str(message):
    content = message.content.lower()
    if message.author in reacted:
        print(triv_str, flush=True)
        if content == triv_str:
            print(triv, flush=True)
            return True
        else:
            return False

async def start_quiz(ctx, cache_msg, bot):
    for reaction in cache_msg.reactions:
            async for user in reaction.users():
                users = []
                users.append(user)
    print(users, flush=True)
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
    
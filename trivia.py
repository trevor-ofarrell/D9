import os
import discord
import json
import random
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import requests
import pprint
from w3lib.html import replace_entities

triv_str = ""
triv = []
reacted = []
multi_choice = []
submited = []

def get_trivia():
    r = requests.get('https://opentdb.com/api.php?amount=18')

    with open("trivia_questions.json", 'r') as f:
        trivia = json.load(f)

    qs = trivia["items"]
    new_list = r.json()['results']
    ret = new_list + random.sample(qs, 2)
    random.shuffle(ret)
    print(ret, flush=True)
    return ret

async def play_trivia(new_msg, ctx, bot, users):

    global triv, reacted, triv_str, multi_choice, submited
    reacted = users
    data = get_trivia()
    random.shuffle(data)
    winners = {}

    for item in data:
        msg = None
        submited = []
        try:
            if item['type']:
                q = item['question']
                a = item['correct_answer']
                ia = item['incorrect_answers']
                cat = item["type"]
                if cat == "multiple":
                    triv = []
                    ia += [a]
                    random.shuffle(ia)
                    processed_question = replace_entities(q)

                    em = discord.Embed(title = processed_question, color=discord.Color.green())
                    em.add_field(
                        name="Multiple Choice! Type one answer in chat!",
                        value="Answers: 1) {} 2) {} 3) {} 4) {}".format(
                            replace_entities(ia[0]),
                            replace_entities(ia[1]),
                            replace_entities(ia[2]),
                            replace_entities(ia[3])
                    ))

                    multi_choice = [
                        {"1" : replace_entities(ia[0])},
                        {"2" : replace_entities(ia[1])},
                        {"3" : replace_entities(ia[2])},
                        {"4" : replace_entities(ia[3])}
                    ]

                    await ctx.send(embed=em)
                    triv.append(replace_entities(a.lower()))

                    for item in multi_choice:
                        ans = list(item.values())[0]
                        if ans.lower() == replace_entities(a.lower()):
                            triv.append(list(item.keys())[0])
                    print(triv, flush=True)

                    try:
                        msg = await bot.wait_for('message', check=check, timeout=16.0)
                        submited.append(msg.author.name)
                    except asyncio.TimeoutError:
                        await ctx.send("Time's up!")

                    try:
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

                    except UnboundLocalError:
                        pass

                elif cat == "boolean":
                    processed_question = replace_entities(q)
                    em = discord.Embed(title = processed_question, color=discord.Color.green())
                    em.add_field(name = 'True or false! type your selection in the chat!', value='** **')
                    await ctx.send(embed=em)

                    triv_str = a.lower()
                    print(triv_str, flush=True)

                    try:
                        msg = await bot.wait_for('message', check=check_str, timeout=16.0)
                    except asyncio.TimeoutError:
                        await ctx.send("Time's up!")

                    try:
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

                    except UnboundLocalError:
                        pass

        except KeyError:
            q = item['q']
            a = item['a']
            triv = [x.lower() for x in a]
            print(triv, flush=True)

            em = discord.Embed(title = q, color=discord.Color.green())
            em.add_field(
                name='Uh oh! No list of answers this time! type your answer in the chat!',
                value='** **'
            )
            await ctx.send(embed=em)

            try:
                msg = await bot.wait_for('message', check=check, timeout=16.0)
            except asyncio.TimeoutError:
                await ctx.send("Time's up!")
            
            try:
                if msg:
                    await msg.add_reaction("\N{SPORTS MEDAL}")
                    await ctx.send(str(msg.author.name) + " wins this one!")
                    winner = msg.author.name
                    try:
                        if winners[winner]:
                            winners[winner] += 1
                    except KeyError:
                        winners.update({winner : 1})
                await asyncio.sleep(2)

            except UnboundLocalError:
                pass

    try:
        high = max(map(lambda x: winners[x], winners))
        result = [k for k,v in winners.items() if v == high]
        print(result, flush=True)

        if len(result) == 1:
            result = result[0]        
            await ctx.send(str(result) + " Wins the Game! Congrats! :trophy:")
        else:
            await ctx.send(', '.join([str(elem) for elem in result]) + " Tied! Congrats! :trophy:")
    except ValueError:
        await ctx.send("No one wins! boooo")

def check(message):
    content = message.content.lower()
    if message.author in reacted:
        if message.author.name not in submited:
            submited.append(message.author.name)
            if content in triv: 
                return True
            elif content == triv[0]:
                return True
            return False
        return False

def check_str(message):
    content = message.content.lower()
    if message.author in reacted:
        if message.author.name not in submited:
            submited.append(message.author.name)
            if content == triv_str:
                return True
            else:
                return False
        return False

async def start_quiz(ctx, cache_msg, bot):

    new_msg = await ctx.send(":books: :books: :books: :books: :books: :books: :books:", delete_after=20)
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

    users = []
    channel = cache_msg.channel
    updated_msg = await channel.fetch_message(cache_msg.id)

    for reaction in updated_msg.reactions:
        async for user in reaction.users():
            users.append(user)

    print(users, flush=True)
    await new_msg.edit(content=":confetti_ball: Game Starting!! :confetti_ball:")
    await asyncio.sleep(1)
    await play_trivia(new_msg, ctx, bot, users)
    
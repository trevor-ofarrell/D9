# bot.py
import os

import discord

import json

from dotenv import load_dotenv

import random

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

bot = commands.Bot(command_prefix='d9 !')

@bot.command()
async def echo(ctx, *args):
    await ctx.send('{}'.format(' '.join(args)))

@bot.command()
async def greet(ctx, members: commands.Greedy[discord.Member]):
    wonderful_people = ", ".join(x.name for x in members)
    await ctx.send('Greetings dearest {} I wish you a wonderful day!'.format(wonderful_people))

@bot.command()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    slapped = ", ".join(x.name for x in members)
    await ctx.send('{} just got slapped for {}'.format(slapped, reason))   

@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = [
        "Not today mf",
        "Sure!",
        "forget about it",
        "not in a million years",
        "most likley, yes",
        "you wouldn't belive me if I told you",
        "Hmmmm, ask Milly",
        "Shane knows",
        "Eric is paying me to withhold this information",
        "I dont wanna talk",
        "drainer knows the answer",
        "Follow you heart",
    ]
    await ctx.send(f'{random.choice(responses)}') 

@bot.command()
async def flipcoin(ctx):
    flip = random.choice(['heads', 'tails'])
    await ctx.send(flip)

@bot.command()
async def balance(ctx):
    await account(ctx.author)
    user = ctx.author
    users = await get_eco_data()
    wallet_amt = 0
    wallet_amt = users[str(user.id)]["wallet"]
    em = discord.Embed(title = f"{ctx.author.name}'s balance", color=discord.Color.red())
    em.add_field(name="Wallet balance", value=wallet_amt)

    await ctx.send(embed=em)

"""@bot.command()
async def send(ctx, members: commands.Greedy[discord.Member]):
    await account(ctx.author)
    users = await get_eco_data()
    wallet_amt = users[str(user.id)]["wallet"]"""

@bot.command()
async def beg(ctx):
    await account(ctx.author)
    users = await get_eco_data()
    user = ctx.author
    earnings = random.randrange(10)
    await ctx.send(f"Someone gave you {earnings} d9's!!!! WOooooaoOoHhhhhwwWAAAaaaaaa")
    users[str(user.id)]["wallet"] += earnings
    with open("usereconomydata.json", "w") as f:
        json.dump(users, f)   

@bot.command()
async def gamble(ctx, arg=1):
    users = await get_eco_data()
    user = ctx.author
    flip = random.choice(['win', 'loose'])
    if flip == 'win':
        users[str(user.id)]["wallet"] += int(arg)
        with open("usereconomydata.json", "w") as f:
            json.dump(users, f)
        em = discord.Embed(title = f"{ctx.author.name} won {arg} d9's!!!", color=discord.Color.green())
        await ctx.send(embed=em)

    else:
        users[str(user.id)]["wallet"] -= int(arg)
        with open("usereconomydata.json", "w") as f:
            json.dump(users, f)
        em = discord.Embed(title = f"{ctx.author.name} lost {arg} d9's :'(", color=discord.Color.green())
        await ctx.send(embed=em)
        await ctx.send(f"f")

    return True



async def account(user):

    users = await get_eco_data()

    if str(user.id) in users:
        return False

    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 100

    with open("usereconomydata.json", 'w') as f:
        json.dump(users, f)
    return True

async def get_eco_data():
    with open("usereconomydata.json", 'r') as f:
        users = json.load(f)
    return users

bot.run(TOKEN)


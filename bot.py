# bot.py
import os
import discord
import json
from dotenv import load_dotenv
import random
from discord.ext import commands
import giphy_client
from discord.ext.commands import Bot
from giphy_client.rest import ApiException

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GIF_TOKEN = os.getenv('GIFY_TOKEN') 

client = discord.Client()

bot = commands.Bot(command_prefix=['d9 !', 'D9 !'])

api_instance = giphy_client.DefaultApi()

@bot.command()
async def echo(ctx, *args):
    await ctx.send('{}'.format(' '.join(args)))

@bot.command()
async def greet(ctx, members: commands.Greedy[discord.Member]):
    wonderful_people = ", ".join(x.name for x in members)
    await ctx.send('Greetings dearest {} I wish you a wonderful day!'.format(wonderful_people))

@bot.command()
async def gif(ctx, arg):
    if not arg:
            await ctx.send('You must specify an argument!')
    gify = await search_gifs(arg)
    await ctx.send(gify)

@bot.command()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    slapped = ", ".join(x.name for x in members)
    slap_urls = [
        "https://media.giphy.com/media/l3YSimA8CV1k41b1u/giphy.gif",
        "https://media.giphy.com/media/RrLbvyvatbi36/giphy.gif",
        "https://media.giphy.com/media/lX03hULhgCYQ8/giphy.gif",
        "https://media.giphy.com/media/Qvwc79OfQOa4g/giphy.gif",
        "https://media.giphy.com/media/Qs0I2VdbIqNkk/giphy.gif",
    ]
    this_slap = random.choices(slap_urls)
    em = discord.Embed(title = '{} just got slapped for {}'.format(slapped, reason), color=discord.Color.red())
    em.set_image(url=this_slap[0])
    await ctx.send(embed=em)

@bot.command()
async def hug(ctx, members: commands.Greedy[discord.Member]):
    hugged = ", ".join(x.name for x in members)
    hug_urls = [
        "https://media.giphy.com/media/EvYHHSntaIl5m/giphy.gif",
        "https://media.giphy.com/media/ZBQhoZC0nqknSviPqT/giphy.gif",
        "https://media.giphy.com/media/gnXG2hODaCOru/giphy.gif",
        "https://media.giphy.com/media/16bJmyPvRbCDu/giphy.gif",
        "https://media.giphy.com/media/VbawWIGNtKYwOFXF7U/giphy.gif",
        "https://media.giphy.com/media/VduFvPwm3gfGO8duNN/giphy.gif",
        "https://media.giphy.com/media/l41lSTVB8eei3U3hC/giphy.gif",
        "https://media.giphy.com/media/hpQcDH5EfJRwxm03Uh/giphy.gif",
    ]
    this_hug = random.choices(hug_urls)
    em = discord.Embed(title = '{} hugs {}! <3 '.format(ctx.author.name, hugged), color=discord.Color.dark_purple())
    em.set_image(url=this_hug[0])
    await ctx.send(embed=em)   

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
        'Without a doubt.', 
        'Outlook good.', 
        'Better not tell you now.', 
        'Cannot predict now.',
        'My reply is no.', 
        'Outlook not so good.',
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
    em = discord.Embed(title = f"{ctx.author.name}'s balance", color=discord.Color.green())
    em.add_field(name="Wallet balance", value=wallet_amt)

    await ctx.send(embed=em)

@bot.command()
async def send(ctx, members: commands.Greedy[discord.Member], amount=1):
    send_to = ", ".join(x.name for x in members)
    await account(ctx.author)
    users = await get_eco_data()
    user = ctx.author
    if amount > users[str(user.id)]["wallet"]:
        wallet_amt = users[str(user.id)]["wallet"]
        await ctx.send('Sorry, you only have {} d9\'s :\'('.format(wallet_amt))
    else:
        await ctx.send(f"You sent {send_to} {amount} d9's!!")
        users[str(user.id)]["wallet"] -= amount
        try:
            users[str(members[0].id)]["wallet"] += amount
       except KeyError:
          with open("usereconomydata.json", "w") as f:
              json.dump({str(members[0].id):{"wallet": 100}}, f)
    return True

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

    if arg > users[str(user.id)]["wallet"]:
        wallet_amt = users[str(user.id)]["wallet"]
        await ctx.send('Sorry, you only have {} d9\'s :\'('.format(wallet_amt))
    else:
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
            em = discord.Embed(title = f"{ctx.author.name} lost {arg} d9's :'(", color=discord.Color.red())
            await ctx.send(embed=em)
            await ctx.send(f"f")

    return True

async def search_gifs(query):
    try:
        response = api_instance.gifs_search_get(GIF_TOKEN, query, limit=15, rating='r')
        lst = list(response.data)
        gif = random.choices(lst)

        return gif[0].url

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

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


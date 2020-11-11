# bot.py
import os
import discord
import json
from dotenv import load_dotenv
import random
from discord.ext import commands
import giphy_client
from discord.ext.commands import Bot
import asyncio
from giphy_client.rest import ApiException
from trivia import start_quiz
from cogs.Admin import Admin
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GIF_TOKEN = os.getenv('GIFY_TOKEN') 
BOT_OWNER_ID = os.getenv('OWNER')

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=['d9 ', 'D9 ', 'd9', 'D9', 'd9 !', 'D9 !', 'd9 $', 'D9 $'], intents=intents, help_command=None)

bot.add_cog(Admin(bot, BOT_OWNER_ID))

api_instance = giphy_client.DefaultApi()

messages = joined = 0

owner_id = BOT_OWNER_ID

async def update_stats():
    await bot.wait_until_ready()
    global messages, joined

    while not bot.is_closed():
        try:
            with open('logs.txt', 'a') as f:
                f.write(f"Time: {int(time.time())}, messages: {messages}, members joined: {joined}\n")
            messages = 0
            joined = 0

            await asyncio.sleep(6.0)
        except Exception as e:
            print(e, flush=True)

@bot.event
async def on_message(message):
    banned_terms = []
    if any(banned_word in message.content for banned_word in banned_terms):
        await message.channel.send("No swearing" + message.author.name)
        await message.delete()
    if message.content.lower() == "d9 help":
        em = discord.Embed(title = 'Command list', color=discord.Color.green())
        em.add_field(name="Actions", value="Commands:\n \a - greet\n \a - hug\n \a - slap\n Usage:\n \a - d9 <command> <@user>", inline = False)
        em.add_field(name="Probability", value="Commands:\n \a - gamble\n \a - flipcoin\n Usage:\n \a - d9 gamble <amount>\n \a - d9 flipcoin", inline = False)
        em.add_field(name="Fun", value="8ball", inline = False)
        em.add_field(name="Economy", value="Commands:\n \a - balance\n \a - beg\n \a - send\n Usage:\n \a - d9 <command>\n \a - d9 send <@user> <amount>", inline = False)
        em.add_field(name="Gifs", value="Commands:\n \a - gif\n Usage:\n \a - d9 !gif <word>", inline = False)
        em.add_field(
            name="Admin/Owner only",
            value="Commands:\n \a - ban\n \a - unban\n \a - add_role\n \a - remove_role\n Usage:\n \a - d9 ban <@user>\n \a - d9 unban <user id>\n \a - d9 add_role/remove_role <@user> <role>"
        )
        await message.channel.send(content=None, embed=em)
    await bot.process_commands(message)


async def get_msg(channel, msgID: int):
    msg = await channel.fetch_message(msgID)
    return(msg)

@bot.command()
async def delete_msg(ctx, arg):
    print(arg, flush=True)
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == int(owner_id):
        msg = await get_msg(ctx.message.channel, arg)
        print(ctx.message.channel, flush=True)
        await msg.delete()
    else:
        return 1

@bot.event
async def on_member_join(member):
    global joined
    joined += 1
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'Enjoy your stay {member.mention}!')

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                'Hello there! Thanks for having me on your server! \nFeel free to put me to work.\nYou can get a list of my commands by typing `d9 help` either in chat or in PM.\n'
            )
        break

@bot.command()
async def get(ctx):
    mb_list = []
    with open('users.txt','w') as f:
        async for member in ctx.guild.fetch_members(limit=None):
            print("{},{}".format(member,member.id), file=f,)
            mb_list.append(member)
    print("done")
    return mb_list
    #await ctx.send(l, delete_after=10)

@bot.command()
async def quiz(ctx):
    embed = discord.Embed(title = f"Trivia! :nerd:", color=discord.Color.green())
    embed.add_field(
        name="Join the Game!",
        value="Add reaction to play. The quickest to answer wins the point, and the most points wins the round!"
    )
    embed.set_image(url="https://media.giphy.com/media/3ohs7Xldjh7DndQnBu/giphy.gif")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('✅')
    await asyncio.sleep(5)
    users = []
    cache_msg = discord.utils.get(bot.cached_messages, id=msg.id)
    await start_quiz(ctx, cache_msg, bot)

@bot.command()
async def notify(ctx, member: discord.Member):
    channel = ctx.message.channel
    i = 0
    while i <= 10:
        i += 1
        await ctx.send("{}".format(member.mention))
        await asyncio.sleep(5)
    return True


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
async def send(ctx, member: discord.Member, amount=1):
    await account(ctx.author)
    users = await get_eco_data()
    user = ctx.author
    if amount > users[str(user.id)]["wallet"]:
        wallet_amt = users[str(user.id)]["wallet"]
        await ctx.send('Sorry, you only have {} d9 buck\'s :\'('.format(wallet_amt))
    else:
        await ctx.send(f"You sent {member.name} {amount} d9 buck's!!")
        users[str(user.id)]["wallet"] -= amount
        try:
          users[str(member.id)]["wallet"] += amount
        except KeyError:
          users[str(member.id)] = {"wallet" : amount, "name": member.name}
          with open("usereconomydata.json", "w") as f:
            json.dump(users, f)
        
        with open("usereconomydata.json", "w") as f:
          json.dump(users, f)
       
    return True

@bot.command()
async def send_all(ctx, amount=100):

    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == int(BOT_OWNER_ID):
        members = await get(ctx)
        users = await get_eco_data()

        for member in members:

            if str(member.id) in users:
                users[str(member.id)]["wallet"] += amount

            else:
                users[str(member.id)] = {"wallet" : amount, "name": member.name}

            with open("usereconomydata.json", "w") as f:
                json.dump(users, f)

        await ctx.send("you added " + str(amount) + " d9 buck's to everyone's wallet!")

    else:
        await ctx.send("you don't have permission to use this command")

@bot.command()
async def beg(ctx):
    await account(ctx.author)
    users = await get_eco_data()
    user = ctx.author
    earnings = random.randrange(10)
    await ctx.send(
        f"Someone gave you {earnings} d9 buck's!!!! Woaahhh"
    )
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
        await ctx.send('Sorry, you only have {} d9 buck\'s :\'('.format(wallet_amt))

    else:
        if flip == 'win':
            users[str(user.id)]["wallet"] += int(arg)

            with open("usereconomydata.json", "w") as f:
                json.dump(users, f)

            em = discord.Embed(title=f"{ctx.author.name} won {arg} d9 buck's!!!", color=discord.Color.green())
            await ctx.send(embed=em)

        else:
            users[str(user.id)]["wallet"] -= int(arg)

            with open("usereconomydata.json", "w") as f:
                json.dump(users, f)

            em = discord.Embed(title=f"{ctx.author.name} lost {arg} d9 buck's :'(", color=discord.Color.red())
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

bot.loop.create_task(update_stats())
bot.run(TOKEN)


"""@bot.command()
async def help(ctx):
    em = discord.Embed(title = 'Command list', color=discord.Color.green())
    em.add_field(name="Actions", value="greet, hug, slap - Usage: d9 !<command> <@username>")
    em.add_field(name="Gamble", value="Usage: d9 !gamble 100")
    em.add_field(name="Flip a coin", value="Usage: d9 !flipcoin")
    em.add_field(name="Fun", value="8ball")
    em.add_field(name="Economy", value="balance, send")
    em.add_field(name="Gifs", value="Usage: d9 !gif <whatever you want a gif of>")"""
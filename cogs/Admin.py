import discord
import json
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

class Admin(commands.Cog):

    def __init__(self, bot, owner_id):
        self.bot = bot
        self._last_member = None
        self.owner_id = owner_id

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))
    
    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == int(self.owner_id):
            await member.ban(reason=reason)
            await ctx.send(member.name + " has been banned")
            return True
        await ctx.send("You dont have permission to use this command.")

    @commands.command()
    async def unban(self, ctx, id: int, reason=None):
        if not id:
            await ctx.send("you failed to specify the user's id.")
            return False
        if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == int(self.owner_id):
            user = await self.bot.fetch_user(id)
            print(type(user), flush=True)
            await ctx.guild.unban(user, reason=reason)
            await ctx.send(user.name + " has been unbanned")
            return True
        await ctx.send("You dont have permission to use this command.")

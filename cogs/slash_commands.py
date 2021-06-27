import json
import requests
import discord
import datetime
import aiohttp
import time
import os
import asyncio
import random
from discord.ext import commands
from discord_slash import cog_ext, SlashCommand, SlashContext
from discord.voice_client import VoiceClient
from discord_slash import SlashCommandOptionType
from discord_slash.utils import manage_commands
from aiohttp import request


global startTime
startTime = time.time()

owner_id = 533964838041419776
bot_id = 840810272720683018
muted = []


prefix = "-"
client = commands.Bot(command_prefix="prefix", intents=discord.Intents.all())
slash = SlashCommand(client, override_type=True, sync_commands=True)

guild_ids = [809464190577541120, 829249975966761001]


class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    def cog_unload(self):
        self.client.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name="ping", description="Check the bot's ping!", guild_ids=guild_ids)
    async def ping(self, ctx: SlashContext):
        start = time.perf_counter()
        message = await ctx.send("Ping...")
        end = time.perf_counter()
        duration = (end - start) * 1000
        await message.edit(content=' 🏓 Pong! {:.2f}ms'.format(duration))

    @cog_ext.cog_slash(name="uptime", description="Check the bot's uptime!", guild_ids=guild_ids)
    async def _uptime(self, ctx: SlashContext):

        uptime = str(datetime.timedelta(
            seconds=int(round(time.time()-startTime))))
        await ctx.send(uptime)

    @cog_ext.cog_slash(name="cogs_test", guild_ids=guild_ids)
    async def _test(self, ctx: SlashContext):
        embed = discord.Embed(title="cogs test")
        await ctx.send(content="cogs oof", embeds=[embed])

    @cog_ext.cog_slash(name="avatar", description="Shows your avatar", guild_ids=guild_ids)
    async def _pfp(self, ctx: SlashContext):
        embed = discord.Embed(
            title=f"Avatar of {ctx.author.display_name}",
            color=discord.Color.teal()
        ).set_image(url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="roll", description="roll a dice lol", guild_ids=guild_ids)
    async def _dice(self, ctx: SlashContext):

        roll = random.choice(["1", "2", "3", "4", "5", "6"])

        await ctx.send("**You rolled a **" + roll)





    @cog_ext.cog_slash(name="how-hot", description="Returns a random percent for how hot is a discord user", guild_ids=guild_ids)
    async def _howhot(self, ctx: SlashContext, user: discord.Member = None):

        if user is None:
            user = ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 25:
            emoji = "❤"
        elif hot > 50:
            emoji = "💖"
        elif hot > 75:
            emoji = "💞"
        else:
            emoji = "💔"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    # get info of server

    @cog_ext.cog_slash(name="serverinfo", description="Shows server info", guild_ids=guild_ids)
    async def _sinf(self, ctx):
        embed = discord.Embed(title="Server Info",
                              color=discord.Color.teal())

        info_title = [
            "Server Name",
            "Server ID",
            "Server Owner",
            "Member Count",
            "Channel Count",
            "Role Count",
            "Region",
        ]

        infos = [
            str(ctx.guild.name),
            str(ctx.guild.id),
            str(ctx.guild.owner),
            str(len(ctx.guild.members)),
            f"{len(ctx.guild.channels)} \n _includes categories and staff channels_",
            str(len(ctx.guild.roles)),
            str(ctx.guild.region),
        ]

        i = 0
        for i in range(len(infos)):
            embed.add_field(name=info_title[i], value=infos[i])

        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="user-info", description="user info sheeshhh", guild_ids=guild_ids)
    async def whois(self, ctx: SlashContext, member: discord.Member = None):

        if member is None:
            member = ctx.author
            roles = [role for role in ctx.author.roles]

        else:
            roles = [role for role in member.roles]

        embed = discord.Embed(title=f"{member}", colour=member.colour)
        embed.set_footer(
            text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_author(name="User Info: ")
        embed.add_field(name="ID:", value=member.id, inline=False)
        embed.add_field(name="User Name:",
                        value=member.display_name, inline=False)
        embed.add_field(name="Discriminator:",
                        value=member.discriminator, inline=False)
        # embed.add_field(name="Current Status:", value=str(member.status).title(), inline=False)
        # embed.add_field(name="Current Activity:", value=f"{str(member.activity.type).title().split('.')[1]} {member.activity.name}" if member.activity is not None else "None", inline=False)
        embed.add_field(name="Created At:", value=member.created_at.strftime(
            "%a, %d, %B, %Y, %I, %M, %p UTC"), inline=False)
        embed.add_field(name="Joined At:", value=member.joined_at.strftime(
            "%a, %d, %B, %Y, %I, %M, %p UTC"), inline=False)
        embed.add_field(name=f"Roles [{len(roles)}]", value=" **|** ".join(
            [role.mention for role in roles]), inline=False)
        embed.add_field(name="Top Role:", value=member.top_role, inline=False)
        embed.add_field(name="Bot?:", value=member.bot, inline=False)
        await ctx.send(embed=embed)
        return

    # # ROLE REMOVE AND ADD:

    @cog_ext.cog_slash(name="addrole", description="Gives a user a role,", options=[manage_commands.create_option("user", "the user you want to assign the role to.", SlashCommandOptionType.USER, True), manage_commands.create_option("role", "the role you're giving.", SlashCommandOptionType.ROLE, True)], guild_ids=guild_ids)
    async def _addrole(self, ctx: SlashContext, user, role):
        if ctx.author.guild_permissions.manage_roles == True:
            await user.add_roles(role)
            embed = discord.Embed(
                title="Role given", description=f"{role} has been given to {user}")
            await ctx.send(embeds=[embed])
        else:
            await ctx.send("You are missing perms bruv")

    @cog_ext.cog_slash(name="removerole", description="Removes a role from a user.", options=[manage_commands.create_option("user", "the user you're removing the role from", SlashCommandOptionType.USER, True), manage_commands.create_option("role", "the role you want to remove.", SlashCommandOptionType.ROLE, True)], guild_ids=guild_ids)
    async def _removerole(self, ctx: SlashContext, user, role):
        if ctx.author.guild_permissions.manage_roles == True:
            await user.remove_roles(role)
            embed = discord.Embed(
                title="Role removed", description=f"{role} has been removed from {user}")
            await ctx.send(embeds=[embed])
        else:
            await ctx.send("You are missing perms bruv")

    @cog_ext.cog_slash(name="animal-fact", description="fact", guild_ids=guild_ids)
    async def animal_fact(self, ctx: SlashContext, animal: str):
        if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]

                else:
                    image_link = None

            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = discord.Embed(title=f"{animal.title()} fact",
                                          description=data["fact"],
                                          colour=ctx.author.colour)
                    if image_link is not None:
                        embed.set_image(url=image_link)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API returned a {response.status} status.")

        else:
            await ctx.send("No facts are available for that animal.")


def setup(client):
    client.add_cog(Slash(client))

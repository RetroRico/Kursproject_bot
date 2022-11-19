import discord
import Config
import random
from discord.ext import commands
from discord import utils

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(command_prefix=Config.Prefix, intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == Config.Post_ID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == '👦':
            role = discord.utils.get(guild.roles, name='Учень')
        elif payload.emoji.name == '🎓':
            role = discord.utils.get(guild.roles, name='Студент')
        elif payload.emoji.name == '💼':
            role = discord.utils.get(guild.roles, name='Работник')

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print("Додано роль для {0}.".format(member))
            else:
                print("Користувача не найдено.")
        else:
            print("Роль не знайдено.")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == Config.Post_ID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == '👦':
            role = discord.utils.get(guild.roles, name='Учень')
        elif payload.emoji.name == '🎓':
            role = discord.utils.get(guild.roles, name='Студент')
        elif payload.emoji.name == '💼':
            role = discord.utils.get(guild.roles, name='Работник')

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print("Віднято роль у {0}.".format(member))
            else:
                print("Користувача не найдено.")
        else:
            print("Роль не знайдено.")

bot.run(Config.TOKEN)
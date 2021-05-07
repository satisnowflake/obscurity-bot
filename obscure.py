import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
from discord import Activity, ActivityType
import datetime
import random
import json
import math
import tracemalloc

client = discord.Client()
bot = commands.Bot(command_prefix='!', case_insensitive=True)

# НИЖЕ ПИСАТЬ ЧО УГОДНО, ДАП, ВЫШЕ НЕ ТРОГАТЬ

@bot.command(pass_context=True)
@bot.event
async def red(message):
    if message.author == bot.user or message.author.bot:
        return

    mention = message.author.mention
    response = f"hey {mention}, you're great!"
    await message.channel.send(response)


@bot.command(name='roll')
async def roll(ctx, iko = 'd6', ako = ''):
    if "d" in iko and str(iko[0]) == "d" and ("+" not in iko and "-" not in iko):
        num1 = len(iko) #3
        num2 = iko.index("d") + 1 #1
        cube = ""
        while num1 > num2:
            cube += str(iko[num2])
            num2 += 1
        resul = random.randint(1, int(cube))
        soob = '<@!' + format(ctx.author.id) + '>\nОбскур кинула d' + str(cube) + ' и наролила: \n[' + str(resul) + ']'
        await ctx.send(soob)
    elif "d" in iko and str(iko[0]) != "d" and ("+" not in iko and "-" not in iko):
        num1 = len(iko)
        num2 = iko.index("d") + 1
        cube = ""
        minmax = []
        while num1 > num2:
            cube += str(iko[num2])
            num2 += 1
        num3 = iko.index("d") - 1 #1 
        num4 = 0
        rolls = ""
        while num3 >= num4:
            rolls += str(iko[num4])
            num4 += 1
        kolvo = int(rolls)
        soob = '<@!' + format(ctx.author.id) + '>\nОбскур кинула ' + str(rolls) + 'd' + str(cube) + ' и наролила: \n' 
        while kolvo > 0:
            resul = random.randint(1, int(cube))
            soob += '[' + str(resul) + '] '
            minmax.append(resul)
            kolvo -= 1
        if ako == "min":
            soob += ('\nМинимальный = [' + str(min(minmax)) + ']')
        if ako == "max":
            soob += ('\nМаксимальный = [' + str(max(minmax)) + ']')
        await ctx.send(soob)
    elif "d" in iko and str(iko[0]) == "d" and ("+" in iko or "-" in iko):
        num1 = len(iko) #5
        num2 = iko.index("d") + 1 #1
        if "+" in iko:
            num3 = iko.index("+") #3
        if "-" in iko:
            num3 = iko.index("-")
        cube = ""
        plusminus = ""
        while num3 > num2:
            cube += str(iko[num2])
            num2 += 1
        while num1 > num3:
            plusminus += str(iko[num3])
            num3 += 1
        caboo = random.randint(1, int(cube))
        resul = caboo + int(plusminus)
        soob = '<@!' + format(ctx.author.id) + '>\nОбскур кинула 1d' + str(cube) + ' и наролила [' + str(caboo) + '] вместе с {' + str(plusminus) + '}. Результат: \n[' + str(resul) + ']'
        await ctx.send(soob)
    elif "d" in iko and str(iko[0]) != "d" and ("+" in iko or "-" in iko):
        num1 = len(iko) #5
        num2 = iko.index("d") + 1
        num22 = iko.index("d") - 1
        if "+" in iko:
            num3 = iko.index("+") #3
        if "-" in iko:
            num3 = iko.index("-")
        cube = ""
        minmax = []
        rolls = ""
        plusminus = ""
        while num3 > num2:
            cube += str(iko[num2])
            num2 += 1
        num4 = 0
        while num22 >= num4:
            rolls += str(iko[num4])
            num4 += 1
        while num1 > num3:
            plusminus += str(iko[num3])
            num3 += 1
            kolvo = int(rolls)
        soob = '<@!' + format(ctx.author.id) + '>\nОбскур кинула ' + str(rolls) + 'd' + str(cube) + ' вместе с {' + str(plusminus) + '} для каждого кубика. Вот результаты: \n' 
        while kolvo > 0:
            resul = random.randint(1, int(cube)) + int(plusminus)
            soob += '[' + str(resul) + '] '
            minmax.append(resul)
            kolvo -= 1
        if ako == "min":
            soob += ('\nМинимальный = [' + str(min(minmax)) + ']')
        if ako == "max":
            soob += ('\nМаксимальный = [' + str(max(minmax)) + ']')
        await ctx.send(soob)



@bot.event
async def on_message(message):
    await bot.process_commands(message)
    with open('lvl.json','r') as f:
        users = json.load(f)
    async def update_data(users,user):
        if not user in users:
            users[user] = {}
            users[user]['exp'] = 0
            users[user]['lvl'] = 1
    async def add_exp(users,user,exp):
        users[user]['exp'] += exp
    async def add_lvl(users,user):
        exp = users[user]['exp']
        lvl = users[user]['lvl']
        if exp > lvl:
            users[user]['exp'] = 0
            users[user]['lvl'] = lvl + 1
            await message.channel.send(f'{message.author.mention} повысил свой уровень! Теперь он ' + str(users[user]['lvl']) + ' уровня!')
            if users[user]['lvl'] == 5 and not message.guild.get_role(835448462522187799) and not message.guild.get_role(835455095159914536) in user.roles() and not message.guild.get_role(835447080616198184) in user.roles() and not message.guild.get_role(835476259853041676) in user.roles():
            	await user.remove_roles(message.guild.get_role(835604124976414721))
            	await user.add_roles(message.guild.get_role(835604186157547540))
            elif users[user]['lvl'] == 10 and not message.guild.get_role(835448462522187799) and not message.guild.get_role(835455095159914536) in user.roles() and not message.guild.get_role(835447080616198184) in user.roles() and not message.guild.get_role(835476259853041676) in user.roles():
            	await user.remove_roles(message.guild.get_role(835604186157547540))
            	await user.add_roles(message.guild.get_role(835449067512659968))
            elif users[user]['lvl'] == 15 and not message.guild.get_role(835448462522187799) and not message.guild.get_role(835455095159914536) in user.roles() and not message.guild.get_role(835447080616198184) in user.roles() and not message.guild.get_role(835476259853041676) in user.roles():
            	await user.remove_roles(message.guild.get_role(835449067512659968))
            	await user.add_roles(message.guild.get_role(835449039155232778))
            elif users[user]['lvl'] == 20 and not message.guild.get_role(835448462522187799) and not message.guild.get_role(835455095159914536) in user.roles() and not message.guild.get_role(835447080616198184) in user.roles() and not message.guild.get_role(835476259853041676) in user.roles():
            	await user.remove_roles(message.guild.get_role(835449039155232778))
            	await user.add_roles(message.guild.get_role(835449020834775080))
            elif users[user]['lvl'] == 25 and not message.guild.get_role(835448462522187799) and not message.guild.get_role(835455095159914536) in user.roles() and not message.guild.get_role(835447080616198184) in user.roles() and not message.guild.get_role(835476259853041676) in user.roles():
            	await user.remove_roles(message.guild.get_role(835449020834775080))
            	await user.add_roles(message.guild.get_role(835448966819741697)) 
            elif users[user]['lvl'] == 30 and not message.guild.get_role(835448462522187799) and not message.guild.get_role(835455095159914536) in user.roles() and not message.guild.get_role(835447080616198184) in user.roles() and not message.guild.get_role(835476259853041676) in user.roles():
            	await user.remove_roles(message.guild.get_role(835448966819741697))
            	await user.add_roles(message.guild.get_role(835448456419344384))           	            	
    await update_data(users,str(message.author.id))
    await add_exp(users,str(message.author.id),0.1)
    await add_lvl(users,str(message.author.id))
    with open('lvl.json','w') as f:
        json.dump(users,f)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(835440433462771772)
    role = member.guild.get_role(835604124976414721)
    await member.add_roles(role)
    await channel.send(f'▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n```Приветики, {member.user.name}-сан! <3```\n`User`: {member.mention}\n`ID`: {member.user.id}')
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(835440433462771772)
    await channel.send(f'▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n```Прощайте, {member.user.name}-сан! :c```\n`User`: {member.mention}\n`ID`: {member.user.id}')

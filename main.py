import os
import random
import discord
from log import Log
from datetime import date, datetime, timedelta
from discord.ext import commands

logs = {}

timeout = 3
TOKEN = os.environ.get('TOKEN')

bot = commands.Bot(command_prefix='!', description='A spam bot for Eric!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.change_presence(game=discord.Game(name='Spamwatch v0.1'))

@bot.event
async def on_message(message):
    #ignore this bot's own messages
    if message.author == bot.user:
        return
    
    if message.author.name in logs:
        delta = message.timestamp-logs[message.author.name].lastMessage
        if(delta.seconds < timeout):
            logs[message.author.name].violations += 1
            await bot.delete_message(message)
            await bot.send_message(message.channel, '{0} earns a spamwich!'.format(message.author))
        
        logs[message.author.name].lastMessage = message.timestamp
    else:
        logs[message.author.name] = Log(message.timestamp)

    # Since we have on_message, need to call the bot commands here
    await bot.process_commands(message)

@bot.command(pass_context=True)
async def ping(ctx):
    start = datetime.now()
    m = await bot.send_message(ctx.message.channel, 'Ping?')
    span = datetime.now()-start
    ms = span.microseconds/1000
    await bot.edit_message(m, 'Pong! {0}ms'.format(ms))

@bot.command(pass_context=True)
async def spam(ctx):
    name = ctx.message.author.name
    if name in logs:
        log = logs[name]
        if log.violations > 0:
            await bot.send_message(ctx.message.channel, '{0} has {1.violations} violations.'.format(name, log))
        else:
            await bot.send_message(ctx.message.channel, '{0} has no violations yet. Good job!'.format(name))
    else:
        bot.send_message(ctx.message.channel, '???')


@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command()
async def threshold(span : int):
    timeout = span
    await bot.say('Updated spam threshold to {0} seconds.'.format(timeout))

bot.remove_command('help')

@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="Spam Bot", description="LESS Eric! :) List of commands are:", color=0xeee657)

    embed.add_field(name="!ping", value="Check the latency", inline=False)
    embed.add_field(name="!info", value="Details on the anti-Eric bot", inline=False)
    embed.add_field(name="!spam", value="Check the number of violations you have", inline=False)
    #threshold hidden command

    await bot.send_message(ctx.message.channel, embed=embed)

# Run bot
bot.run(TOKEN)

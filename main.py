import os
import sys
import discord
import log
from datetime import date, datetime
from discord.ext import commands

logs = {}

timeout = 3000
TOKEN = os.environ.get('TOKEN')

bot = commands.Bot(command_prefix='!', description='A spam bot for Eric!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.change_presence(activity=discord.Game(name="Whackamole with spammers"))

@bot.event
async def on_message(message):
    #ignore this bot's own messages
    #if message.author == client.user:
     #   return
    
    if(message.author.username in logs):
        now = datetime.now()
        delta = now-logs[message.author.username].lastMessage
        if(delta.microsecond < timeout):
            await message.delete()
            
        logs[message.author.username].lastMessage = datetime.now()
    else:
        logs[message.author.username] = Log(datetime.now())
        pass

@bot.command()
async def ping(ctx):
    m = await ctx.send('Ping?')
    ctx.send('Pong!')
    #{m.createdTimeStamp - ctx.createdTimestamp}ms {Math.round(client.ping)}

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Spam Bot", description="To stop Eric's incessant spamming", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="geonigma")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Spam Bot", description="LESS Eric! :) List of commands are:", color=0xeee657)

    embed.add_field(name="!ping", value="Check the latency", inline=False)
    embed.add_field(name="!info", value="Details on the anti-Eric bot", inline=False)

    await ctx.send(embed=embed)

# Run bot
sys.stdout.write(TOKEN)
bot.run(TOKEN)

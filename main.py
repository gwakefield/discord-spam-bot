import os
import discord
from log import Log
from datetime import date, datetime, timedelta
from discord import Message
from discord.ext import commands

logs = {}

timeout = 3
TOKEN = "NDYyMzM0OTUzNDgxMzA2MTEy.DhvbmA.YmBcAt3980kofhSOazt5kOd4R-s"#os.environ.get('TOKEN')

bot = commands.Bot(command_prefix='!', description='A spam bot for Eric!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.change_presence(activity=discord.Game(name="Whackamole with spammers"))

@bot.event
async def on_message(ctx):
    print("message received")
    #ignore this bot's own messages
    if ctx.author == bot.user:
        return
    
    if ctx.author.name in logs:
        delta = ctx.created_at-logs[ctx.author.name].lastMessage
        if(delta.seconds < timeout):
            await ctx.channel.send('{0} earns a spamwich!'.format(ctx.author))
            await ctx.delete()
            
        logs[ctx.author.name].lastMessage = ctx.created_at
    else:
        logs[ctx.author.name] = Log(ctx.created_at)

@bot.command()
async def ping(ctx):
    print('ping received')
    m = await ctx.channel.send('Ping?')
    print("ping sent")
    a = ctx.channel.send('Pong!')
    print("pong sent")
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
bot.run(TOKEN)

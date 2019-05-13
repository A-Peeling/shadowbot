import discord
from discord.ext import commands

p = 'shadowbot '
client = commands.Bot(command_prefix=p)

f = open('token.txt', 'r')
token = f.read()
f.seek(0)
f.close()

f = open('game.txt', 'r')
lastgame = f.read()
f.seek(0)
f.close()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name=lastgame))

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.command(pass_context=True, brief='Define Linux/UNIX terminology', description='Define terms. Ex. `shadowbot define linux` Please use lowercase I am offended by capital latters.')
async def define(ctx, arg = None):
    if arg:
        f = open('terms/' + arg + '.txt', 'r')
        answer = f.read()
        f.seek(0)
        f.close()

        if answer is 'red':
            await ctx.send("The definition of Red Hat is: " + answer)

        await ctx.send("The definition of " + arg + " is: " + answer)
    else:
        await ctx.send('You need to give me terms to define')

@define.error
async def define_error(ctx, error):
    await ctx.send('Could not recognize term')

client.run(token)

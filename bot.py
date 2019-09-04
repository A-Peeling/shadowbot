import discord
from discord.ext import commands
from pathlib import Path

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


@client.command(pass_context=True, brief="Print info about bot", description='Same as defining shadowbot')
async def about(ctx):
    f = open('terms/shadowbot.txt', 'r')
    await ctx.send(f.read())
    f.seek(0)
    f.close()


@client.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(client.latency, 4)*1000) + ' ms')


@client.command(
    pass_context=True,
    brief='Define Linux/UNIX terminology',
    description='Define terms. Ex. `shadowbot define linux`')
async def define(ctx, arg=None):
    if arg:
        f = open('terms/' + arg.lower() + '.txt', 'r')
        answer = f.read()
        f.seek(0)
        f.close()

        if arg.lower() == 'red':
            await ctx.send("The definition of Red Hat is: " + answer)
        else:
            await ctx.send("The definition of " + arg + " is: " + answer)
    else:
        await ctx.send('You need to give me terms to define. Do \"shadowbot terms\" for a list')


@define.error
async def define_error(ctx, error):
    await ctx.send('Error could not find file.')


@client.command()
async def make(ctx, arg1=None, arg2=None):
    if ctx.message.author.id == 177169904376610816 or 291663444883800064:
        if arg1 or arg2:
            f = open('terms/' + arg1 + '.txt', 'w+')
            f.write(arg2)
            f.close()
            f = open('terms.txt', 'a')
            f.write(", "+arg1)
            f.close()
            await ctx.send("k done.")
        else:
            await ctx.send('You need to type a name and text for the file you dumbo.')


@client.command()
async def terms(ctx):
    await ctx.send("Check your DMs for the terms.")
    await ctx.message.author.send("```"+open('terms.txt', 'r').read()+'\n```')
    f.close()


@client.command()
async def bal(ctx, arg=None):
    temp = ctx.author.id
    if arg == None:
        my_file = Path('users/' + str(temp) + '.txt')
        if my_file.is_file():
            f = open('users/' + str(temp) + '.txt', 'r')
            answer = f.read()
            f.seek(0)
            f.close()
            await  ctx.send("Your balance is "+ answer)
        else:
            await ctx.send("Creating file.")
            f = open('users/' + str(temp) + '.txt', 'w+')
            f.write("0")
            f.close()
            await ctx.send("Your balance is 0")
    else:
        if arg:
            arg = arg.replace("<", "")
            arg = arg.replace("@", "")
            arg = arg.replace(">", "")
            my_file = Path('users/' + arg + '.txt')
            if my_file.is_file():

                f = open('users/' + arg + '.txt', 'r')
                answer = f.read()
                f.seek(0)
                f.close()
                await  ctx.send("Their balance is "+ answer)
            else:
                await ctx.send("Creating file.")
                f = open('users/' + arg + '.txt', 'w+')
                f.write("0")
                f.close()
                await ctx.send("Their balance is 0")
client.run(token)

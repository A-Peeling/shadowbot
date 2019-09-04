import discord
import re
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
    await ctx.send('Error could not find file. Do shadowbot terms for a list of terms')


@client.command()
async def make(ctx, arg1=None, arg2=None):
    if ctx.message.author.id == 177169904376610816 or ctx.message.author.id == 291663444883800064:
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
    else:
        await ctx.send("Your not cool enough to make a definition. :sunglasses:")


@client.command()
async def terms(ctx):
    await ctx.send("Check your DMs for the terms.")
    await ctx.message.author.send("```"+open('terms.txt', 'r').read()+'\n```')
    f.close()


@client.command(
    aliases=['balance','money','bank'],
    brief = 'Diamond balance.')
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
            if re.search('[a-zA-Z]', arg):
                await ctx.send("Error")
            else:
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


@client.command(
    brief = '@user amount to add (use negatives to subtract)',
    description = 'To change somebody\'s balance do @user + or - amount',
    aliases=['add','change','changebal'])
@commands.has_permissions(manage_guild=True)
async def addbal(ctx, arg1=None, arg2=None):
        if arg1:
            arg1 = arg1.replace("<", "")
            arg1 = arg1.replace("@", "")
            arg1 = arg1.replace(">", "")
            my_file = Path('users/' + arg1 + '.txt')
            if my_file.is_file():
                f = open('users/' + arg1 + '.txt', 'r+')
                answer = f.read()
                f.seek(0)
                answer = int(answer)+int(arg2)
                f.write(str(answer))
                f.close()
                await  ctx.send("Their balance is now " + str(answer))
            else:
                if re.search('[a-zA-Z]', arg1):
                    await ctx.send("Error")
                else:
                    await ctx.send("Creating file.")
                    f = open('users/' + arg1 + '.txt', 'w+')
                    f.write(str(arg2))
                    f.close()
                    await ctx.send("Their balance has been created and set to " + str(arg2))
@addbal.error
async def addbal_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Trying to cheat I see :eyes:. You need manage sever to run this command.")

client.run(token)

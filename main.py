import discord
import re
import random

import client_token

client = discord.Client()


@client.event
async def on_message(message):
    # per the discord.py docs, this is so to not have the bot respond to itself
    if message.author == client.user:
        return
    # if the bot sees the command !hello we will respond with our msg string
    if message.content.startswith('!roll'):
        msg = roll(message)
        if msg != 'ERROR':
            await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def roll(message):
    split_command = message.content.split()
    if len(split_command) == 1:
        dice = '1d20'
    else:
        dice = split_command[1]
    try:
        a, b, c = re.findall("^(\d*)d(\d+)(\+\d+)?$", dice)[0]
        the_roll = int(c or 0)+(sum(random.randint(1, int(b))for i in range(int(a or 1))) or q)
        return '<:d20:313202276053286923> {} rolled {} and got {}.'.format(message.author.mention, dice, the_roll)
    except:
        return 'ERROR'


client.run(client_token.token)

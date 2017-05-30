import discord
import re
import random
import csv

from fuzzywuzzy import process

import client_token

client = discord.Client()

spells = open('dnd_5e_spells_edit.csv', 'r')
spell_reader = csv.reader(spells)

list_of_spells = []

for row in spell_reader:
    list_of_spells.append(row[1])

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
    if message.content.startswith('!spell'):
        msg = get_spell(message)
        if msg != 'ERROR':
            while len(msg) > 2000:
                await client.send_message(message.channel, msg[:2000])
                msg = msg[2000:]
            await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def get_spell(message):
    split_command = message.content.split()
    if len(split_command) == 1:
        return 'ERROR'
    spell = ' '.join(split_command[1:]).strip()
    print(spell)
    return_spell = ''
    spells.seek(0)
    for row in spell_reader:
        if spell.lower() == row[1].lower():
            # return_spell = 'Found Spell: {}'.format(row[1])
            name = row[1]
            components = ''
            description = row[12].replace('<br> ', '\n\t')
            ritual = ''
            if row[2] == '1':
                ritual = ' (ritual)'
            if row[11] != '':
                components = '(' + row[11] + ')'
            higher_levels = ''
            if row[13] != '':
                higher_levels = '\n\t***At Higher Levels.*** ' + row[13].replace('<br> ', '\n\t')
            return_spell = '''__**{}**__
*{}{}*
**Casting Time:** {}
**Range:** {}
**Components:** {} {}
**Duration:** {}
{}{}
'''.format(name, row[6], ritual, row[7], row[8], row[10], components, row[9], description, higher_levels)
    if return_spell == '':
        return_spell, score = process.extractOne(spell, list_of_spells, score_cutoff=55)
        print(return_spell)
        if return_spell is None:
            return_spell = 'Spell not found.'
        else:
            return_spell = 'Did you mean ' + return_spell + '?'
    return return_spell


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

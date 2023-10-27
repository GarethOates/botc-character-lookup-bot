import os
import discord

from dotenv import load_dotenv
from discord.ext import commands
from urllib.parse import quote

from get_character import get_info_for_character

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
IMAGE_BASE = os.getenv('IMAGE_BASE')
BOTC_BASE = os.getenv('BOTC_BASE')
ENABLE_EASTER_EGGS = os.getenv('ENABLE_EASTER_EGGS')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

def get_image_url(name):
    return name.lower().replace(' ', '').replace('-', '').replace("'", "")


def create_embed(info):
    editionLink = f'[{info["edition"]}]({BOTC_BASE}{quote(info["edition"])})'
    characterLink = f'[{info["name"]}]({BOTC_BASE}{quote(info["name"])})'

    embed = discord.Embed(title=info["name"], description=info["type"], color=info["colour"])
    embed.set_thumbnail(url=f'{IMAGE_BASE}{info["type"].lower()}/{get_image_url(info["name"])}.png?raw=true')
    embed.add_field(name="Ability", value=info["ability"], inline=False)
    embed.add_field(name="Found In", value=f'{editionLink} - {characterLink}', inline=False)

    return embed

def easter_eggs(character):
    match character:
        case "Lars Erik":
            return "Empath"
        case "Kristaver":
            return "Sweetheart"
        case "Hammad":
            return "Ravenkeeper"
        case "Mikkel":
            return "Saint"
        case _:
            return character


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='lookup', help='Looks up a botc character from the Wiki')
async def lookup(ctx, *, character):
    if ctx.message.author == bot.user.name:
        return
    try:
        if ENABLE_EASTER_EGGS == 'True':
            character = easter_eggs(character)

        info = get_info_for_character(character)

        if "error" in info:
            await ctx.send(info["error"])
            return
    
        await ctx.send(f'Found 1 result for "{info["name"]}"')
        embed = create_embed(info)

        await ctx.send(embed=embed)
    except Exception as error:
        print(error)
        await ctx.send("Something went wrong. Could not fetch data.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('!'):
        await bot.process_commands(message)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    exit()

def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
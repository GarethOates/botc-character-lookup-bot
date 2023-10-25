import os
import discord

from dotenv import load_dotenv
from discord.ext import commands
from urllib.parse import quote

from getCharacter import get_info_for_character

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
IMAGE_BASE = os.getenv('IMAGE_BASE')
BOTC_BASE = os.getenv('BOTC_BASE')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

def get_image_url(name):
    return name.lower().replace(' ', '').replace('-', '').replace("'", "")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='lookup', help='Looks up a botc character from the Wiki')
async def lookup(ctx, *, character):
    if ctx.message.author == bot.user.name:
        return
    try:
        info = get_info_for_character(character)
        
        if "error" in info:
            await ctx.send(info["error"])
        else:
            await ctx.send(f'Found 1 result for "{info["name"]}"')

            editionLink = f'[{info["found"]}]({BOTC_BASE}{quote(info["found"])})'
            characterLink = f'[{info["name"]}]({BOTC_BASE}{quote(info["name"])})'
            lowerType = info["type"].lower()
            lowerName = get_image_url(info["name"])

            embed = discord.Embed(title=info["name"], description=info["type"], color=info["color"])
            embed.set_thumbnail(url=f'{IMAGE_BASE}{lowerType}/{lowerName}.png?raw=true')
            embed.add_field(name="Ability", value=info["ability"], inline=False)
            embed.add_field(name="Found In", value=f'{editionLink} - {characterLink}', inline=False)

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
async def shutdown(context):
    exit()

bot.run(TOKEN)
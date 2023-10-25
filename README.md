# BOTC Character Lookup Bot

This is a very basic discord bot that fetches the ability, type, edition and url for a character
in Blood on the Clocktower.  It uses the official Blood on the Clocktower Wiki website, and the
MediaWiki api functionality to extract information from the page about the selected character,
and then presents that to the channel in the form of a Discord Embed.

It takes the images from a public GitHub repository by Skateside called Pocket-Grimoire.

Both of these data sources are flakey and could change at any time.  This bot works for now
but may fail in future and require modification.

## Warning

Please note, the means by which the Docker container is created is not safe.  Your .env file
with your Discord token is being copied inside the Docker image.  If you make your image
available on a public repository, anyone with access to the image, can steal your bot's token.

The better way to do this would be to add the variable in as an environment variable when
running the docker container with the `-e` flag.

## What you need to run the bot

You will need to crate a .env file, with the following values:

```cfg
DISCORD_TOKEN=<YOUR BOT TOKEN HERE>
WIKI_BASE=https://wiki.bloodontheclocktower.com/api.php?action=parse&page={}&prop=wikitext&format=json&formatversion=2
IMAGE_BASE=https://raw.githubusercontent.com/Skateside/pocket-grimoire/main/assets/img/icon/
BOTC_BASE=https://wiki.bloodontheclocktower.com/
```

## How to run

```bash
python main.py
```

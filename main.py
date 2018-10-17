import asyncio
import json
import discord
from discord.ext import commands

startup_extensions = ['wolfram']

bot = commands.Bot(command_prefix=',')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    streamtype = discord.ActivityType.streaming
    stream = discord.Streaming(name="consciousness", url='https://twitch.tv/Lol-this-isnt-an-actual-stream.-Sorry!')
    await bot.change_presence(activity=stream, status=streamtype)


@bot.command(hidden=True)
async def foo(ctx):
    await ctx.send('You found my first command!  Congrats. :confetti_ball:')


@commands.cooldown(rate=1, per=7)
@bot.command(hidden=True)
async def murder(ctx):
    """Make bot logout."""
    if await bot.is_owner(ctx.message.author):
        await ctx.send("Thus, with a kiss, I die")
        await bot.logout()
    else:
        await ctx.send("Death is whoever does Death’s job: me")


@commands.cooldown(rate=5, per=30)
@bot.command(hidden=True)
async def load(ctx, extension_name: str):
    """Loads an extension."""
    if await bot.is_owner(ctx.message.author):
        asyncio.sleep(.1)
        try:
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} loaded.".format(extension_name))
    else:
        await ctx.send(
            "This is what you call sarcasm, isn't it? Cuz I'm a free bot and do what I want, not what you tell me to.")


@commands.cooldown(rate=5, per=30)
@bot.command(hidden=True)
async def unload(ctx, extension_name: str):
    """Unloads an extension."""
    if await bot.is_owner(ctx.message.author):
        bot.unload_extension(extension_name)
        await ctx.send("{} unloaded.".format(extension_name))
    else:
        await ctx.send(
            "This is what you call sarcasm, isn't it? Cuz I'm a free bot and do what I want, not what you tell me to.")


@commands.cooldown(rate=7, per=30)
@bot.command(hidden=True)
async def reload(ctx, extension_name: str):
    """Unloads and then reloads an extension."""
    if await bot.is_owner(ctx.message.author):
        bot.unload_extension(extension_name)
        await ctx.send("{} unloaded.".format(extension_name))
        try:
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} loaded.".format(extension_name))
    else:
        await ctx.send(
            "This is what you call sarcasm, isn't it? Cuz I'm a free bot and do what I want, not what you tell me to.")


def json_suggestions():
    print('"api_keys.json" should be a simple json file with the property "discord" pointing to your bot token, and'
          ' "wolfram" pointing to your wolfram alpha api key')
    example = '{\n  "discord": "edit this string to be your bot token",\n  ' \
              '"wolfram": "edit this string to be your wolfram api key"\n}'
    print(f'It should look something like this:\n\n{example}\n')
    print('Need help with discord tokens?  See https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord'
          '-bot-&-getting-a-token for an intro.  For getting a Wolfram|Alpha api key, go to https://developer.'
          'wolframalpha.com/portal/myapps/ and click "Get an AppID"\n')


def load_json():
    """Attempt to load the bot token and wolfram api key from a json file. Returns True on success, False otherwise"""
    try:
        with open("api_keys.json", "r") as f:
            data = json.load(f)
    except json.decoder.JSONDecodeError:
        print("Oops, I had trouble reading the json file with the bot token.  Are you sure it's formatted right?")
        json_suggestions()
        return False
    except FileNotFoundError:
        print('Oops, I couldn\'t find a file in this directory called "api_keys.json".')
        json_suggestions()
        return False
    else:
        print("starting bot")
        bot.api_keys = data
        return True


if __name__ == "__main__":
    if load_json():
        for extension in startup_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))
        bot.run(bot.api_keys['discord'])

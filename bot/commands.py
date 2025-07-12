from core.discord_client import bot
import discord.ext.commands as cmd
import requests

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def hola(ctx):
    await ctx.send('Hello World')

@bot.command()
async def poke(ctx, arg):
    try:
        pokemon = arg.split(' ',1)[0].lower()
        response = requests.get('https://pokeapi.co/api/v2/pokemon/'+pokemon)
        
        if response.text == 'Not Found':
            await ctx.send('Pokemon not found')
            return
        else:
            data = response.json()
            await ctx.send(data['sprites']['front_default'])

    except Exception as e:
        print(e)
        await ctx.send('Error')

@poke.error
async def poke_error(ctx, error):
    if isinstance(error, cmd.MissingRequiredArgument):
        await ctx.send('Please provide a pokemon name')
    else:
        await ctx.send('Error')



@bot.command()
async def cls(ctx):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send('You do not have permission to clear messages.', delete_after=5)
        return
    await ctx.channel.purge()
    await ctx.send('Cleared chat', delete_after=3)
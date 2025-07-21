import discord
from discord.ext import commands
import logging 
import asyncio
from dotenv import load_dotenv 
import os 

load_dotenv()
token = os.getenv('DISCORD_TOKEN') 

if token is None:
    raise ValueError("Token Discord mancante nel file .env!")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') 
intents = discord.Intents.default() 
intents.message_content = True  
intents.members = True 

logging.basicConfig(level=logging.INFO, handlers=[handler])
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


@bot.event 
async def on_ready():
    print(f"Ready to use {bot.user.name}")
    print(f"📋 Comandi caricati: {[command.name for command in bot.commands]}")

@bot.event 
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando non trovato. Digita !help per una lista di comandi disponibili.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Argomenti mancanti. Controlla la sintassi del comando.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Non hai i permessi per usare questo comando!")
    else:
        await ctx.send("Si è verificato un errore imprevisto.")
        raise error 

@bot.command()
async def help(ctx):
    comandi = "\n".join(f"- `{cmd.name}`" for cmd in bot.commands)
    await ctx.send(f"Ecco una lista di tutti i comandi disponibili: \n{comandi}")


async def load_extensions():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')
                print(f"✅ Estensione caricata: commands.{filename[:-3]}")
            except Exception as e:
                print(f"❌ Errore caricando {filename}: {e}")

async def main():
    await load_extensions()
    await bot.start(token)


asyncio.run(main()) 
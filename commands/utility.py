from discord.ext import commands 
import time
import requests
from dotenv import load_dotenv 
import os 
import ast


load_dotenv()
WeatherAPIToken = os.getenv('WEATHER_TOKEN') 

class Utility(commands.Cog):
    """Cog che contiene comandi utili vari come orario, ping, info, valutazione espressioni e meteo."""

    def __init__(self, bot):
        self.bot = bot      
        print("⚙️ Cog Utility caricato")
    
    @commands.command()   
    async def Orario(self, ctx):
        """Mostra l'orario corrente del sistema."""
        current_time = time.strftime("%H:%M:%S", time.localtime())
        await ctx.send(f"L'orario attuale è : {current_time}")
    
    @commands.command() 
    async def Ping(self, ctx):
        """Risponde con 'Pong!' per verificare che il bot sia attivo."""
        await ctx.send('Pong!')
    
    @commands.command()
    async def Info(self, ctx):
        """Fornisce informazioni sul bot."""
        await ctx.send('Questo bot è stato creato da Giovixx10 per avere un progetto personale da mettere su GitHub.')

    @commands.command()
    async def Evaluate(self, ctx, *, msg):
        """
        Valuta in sicurezza un'espressione Python semplice.
        
        Attenzione: supporta solo espressioni letterali sicure, come numeri, liste, dizionari.
        """
        try:
            res = ast.literal_eval(msg)
            await ctx.send(f'Il risultato è {res}')
        except:
            await ctx.send('Espressione invalida! Usa solo espressioni semplici (numeri, liste, dizionari).')
    
    @commands.command()
    async def Weather(self, ctx, *, msg):
        """
        Fornisce il meteo della città specificata usando OpenWeather API.
        
        Esempio: !Weather Milano
        """
        try:
            site = f'https://api.openweathermap.org/data/2.5/weather?q={msg}&appid={WeatherAPIToken}'
            response = requests.get(site).json()

            if response.get("cod") != 200:
                await ctx.send("Città non trovata o errore nell'API.")
                return 

            condition = response['weather'][0]['main']
            temp = int(response['main']['temp'] - 273.15)
            Umidità = response['main']['humidity']
            Pressione = response['main']['pressure']

            await ctx.send(
                f"Meteo a {msg.title()}:\n"
                f"- Condizioni: {condition.capitalize()}\n"
                f"- Temperatura: {temp}°C\n"
                f"- Umidità: {Umidità}%\n"
                f"- Pressione: {Pressione} mbar"
            )

        except Exception as e:
            await ctx.send('Errore durante la richiesta meteo.')

async def setup(bot): 
    await bot.add_cog(Utility(bot)) 
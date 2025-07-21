from discord.ext import commands
import random

class Fun(commands.Cog):
    """Cog che contiene comandi divertenti come Dado, MagicBall, TestaOCroce."""

    def __init__(self, bot):
        self.bot = bot
        print("⚙️ Cog Fun caricato")

    @commands.command()
    async def Dado(self, ctx):
        """Lancia un dado e restituisce un numero casuale tra 1 e 6."""
        randval = random.randint(1, 6)
        await ctx.send(f'Il numero casuale tra 1 e 6 è {randval}')

    @commands.command()
    async def MagicBall(self, ctx):
        """Risponde con una risposta casuale come una sfera magica."""
        RandAns = ["Si", "No", "Forse", "Probabilmente", "Decisamente si", "Decisamente no", "Un'altra volta", "Forse in futuro"]
        await ctx.send(random.choice(RandAns))

    @commands.command()
    async def TestaOCroce(self, ctx):
        """Lancia una moneta e risponde con Testa o Croce."""
        RandAns = ["Testa", "Croce"]
        await ctx.send("E' uscito " + random.choice(RandAns) + "!")
    
async def setup(bot):
    await bot.add_cog(Fun(bot))

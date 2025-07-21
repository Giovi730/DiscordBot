from discord.ext import commands 
import pymysql
import os
from dotenv import load_dotenv 


load_dotenv()



host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
passwd = os.getenv("DB_PASS")
database = os.getenv("DB_NAME")


def AccessToDB():
    """
    Crea e restituisce una connessione al database MySQL.
    Restituisce None in caso di errore.
    """
    try: 
        conn = pymysql.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )
        print("Connessione al database 'discordDataBase' riuscita.")
        return conn

    except Exception as e:
        print(f"Errore nella connessione: {e}")
        return None


class ToDo(commands.Cog):
    """
    Cog per la gestione di una lista attività privata per ogni utente,
    memorizzata su database MySQL.
    """
        
    def __init__(self, bot):
        self.bot = bot
        print("⚙️ Cog ToDo caricato")

    @commands.command()
    async def Add(self, ctx, *, msg):
        """
        Aggiunge una nuova attività alla lista dell'utente.
        """
        conn = AccessToDB()
        if conn:
            try:
                with conn.cursor() as cursor: 
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS discordServerT (
                            nome VARCHAR(100),
                            attivita VARCHAR(100)
                        )
                    """)
                    cursor.execute("INSERT INTO discordServerT (nome, attivita) VALUES (%s, %s);", (str(ctx.author), msg))
                    conn.commit()
                    await ctx.send('La tua attività è stata salvata correttamente.')
            except Exception as e:
                await ctx.send(f"Errore durante l'inserimento dell'attività nel DataBase: {e}")
            finally:
                conn.close()
        else:
            await ctx.send("Errore nell'accesso al DataBase.")
    
    @commands.command()
    async def List(self, ctx, page: int = 1):
        """
        Mostra la lista delle attività salvate dall'utente.
        """
        if page < 1:
            await ctx.send("Il numero di pagina deve essere almeno 1. Visualizzo pagina 1.")
            page = 1
        conn = AccessToDB()
        if conn:
            try: 
                with conn.cursor() as cursor:
                    cursor.execute("SHOW TABLES LIKE 'discordServerT'")
                    result = cursor.fetchone()
                    if result:
                        cursor.execute("SELECT * FROM discordServerT WHERE nome = %s", (str(ctx.author),))
                        r = cursor.fetchall()
                        items_per_page = 5
                        start = (page - 1) * items_per_page
                        end = start + items_per_page
                        riga_specifica = [z[1] for z in r[start:end]]

                        if riga_specifica:
                            await ctx.send(f"Le tue attività (pagina {page}): {riga_specifica}")
                        else:
                            await ctx.send(f"Nessuna attività trovata per la pagina {page}.")
                    else:
                        await ctx.send("Non è stata ancora creata nessuna attività!")
            except Exception as e:
                await ctx.send(f"Errore durante l'inserimento dell'attività nel DataBase: {e}")
            finally:
                conn.close()
        else:
            await ctx.send("Errore nell'accesso al DataBase.")

    @commands.command()
    async def RemoveSpecific(self, ctx, *, msg):
        """
        Rimuove una specifica attività dalla lista dell'utente.
        """
        conn = AccessToDB()
        if conn:
            try: 
                with conn.cursor() as cursor:
                    cursor.execute("SHOW TABLES LIKE 'discordServerT'")
                    result = cursor.fetchone()
                    if result:
                        cursor.execute("SELECT COUNT(*) FROM discordServerT WHERE nome = %s AND attivita = %s", (str(ctx.author), msg,))
                        result = cursor.fetchone()
                        count = result[0]
                        if count > 0:
                            cursor.execute("DELETE FROM discordServerT WHERE nome = %s AND attivita = %s;", (str(ctx.author), msg,))
                            conn.commit()
                            await ctx.send(f"L'attività `{msg}` è stata eliminata correttamente.") #protegge da mention/Markdown l'uso di ''
                        else:
                            await ctx.send("Questa attività non esiste!")
                    else:
                        await ctx.send("Non è stata ancora creata nessuna attività!")
            except Exception as e:
                await ctx.send(f"Errore durante la rimozione dell'attività: {e}")
            finally:
                conn.close()
        else:
            await ctx.send("Errore nell'accesso al DataBase.")


    @commands.command()
    async def ClearAll(self, ctx):
        """
        Elimina tutte le attività salvate dall'utente.
        """
        conn = AccessToDB()
        if conn:
            try: 
                with conn.cursor() as cursor:
                    cursor.execute("SHOW TABLES LIKE 'discordServerT'")
                    result = cursor.fetchone()
                    if result:
                        cursor.execute("SELECT COUNT(*) FROM discordServerT WHERE nome = %s", (str(ctx.author),))
                        result = cursor.fetchone()
                        count = result[0]
                        if count > 0:
                            cursor.execute("DELETE FROM discordServerT WHERE nome = %s;", (str(ctx.author),))
                            conn.commit()
                            await ctx.send("Tutte le attività sono state correttamente eliminate.") 
                        else:
                            await ctx.send("Nessuna attività salvata!")
                    else:
                        await ctx.send("Non è stata ancora creata nessuna attività!")
            except Exception as e:
                await ctx.send(f"Errore durante la rimozione dell'attività: {e}")
            finally:
                conn.close()
        else:
            await ctx.send("Errore nell'accesso al DataBase.")

async def setup(bot): 
    await bot.add_cog(ToDo(bot))   
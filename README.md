# Discord Utility Bot

Bot per Discord sviluppato con Python. 

## Funzionalità

- `!Ping` – Risponde con "Pong!"
- `!Dado` – Risponde con un numero casuale compreso tra 1 e 6.
- `!MagicBall` – Risponde in modo casuale scegliendo tra "Si", "No", "Forse", "Probabilmente", "Decisamente si", "Decisamente no", "Un'altra volta", "Forse in futuro".
- `!TestaOCroce` – Risponde in modo casuale "Testa" o "Croce".
- `!Orario` – Risponde con l'orario attuale con il fuso orario pari a quello impostato sul sistema operativo. 
- `!Info` – Risponde con informazioni sul bot.
- `!Evaluate` – Risponde valutando l'espressione posta nel messaggio.
- `!Weather` – Risponde mostrando Temperatura, Condizione meteo, Umidità e Pressioen nella città scelta. Usa l'API OpenWeather.
- `Add` – Aggiunge l'attività specificata dall'utente nel messaggio alla lista di attività da fare dell'utente (privata per ogni utente).
- `List` – Mostra tutte le attività dell'utente. Essa funziona a pagine, e quindi va specificato il numero della pagina che si vuole vedere (Ogni pagina contiene 5 attività). Di default il numero di pagina è 1.
- `RemoveSpecific` – Rimuove un'attività specifica scelta dall'utente.
- `ClearAll` – Rimuove tutte le attività dell'utente. 

## Setup 

1. Crea un file `.env` con i tuoi seguenti token:
DISCORD_TOKEN=il-tuo-token-discord;
WEATHER_TOKEN=il-tuo-weather-api-token-qui (OpenWeather API)

2. Installa le dipendenze richieste:

pip install -r requirements.txt


3. Avvia il bot:

```bash
python DiscordBot.py
```

## Requisiti

- Python 3.9+
- discord.py 2.x
- python-dotenv
- requests
- pymysql
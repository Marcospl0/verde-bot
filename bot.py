import discord
from discord.ext import commands, tasks
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
API_FOOTBALL_TOKEN = os.getenv("API_FOOTBALL_TOKEN")
API_FOOTBALL_URL = "https://v3.football.api-sports.io/fixtures"
headers = {"x-apisports-key": API_FOOTBALL_TOKEN}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

CANAL_ID = 1382841694642245774  # Canal definido pelo usuário

@bot.event
async def on_ready():
    print(f'Bot VERDE online como {bot.user}')
    enviar_sinal_automatico.start()

@bot.command()
async def sinal(ctx):
    mensagem = gerar_palpite()
    await ctx.send(mensagem)

@tasks.loop(minutes=30)
async def enviar_sinal_automatico():
    canal = bot.get_channel(CANAL_ID)
    if canal:
        mensagem = gerar_palpite()
        await canal.send(mensagem)

def gerar_palpite():
    params = {"league": 71, "season": 2024, "next": 1}
    try:
        response = requests.get(API_FOOTBALL_URL, headers=headers, params=params)
        data = response.json()
        jogo = data['response'][0]['teams']
        home = jogo['home']['name']
        away = jogo['away']['name']
        return f"🌟 PALPITE AUTOMÁTICO DO VERDE:\n{home} x {away}\nSugestão: Ambas equipes marcam ✅"
    except Exception:
        return "⚠️ Erro ao gerar palpite automático."

bot.run(TOKEN)

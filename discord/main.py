import disnake
from disnake.ext import commands
from dotenv import load_dotenv
# from interactions import SlashCommand
import os
from supabase import create_client, Client

# load credentials
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

# instantiate supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
startup = supabase.table("discordlog").insert({"action":"Startup"}).execute()

# instantiate a bot
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='%',
    intents=intents,
    test_guilds=[979375763348406292]
)

@bot.event
async def on_ready():
    print('Ready.')

@bot.event
async def on_message(message):
    if type(message.channel) == disnake.channel.DMChannel:
        if message.content == "ping":
            await message.reply("pong")

bot.load_extension("cogs.Slash")
bot.run(BOT_TOKEN)
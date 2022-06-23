import disnake
from disnake.ext import commands
from dotenv import load_dotenv
# from interactions import SlashCommand
import os
from supabase import create_client, Client


SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

async def send_event(event: dict):
    supabase.table("event").insert(event).execute()
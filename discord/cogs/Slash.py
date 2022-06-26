import asyncio
import disnake
from disnake.ext import commands
from typing import List
from datetime import datetime, timezone, timedelta
import sys
sys.path.append('..')
from connection import supabaseinteraction
import pytz
# from interactions import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    local_tz = pytz.timezone('Asia/Singapore')

    def utc_to_local(utc_dt):
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(Slash.local_tz)
        return Slash.local_tz.normalize(local_dt).strftime("%d/%m/%Y, %H%M")

    # autocompleteOptions = ["a", "b", "c", "d", "e"]

    async def autocomplete_options(inter, string: str) -> List[str]:
        return [x for x in ["a", "b", "c", "d", "e"] if string.lower() in x.lower()]

    @commands.slash_command(description="Test command")
    async def test(inter):
        embed = disnake.Embed(title="Working")
        await inter.response.send_message(embeds=[embed])

    @commands.slash_command(description="Return your UID")
    async def myid(inter):
        await inter.response.send_message(str(inter.author.id))

    @commands.slash_command(description="Create an Event, specify date as DDMMYY, time in HHMM, and duration in hours")
    async def createevent(inter, activity: str, date: str, time: str, duration: int = 0):
        if(len(date) != 6 or len(time) != 4):
            await inter.response.send_message("Invalid Date/Time!")
            return
        day = int(date[0:2])
        month = int(date[2:4])
        year = int(date[4:]) + 2000
        hour = int(time[0:2]) - 8
        minute = int(time[2:])
        
        try:
            scheduled = datetime(year, month, day, hour, minute)
            ts = scheduled.isoformat() 
            event = {
                "activity": activity,
                "starttime": ts,
                "duration": duration,
                "discgrp": inter.channel_id
            }
            await supabaseinteraction.send_event(event)
            metadata = disnake.GuildScheduledEventMetadata()
            metadata.location = "Somewhere"
            await inter.guild.create_scheduled_event(
                name = activity,
                entity_type = disnake.GuildScheduledEventEntityType(3),
                entity_metadata = metadata,
                scheduled_start_time = scheduled,
                scheduled_end_time = datetime(year, month, day, hour + 1, minute)
            )
            await inter.response.send_message(str(inter.author.id))
        except ValueError:
            await inter.response.send_message("Invalid Date/Time!")
        # except:
        #     await inter.response.send_message("Something went wrong...")
            

        

    @commands.slash_command(description="Edit an event")
    async def editevent(inter, action: str, activty: str, x):
        await inter.response.send_message(str(inter.author.id))

    @commands.slash_command(description="List all events")
    async def listevent(inter):
        x = map(
            lambda x: x.name + " at \"" + x.entity_metadata.location + "\" on " + Slash.utc_to_local(x.scheduled_start_time) + "hrs. ",
            await inter.guild.fetch_scheduled_events()
        )
        await inter.response.send_message('\n'.join(x))


    @commands.slash_command(description="Return your UID")
    async def autocomplete(
        inter,
        text: str = commands.Param(autocomplete=autocomplete_options)
    ):
        await inter.response.send_message(text)
    
def setup(bot):
    bot.add_cog(Slash(bot))
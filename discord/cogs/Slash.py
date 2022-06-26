import disnake
from disnake.ext import commands
from typing import List
from datetime import datetime
import sys
sys.path.append('..')
from connection import supabaseinteraction
# from interactions import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # autocompleteOptions = ["a", "b", "c", "d", "e"]

    async def autocomplete_options(inter, string: str) -> List[str]:
        return [x for x in ["a", "b", "c", "d", "e"] if string.lower() in x.lower()]

    @commands.slash_command(description="Test command")
    async def test(ctx):
        embed = disnake.Embed(title="Working")
        await ctx.response.send_message(embeds=[embed])

    @commands.slash_command(description="Return your UID")
    async def myid(ctx):
        await ctx.response.send_message(str(ctx.author.id))

    @commands.slash_command(description="Create an Event, specify date as DDMMYY, time in HHMM, and duration in hours")
    async def createevent(ctx, activity: str, date: str, time: str, duration: int = 0):
        if(len(date) != 6 or len(time) != 4):
            await ctx.response.send_message("Invalid Date/Time!")
            return
        day = int(date[0:2])
        month = int(date[2:4])
        year = int(date[4:]) + 2000
        hour = int(time[0:2]) - 8
        minute = int(time[2:])
        try:
            ts = datetime(year, month, day, hour, minute).isoformat() 
            event = {
                "activity": activity,
                "starttime": ts,
                "duration": duration,
                "discgrp": ctx.channel_id
            }
            await supabaseinteraction.send_event(event)
            await ctx.response.send_message(str(ctx.author.id))
        except ValueError:
            await ctx.response.send_message("Invalid Date/Time!")

        

    @commands.slash_command(description="Edit an event")
    async def editevent(ctx, action: str, activty: str, x):
        await ctx.response.send_message(str(ctx.author.id))

    @commands.slash_command(description="Return your UID")
    async def autocomplete(
        ctx,
        text: str = commands.Param(autocomplete=autocomplete_options)
    ):
        await ctx.response.send_message(text)
    
def setup(bot):
    bot.add_cog(Slash(bot))
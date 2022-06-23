import xdrlib
import disnake
from disnake.ext import commands
from typing import List
from datetime import date
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

    @commands.slash_command(description="Create an Event, specify date as DDMMYY, and duration in hours")
    async def createevent(ctx, activity: str, day: str, duration: int = 0):
        event = {
            "activity": activity,
            "duration": duration,
        }
        await supabaseinteraction.send_event(event)
        await ctx.response.send_message(str(ctx.author.id))

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
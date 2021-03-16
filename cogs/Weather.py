import discord
from discord.ext import commands

from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

# pyowm Settings
owm = OWM('21a163c142a502fa9a2bfddfaf0849ce')
mgr = owm.weather_manager()

class Weather(commands.Cog):
    def __init__(self):
        self.client = client
    
    @commands.command()
    async def weather(self, ctx, location=None):
        if location is None:
            location = 'Don Mueang,TH'

        observation = mgr.weather_at_place(location)
        w = observation.weather

        await ctx.send(temp.temp for temp in w.temperature('celsius'))


def setup(client):
    client.add_cog(Weather(client))
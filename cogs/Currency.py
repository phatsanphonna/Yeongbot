import discord
from discord.ext import commands

from currency_converter import CurrencyConverter
c = CurrencyConverter()


class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def convert(self, ctx, *, convert_text):
        convert_text = str(input())
        currency1, currency2 = convert_text.split(' to ')
        amount, currency1 = currency1.split(' ')

        converted_currency = c.convert(int(amount), currency1, currency2)

        await ctx.send(f'{currency1} {amount} is equal {currency2} {converted_currency:.3}')


def setup(client):
    client.add_cog(Currency(client))

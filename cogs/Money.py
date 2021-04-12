import discord
from discord.ext import commands

from currency_converter import CurrencyConverter
c = CurrencyConverter()


class Money(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def convert(self, ctx, *, convert_text):
        currency1, currency2 = convert_text.split(' to ')
        amount, currency1 = currency1.split(' ')

        converted_currency = c.convert(float(amount), currency1.upper(), currency2.upper())

        await ctx.send(f'{currency1} {amount} is equals {currency2} {converted_currency:.3}')

    @commands.command()
    async def currency(self, ctx, convert_c):
        currency = c.convert(1, convert_c, 'THB')

        await ctx.send(f'1 {convert_c} is equals {currency:.2f} Thai Baht')


def setup(client):
    client.add_cog(Money(client))

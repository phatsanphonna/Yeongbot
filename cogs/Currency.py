import discord
from discord.ext import commands

import json


class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stats(self, ctx, member):
        with open('users.json', encoding='utf-8') as f:
            users = json.load(f)

        if str(ctx.author.id) not in users:
            data = {
                str(ctx.author.id): {
                    'relations': 100
                }
            }
            users.update(data)

            with open('users.json', 'w', encoding='utf-8') as f:
                json.dump(users, f)
        else:
            users[str(ctx.author.id)]['money'] += 1
            await ctx.send(users[str(ctx.author.id)]['money'])


def setup(client):
    client.add_cog(Currency(client))

import discord
from discord.ext import commands

import json


class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def money(self, ctx):
        with open('users.json', encoding='utf-8') as f:
            users = json.load(f)

        if str(ctx.author.id) not in users:
            users[str(ctx.author.id)]['relations'] = 1
            users[str(ctx.author.id)]['relations'] = 1
            
            with open('users.json', 'w', encoding='utf-8') as f:
                json.dump(users, f)
        
        print(users)


def setup(client):
    client.add_cog(Currency(client))

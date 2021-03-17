import discord
from discord.ext import commands
import random
import asyncio
import requests
import os
import json

# * lINE Bot Notifications
linebot_url = 'https://notify-api.line.me/api/notify'
linebot_token = os.environ['line_token']
linebot_headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer '+linebot_token
}

CRIT_RATE = 33
CRIT2X_RATE = 35
CRIT_MULTIPLY_RATE1, CRIT_MULTIPLY_RATE2 = 1, 2


class MessageEvent(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        sender = message.author

        # ? Check is sender = client?
        if sender == self.client.user:
            return

        # ? When users mention the client.
        if self.client.user.mentioned_in(message):
            await message.channel.send(
                f"น้อง {sender.display_name} เรียกน้องหยองหรอคะ?\n"
                + "สามารถเรียกน้องหยองได้โดยพิมพ์ .help ในช่องแชทเลย"
            )

        # ? When users mention the guild owner.
        if message.guild:
            if message.guild.owner.mentioned_in(message):
                if sender.bot:
                    return
                else:
                    msg = f'{sender.name} has mention you on {message.guild.name}, {message.channel.name}'
                    r = requests.post(linebot_url, headers=linebot_headers,
                                      data={'message': msg})
                    print('LINE Pinging:', r.text)
                    return

        # ? When users type "ควย"
        kuy = ['kuy', 'ควย']
        for kuy in kuy:
            if kuy in message.content.lower():
                await message.channel.send("เป็นเหี้ยอะไรหล่ะ")
                return

        # ? If user type "เหี้ย"
        here = ['เชี่ย', 'เหี้ย', 'here']
        for here in here:
            if here in message.content.lower():
                if sender.bot:
                    return
                else:
                    here_msg = [
                        'มีปัญหาหรอสัส!',
                        'เป็นควยไรหล่ะ',
                        'อยากมีปัญหาหรอวะ'
                    ]
                    rd = random.choice(here_msg)

                    await message.channel.send(f'{rd}')
                    return

        # ? If user type "เงียบ"
        if 'เงียบ' in message.content.lower():
            await message.channel.send(
                f"ก็กูอยากเงียบอ่ะ มีปัญหาหรอวะ แน่จริง 1-1 หลังเซเว่นปิดดิ {sender.mention}"
            )
            return

        # ? If user type "sundick"
        sundick = ['sundick', 'ซันดิ้ก', 'mute me senpai']
        for sundick in sundick:
            if sundick in message.content.lower():
                with open('users.json', 'r') as f:
                    users = json.load(f)
                f'''
                    # ! = ALGORITHM EXPLAINED =
                    This is a random that user will get mute
                    # ? if mute_rate is below {CRIT_RATE} will get muted but:
                            if user get crit_rate below {CRIT2X_RATE}
                                will get critical mute(critical range: 1.0-2.0),
                            else is user got 5 second mute
                        else is 'You are free!'
                '''

                mute_rate = random.randint(1, 100)

                # ! If user random a number that hit mute rate
                if mute_rate <= CRIT_RATE:
                    counting = int()
                    crit_rate = int(random.randint(1, 100))

                    # ? If user random a number that hit critical rate
                    if crit_rate <= CRIT2X_RATE:
                        crit_multiply = float('{:.2f}'.format(
                            random.uniform(CRIT_MULTIPLY_RATE1,
                                           CRIT_MULTIPLY_RATE2)
                        ))
                        timer = int(5*crit_multiply)
                        await message.channel.send(
                            f":crossed_swords: `ติดคริติคอล` **{int(100*(crit_multiply-1.00))}%**\n"
                            + f"น้อง {sender.display_name} โดนปิดไมค์ไป `{timer}` วินาที"
                        )
                        pass

                    else:
                        timer = int(5)
                        await message.channel.send(
                            f"น้อง {sender.display_name} โดนปิดไมค์ไป `{timer}` วินาที"
                        )
                        pass

                    await sender.edit(mute=True, deafen=True)

                    for _ in range(timer):
                        counting += 1
                        await asyncio.sleep(1)

                        while counting >= timer:
                            await sender.edit(mute=False, deafen=False)
                            break

                else:
                    await message.channel.send(
                        f"น้อง {sender.display_name} โชคดีที่ไม่โดนปิดไมค์ไปนะ "
                        + "แต่ครั้งหน้าก็ระวังไว้ด้วยละกันหล่ะ"
                    )
                return
        sleep = ['ง่วง', 'อยากนอน']
        for sleep in sleep:
            if sleep in message.content.lower():
                await message.channel.send('ไปนอนสิ')

                msg = await self.client.wait_for(
                    'message',
                    check=lambda channel: message.channel == message.channel
                )

                yes = ['ได้', 'โอเค', 'ด้าย', 'yes']
                for yes in yes:
                    if yes in msg.content.lower():
                        await message.channel.send('Good Job!')
                        break

                no = ['ไม่', 'no']
                for no in no:
                    if no in msg.content.lower():
                        await message.channel.send('ทำไมไม่ไปนอนหล่ะ บอกให้ไปนอนไง!')
                        break


async def update_data(users, user):
    users[user.id] = {}
    users[user.id]['relation_score'] = 100


async def add_relation_score(users, user, relation_score):
    users[user.id]['relation_score'] += relation_score


async def remove_relation_score(users, user, relation_score):
    users[user.id]['relation_score'] -= relation_score


def setup(client):
    client.add_cog(MessageEvent(client))

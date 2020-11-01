import discord
from bot.settings import SERVER_ID


class Broadcast(discord.Client):
    async def get_all_channels(self):
        channels = []
        for server in self.guilds:
            if server.id == int(SERVER_ID):
                for channel in server.text_channels:
                    if 'privado' in channel.name:
                        channels.append(channel)
        return channels

    async def on_ready(self):
        print(f'We have logged in as {self.user}!')

    async def send_all(self, message):
        message_to_send = message.replace('/broadcast', '')
        for channel in await Broadcast.get_all_channels(self):
            await channel.send(message_to_send)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.guild.id == int(SERVER_ID) and message.content.lower().startswith('/broadcast'):
            for role in message.author.roles:
                if role.name == 'Organização':
                    # await message.delete()
                    await Broadcast.send_all(self, message.content)
                    await message.add_reaction('👌')

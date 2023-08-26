from discord import Bot
from discord.ext.commands import Cog

from config import TOKEN
from cog_manager import CogManager

class DiscordBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_cog(CogManager(self))

    def run(self):
        super().run(TOKEN)

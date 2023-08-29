from discord import ApplicationContext, Bot, ExtensionNotFound, ExtensionAlreadyLoaded, ExtensionNotLoaded, ExtensionFailed, Permissions, SlashCommandGroup
from discord.ext.commands import Cog
from json import loads

from typing import Union


class CogManager(Cog):
    cogs_config: dict[str, dict[str, Union[str, bool]]] = {}
    cogs_name_map: dict[str, str]
    permissions = Permissions.none()
    permissions.update(administrator=True)
    group = SlashCommandGroup(
        name="cogs",
        description="Manage Cogs",
        default_member_permissions=permissions
    )

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.load_config()
        self.bot.load_extensions(*[
            data["path"]
            for data in filter(lambda data: data["load"], self.cogs_config.values())
        ])

    def load_config(self):
        with open("cogs/config.json", "rb") as cogs_config_file:
            cogs_config: dict[str, dict[str, Union[str, bool]]] = loads(
                cogs_config_file.read())
        self.cogs_config = cogs_config
        self.cogs_name_map = {
            data["name"]: data["path"]
            for data in cogs_config.values()
        }

    def cog_name2path(self, cog_name):
        return self.cogs_name_map[cog_name] if cog_name in self.cogs_name_map.keys() else cog_name

    @group.command()
    async def reload_config(self, ctx: ApplicationContext):
        self.load_config()
        await ctx.respond(content="Config reloaded.", ephemeral=True)

    @group.command()
    async def list(self, ctx: ApplicationContext):
        active_cogs = set(self.bot.cogs.keys())
        results = []
        for class_name, data in self.cogs_config.items():
            results.append("\n".join([
                f"{class_name}:"
                f"   - name:   {data['name']}"
                f"   - path:   {data['path']}"
                f"   - enable: {class_name in active_cogs}"
            ]))
        results = "\n\n" + "\n".join(results)
        await ctx.respond(content=f"```Both of cogs' name and path can be used in load/unload cogs.{results}```", ephemeral=True)

    @group.command()
    async def load(self, ctx: ApplicationContext, *, cog_name: str):
        cog_name = self.cog_name2path(cog_name)
        try:
            self.bot.load_extension(cog_name)
            content = f"`{cog_name}` loaded."
        except ExtensionNotFound:
            content = f"`{cog_name}` not found."
        except ExtensionAlreadyLoaded:
            content = f"`{cog_name}` is already loaded."
        except ExtensionFailed:
            content = f"`{cog_name}` load failed."
        finally:
            await ctx.respond(content=content, ephemeral=True)

    @group.command()
    async def unload(self, ctx: ApplicationContext, *, cog_name: str):
        cog_name = self.cog_name2path(cog_name)
        try:
            self.bot.unload_extension(cog_name)
            content = f"`{cog_name}` unloaded."
        except ExtensionNotFound:
            content = f"`{cog_name}` not found."
        except ExtensionNotLoaded:
            content = f"`{cog_name}` was not loaded."
        finally:
            await ctx.respond(content=content, ephemeral=True)

    @group.command()
    async def reload(self, ctx: ApplicationContext, *, cog_name: str):
        cog_name = self.cog_name2path(cog_name)
        try:
            self.bot.reload_extension(cog_name)
            content = f"`{cog_name}` reloaded."
        except ExtensionNotFound:
            content = f"`{cog_name}` not found."
        except ExtensionNotLoaded:
            content = f"`{cog_name}` was not loaded."
        except ExtensionFailed:
            content = f"`{cog_name}` reload failed."
        finally:
            await ctx.respond(content=content, ephemeral=True)

from discord import ApplicationContext, Bot, Option
from discord.ext.commands import BucketType, Cog, CommandOnCooldown, CommandError, Context, cooldown, slash_command

from config import VALID_ROLE

ENG_MAP = {
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 4,
    "H": 6,
    "I": 7,
    "K": 9,
    "L": 10,
    "M": 11,
    "N": 12,
    "P": 13,
    "Q": 14,
    "R": 15,
    "S": 16,
    "T": 17,
    "U": 18,
    "V": 19,
    "W": 20,
    "Z": 22,
}

def validator(sid: str):
    if len(sid) != 9:
        return False
    result = 0
    for i, c in enumerate(sid[:-1], 1):
        c = ENG_MAP[c.upper()] if i == 1 else int(c)
        result += c * i
    return result % 10 == int(sid[-1])

class Validation(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @slash_command()
    @cooldown(1, 15, BucketType.user)
    async def valid(self, ctx: ApplicationContext, *, sid: Option(str, description="請輸入學號以進行驗證(部分學系學號前兩碼均為英文者，請洽管理員辦理人工驗證)。", name="學號")):
        
        try:
            if validator(sid):
                print(f"[Validator]: {ctx.author} - {sid} - Success")
                await ctx.respond("驗證通過。", ephemeral=True)
                valid_role = ctx.author.guild.get_role(VALID_ROLE)
                await ctx.author.add_roles(valid_role, reason=f"{ctx.author.display_name}驗證通過，學號: {sid}")
            else:
                print(f"[Validator]: {ctx.author} - {sid} - Failed")
                await ctx.respond("驗證未通過，請於15秒後重新嘗試，或洽管理員進行人工驗證。", ephemeral=True)
        except:
            print(f"[Validator]: {ctx.author} - {sid} - Error")
            await ctx.respond("發生錯誤，學號前兩碼均為英文者，請洽管理員辦理人工驗證。", ephemeral=True)

    @valid.error
    async def valid_error(self, ctx: ApplicationContext, error: CommandError):
        if isinstance(error, CommandOnCooldown):
            await ctx.respond(f"驗證冷卻中，請於 `{format(error.retry_after, '.1f')}` 秒後重新嘗試。", ephemeral=True)

def setup(bot: Bot):
    bot.add_cog(Validation(bot))

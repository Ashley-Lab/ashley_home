from disnake.ext import commands
from resources.check import check_it
from resources.db import Database


class Miner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.group(name='miner', aliases=['minerador'])
    async def miner(self, ctx):
        await ctx.send("Em desenvolvimento...")


def setup(bot):
    bot.add_cog(Miner(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mMINER_GROUP\033[1;32m foi carregado com sucesso!\33[m')

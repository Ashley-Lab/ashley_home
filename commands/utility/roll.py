import random

from discord.ext import commands
from resources.check import check_it
from resources.db import Database

result = None


class DadoClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='roll', aliases=['rolar'])
    async def roll(self, ctx, dice: str = 'none'):
        """Comando usado pra rolar um dado
        Use ash roll xdy, x sendo o numero de dados e y o numero do dado"""
        if dice == 'none':
            return await ctx.send('<:alert:739251822920728708>│` Você precisa dizer: quantos e qual tipo de '
                                  'dado você quer rolar!`')
        try:
            rolls, limit = map(int, dice.split('d'))
        except ValueError:
            await ctx.send('<:alert:739251822920728708>│`Não foi um formato:` **N**`d`**N**!')
            return
        global result
        result = ''
        if rolls > 99:
            return await ctx.send('<:alert:739251822920728708>│`Número muito grande de dados!`')
        if limit > 99999:
            return await ctx.send('<:alert:739251822920728708>│`Número muito grande de lados!`')
        for r in range(rolls):
            result += ''.join(str(random.randint(1, limit))) + ', '
        await ctx.send(f'```{result[:-1]}```')


def setup(bot):
    bot.add_cog(DadoClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mROLARDADO\033[1;32m foi carregado com sucesso!\33[m')

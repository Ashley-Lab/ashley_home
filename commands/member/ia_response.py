import disnake

from disnake.ext import commands
from resources.check import check_it
from resources.db import Database


class IaResponseClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='ia', aliases=['ai'])
    async def ia(self, ctx):
        """comando para habilitar/desabilitar a iteração com a IA da ashley
        use ash ia ou ash ai"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        update['user']['ia_response'] = not update['user']['ia_response']
        response = update['user']['ia_response']
        await self.bot.db.update_data(data, update, "users")
        if response:
            embed = disnake.Embed(
                color=disnake.Color.green(),
                description=f'<:confirmed:721581574461587496>│`Interação com a Inteligencia Artificial '
                            f'habilitada com sucesso!`')
            await ctx.send(embed=embed)
        else:
            embed = disnake.Embed(
                color=disnake.Color.red(),
                description=f'<:negate:721581573396496464>│`Interação com a Inteligencia Artificial '
                            f'desabilitada com sucesso!`')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(IaResponseClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mIA_RESPONSE\033[1;32m foi carregado com sucesso!\33[m')

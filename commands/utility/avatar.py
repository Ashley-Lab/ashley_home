import discord

from resources.check import check_it
from discord.ext import commands
from resources.db import Database


class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='avatar', aliases=['a'])
    async def avatar(self, ctx):
        """Comando usado pra ter uma imagem ampliada do avatar de um usuario
        Use ash avatar <usuario em questão>"""
        try:
            user = ctx.message.mentions[0]
        except IndexError:
            user = ctx.author

        embed = discord.Embed(
            title="Avatar de: {}".format(user.name),
            color=self.color)
        embed.set_image(url=user.avatar_url)
        embed.set_footer(text="Pedido por {}#{}".format(ctx.author.name, ctx.author.discriminator))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Avatar(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mAVATAR\033[1;32m foi carregado com sucesso!\33[m')

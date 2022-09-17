import disnake

from disnake.ext import commands
from resources.check import check_it
from resources.db import Database


class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='userinfo', aliases=['infouser', 'ui', 'iu'])
    async def userinfo(self, ctx, member: disnake.Member = None):
        """comando que da uma lista de informações sobre o usuario
        Use ash userinfo <@usuario em questão>"""
        if member is None:
            member = ctx.author

        data = await self.bot.db.get_data("user_id", member.id, "users")
        if data is not None:
            link = f'{self.bot.config["config"]["site"]}/user/{member.id}'
            database = f"**[Clique Aqui]({link})**"
        else:
            database = "USUARIO NAO CADASTRADO"

        role = ",".join([r.mention for r in member.roles if r.name != "@everyone"])
        role = "Você não tem cargos" if len(role) == 0 else role
        userjoinedat = member.joined_at
        usercreatedat = member.created_at

        embed = disnake.Embed(
            title=":pushpin:Informações pessoais de:",
            color=self.color,
            description=member.name
        )
        embed.add_field(name=":door:Entrou no server em:", value=f"<t:{userjoinedat:%s}:f>", inline=True)
        embed.add_field(name="📅Conta criada em:", value=f"<t:{usercreatedat:%s}:f>", inline=True)
        embed.add_field(name="💻ID:", value=str(member.id), inline=True)
        embed.add_field(name=":label:Tag:", value=str(member.discriminator), inline=True)
        embed.add_field(name="Cargos:", value=role, inline=True)
        embed.add_field(name="DataBase:", value=database)
        embed.set_footer(text=f"Pedido por {ctx.author}")
        embed.set_thumbnail(url=str(member.display_avatar))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(UserInfo(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mUSERINFO\033[1;32m foi carregado com sucesso!\33[m')

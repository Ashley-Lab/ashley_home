import disnake

from disnake.ext import commands
from random import randint
from resources.check import check_it
from resources.db import Database
from asyncio import TimeoutError
from datetime import datetime


class PokemonClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='pokemon', aliases=['poke'])
    async def pokemon(self, ctx):
        """QUEM É ESSE POKEMON?
        Use ash pokemon ou ash poke pra jogar"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        try:
            if data['inventory']['coins']:
                pass
        except KeyError:
            embed = disnake.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│`VOCE NÃO TEM FICHA!`')
            return await ctx.send(embed=embed)

        ct = 25
        if data['rpg']['active']:
            date_old = data['rpg']['activated_at']
            date_now = datetime.today()
            days = abs((date_old - date_now).days)
            if days <= 10:
                ct = 5

        if data['inventory']['coins'] > ct and ctx.author.id not in self.bot.jogando:
            self.bot.jogando.append(ctx.author.id)

            def check(m):
                return m.author == ctx.author

            pokemon = self.bot.config['poke']['list']
            response = pokemon[randint(0, 399)]
            embed = disnake.Embed(
                title='QUAL O NOME DESSE POKEMON?',
                color=self.color,
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
            embed.set_image(url=response['foto'])
            await ctx.send(embed=embed)

            if ctx.author.id == self.bot.owner_ids[0]:
                await ctx.send(f"`OLÁ MESTRE, SUA RESPOSTA É:` **{response['nome'].upper()}**")

            try:
                answer = await self.bot.wait_for('message', check=check, timeout=30.0)
            except TimeoutError:
                self.bot.jogando.remove(ctx.author.id)
                return await ctx.send('<:negate:721581573396496464>│`Desculpe, você demorou muito:` **COMANDO'
                                      ' CANCELADO**')

            update['inventory']['coins'] -= ct
            if answer.content.upper() == response['nome'].upper():
                await ctx.send(f'<:rank:519896825411665930>│`VOCÊ ACERTOU!` 🎊 **PARABENS** 🎉 `O pokemon era` '
                               f'**{response["nome"]}** `e vc respondeu` **{answer.content}** `Ganhou 12 pontos!`')
                update['config']['points'] += 12
            else:
                await ctx.send(f'<:negate:721581573396496464>│`O pokemon era` **{response["nome"]}** `e vc '
                               f'respondeu` **{answer.content}** `INFELIZMENTE VOCE PERDEU! LOGO PERDE 8 PONTOS`')

                if update['config']['points'] - 8 >= 0:
                    update['config']['points'] -= 8
                else:
                    update['config']['points'] = 0

            self.bot.jogando.remove(ctx.author.id)
            await self.bot.db.update_data(data, update, 'users')
        else:
            if ctx.author.id in self.bot.jogando:
                await ctx.send('<:alert:739251822920728708>│`VOCÊ JÁ ESTÁ JOGANDO!`')
            else:
                await ctx.send(f'<:alert:739251822920728708>│`VOCÊ PRECISA DE + DE {ct} FICHAS PARA JOGAR`\n'
                               f'**OBS:** `USE O COMANDO` **ASH SHOP** `PARA COMPRAR FICHAS!`')


def setup(bot):
    bot.add_cog(PokemonClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mPOKEMONCLASS\033[1;32m foi carregado com sucesso!\33[m')

import discord

from discord.ext import commands
from random import randint
from resources.check import check_it
from resources.db import Database
from asyncio import TimeoutError
from datetime import datetime


class CardsClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='card', aliases=['carta', 'yugioh'])
    async def card(self, ctx):
        """use ash cards e tente adivinhar que carta de yugioh esta na tela"""

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        try:
            if data['inventory']['coins']:
                pass
        except KeyError:
            embed = discord.Embed(
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

            cards = self.bot.config['cards']['list']
            card = cards[randint(0, 399)]
            embed = discord.Embed(
                title='QUAL O NOME DESSA CARTA?',
                color=self.color,
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_image(url=card['foto'])
            await ctx.send(embed=embed)

            if ctx.author.id == self.bot.owner_id:
                await ctx.send(f"`OLÁ MESTRE, SUA RESPOSTA É:` **{card['nome'].upper()}**")

            try:
                answer = await self.bot.wait_for('message', check=check, timeout=30.0)
            except TimeoutError:
                self.bot.jogando.remove(ctx.author.id)
                return await ctx.send('<:negate:721581573396496464>│`Desculpe, você demorou muito:` **COMANDO'
                                      ' CANCELADO**')

            update['inventory']['coins'] -= ct
            if answer.content.upper() == card['nome'].upper():
                await ctx.send(f'<:rank:519896825411665930>│`VOCÊ ACERTOU!` 🎊 **PARABENS** 🎉 `A carta era` '
                               f'**{card["nome"]}** `e vc respondeu` **{answer.content}** `Ganhou 12 pontos!`')
                update['config']['points'] += 12
            elif len([name for name in answer.content.upper().split() if len(name) >= 2 and
                     name in card['nome'].upper().split()]) > (len(card['nome'].upper().split()) / 2):
                await ctx.send(f'<:rank:519896825411665930>│`VOCÊ QUASE ACERTOU!` 🎊 **PARABENS** 🎉 `A carta era`'
                               f' **{card["nome"]}** `e vc respondeu` **{answer.content}** `Ganhou 4 pontos!`')
                update['config']['points'] += 4
            else:
                await ctx.send(f'<:negate:721581573396496464>│`A carta era` **{card["nome"]}** `e vc respondeu` '
                               f'**{answer.content}** `INFELIZMENTE VOCE PERDEU! LOGO PERDE 8 PONTOS`')

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
    bot.add_cog(CardsClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mCARDSCLASS\033[1;32m foi carregado com sucesso!\33[m')

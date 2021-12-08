import disnake

from random import choice
from disnake.ext import commands
from resources.db import Database
from resources.check import check_it


class HugClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='hug', aliases=['abraço', 'abraco'])
    async def hug(self, ctx, member: disnake.Member = None):
        """Comando de gifs de abraço
        Use ash hug <@usuario a sua escolha>"""
        if member is None:
            return await ctx.send("<:alert:739251822920728708>│`Você precisa mencionar alguem!`")
        try:
            await ctx.message.delete()
        except disnake.errors.Forbidden:
            pass
        try:
            hug_img = ['http://media1.tenor.com/images/e58eb2794ff1a12315665c28d5bc3f5e/tenor.gif?itemid=10195705',
                       'http://media1.tenor.com/images/949d3eb3f689fea42258a88fa171d4fc/tenor.gif?itemid=4900166',
                       'http://media1.tenor.com/images/11889c4c994c0634cfcedc8adba9dd6c/tenor.gif?itemid=5634578',
                       'http://media1.tenor.com/images/d7529f6003b20f3b21f1c992dffb8617/tenor.gif?itemid=4782499',
                       'https://media1.tenor.com/images/7db5f172665f5a64c1a5ebe0fd4cfec8/tenor.gif?itemid=9200935',
                       'https://media1.tenor.com/images/1069921ddcf38ff722125c8f65401c28/tenor.gif?itemid=11074788',
                       'https://media1.tenor.com/images/3c83525781dc1732171d414077114bc8/tenor.gif?itemid=7830142']
            hug = choice(hug_img)
            hug_embed = disnake.Embed(title='Abraço :heart:',
                                      description='**{}** Ele(a) recebeu um abraço de **{}**! Que casal fofo! '
                                                  ':heart_eyes: '.format(member.name, ctx.author.name),
                                      color=self.color)
            hug_embed.set_image(url=hug)
            hug_embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=hug_embed)

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            try:
                update['ship'][str(member.id)] += 5
            except KeyError:
                update['ship'][str(member.id)] = 5
            await self.bot.db.update_data(data, update, 'users')

        except IndexError:
            await ctx.send(
                '<:negate:721581573396496464>│`Você precisa mencionar um usuário específico para abraçar!`')


def setup(bot):
    bot.add_cog(HugClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mABRAÇO\033[1;32m foi carregado com sucesso!\33[m')

import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from random import choice
from asyncio import sleep, TimeoutError


git = ["https://media1.tenor.com/images/adda1e4a118be9fcff6e82148b51cade/tenor.gif?itemid=5613535",
       "https://media1.tenor.com/images/daf94e676837b6f46c0ab3881345c1a3/tenor.gif?itemid=9582062",
       "https://media1.tenor.com/images/0d8ed44c3d748aed455703272e2095a8/tenor.gif?itemid=3567970",
       "https://media1.tenor.com/images/17e1414f1dc91bc1f76159d7c3fa03ea/tenor.gif?itemid=15744166",
       "https://media1.tenor.com/images/39c363015f2ae22f212f9cd8df2a1063/tenor.gif?itemid=15894886"]


class MeltedClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.i = self.bot.items
        self.art = ["braço_direito", "braço_esquerdo", "perna_direita", "perna_esquerda", "the_one", "anel", "balança",
                    "chave", "colar", "enigma", "olho", "vara", "aquario", "aries", "cancer", "capricornio",
                    "escorpiao", "gemeos", "leao", "peixes", "sargitario", "libra", "touro", "virgem"]

        self.cost = {
            "solution_agent_green": 3,
            "solution_agent_blue": 3,
            "nucleo_xyz": 2,
            "enchanted_stone": 1,
            "Discharge_Crystal": 5,
            "Acquittal_Crystal": 5,
            "Crystal_of_Energy": 5,
            "crystal_of_death": 1
        }

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='melted', aliases=['derreter', 'melt'])
    async def melted(self, ctx):
        """Comando especial para derreter artefatos, criando o item artefato derretido"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        msg = f"\n".join([f"{self.i[k][0]} `{v}` `{self.i[k][1]}`" for k, v in self.cost.items()])
        msg += "\n\n**OBS:** `PARA CONSEGUIR OS ITENS VOCE PRECISA USAR O COMANDO` **ASH BOX**"

        Embed = discord.Embed(
            title="O CUSTO PARA VOCE DERRETER UM ARTEFATO:",
            color=self.bot.color,
            description=msg)
        Embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        Embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
        Embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        await ctx.send(embed=Embed)

        artifacts = []
        for i_, amount in data['inventory'].items():
            if i_ in self.art:
                artifacts += [i_] * amount

        if len(artifacts) < 3:
            return await ctx.send("<:negate:721581573396496464>│`Voce nao tem o minimo de 3 arfetados...`\n"
                                  "**Obs:** `VOCE CONSEGUE ARTEFATOS USANDO O COMANDO` **ASH RIFA** `E PEGANDO"
                                  " UM ARTEFATO REPETIDO.`")

        cost = {}
        for i_, amount in self.cost.items():
            if i_ in data['inventory']:
                if data['inventory'][i_] < self.cost[i_]:
                    cost[i_] = self.cost[i_]
            else:
                cost[i_] = self.cost[i_]

        if len(cost) > 0:
            msg = f"\n".join([f"{self.i[key][0]} **{key.upper()}**" for key in cost.keys()])
            return await ctx.send(f"<:alert:739251822920728708>│`Lhe faltam esses itens para derreter um arfetafo:`"
                                  f"\n{msg}\n`OLHE SEU INVENTARIO E VEJA A QUANTIDADE QUE ESTÁ FALTANDO.`")

        def check_option(m):
            return m.author == ctx.author and m.content == '0' or m.author == ctx.author and m.content == '1'

        msg = await ctx.send(f"<:alert:739251822920728708>│`VOCE JA TEM TODOS OS ITEM NECESSARIOS, DESEJA DERRETER "
                             f"SEUS ARTEFATOS AGORA?`\n**1** para `SIM` ou **0** para `NÃO`")
        try:
            answer = await self.bot.wait_for('message', check=check_option, timeout=30.0)
        except TimeoutError:
            await msg.delete()
            return await ctx.send("<:negate:721581573396496464>│`COMANDO CANCELADO!`")
        if answer.content == "0":
            await msg.delete()
            return await ctx.send("<:negate:721581573396496464>│`COMANDO CANCELADO!`")
        await msg.delete()

        msg = await ctx.send("<a:loading:520418506567843860>│`Escolhendo 3 artefatos para derreter...`")
        await sleep(2)
        art1 = choice(artifacts)
        await msg.edit(content=f"<:confirmed:721581574461587496>│`O primeiro foi` {self.i[art1][0]} **{art1}**")
        await sleep(2)
        artifacts.remove(art1)
        art2 = choice(artifacts)
        await msg.edit(content=f"<:confirmed:721581574461587496>│`O segundo foi` {self.i[art2][0]} **{art2}**")
        await sleep(2)
        artifacts.remove(art2)
        art3 = choice(artifacts)
        await msg.edit(content=f"<:confirmed:721581574461587496>│`O terceiro foi` {self.i[art3][0]} **{art3}**")
        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│`removendo os itens de custo e os artefatos da sua "
                               f"conta...`")
        for i_, amount in self.cost.items():
            update['inventory'][i_] -= amount
            if update['inventory'][i_] < 1:
                del update['inventory'][i_]

        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│`removendo 1/3`")

        update['inventory'][art1] -= 1
        if update['inventory'][art1] < 1:
            del update['inventory'][art1]

        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│`removendo 2/3`")

        update['inventory'][art2] -= 1
        if update['inventory'][art2] < 1:
            del update['inventory'][art2]

        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│`removendo 3/3`")

        update['inventory'][art3] -= 1
        if update['inventory'][art3] < 1:
            del update['inventory'][art3]
        await msg.edit(content=f"<:confirmed:721581574461587496>│`itens retirados com sucesso...`")
        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│`Adicionando o` <:melted_artifact:739573767260471356>"
                               f" **Melted Artifact** `para sua conta...`")
        try:
            update['inventory']['melted_artifact'] += 2
        except KeyError:
            update['inventory']['melted_artifact'] = 2
        await sleep(2)
        await msg.edit(content=f"<:confirmed:721581574461587496>│<:melted_artifact:739573767260471356> `2`"
                               f"**Melted Artifact** `adicionado ao seu inventario com sucesso...`")

        img = choice(git)
        embed = discord.Embed(color=self.bot.color)
        embed.set_image(url=img)
        await ctx.send(embed=embed)
        await self.bot.db.update_data(data, update, 'users')
        await self.bot.data.add_sts(ctx.author, "melted", 1)


def setup(bot):
    bot.add_cog(MeltedClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mMELTED\033[1;32m foi carregado com sucesso!\33[m')

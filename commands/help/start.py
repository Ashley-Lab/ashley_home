import copy
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=False)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='help', aliases=['ajuda'])
    async def help(self, ctx, *, command_help=None):
        """há fala serio!"""
        if command_help is None:
            embed = discord.Embed(title="-==Artigo de Ajuda==-\nPara detalhar o comando use: ash help <command>",
                                  color=self.color, description=f"Olá {ctx.author.name}, eu sou a **Ashley**, um bot "
                                                                f"de diversão e jogos, incluindo RPG de turnos e "
                                                                f"sistemas de economia completo!")

            embed.add_field(name="**Um pouco acerca dos meus sistemas**",
                            value=">>> Possuo um sistema de economia muito completo e fechado, ou seja, o meu dono "
                                  "não tem controle sobre ele. É um sistema que tem vindo a ser atualizado ao longo "
                                  "do tempo para que possa ser o mais semelhante possível à economia real.\nExiste "
                                  "também um sistema de RPG, que se baseia em juntar itens para criar equipamentos "
                                  "melhores e batalhar contra monstros mais fortes!",
                            inline=False)

            embed.add_field(name="**Inteligência Artificial**",
                            value="Inteligência Artificial, mais conhecida como IA, é uma inteligência "
                                  "semelhante à humana, pertencente a sistemas tecnológicos. Por palavras"
                                  " mais simples, é como se as \"máquinas\" tivessem mente própria.\nEu "
                                  "proporciono um sistema de IA que, atualmente, responde a mensagens dos"
                                  " membros, desde bons-dias e boas-noites até várias perguntas ou até "
                                  "mesmo brincar consigo, e pode ser ativado/desativado utilizando o "
                                  "comando abaixo.\n\n_Note que, para usufruir deste sistema de IA "
                                  "totalmente, terá que ativar o meu Serviço de Interação com Membros "
                                  "(SIM) através do comando `ash config interaction`.\nNote também que existe "
                                  "uma diferença entre o SIM e o comando `ash ia`. O SIM ativa a IA em si"
                                  " e o comando ativa as respostas automáticas, ou seja, eu irei responder"
                                  " a você mesmo quando você não fale comigo diretamente!_",
                            inline=False)

            embed.add_field(name="**Entretenimento**",
                            value=">>> Existem categorias de entretenimento que contêm (mini)jogos e outros diversos. "
                                  "Se você é um colecionador, irá adorar o meu sistema de coleção de artefactos.",
                            inline=False)

            embed.add_field(name="**Acesso nossa WIKI de Ajuda**",
                            value="[Clique Aqui](https://github.com/Ashley-Lab/ashley_home/wiki)",
                            inline=False)

            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="http://sisadm2.pjf.mg.gov.br/imagem/ajuda.png")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=embed)
        else:
            msg = copy.copy(ctx.message)
            msg.content = 'ash ' + command_help
            ctx_ = await self.bot.get_context(msg)
            if ctx_.command is not None:
                if ctx_.command.help is not None:
                    text = f"`{ctx_.prefix + ctx_.command.qualified_name + ' ' + ctx_.command.signature}`"
                    return await ctx.send(f"**Modo de Uso:** {text}\n```{ctx_.command.help}```")
                await ctx.send("<:alert:739251822920728708>│`Comando Ainda nao tem uma ajuda definida`")
            else:
                await ctx.send("<:alert:739251822920728708>│`Comando Inválido`")


def setup(bot):
    bot.add_cog(Helper(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mAJUDA\033[1;32m foi carregado com sucesso!\33[m')

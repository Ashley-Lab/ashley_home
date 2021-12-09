import disnake

from disnake.ext import commands


class HelperSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.slash_command(name="help", description="Artigos de Ajuda", guild_ids=[519894833783898112])
    async def help(self, inter, *, command_help=None):
        """há fala serio!"""
        if command_help is None:
            embed = disnake.Embed(title="-==Artigo de Ajuda==-\nPara detalhar o comando use: ash help <command>",
                                  color=self.color, description=f"Olá {inter.author.name}, eu sou a **Ashley**, um bot"
                                                                f" de diversão e jogos, incluindo RPG de turnos e "
                                                                f"sistemas de economia completo!")

            embed.add_field(name="**Categorias de comandos - Utilidades**:",
                            value="🔧 [Comandos Admin](https://github.com/D3NKYT0/ashley_home/wiki/Comandos#-comandos"
                                  "-admin)\n "
                                  "👩 [Comandos Ashley](https://github.com/D3NKYT0/ashley_home/wiki/Comandos"
                                  "#-comandos-ashley)\n "
                                  "ℹ️ [Comandos Utility](https://github.com/D3NKYT0/ashley_home/wiki/Comandos#%E2%84"
                                  "%B9%EF%B8%8F-comandos-utility)\n "
                                  "👑 [Comandos VIP](https://github.com/D3NKYT0/ashley_home/wiki/Comandos#-comandos"
                                  "-vip)\n "
                                  "👥 [Comandos Guild](https://github.com/D3NKYT0/ashley_home/wiki/Comandos#-comandos"
                                  "-guild)\n "
                                  "👤 [Comandos Member](https://github.com/D3NKYT0/ashley_home/wiki/Comandos"
                                  "#-comandos-member)",
                            inline=False)
            embed.add_field(name="**Categorias de comandos - Diversão**:",
                            value="⚔️ [Comandos RPG](https://github.com/D3NKYT0/ashley_home/wiki/Comandos#%EF%B8%8F"
                                  "-comandos-rpg)\n "
                                  "💰 [Comandos Economy](https://github.com/D3NKYT0/ashley_home/wiki/Comandos"
                                  "#-comandos-economy)\n "
                                  "🕹️ [Comandos Mini-Games](https://github.com/D3NKYT0/ashley_home/wiki/Comandos"
                                  "#%EF%B8%8F-comandos-mini-games)\n "
                                  "❇️ [Comandos Funny](https://github.com/D3NKYT0/ashley_home/wiki/Comandos#%EF%B8"
                                  "%8F-comandos-funny)\n "
                                  "🖼️ [Comandos Image](https://github.com/D3NKYT0/ashley_home/wiki/Comandos#%EF%B8"
                                  "%8F-comandos-image)",
                            inline=False)

            embed.add_field(name="**Extras:**",
                            value="ℹ [Sobre a Ashley](https://github.com/D3NKYT0/ashley_home/wiki/Sobre)\n"
                                  "📓 [Iniciando na Ashley](https://github.com/D3NKYT0/ashley_home/wiki/Iniciando-na"
                                  "-Ashley)\n "
                                  "👑 [Benefícios VIP](https://github.com/D3NKYT0/ashley_home/wiki/Beneficios-VIP)\n"
                                  "<:gemash:761064114650873877> [Blessed Ethernya]("
                                  "https://github.com/D3NKYT0/ashley_home/wiki/Blessed-Ethernya)\n "
                                  "🏰 [Lore](https://github.com/D3NKYT0/ashley_home/wiki/Lore)\n"
                                  "🌎 [Províncias](https://github.com/D3NKYT0/ashley_home/wiki/Provincias)\n",
                            inline=False)

            embed.add_field(name="**Acesse a minha wiki para mais informações:**",
                            value="[Clique Aqui](https://github.com/D3NKYT0/ashley_home/wiki)",
                            inline=False)

            embed.set_author(name=inter.me.name, icon_url=inter.me.display_avatar)
            embed.set_thumbnail(url="http://sisadm2.pjf.mg.gov.br/imagem/ajuda.png")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await inter.response.send_message(embed=embed)
        else:

            all_commands = []
            for command in self.bot.commands:
                all_commands.append(command)
                if isinstance(command, commands.Group):
                    all_commands.extend(command.commands)

            command = None
            for cmd in all_commands:
                if cmd.qualified_name == command_help:
                    command = cmd

            if command is not None:

                if command.help is not None:
                    text = f"ash `{command.qualified_name + ' ' + command.signature}`"
                    return await inter.response.send_message(f"**Modo de Uso:** {text}\n```{command.help}```")

                await inter.response.send_message("<:alert:739251822920728708>│`Comando Ainda nao tem uma ajuda"
                                                  " definida`")

            else:
                await inter.response.send_message("<:alert:739251822920728708>│`Comando Inválido`")


def setup(bot):
    bot.add_cog(HelperSlash(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mAJUDA\033[1;32m foi carregado com sucesso!\33[m')

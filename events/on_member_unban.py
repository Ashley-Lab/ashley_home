import disnake

from disnake.ext import commands


class UnBanClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        if guild is not None:
            data = await self.bot.db.get_data("guild_id", guild.id, "guilds")
            if data is not None:
                try:
                    if data['log_config']['log'] and data['log_config']['member_unBan']:
                        canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                        if canal is None:
                            return
                        to_send = disnake.Embed(
                            title=":star2: **Membro Desbanido**",
                            color=self.color,
                            description=f"**Membro:** {user.name}")
                        to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                        ashley = canal.guild.get_member(self.bot.user.id)
                        perms = canal.permissions_for(ashley)
                        if perms.send_messages and perms.read_messages:
                            if not perms.embed_links or not perms.attach_files:
                                await canal.send("<:negate:721581573396496464>│`PRECISO DA PERMISSÃO DE:` "
                                                 "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                                 " CORRETAMENTE!**")
                            else:
                                await canal.send(embed=to_send)
                except AttributeError:
                    pass
                except disnake.errors.NotFound:
                    pass
                except disnake.errors.HTTPException:
                    pass
                except TypeError:
                    pass


def setup(bot):
    bot.add_cog(UnBanClass(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mUN_BAN_CLASS\033[1;33m foi carregado com sucesso!\33[m')

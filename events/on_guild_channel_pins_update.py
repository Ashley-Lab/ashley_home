import disnake

from disnake.ext import commands


class ChannelPinUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        data = await self.bot.db.get_data("guild_id", channel.guild.id, "guilds")

        if not data:
            return

        data = data['log_config']

        if data['log'] and data['channel_edit']:
            canal = self.bot.get_channel(data['log_channel_id'])

            if not canal:
                return

            fix_ = "fixada"
            time_ = ''
            if last_pin:
                time_ = "em: " + str(last_pin)
            else:
                fix_ = "dex" + fix_

            embed = disnake.Embed(color=self.color,
                                  title=f":bangbang: **Uma mensagem foi {fix_}**",
                                  description=f"**Canal de texto:** {channel!s} \n{time_}")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")

            ashley = canal.guild.get_member(self.bot.user.id)
            perms = canal.permissions_for(ashley)
            if perms.send_messages and perms.read_messages:
                if not perms.embed_links or not perms.attach_files:
                    await canal.send("<:negate:721581573396496464>│`PRECISO DA PERMISSÃO DE:` "
                                     "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                     " CORRETAMENTE!**")
                else:
                    await canal.send(embed=embed)


def setup(bot):
    bot.add_cog(ChannelPinUpdate(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mCHANNEL_PINS_UPDATE\033[1;33m foi carregado com sucesso!\33[m')

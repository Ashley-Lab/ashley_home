import discord

from resources.img_edit import welcome
from discord.ext import commands


class OnMemberRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        data = await self.bot.db.get_data("guild_id", member.guild.id, "guilds")

        if not data:
            return
        
        if data is not None:
            try:
                if data['func_config']['member_remove']:
                    canal = self.bot.get_channel(data['func_config']['member_remove_id'])

                    if canal is None:
                        return

                    data_goodbye = {
                        "type": "goodbye",
                        "name": str(member.name),
                        "avatar": member.avatar_url_as(format="png"),
                        "text": None
                    }

                    await welcome(data_goodbye)

                    file = discord.File('goodbye.png')
                    if file is not None:
                        try:
                            await canal.send(file=file, content="> `CLIQUE NA IMAGEM PARA MAIORES DETALHES`")
                        except discord.errors.HTTPException:
                            pass
                    else:
                        embed = discord.Embed(title=f"{member.name.upper()} Saiu!", color=self.bot.color)
                        userjoinedat = str(member.joined_at).split('.', 1)[0]
                        usercreatedat = str(member.created_at).split('.', 1)[0]
                        embed.add_field(name="Entrou no server em:", value=userjoinedat, inline=True)
                        embed.add_field(name="Conta criada em:", value=usercreatedat, inline=True)
                        embed.add_field(name="ID:", value=str(member.id), inline=True)
                        embed.set_thumbnail(url=member.avatar_url)
                        ashley = canal.guild.get_member(self.bot.user.id)
                        perms = canal.permissions_for(ashley)
                        if perms.send_messages and perms.read_messages:
                            if not perms.embed_links or not perms.attach_files:
                                await canal.send("<:negate:721581573396496464>│`PRECISO DA PERMISSÃO DE:` "
                                                 "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                                 " CORRETAMENTE!**")
                            else:
                                await canal.send(embed=embed)

            except AttributeError:
                pass
            except discord.errors.Forbidden:
                pass
            except discord.errors.NotFound:
                pass

            try:
                if data['func_config']['cont_users']:
                    numbers = ['<:0_:578615675182907402>', '<:1_:578615669487304704>', '<:2_:578615674109165568>',
                               '<:3_:578615683424976916>', '<:4_:578615679406833685>', '<:5_:578615684708171787>',
                               '<:6_:578617070309343281>', '<:7_:578615679041798144>', '<:8_:578617071521497088>',
                               '<:9_:578617070317469708>']
                    canal = self.bot.get_channel(data['func_config']['cont_users_id'])
                    if canal is None:
                        return
                    text = str(member.guild.member_count)
                    list_ = list()
                    for letter in text:
                        list_.append(numbers[int(letter)])
                    list_ = str(list_).replace('[', '').replace(']', '').replace(',', '.')
                    ashley = canal.guild.get_member(self.bot.user.id)
                    perms = canal.permissions_for(ashley)
                    if perms.send_messages and perms.read_messages:
                        if not perms.embed_links or not perms.attach_files:
                            await canal.send("<:negate:721581573396496464>│`PRECISO DA PERMISSÃO DE:` "
                                             "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                             " CORRETAMENTE!**")
                        else:
                            await canal.edit(topic="<a:caralho:525105064873033764> **Membros:**  " + list_)
            except discord.Forbidden:
                pass
            except discord.errors.NotFound:
                pass


def setup(bot):
    bot.add_cog(OnMemberRemove(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mMEMBER_REMOVE\033[1;33m foi carregado com sucesso!\33[m')

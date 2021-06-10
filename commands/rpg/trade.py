import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class TradeClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='sell', aliases=['vender'])
    async def sell(self, ctx, amount: int = None, *, item=None):
        """Comando usado para vender equipamentos, para o proprio bot"""
        if amount is None:
            return await ctx.send("<:alert:739251822920728708>│`Você precisa dizer uma quantia!`")
        if amount < 1:
            return await ctx.send("<:alert:739251822920728708>│`Você precisa dizer uma quantia maior que 0.`")
        if item is None:
            return await ctx.send("<:alert:739251822920728708>│`Você esqueceu de falar o nome do item para vender!`")

        equips_list = list()
        for ky in self.bot.config['equips'].keys():
            for k, v in self.bot.config['equips'][ky].items():
                equips_list.append((k, v))

        if item not in [i[1]["name"] for i in equips_list]:
            if "sealed" in item.lower():
                return await ctx.send("<:negate:721581573396496464>│`ESSE ITEM ESTÁ SELADO, ANTES DISSO TIRE O SELO "
                                      "USANDO O COMANDO:` **ASH LIBERAR**")
            return await ctx.send("<:negate:721581573396496464>│`ESSE ITEM NAO EXISTE...`")

        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user

        if ctx.author.id in self.bot.jogando:
            return await ctx.send("<:alert:739251822920728708>│`VocÊ está jogando, aguarde para quando"
                                  " vocÊ estiver livre!`")

        if not data_user['rpg']['active']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│`USE O COMANDO` **ASH RPG** `ANTES!`')
            return await ctx.send(embed=embed)

        if ctx.author.id in self.bot.batalhando:
            msg = '<:negate:721581573396496464>│`VOCE ESTÁ BATALHANDO!`'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        item_key = None
        for key in data_user['rpg']['items'].keys():
            for name in equips_list:
                if name[0] == key and name[1]["name"] == item:
                    item_key = name
        if item_key is None:
            return await ctx.send("<:negate:721581573396496464>│`VOCE NAO TEM ESSE ITEM...`")

        if data_user['rpg']['items'][item_key[0]] >= amount:
            update_user['rpg']['items'][item_key[0]] -= amount
            if update_user['rpg']['items'][item_key[0]] < 1:
                del update_user['rpg']['items'][item_key[0]]
            await self.bot.db.update_data(data_user, update_user, 'users')

            money = 0
            for _ in range(amount):
                money += item_key[1]['sell']

            msg = await self.bot.db.add_money(ctx, money, True)
            await self.bot.data.add_sts(ctx.author, "sell", 1)
            return await ctx.send(f'<:confirmed:721581574461587496>│`PARABENS, VC VENDEU {amount} DE '
                                  f'{item_key[1]["name"].upper()} COM SUCESSO!`\n'
                                  f'`E POR VENDER UM ITEM, VOCE GANHOU` {msg}')
        else:
            return await ctx.send(f"<:alert:739251822920728708>│`VOCÊ NÃO TEM ESSA QUANTIDADE DISPONIVEL DE "
                                  f"{item_key[1]['name'].upper()}!`")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='trade', aliases=['trocar'])
    async def trade(self, ctx, member: discord.Member = None, amount: int = None, *, item=None):
        """Comando usado para trocar equipamentos com os jogadores"""
        if member is None:
            return await ctx.send("<:alert:739251822920728708>│`Você precisa mencionar alguem!`")
        if amount is None:
            return await ctx.send("<:alert:739251822920728708>│`Você precisa dizer uma quantia!`")
        if amount < 1:
            return await ctx.send("<:alert:739251822920728708>│`Você precisa dizer uma quantia maior que 0.`")
        if member.id == ctx.author.id:
            return await ctx.send("<:alert:739251822920728708>│`Você não pode dar um item a si mesmo!`")
        if item is None:
            return await ctx.send("<:alert:739251822920728708>│`Você esqueceu de falar o nome do item para dar!`")

        equips_list = list()
        for ky in self.bot.config['equips'].keys():
            for k, v in self.bot.config['equips'][ky].items():
                equips_list.append((k, v))

        if item not in [i[1]["name"] for i in equips_list]:
            if "sealed" in item.lower() and item.lower() != "unsealed stone":
                return await ctx.send("<:negate:721581573396496464>│`ESSE ITEM ESTÁ SELADO, ANTES DISSO TIRE O SELO "
                                      "USANDO O COMANDO:` **ASH LIBERAR**")
            return await ctx.send("<:negate:721581573396496464>│`ESSE ITEM NAO EXISTE, OU NAO É UM EQUIPAMENTO...`")

        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        data_member = await self.bot.db.get_data("user_id", member.id, "users")
        update_user = data_user
        update_member = data_member

        if ctx.author.id in self.bot.jogando:
            return await ctx.send("<:alert:739251822920728708>│`Você está jogando, aguarde para quando"
                                  " vocÊ estiver livre!`")

        if not data_user['rpg']['active']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│`USE O COMANDO` **ASH RPG** `ANTES!`')
            return await ctx.send(embed=embed)

        if ctx.author.id in self.bot.batalhando:
            msg = '<:negate:721581573396496464>│`VOCE ESTÁ BATALHANDO!`'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if data_member is None:
            return await ctx.send('<:alert:739251822920728708>│**ATENÇÃO** : '
                                  '`esse usuário não está cadastrado!`', delete_after=5.0)

        if member.id in self.bot.jogando:
            return await ctx.send("<:alert:739251822920728708>│`O usuario está jogando, aguarde para quando"
                                  " ele estiver livre!`")

        if not data_member['rpg']['active']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│`O USUARIO DEVE USAR O COMANDO` **ASH RPG** `ANTES!`')
            return await ctx.send(embed=embed)

        if member.id in self.bot.jogando:
            msg = '<:negate:721581573396496464>│`O USUARIO ESTÁ BATALHANDO!`'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        _class = data_member["rpg"]["class_now"]
        _db_class = data_member["rpg"]["sub_class"][_class]
        if _db_class['level'] < 26:
            msg = '<:negate:721581573396496464>│`O USUARIO PRECISA ESTA NO NIVEL 26 OU MAIOR PARA TROCAR ' \
                  'EQUIPAMENTOS!\nPEÇA PARA ELE OLHAR O NIVEL NO COMANDO:` **ASH SKILL**'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        item_key = None
        for key in data_user['rpg']['items'].keys():
            for name in equips_list:
                if name[0] == key and name[1]["name"] == item:
                    item_key = name
        if item_key is None:
            return await ctx.send("<:negate:721581573396496464>│`VOCE NAO TEM ESSE ITEM...`")

        if data_user['rpg']['items'][item_key[0]] >= amount:
            update_user['rpg']['items'][item_key[0]] -= amount
            if update_user['rpg']['items'][item_key[0]] < 1:
                del update_user['rpg']['items'][item_key[0]]
            try:
                update_member['rpg']['items'][item_key[0]] += amount
            except KeyError:
                update_member['rpg']['items'][item_key[0]] = amount
            await self.bot.db.update_data(data_user, update_user, 'users')
            await self.bot.db.update_data(data_member, update_member, 'users')
            await self.bot.data.add_sts(ctx.author, "trade", 1)
            return await ctx.send(f'<:confirmed:721581574461587496>│`PARABENS, VC DEU {amount} DE '
                                  f'{item_key[1]["name"].upper()} PARA {member.name} COM SUCESSO!`')
        else:
            return await ctx.send(f"<:alert:739251822920728708>│`VOCÊ NÃO TEM ESSA QUANTIDADE DISPONIVEL DE "
                                  f"{item_key[1]['name'].upper()}!`")


def setup(bot):
    bot.add_cog(TradeClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mTRADE_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')

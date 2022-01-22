import disnake

from disnake.ext import commands
from resources.check import check_it
from resources.db import Database
from random import choice, randint
from resources.utility import convert_item_name as cin
from resources.verify_cooldown import verify_cooldown
from asyncio import sleep


cooldown_sell = 86400  # Default: 86400 24 horas
git = ["https://media1.tenor.com/images/adda1e4a118be9fcff6e82148b51cade/tenor.gif?itemid=5613535",
       "https://media1.tenor.com/images/daf94e676837b6f46c0ab3881345c1a3/tenor.gif?itemid=9582062",
       "https://media1.tenor.com/images/0d8ed44c3d748aed455703272e2095a8/tenor.gif?itemid=3567970",
       "https://media1.tenor.com/images/17e1414f1dc91bc1f76159d7c3fa03ea/tenor.gif?itemid=15744166",
       "https://media1.tenor.com/images/39c363015f2ae22f212f9cd8df2a1063/tenor.gif?itemid=15894886"]


class ViewDefault(disnake.ui.View):
    def __init__(self, author):
        self.author = author
        super().__init__()

    async def interaction_check(self, inter):
        if inter.user.id != self.author.id:
            return False
        else:
            return True


class SelectProvinces(disnake.ui.Select):
    def __init__(self, provinces, bot, amount):
        self.provinces = provinces
        self.bot = bot
        self.amount = amount
        self.i = self.bot.items
        super().__init__(
            placeholder="Selecione uma provincia",
            options=[disnake.SelectOption(label=province, value=province) for province in self.provinces],
            min_values=1, max_values=1)

    async def callback(self, inter):
        exchange = inter.values[0]

        description = f"```\n" \
                      f"Provincia selecionada: {exchange}" \
                      f"```"

        embed = disnake.Embed(color=self.bot.color, title="BITASH CORRETORA", description=description)
        cd = await self.bot.db.cd("exchanges")
        tot, emo = 1000, ['🟢', '🔴', '🟠', '⚪']  # verde / vermelho / laranja / branco

        value = self.bot.broker.get_exchange(exchange)
        be = self.bot.broker.format_bitash(value / self.bot.current_rate)
        be_tot = self.bot.broker.format_bitash(value / self.bot.current_rate * tot)
        assets = [cin(_, self.i) for _ in self.bot.broker.get_assets(exchange)]
        asset = '\n'.join([f"{self.i[_][0]} **{self.i[_][1]}**" for _ in assets])
        flutuation = self.bot.tradingview.get_link(exchange)

        data = await cd.find_one({"_id": exchange})
        ast, sold = len(data['assets'].keys()), len(data['sold'].keys())

        text = f"`Able:` **{ast}**`/1000`\n" \
               f"`Sold:` **{sold}**\n" \
               f"`Value:` **{be}** `BTA`\n" \
               f"`Total:` **{be_tot}**\n" \
               f"`Flutuation:` **[{flutuation[1]}]({flutuation[0]})**\n\n" \
               f"`Assets:`\n{asset}"

        _emo = emo[3] if ast == tot else emo[0] if 100 <= ast <= 999 else emo[2] if 1 <= ast <= 99 else emo[1]
        embed.add_field(name=f"{_emo} {exchange}", value=text, inline=True)

        embed.set_thumbnail(url=inter.user.display_avatar)
        embed.set_footer(text=f"Ashley ® Todos os direitos reservados.")

        try:
            await inter.response.edit_message(embed=embed, view=ProvinceExchange(self.bot, exchange, self.amount))
        except disnake.errors.NotFound:
            pass


class ProvinceExchange(disnake.ui.View):
    def __init__(self, bot, exchange, amount):
        self.bot = bot
        self.amount = amount
        self.i = self.bot.items
        self.exchange = exchange
        super().__init__()

    @disnake.ui.button(emoji="<:buy:933202206218416160>", label="Buy", style=disnake.ButtonStyle.green)
    async def _buy(self, button, inter):

        if button:
            pass

        cd = await self.bot.db.cd("users")
        data = await cd.find_one({"user_id": inter.user.id}, {"true_money": 1})
        bitash = data["true_money"]["bitash"]

        exchange = self.exchange
        description = f"```\n" \
                      f"Provincia selecionada: {exchange}" \
                      f"```"

        embed = disnake.Embed(color=self.bot.color, title="BITASH CORRETORA", description=description)
        cd = await self.bot.db.cd("exchanges")
        tot, emo = 1000, ['🟢', '🔴', '🟠', '⚪']  # verde / vermelho / laranja / branco

        value = self.bot.broker.get_exchange(exchange)
        be = self.bot.broker.format_bitash(value / self.bot.current_rate)
        be_tot = self.bot.broker.format_bitash(value / self.bot.current_rate * tot)

        data = await cd.find_one({"_id": exchange})
        ast, sold = len(data['assets'].keys()), len(data['sold'].keys())
        amount = float(be.replace(",", "."))
        price = int(bitash / amount) if int(bitash / amount) > 0 else 0
        assets = [cin(_, self.i) for _ in self.bot.broker.get_assets(exchange)]
        asset = '\n'.join([f"{self.i[_][0]} **{self.i[_][1]}**" for _ in assets])

        if price > ast:
            price = ast

        text = f"`Able:` **{ast}**`/1000`\n" \
               f"`Sold:` **{sold}**\n" \
               f"`Value:` **{be}** `BTA`\n" \
               f"`Total:` **{be_tot}**\n\n" \
               f"`Your Wallet:` **{self.bot.broker.format_bitash(bitash)}**\n" \
               f"`Buy Max:` **{price}**\n\n" \
               f"`Assets:`\n{asset}"

        _emo = emo[3] if ast == tot else emo[0] if 100 <= ast <= 999 else emo[2] if 1 <= ast <= 99 else emo[1]
        embed.add_field(name=f"{_emo} {exchange}", value=text, inline=True)

        embed.set_thumbnail(url=inter.user.display_avatar)
        embed.set_footer(text=f"Ashley ® Todos os direitos reservados.")

        try:
            await inter.response.edit_message(embed=embed, view=BuyAndSell(self.bot, self.exchange, self.amount))
        except disnake.errors.NotFound:
            pass

    @disnake.ui.button(emoji="<:sell:933202206029672498>", label="Sell", style=disnake.ButtonStyle.primary)
    async def _sell(self, button, inter):

        if button:
            pass

        exchange = self.exchange
        description = f"```\n" \
                      f"Provincia selecionada: {exchange}" \
                      f"```"

        embed = disnake.Embed(color=self.bot.color, title="BITASH CORRETORA", description=description)
        cd = await self.bot.db.cd("exchanges")
        tot, emo = 1000, ['🟢', '🔴', '🟠', '⚪']  # verde / vermelho / laranja / branco

        value = self.bot.broker.get_exchange(exchange)
        be = self.bot.broker.format_bitash(value / self.bot.current_rate)
        be_tot = self.bot.broker.format_bitash(value / self.bot.current_rate * tot)

        data = await cd.find_one({"_id": exchange})
        ast, sold = len(data['assets'].keys()), len(data['sold'].keys())

        tot_asset = 0
        for asset in data['sold'].keys():
            if data['sold'][asset]['owner'] == inter.user.id:
                tot_asset += 1

        text = f"`Able:` **{ast}**`/1000`\n" \
               f"`Sold:` **{sold}**\n" \
               f"`Value:` **{be}** `BTA`\n" \
               f"`Total:` **{be_tot}**\n\n" \
               f"`Your Assets:` **{tot_asset}**"

        _emo = emo[3] if ast == tot else emo[0] if 100 <= ast <= 999 else emo[2] if 1 <= ast <= 99 else emo[1]
        embed.add_field(name=f"{_emo} {exchange}", value=text, inline=True)

        embed.set_thumbnail(url=inter.user.display_avatar)
        embed.set_footer(text=f"Ashley ® Todos os direitos reservados.")

        try:
            await inter.response.edit_message(embed=embed, view=SellAndBuy(self.bot, self.exchange, self.amount))
        except disnake.errors.NotFound:
            pass

    @disnake.ui.button(emoji="<:back:933204477492744252>", label="Back", style=disnake.ButtonStyle.gray)
    async def _back(self, button, inter):

        if button:
            pass

        try:
            await inter.response.defer()

            provinces = list(self.bot.broker.exchanges.keys())
            view = ViewDefault(inter.user)
            view.add_item(SelectProvinces(provinces, self.bot, self.amount))

            description = "```\n" \
                          "Legenda das Cores:\n" \
                          "Branco: Todas as ações disponivel\n" \
                          "Verde: Muitas ações disponiveis\n" \
                          "Laranja: Poucas ações disponiveis\n" \
                          "Vermelho: Nenhuma ação disponivel" \
                          "```"

            embed = disnake.Embed(color=self.bot.color, title="BITASH CORRETORA", description=description)
            cd = await self.bot.db.cd("exchanges")
            all_data = [d async for d in cd.find()]
            tot_global, tot, emo = 0, 1000, ['🟢', '🔴', '🟠', '⚪']  # verde / vermelho / laranja / branco

            for exchange in provinces:
                value = self.bot.broker.get_exchange(exchange)
                be = self.bot.broker.format_bitash(value / self.bot.current_rate)
                be_tot = self.bot.broker.format_bitash(value / self.bot.current_rate * tot)
                tot_global += value / self.bot.current_rate * tot
                flutuation = self.bot.broker.format_flutuation(float(self.bot.tradingview.get_flutuation(exchange)))

                data = [d for d in all_data if d["_id"] == exchange][0]
                ast, sold = len(data['assets'].keys()), len(data['sold'].keys())

                text = f"`Able:` **{ast}**`/1000`\n" \
                       f"`Sold:` **{sold}**\n" \
                       f"`Value:` **{be}** `BTA`\n" \
                       f"`Flutuation:` **{flutuation}%**\n" \
                       f"`Total:` **{be_tot}**"

                _emo = emo[3] if ast == tot else emo[0] if 100 <= ast <= 999 else emo[2] if 1 <= ast <= 99 else emo[1]
                embed.add_field(name=f"{_emo} {exchange}", value=text, inline=True)

            embed.set_thumbnail(url=inter.user.display_avatar)
            et = self.bot.broker.format_value(tot_global * self.bot.current_rate)
            bk = self.bot.broker.format_bitash(tot_global)
            embed.set_footer(text=f"Valor Total da bolsa: {bk} BTA (bitash) | {et} ethernyas")

            await inter.edit_original_message(embed=embed, view=view)

        except (disnake.errors.NotFound, disnake.errors.InteractionNotResponded):
            msg = "<:alert:739251822920728708>│`Algo ocorreu errado, por favor tente novamente!`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            return await inter.edit_original_message(embed=embed, view=None)

    @disnake.ui.button(emoji="❌", label="Exit", style=disnake.ButtonStyle.danger)
    async def _exit(self, button, inter):

        if button:
            pass

        msg = "<:confirmed:721581574461587496>│`Voce fechou a corretora!`"
        embed = disnake.Embed(color=self.bot.color, description=msg)
        try:
            await inter.response.edit_message(embed=embed, view=None)
        except disnake.errors.NotFound:
            pass


class BuyAndSell(disnake.ui.View):
    def __init__(self, bot, exchange, amount):
        self.bot = bot
        self.amount = amount
        self.exchange = exchange
        super().__init__()

    @disnake.ui.button(emoji="<:buy:933202206218416160>", label="Buy 1", style=disnake.ButtonStyle.green)
    async def _buy_one(self, button, inter):

        if button:
            pass

        cd = await self.bot.db.cd("users")
        data = await cd.find_one({"user_id": inter.user.id}, {"true_money": 1})
        bitash = data["true_money"]["bitash"]
        value = self.bot.broker.get_exchange(self.exchange)
        be = self.bot.broker.format_bitash(value / self.bot.current_rate)
        charged = float(be.replace(",", ".")) - (float(be.replace(",", ".")) * 2)

        if bitash - float(be.replace(",", ".")) < 0:
            msg = "<:negate:721581573396496464>│`Você nao tem` **bitash** `suficiente para essa operação!`"
            embed = disnake.Embed(description=msg)
            return await inter.response.edit_message(embed=embed, view=None)

        cdc = await self.bot.db.cd("exchanges")
        assets = await cdc.find_one({"_id": self.exchange})

        if len(list(assets['assets'].keys())) <= 0:
            msg = f"<:negate:721581573396496464>│`A provincia de` **{self.exchange}** `não possui mais ações a venda!`"
            embed = disnake.Embed(description=msg)
            return await inter.response.edit_message(embed=embed, view=None)

        if len(list(assets['assets'].keys())) - 1 < 0:
            msg = f"<:negate:721581573396496464>│`A provincia de` **{self.exchange}** `não possui mais ações a venda!`"
            embed = disnake.Embed(description=msg)
            return await inter.response.edit_message(embed=embed, view=None)

        await cd.update_one({"user_id": inter.user.id}, {"$inc": {f"true_money.bitash": charged}})

        asset = choice(list(assets['assets'].keys()))
        assets['sold'][asset] = assets['assets'][asset]
        assets['sold'][asset]['owner'] = inter.user.id
        del assets['assets'][asset]
        await cdc.update_one({"_id": self.exchange}, {"$unset": {f"assets.{asset}": ""},
                                                      "$set": {f"sold.{asset}": assets['sold'][asset]}})

        msg = f"<:confirmed:721581574461587496>│`Você comprou` **1** `ação da provincia de:` **{self.exchange}**"
        embed = disnake.Embed(description=msg)
        try:
            await inter.response.edit_message(embed=embed, view=None)
        except disnake.errors.NotFound:
            pass

    @disnake.ui.button(emoji="<:buy:933202206218416160>", label="Buy All", style=disnake.ButtonStyle.green)
    async def _buy_all(self, button, inter):

        if button:
            pass

        cd = await self.bot.db.cd("users")
        data = await cd.find_one({"user_id": inter.user.id}, {"true_money": 1})
        bitash = data["true_money"]["bitash"]
        value = self.bot.broker.get_exchange(self.exchange)
        be = self.bot.broker.format_bitash(value / self.bot.current_rate)

        amount = float(be.replace(",", "."))
        tot_buy = int(bitash / amount) if int(bitash / amount) > 0 else 0
        charged = (float(be.replace(",", ".")) - (float(be.replace(",", ".")) * 2)) * tot_buy

        cdc = await self.bot.db.cd("exchanges")
        assets = await cdc.find_one({"_id": self.exchange})

        if self.amount is not None:
            tot_buy = self.amount

        if tot_buy > len(list(assets['assets'].keys())):
            tot_buy = len(list(assets['assets'].keys()))

        if bitash - (float(be.replace(",", ".")) * tot_buy) < 0:
            msg = "<:negate:721581573396496464>│`Você nao tem` **bitash** `suficiente para essa operação!`"
            embed = disnake.Embed(description=msg)
            return await inter.response.edit_message(embed=embed, view=None)

        if len(list(assets['assets'].keys())) <= 0:
            msg = f"<:negate:721581573396496464>│`A provincia de` **{self.exchange}** `não possui mais ações a venda!`"
            embed = disnake.Embed(description=msg)
            return await inter.response.edit_message(embed=embed, view=None)

        if len(list(assets['assets'].keys())) - tot_buy < 0:
            msg = f"<:negate:721581573396496464>│`A provincia de` **{self.exchange}** `não possui {tot_buy} ações!`"
            embed = disnake.Embed(description=msg)
            return await inter.response.edit_message(embed=embed, view=None)

        await cd.update_one({"user_id": inter.user.id}, {"$inc": {f"true_money.bitash": charged}})

        query = {"$unset": {}, "$set": {}}
        for _ in range(tot_buy):
            asset = choice(list(assets['assets'].keys()))
            assets['sold'][asset] = assets['assets'][asset]
            assets['sold'][asset]['owner'] = inter.user.id
            del assets['assets'][asset]
            query["$unset"][f"assets.{asset}"] = ""
            query["$set"][f"sold.{asset}"] = assets['sold'][asset]
        await cdc.update_one({"_id": self.exchange}, query)

        msg = f"<:confirmed:721581574461587496>│`Você comprou` **{tot_buy}** `ações da provincia:` **{self.exchange}**"
        embed = disnake.Embed(description=msg)
        try:
            await inter.response.edit_message(embed=embed, view=None)
        except disnake.errors.NotFound:
            pass

    @disnake.ui.button(emoji="❌", label="Exit", style=disnake.ButtonStyle.danger)
    async def _exit(self, button, inter):

        if button:
            pass

        msg = "<:confirmed:721581574461587496>│`Voce fechou a corretora!`"
        embed = disnake.Embed(color=self.bot.color, description=msg)
        await inter.response.edit_message(embed=embed, view=None)


class SellAndBuy(disnake.ui.View):
    def __init__(self, bot, exchange, amount):
        self.bot = bot
        self.amount = amount
        self.exchange = exchange
        super().__init__()

    @disnake.ui.button(emoji="<:sell:933202206029672498>", label="Sell 1", style=disnake.ButtonStyle.primary)
    async def _sell_one(self, button, inter):

        if button:
            pass

        if await verify_cooldown(self.bot, f"sell_one_{inter.user.id}", cooldown_sell, exchange=True):
            try:
                await inter.response.defer()

                channel = self.bot.get_channel(inter.channel_id)
                _MSG = await channel.send("<a:loading:520418506567843860>│ `AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!`\n"
                                          "**mesmo que demore, aguarde o fim do processamento...**")

                cdc = await self.bot.db.cd("exchanges")
                assets = await cdc.find_one({"_id": self.exchange})
                acoes, amount = {"sold": dict()}, 0
                for asset in assets["sold"].keys():
                    if assets["sold"][asset]["owner"] == inter.user.id:
                        amount += 1
                        acoes["sold"][asset] = assets["sold"][asset]

                value = self.bot.broker.get_exchange(self.exchange)
                be = self.bot.broker.format_bitash(value / self.bot.current_rate)
                charged = float(be.replace(",", "."))

                if amount == 0:
                    msg = f"<:negate:721581573396496464>│`Você não tem ações de` **{self.exchange}** " \
                          f"`suficiente para essa operação!`"
                    embed = disnake.Embed(description=msg)
                    return await inter.response.edit_message(embed=embed, view=None)

                query = {"$unset": dict(), "$set": dict()}

                asset = choice(list(acoes['sold'].keys()))
                assets['assets'][asset] = assets['sold'][asset]
                assets['assets'][asset]['owner'] = None
                del assets['sold'][asset]
                del acoes['sold'][asset]

                query["$set"] = {f"assets.{asset}": assets['assets'][asset]}
                query["$unset"] = {f"sold.{asset}": ""}

                await cdc.update_one({"_id": self.exchange}, query)

                # dando o bitash paro usuario
                cd = await self.bot.db.cd("users")
                await cd.update_one({"user_id": inter.user.id}, {"$inc": {f"true_money.bitash": charged}})

                msg = f"✅│`Você vendeu` **1** `ação da provincia de:` " \
                      f"**{self.exchange}**"
                embed = disnake.Embed(description=msg)
                await _MSG.delete()
                await inter.edit_original_message(embed=embed, view=None)

            except (disnake.errors.NotFound, disnake.errors.InteractionNotResponded):
                msg = "<:alert:739251822920728708>│`Algo ocorreu errado, por favor tente novamente!`"
                embed = disnake.Embed(color=self.bot.color, description=msg)
                return await inter.edit_original_message(embed=embed, view=None)

        else:
            msg = "<:negate:721581573396496464>│`Você esta em cooldown...`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            await inter.response.edit_message(embed=embed, view=None)

    @disnake.ui.button(emoji="<:sell:933202206029672498>", label="Sell All", style=disnake.ButtonStyle.primary)
    async def _sell_all(self, button, inter):

        if button:
            pass

        if await verify_cooldown(self.bot, f"sell_many_{inter.user.id}", cooldown_sell, exchange=True):
            try:
                await inter.response.defer()

                channel = self.bot.get_channel(inter.channel_id)
                _MSG = await channel.send("<a:loading:520418506567843860>│ `AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!`\n"
                                          "**mesmo que demore, aguarde o fim do processamento...**")

                cdc = await self.bot.db.cd("exchanges")
                assets = await cdc.find_one({"_id": self.exchange})
                acoes, amount = {"sold": dict()}, 0
                for asset in assets["sold"].keys():
                    if assets["sold"][asset]["owner"] == inter.user.id:
                        amount += 1
                        acoes["sold"][asset] = assets["sold"][asset]

                value = self.bot.broker.get_exchange(self.exchange)
                be = self.bot.broker.format_bitash(value / self.bot.current_rate)
                charged = float(be.replace(",", ".")) * amount

                if amount == 0:
                    msg = f"<:negate:721581573396496464>│`Você não tem ações de` **{self.exchange}** " \
                          f"`suficiente para essa operação!`"
                    embed = disnake.Embed(description=msg)
                    return await inter.response.edit_message(embed=embed, view=None)

                if self.amount is None:

                    for _ in list(acoes['sold'].keys()):
                        assets['assets'][_] = assets['sold'][_]
                        assets['assets'][_]['owner'] = None
                        del assets['sold'][_]

                else:

                    if self.amount > amount:
                        msg = f"<:negate:721581573396496464>│`Você não tem {self.amount} ações de` " \
                              f"**{self.exchange}** `para essa operação!`"
                        embed = disnake.Embed(description=msg)
                        return await inter.response.edit_message(embed=embed, view=None)

                    for _ in range(self.amount):
                        asset = choice(list(acoes['sold'].keys()))
                        assets['assets'][asset] = assets['sold'][asset]
                        assets['assets'][asset]['owner'] = None
                        del assets['sold'][asset]
                        del acoes['sold'][asset]

                query = {"$set": {"assets": assets["assets"], "sold": assets['sold']}}
                await cdc.update_one({"_id": self.exchange}, query)

                # dando o bitash paro usuario
                cd = await self.bot.db.cd("users")
                await cd.update_one({"user_id": inter.user.id}, {"$inc": {f"true_money.bitash": charged}})

                amount = amount if self.amount is None else self.amount
                msg = f"✅│`Você vendeu` **{amount}** `ação da provincia de:` " \
                      f"**{self.exchange}**"
                embed = disnake.Embed(description=msg)
                await _MSG.delete()
                await inter.edit_original_message(embed=embed, view=None)

            except (disnake.errors.NotFound, disnake.errors.InteractionNotResponded):
                msg = "<:alert:739251822920728708>│`Algo ocorreu errado, por favor tente novamente!`"
                embed = disnake.Embed(color=self.bot.color, description=msg)
                return await inter.edit_original_message(embed=embed, view=None)

        else:
            msg = "<:negate:721581573396496464>│`Você esta em cooldown...`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            await inter.response.edit_message(embed=embed, view=None)

    @disnake.ui.button(emoji="❌", label="Exit", style=disnake.ButtonStyle.danger)
    async def _exit(self, button, inter):

        if button:
            pass

        msg = "<:confirmed:721581574461587496>│`Voce fechou a corretora!`"
        embed = disnake.Embed(color=self.bot.color, description=msg)
        await inter.response.edit_message(embed=embed, view=None)


class Miner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.st = []
        self.color = self.bot.color
        self.broker = self.bot.broker
        self.i = self.bot.items
        self.b = self.bot.broker

        self.art = ["braço_direito", "braço_esquerdo", "perna_direita", "perna_esquerda", "the_one", "anel", "balança",
                    "chave", "colar", "enigma", "olho", "vara", "aquario", "aries", "cancer", "capricornio",
                    "escorpiao", "gemeos", "leao", "peixes", "sargitario", "libra", "touro", "virgem"]

        self.cost = {
            "full_heart": 50,

            "solution_agent_blue": 10,
            "solution_agent_green": 10,

            "nucleo_xyz": 5,
            "enchanted_stone": 5,
            "crystal_of_death": 5,

            "Discharge_Crystal": 50,
            "Acquittal_Crystal": 50,
            "Crystal_of_Energy": 50,

            "fused_diamond": 10,
            "fused_ruby": 10,
            "fused_sapphire": 10,
            "fused_emerald": 10,

            "unsealed_stone": 10,
            "melted_artifact": 10,

            "gold_cube": 5,
            "golden_apple": 5,
            "golden_egg": 5,

            "transmogrifador": 50,
            "adamantium": 50
        }

    def status(self):
        for v in self.bot.data_cog.values():
            self.st.append(v)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='broker', aliases=['corretora', 'bk'])
    async def broker(self, ctx, amount: int = None):

        msg = await ctx.send("<a:loading:520418506567843860>│ `AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!`\n"
                             "**mesmo que demore, aguarde o fim do processamento...**")

        provinces = list(self.bot.broker.exchanges.keys())
        view = ViewDefault(ctx.author)
        view.add_item(SelectProvinces(provinces, self.bot, amount))

        description = "```\n" \
                      "Legenda das Cores:\n" \
                      "Branco: Todas as ações disponivel\n" \
                      "Verde: Muitas ações disponiveis\n" \
                      "Laranja: Poucas ações disponiveis\n" \
                      "Vermelho: Nenhuma ação disponivel" \
                      "```"

        embed = disnake.Embed(color=self.bot.color, title="BITASH CORRETORA", description=description)
        cd = await self.bot.db.cd("exchanges")
        all_data = [d async for d in cd.find()]
        tot_global, tot, emo = 0, 1000, ['🟢', '🔴', '🟠', '⚪']  # verde / vermelho / laranja / branco

        for exchange in provinces:
            value = self.bot.broker.get_exchange(exchange)
            be = self.bot.broker.format_bitash(value / self.bot.current_rate)
            be_tot = self.bot.broker.format_bitash(value / self.bot.current_rate * tot)
            tot_global += value / self.bot.current_rate * tot
            flutuation = self.bot.broker.format_flutuation(float(self.bot.tradingview.get_flutuation(exchange)))

            data = [d for d in all_data if d["_id"] == exchange][0]
            ast, sold = len(data['assets'].keys()), len(data['sold'].keys())

            text = f"`Able:` **{ast}**`/1000`\n" \
                   f"`Sold:` **{sold}**\n" \
                   f"`Value:` **{be}** `BTA`\n" \
                   f"`Flutuation:` **{flutuation}%**\n" \
                   f"`Total:` **{be_tot}**"

            _emo = emo[3] if ast == tot else emo[0] if 100 <= ast <= 999 else emo[2] if 1 <= ast <= 99 else emo[1]
            embed.add_field(name=f"{_emo} {exchange}", value=text, inline=True)

        embed.set_thumbnail(url=ctx.author.display_avatar)
        et = self.bot.broker.format_value(tot_global * self.bot.current_rate)
        bk = self.bot.broker.format_bitash(tot_global)
        embed.set_footer(text=f"Valor Total da bolsa: {bk} BTA (bitash) | {et} ethernyas")

        await msg.delete()
        await ctx.send(embed=embed, view=view)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='bkw', aliases=['bkwallet'])
    async def bkw(self, ctx):

        msg = await ctx.send("<a:loading:520418506567843860>│ `AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!`\n"
                             "**mesmo que demore, aguarde o fim do processamento...**")

        cdc = await self.bot.db.cd("users")
        data = await cdc.find_one({"user_id": ctx.author.id}, {"true_money": 1})
        bitash = data["true_money"]["bitash"]

        cd = await self.bot.db.cd("exchanges")
        all_data = [d async for d in cd.find()]

        provincias, assets = dict(), list()
        for d in all_data:
            for asset in d["sold"].keys():
                if d["sold"][asset]["owner"] == ctx.author.id:

                    if d["_id"] not in provincias.keys():
                        provincias[d["_id"]] = 1
                    else:
                        provincias[d["_id"]] += 1

                    if d["sold"][asset]["item"] not in assets:
                        assets.append(d["sold"][asset]["item"])

        be_tot = 0.0
        for key in provincias.keys():
            value = self.bot.broker.get_exchange(key)
            if value != -1:
                price = value / self.bot.current_rate
                be_tot += price * provincias[key]

        def perc(num):
            percent = num / 1000 * 100
            return f"{percent:,.2f}"

        _assets = [cin(_, self.i) for _ in assets]
        asset = '\n'.join([f"{self.i[_][0]} `{self.i[_][1]}`" for _ in _assets])
        prov = '\n'.join([f"`{x}:` **{provincias[x]}**`/1000` **{perc(provincias[x])}%**" for x in provincias.keys()])
        description = f"```\nInformações da sua Wallet```"
        embed = disnake.Embed(color=self.bot.color, title="BITASH WALLET", description=description)
        wallet = f"`Total in Exchanges:` **{self.bot.broker.format_bitash(be_tot)}** `BTA`\n" \
                 f"`Total in Your Wallet:` **{self.bot.broker.format_bitash(bitash)}** `BTA`"

        prov = "`Você não tem ações na sua carteira`" if len(prov) == 0 else prov
        asset = "`Você não tem ativos na sua carteira`" if len(asset) == 0 else asset

        embed.add_field(name=f"⚖️ Ações", value=prov, inline=False)
        embed.add_field(name=f"💵 Wallet", value=wallet, inline=False)
        embed.add_field(name=f"🪙 Assets", value=asset, inline=False)

        embed.set_thumbnail(url=ctx.author.display_avatar)
        embed.set_footer(text=f"Ashley ® Todos os direitos reservados.")
        await msg.delete()
        await ctx.send(embed=embed)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.group(name='miner', aliases=['minerador'])
    async def miner(self, ctx):
        if ctx.invoked_subcommand is None:
            self.status()
            embed = disnake.Embed(color=self.color)
            embed.add_field(name="Miner Commands:",
                            value=f"{self.st[117]} `miner create`\n"
                                  f"{self.st[117]} `miner start`\n"
                                  f"{self.st[117]} `miner stop`\n"
                                  f"{self.st[117]} `miner reward`")
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
            embed.set_thumbnail(url=self.bot.user.display_avatar)
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=embed)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @miner.group(name='reward', aliases=['r'])
    async def _reward(self, ctx):
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if "miner" not in update.keys():
            msg = "<:negate:721581573396496464>│`Você ainda não tem um minerador!`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if f"{ctx.author.id}" in self.bot.minelist.keys():
            if self.bot.minelist[f"{ctx.author.id}"]["active"]:
                msg = "<:negate:721581573396496464>│`Você ja tem um minerador ativo`"
                embed = disnake.Embed(color=self.bot.color, description=msg)
                return await ctx.send(embed=embed)

            else:
                msg = "<:negate:721581573396496464>│`Você ja tem um minerador esperando para iniciar`"
                embed = disnake.Embed(color=self.bot.color, description=msg)
                return await ctx.send(embed=embed)

        miner = update["miner"]

        if len(miner["inventory"].keys()) == 0 and miner["bitash"] == 0.0 and miner["fragment"] == 0:
            msg = "<:negate:721581573396496464>│`Você não tem recompensas mineradas!`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if miner["bitash"] > 0:
            bitash = miner["bitash"]
            update["true_money"]["bitash"] += bitash
            miner["bitash"] = 0.0

            msg = f"<:confirmed:721581574461587496>│`Você obteve` **{self.b.format_bitash(bitash)} BTA** `mineradas!`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            await ctx.send(embed=embed)

        if miner["fragment"] > 0:
            fragment = miner["fragment"]
            update["true_money"]["fragment"] += fragment
            miner["fragment"] = 0

            ct = "Fragmentos de Blessed Ethernya"
            msg = f"<:confirmed:721581574461587496>│`Você obteve` **{fragment} {ct}** `minerados!`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            await ctx.send(embed=embed)

        if len(miner["inventory"].keys()) > 0:
            items = dict(miner["inventory"])
            for item in miner["inventory"].keys():
                if item in update["inventory"].keys():
                    update["inventory"][item] += miner["inventory"][item]
                else:
                    update["inventory"][item] = miner["inventory"][item]
            miner["inventory"] = dict()

            asset = '\n'.join([f"{self.i[_][0]} **{items[_]}** `{self.i[_][1]}`" for _ in items])
            msg = f"<:confirmed:721581574461587496>│`Você obteve os seguintes items:\n`{asset}"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            await ctx.send(embed=embed)

        update["miner"] = miner
        await self.bot.db.update_data(data, update, 'users')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @miner.group(name='create', aliases=['c'])
    async def _create(self, ctx):
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if "miner" in update.keys():
            msg = "<:negate:721581573396496464>│`Você ja criou o minerador!`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        msg = f"\n".join([f"{self.i[k][0]} `{v}` `{self.i[k][1]}`" for k, v in self.cost.items()])
        msg += "\n\n**OBS:** `PARA CONSEGUIR OS ITENS VOCE PRECISA USAR O COMANDO` **ASH BOX**"

        embed = disnake.Embed(
            title="O CUSTO PARA VOCE CRIAR UM MINERADOR:",
            color=self.bot.color,
            description=msg)
        embed.set_author(name=self.bot.user, icon_url=self.bot.user.display_avatar)
        embed.set_thumbnail(url="{}".format(ctx.author.display_avatar))
        embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        await ctx.send(embed=embed)

        artifacts = []
        for i_, amount in data['inventory'].items():
            if i_ in self.art:
                artifacts += [i_] * amount

        if len(artifacts) < 10:
            return await ctx.send("<:negate:721581573396496464>│`Voce nao tem o minimo de 10 arfetados...`\n"
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
            msg = ""
            for key in cost.keys():
                amount = cost[key]
                if key in data['inventory']:
                    amount = cost[key] - data['inventory'][key]
                msg += f"\n{self.i[key][0]} `{amount}` **{key.upper()}**"
            return await ctx.send(f"<:alert:739251822920728708>│`Lhe faltam esses itens para criar um minerador:`"
                                  f"{msg}\n`OLHE SEU INVENTARIO E VEJA A QUANTIDADE QUE ESTÁ FALTANDO.`")

        def check_option(m):
            return m.author == ctx.author and m.content == '0' or m.author == ctx.author and m.content == '1'

        msg = await ctx.send(f"<:alert:739251822920728708>│`VOCE JA TEM TODOS OS ITEM NECESSARIOS, DESEJA CRIAR SEU"
                             f" MINERADOR AGORA?`\n**1** para `SIM` ou **0** para `NÃO`")
        try:
            answer = await self.bot.wait_for('message', check=check_option, timeout=30.0)
        except TimeoutError:
            await msg.delete()
            return await ctx.send("<:negate:721581573396496464>│`COMANDO CANCELADO!`")
        if answer.content == "0":
            await msg.delete()
            return await ctx.send("<:negate:721581573396496464>│`COMANDO CANCELADO!`")
        await msg.delete()

        msg = await ctx.send("<a:loading:520418506567843860>│`Escolhendo 10 artefatos para derreter...`")
        await sleep(2)

        arts = list()
        for _ in range(10):
            artifact = choice(artifacts)
            arts.append(artifact)
            artifacts.remove(artifact)

        await msg.edit(content=f"<a:loading:520418506567843860>│`removendo os itens de custo e os artefatos da sua "
                               f"conta...`")

        for i_, amount in self.cost.items():
            update['inventory'][i_] -= amount
            if update['inventory'][i_] < 1:
                del update['inventory'][i_]

        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│`removendo artefatos...`")

        for _ in range(10):

            update['inventory'][arts[_]] -= 1
            if update['inventory'][arts[_]] < 1:
                del update['inventory'][arts[_]]

        await sleep(2)
        await msg.edit(content=f"<:confirmed:721581574461587496>│`itens retirados com sucesso...`")
        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│`Adicionando o` **minerador** `para sua conta...`")

        # --------------------------
        # a parte do codigo que coloca o minerador na conta

        update["miner"] = {
            "active": False,
            "exchanges": list(),
            "inventory": dict(),
            "bitash": 0.0,
            "fragment": 0,
            "assets": list(),
            "percent": 0.0
        }

        # --------------------------

        await sleep(2)
        await msg.edit(content=f"<:confirmed:721581574461587496>│`O` **Minerador** `foi adicionado a sua conta com"
                               f" sucesso...`")

        img = choice(git)
        embed = disnake.Embed(color=self.bot.color)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

        await self.bot.db.update_data(data, update, 'users')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @miner.group(name='start', aliases=['s', 'iniciar', 'inicio'])
    async def _start(self, ctx, limit: int = None, uptime: str = None):
        if limit is None:
            msg = "<:negate:721581573396496464>│`Voce precisa dizer um limite de mineração`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if limit > 25:
            msg = "<:negate:721581573396496464>│`O limite de mineração nao pode ser maior que 25`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if "miner" not in update.keys():
            msg = "<:negate:721581573396496464>│`Você ainda não tem um minerador!`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if f"{ctx.author.id}" in self.bot.minelist.keys():
            if self.bot.minelist[f"{ctx.author.id}"]["active"]:
                msg = "<:negate:721581573396496464>│`Você ja tem um minerador ativo`"
                embed = disnake.Embed(color=self.bot.color, description=msg)
                return await ctx.send(embed=embed)

            else:
                msg = "<:negate:721581573396496464>│`Você ja tem um minerador esperando para iniciar`"
                embed = disnake.Embed(color=self.bot.color, description=msg)
                return await ctx.send(embed=embed)

        _uptime = update["inventory"].get("uptime", 0)
        adamantium = update["inventory"].get("adamantium", 0)
        energy = update["inventory"].get("Energy", 0)
        max_time = False
        msg_return = ""

        if not update["miner"]["active"]:

            if uptime == "uptime":
                if _uptime < 1:
                    msg = f"<:negate:721581573396496464>│`Você não tem` **1 Uptime** `disponivel!`"
                    embed = disnake.Embed(color=self.bot.color, description=msg)
                    return await ctx.send(embed=embed)

                update["inventory"]["uptime"] -= 1
                if update["inventory"]["uptime"] <= 0:
                    del update["inventory"]["uptime"]

                max_time = True

            if adamantium < limit:
                msg = f"<:negate:721581573396496464>│`Você não tem` **{limit} Adamantium** `disponiveis!`"
                embed = disnake.Embed(color=self.bot.color, description=msg)
                return await ctx.send(embed=embed)

            update["inventory"]["adamantium"] -= limit
            if update["inventory"]["adamantium"] <= 0:
                del update["inventory"]["adamantium"]

            if energy < limit * 500:
                msg = f"<:negate:721581573396496464>│`Você não tem` **{limit * 500} Energy** `disponiveis!`"
                embed = disnake.Embed(color=self.bot.color, description=msg)
                return await ctx.send(embed=embed)

            update["inventory"]["Energy"] -= limit * 500
            if update["inventory"]["Energy"] <= 0:
                del update["inventory"]["Energy"]

            bonus = 2
            if self.bot.event_special:
                bonus += 1

            limit = limit * bonus  # adição do bonus

        else:
            msg_return += '`Que teve custo 0 por que o bot foi reiniciado enquanto o minerador estava ativo!`'
            max_time = True
            limit = update["miner"]["limit"]

        mensagem = await ctx.send("<a:loading:520418506567843860>│ `AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!`\n"
                                  "**mesmo que demore, aguarde o fim do processamento...**")

        cd = await self.bot.db.cd("exchanges")
        all_data = [d async for d in cd.find()]

        provincias, assets = dict(), list()
        for d in all_data:
            for asset in d["sold"].keys():
                if d["sold"][asset]["owner"] == ctx.author.id:

                    if d["_id"] not in provincias.keys():
                        provincias[d["_id"]] = 1
                    else:
                        provincias[d["_id"]] += 1

                    if d["sold"][asset]["item"] not in assets:
                        assets.append(d["sold"][asset]["item"])

        if len(provincias.keys()) == 0:
            await mensagem.delete()
            msg = "<:negate:721581573396496464>│`Você não tem ações pra minerar!`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if len(assets) == 0:
            await mensagem.delete()
            msg = "<:negate:721581573396496464>│`Você não tem ativos pra minerar!`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        percent = 0.0
        for exchange in provincias:
            percent += provincias[exchange] * 0.01

        miner = update["miner"]
        miner["active"] = True

        if "fragment" not in miner.keys():
            miner["fragment"] = 0

        miner["exchanges"] = [ex for ex in provincias.keys()]
        miner["assets"] = [cin(asset, self.i) for asset in assets]
        miner["percent"] = percent
        miner["limit"] = limit
        update["miner"] = miner
        await self.bot.db.update_data(data, update, 'users')

        miner = {"active": False, "user_id": ctx.author.id, "limit": limit, "data": miner, "uptime": max_time}
        self.bot.minelist[f"{ctx.author.id}"] = miner
        msg = f"<:confirmed:721581574461587496>│`Seu minerador esta esperando para iniciar!` {msg_return}"
        embed = disnake.Embed(color=self.bot.color, description=msg)
        await mensagem.delete()
        await ctx.send(embed=embed)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @miner.group(name='stop', aliases=['st'])
    async def _stop(self, ctx):
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if "miner" not in update.keys():
            msg = "<:negate:721581573396496464>│`Você ainda não tem um minerador!`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if str(ctx.author.id) not in self.bot.minelist.keys():
            msg = "<:negate:721581573396496464>│`Você nao tem um minerador ativo no momento!`"
            embed = disnake.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        miner = update["miner"]
        miner["active"] = False
        miner["exchanges"] = list()
        miner["assets"] = list()
        miner["percent"] = 0.0
        update["miner"] = miner
        await self.bot.db.update_data(data, update, 'users')

        self.bot.minelist[f"{ctx.author.id}"]["status"] = False
        msg = "<:confirmed:721581574461587496>│`Minerador esta esperando para ser parado com sucesso`"
        embed = disnake.Embed(color=self.bot.color, description=msg)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Miner(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mMINER_GROUP\033[1;32m foi carregado com sucesso!\33[m')

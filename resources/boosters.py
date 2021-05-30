from random import randint, choice


class Booster(object):
    def __init__(self, items_):
        self.items = items_
        self.ranking = None
        self.is_vip = None
        self.item_ = None

        # box configs
        self.box = {"status": {"active": True, "secret": 0, "ur": 0, "sr": 0, "r": 0, "i": 0, "c": 0}}
        self.legend = {"Comum": 0, "Incomum": 1, "Raro": 2, "Super Raro": 3, "Ultra Raro": 4, "Secret": 5}
        self.bl = {"Comum": "c", "Incomum": "i", "Raro": "r", "Super Raro": "sr", "Ultra Raro": "ur",
                   "Secret": "secret"}
        self.rarity = {
            "Comum": [600, [0.01, 0.02, 0.07, 0.10, 0.20, 0.60]],
            "Incomum": [500, [0.02, 0.04, 0.10, 0.24, 0.50, 0.10]],
            "Raro": [400, [0.03, 0.07, 0.10, 0.50, 0.20, 0.10]],
            "Super Raro": [300, [0.04, 0.06, 0.40, 0.10, 0.20, 0.20]],
            "Ultra Raro": [200, [0.20, 0.40, 0.10, 0.10, 0.10, 0.10]],
            "Secret": [100, [0.40, 0.20, 0.15, 0.10, 0.10, 0.05]]
        }

        # booster configs
        self.booster_choice = {"Comum": 0, "Incomum": 0, "Raro": 0, "Super Raro": 0, "Ultra Raro": 0, "Secret": 0}
        # rarity configs
        self.rarity_choice = {"Comum": 25, "Incomum": 25, "Raro": 20, "Super Raro": 15, "Ultra Raro": 10, "Secret": 5}

        # contadores de itens
        self.secret = 0
        self.ur = 0
        self.sr = 0
        self.r = 0
        self.i = 0
        self.c = 0

        # contador de itens por box
        self.box_count = 0

        # Limites dos itens
        self.l_secret = 0
        self.l_ur = 0
        self.l_sr = 0
        self.l_r = 0
        self.l_i = 0
        self.l_c = 0

    def reset_counts(self):
        self.box = {"status": {"active": True, "secret": 0, "ur": 0, "sr": 0, "r": 0, "i": 0, "c": 0}}
        self.box_count = 0
        self.secret = 0
        self.ur = 0
        self.sr = 0
        self.r = 0
        self.i = 0
        self.c = 0

    def define_limit(self, rarity):
        # Limites dos itens
        self.l_secret = int(rarity[0] * rarity[1][0])
        self.l_ur = int(rarity[0] * rarity[1][1])
        self.l_sr = int(rarity[0] * rarity[1][2])
        self.l_r = int(rarity[0] * rarity[1][3])
        self.l_i = int(rarity[0] * rarity[1][4])
        self.l_c = int(rarity[0] * rarity[1][5])

    def create_box(self, summon):
        rarity_choice = []
        for i_, amount in self.rarity_choice.items():
            rarity_choice += [i_] * amount
        rarity = choice(rarity_choice)

        if summon is not None:
            rarity = summon

        size = self.rarity[rarity][0]
        self.reset_counts()
        self.define_limit(self.rarity[rarity])
        self.box['status']['rarity'] = rarity
        self.box['status']['size'] = size
        self.box['items'] = {"Comum": {}, "Incomum": {}, "Raro": {}, "Super Raro": {}, "Ultra Raro": {}, "Secret": {}}
        while self.box_count < size:
            item = choice(list(self.items.keys()))
            if self.items[item][3] == 5:
                if self.secret < self.l_secret:
                    if item not in self.box['items']['Secret']:
                        self.box['items']['Secret'][item] = {"size": 1, "data": self.items[item]}
                        self.box['status']['secret'] += 1
                    else:
                        self.box['items']['Secret'][item]['size'] += 1
                        self.box['status']['secret'] += 1
                    self.secret += 1
                    self.box_count += 1
            elif self.items[item][3] == 4:
                if self.ur < self.l_ur:
                    if item not in self.box['items']['Ultra Raro']:
                        self.box['items']['Ultra Raro'][item] = {"size": 1, "data": self.items[item]}
                        self.box['status']['ur'] += 1
                    else:
                        self.box['items']['Ultra Raro'][item]['size'] += 1
                        self.box['status']['ur'] += 1
                    self.ur += 1
                    self.box_count += 1
            elif self.items[item][3] == 3:
                if self.sr < self.l_sr:
                    if item not in self.box['items']['Super Raro']:
                        self.box['items']['Super Raro'][item] = {"size": 1, "data": self.items[item]}
                        self.box['status']['sr'] += 1
                    else:
                        self.box['items']['Super Raro'][item]['size'] += 1
                        self.box['status']['sr'] += 1
                    self.sr += 1
                    self.box_count += 1
            elif self.items[item][3] == 2:
                if self.r < self.l_r:
                    if item not in self.box['items']['Raro']:
                        self.box['items']['Raro'][item] = {"size": 1, "data": self.items[item]}
                        self.box['status']['r'] += 1
                    else:
                        self.box['items']['Raro'][item]['size'] += 1
                        self.box['status']['r'] += 1
                    self.r += 1
                    self.box_count += 1
            elif self.items[item][3] == 1:
                if self.i < self.l_i:
                    if item not in self.box['items']['Incomum']:
                        self.box['items']['Incomum'][item] = {"size": 1, "data": self.items[item]}
                        self.box['status']['i'] += 1
                    else:
                        self.box['items']['Incomum'][item]['size'] += 1
                        self.box['status']['i'] += 1
                    self.i += 1
                    self.box_count += 1
            elif self.items[item][3] == 0:
                if self.c < self.l_c:
                    if item not in self.box['items']['Comum']:
                        self.box['items']['Comum'][item] = {"size": 1, "data": self.items[item]}
                        self.box['status']['c'] += 1
                    else:
                        self.box['items']['Comum'][item]['size'] += 1
                        self.box['status']['c'] += 1
                    self.c += 1
                    self.box_count += 1
        return self.box

    async def buy_box(self, bot, ctx, summon):
        query = {"_id": 0, "user_id": 1, "treasure": 1}
        data_user = await (await bot.db.cd("users")).find_one({"user_id": ctx.author.id}, query)

        if data_user['treasure']['money'] > 2000:
            answer = await bot.db.take_money(ctx, 2000)
        else:
            return await ctx.send("<:alert:739251822920728708>│`VOCÊ NÃO TEM DINHEIRO PARA COMPRAR "
                                  "A BOX!\nVOCÊ PRECISA DE 2.000 ETHERNYAS PARA COMPRAR UMA BOX.`")
        query_user = {"$set": {}}
        box = self.create_box(summon)
        query_user["$set"]["box"] = box
        cl = await bot.db.cd("users")
        await cl.update_one({"user_id": data_user["user_id"]}, query_user, upsert=False)
        await ctx.send(answer)
        await ctx.send("```A BOX ENCONTRA-SE NA SUA CONTA!```")

    def buy_item(self, box_):
        self.item_ = None
        for k, v in self.bl.items():
            self.booster_choice[k] = box_['status'][v]

        list_items = []
        for i_, amount in self.booster_choice.items():
            list_items += [i_] * amount

        try:
            result = choice(list_items)
        except IndexError:
            return "<:alert:739251822920728708>│`VOCÊ FALHOU EM COMPRAR O ITEM...`", None

        temp_list = []
        for k in box_['items'][result].keys():
            if box_['items'][result][k]['size'] > 0:
                temp_list += [k] * box_['items'][result][k]['size']

        self.item_ = choice(temp_list)
        return self.item_, box_['items'][result][self.item_]

    async def buy_booster(self, bot, ctx, vip):
        query = {"_id": 0, "user_id": 1, "box": 1, "user": 1, "treasure": 1, "config": 1}
        data_user = await (await bot.db.cd("users")).find_one({"user_id": ctx.author.id}, query)
        if not data_user['box']['status']['active']:
            return "<:alert:739251822920728708>|`BOX INATIVA!`", None

        price = 500
        if data_user['user']['ranking'] == "Bronze":
            price -= 50
        if data_user['user']['ranking'] == "Silver":
            price -= 75
        if data_user['user']['ranking'] == "Gold":
            price -= 125
        if data_user['config']['vip']:
            price -= 50

        if data_user['treasure']['money'] < price:
            return (f"<:alert:739251822920728708>│`VOCÊ NÃO TEM DINHEIRO PARA COMPRAR UM BOOSTER"
                    f"\nVOCÊ PRECISA DE {price} ETHENYAS PARA COMPRAR UM BOOSTER.`", None)

        await bot.db.take_money(ctx, price)
        query_user = {"$inc": {}}

        item = self.buy_item(data_user['box'])
        if item is None:
            return "<:alert:739251822920728708>│`VOCÊ FALHOU EM COMPRAR O ITEM...`", None

        Empty = False
        rarity = list(self.legend.keys())[list(self.legend.values()).index(item[1]['data'][3])]
        query_user["$inc"][f"box.status.{self.bl[rarity]}"] = -1
        query_user["$inc"][f"box.items.{rarity}.{item[0]}.size"] = -1
        query_user["$inc"][f"box.status.size"] = -1
        data_user['box']['status']['size'] -= 1

        if data_user['box']['status']['size'] < 1:
            query_user["$set"] = {}
            query_user["$set"]["box.status.active"] = False
            Empty = True

        _bonus = ['crystal_fragment_light', 'crystal_fragment_energy', 'crystal_fragment_dark']
        gem = {"copper": 8, "silver": 8, "gold": 8, "platinum": 8, "sapphire": 4,
               "ruby": 4, "emerald": 4, "amethyst": 4, "onyx": 2, "diamond": 2}
        _reward = list()
        for k in gem.keys():
            _reward += [k] * gem[k]
        _list = _reward if randint(1, 100) < 9 else _bonus

        bonus_1 = choice(_list)
        bonus_2 = choice(["Melted_Bone", "Life_Crystal", "Death_Blow", "Stone_of_Soul", "Vital_Force", "Energy"])
        quant_1, quant_2, quant_3 = randint(1, 3), randint(1, 3), randint(1, 3)

        query_user["$inc"][f"inventory.{item[0]}"] = quant_1
        query_user["$inc"][f"inventory.{bonus_1}"] = quant_2
        query_user["$inc"][f"inventory.{bonus_2}"] = quant_3

        cl = await bot.db.cd("users")
        await cl.update_one({"user_id": data_user["user_id"]}, query_user, upsert=False)

        if Empty:
            item_1 = choice(['Unearthly', 'Surpassing', 'Hurricane', 'Heavenly', 'Blazing', 'Augur'])
            item_2 = choice(['Crystal_of_Energy', 'Discharge_Crystal', 'Acquittal_Crystal'])
            item_3 = choice(['SoulStoneYellow', 'SoulStoneRed', 'SoulStonePurple', 'SoulStoneGreen',
                             'SoulStoneDarkGreen', 'SoulStoneBlue'])
            reward = [item_1, item_2, item_3]
            response = await bot.db.add_reward(ctx, reward)
            empty = f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 `VOCE ACABA DE ESVAZIAR SUA BOX, " \
                    f"COMO PREMIO VOCE ACABA DE GANHAR UM ITEM:` ✨ **LEGENDARY** ✨\n{response.upper()}"
            await bot.data.add_sts(ctx.author, "boxes_finished", 1)
        else:
            empty = None

        if rarity.lower() in ["ultra raro", "secret"]:
            if vip:
                return (f"`{quant_1}` - **{item[1]['data'][1]}**\n"
                        f"**+{quant_2}** - {self.items[bonus_1][1]} | "
                        f"**+{quant_3}** - {self.items[bonus_2][1]}", empty)

            return (f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 `VOCE TIROU:`\n"
                    f"`{quant_1}` {item[1]['data'][0]} **{item[1]['data'][1]}** "
                    f"`ELE TEM O TIER` ✨ **{rarity.upper()}** ✨\n"
                    f"`+{quant_2}` {self.items[bonus_1][0]} **{self.items[bonus_1][1]}** | "
                    f"`+{quant_3}` {self.items[bonus_2][0]} **{self.items[bonus_2][1]}**", empty)

        if vip:
            return (f"**{quant_1}** - {item[1]['data'][1]}\n"
                    f"**+{quant_2}** - {self.items[bonus_1][1]} | "
                    f"**+{quant_3}** - {self.items[bonus_2][1]}", empty)

        return (f"<:mito:745375589145247804>│`VOCE TIROU:`\n"
                f"`{quant_1}` {item[1]['data'][0]} **{item[1]['data'][1]}** "
                f"`ELE TEM O TIER` **{rarity.upper()}**\n"
                f"`+{quant_2}` {self.items[bonus_1][0]} **{self.items[bonus_1][1]}** | "
                f"`+{quant_3}` {self.items[bonus_2][0]} **{self.items[bonus_2][1]}**", empty)

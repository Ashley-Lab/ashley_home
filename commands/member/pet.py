import disnake

from resources.color import random_color
from disnake import Embed
from disnake.ext import commands
from resources.webhook import Webhook
from datetime import datetime
from resources.check import check_it
from resources.db import Database
from random import choice
from resources.utility import get_content


class Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z')

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='pet')
    async def pet(self, ctx, *, msg: str = "Oiiiii"):
        """Comando usado pra se comunicar com pet
        Use ash pet <pergunta ou qualquer besteira>"""
        try:
            pet_n = choice(list(self.bot.pets.keys()))
            pet = self.bot.pets[pet_n]
            if pet['colour'][0] is True:
                pet_c = choice(pet['colour'][2])
                indice = pet['colour'][2].index(pet_c)
                mask = choice(self.letters[:pet['mask'][indice]])
                link_ = f'images/pet/{pet_n}/{pet_c}/mask_{mask}.png'
            else:
                mask = choice(self.letters[:pet['mask'][0]])
                link_ = f'images/pet/{pet_n}/mask_{mask}.png'

            avatar = open(link_, 'rb')
            _webhook = await ctx.channel.create_webhook(name=pet_n, avatar=avatar.read())
            avatar_webhook = _webhook.avatar
            if 'a_' in avatar_webhook.url:
                format_1 = '.gif'
            else:
                format_1 = '.webp'
            webhook = Webhook(url=_webhook.url)
            webhook.embed = Embed(
                colour=random_color(),
                description=f"```{get_content(msg.lower())}```",
                timestamp=datetime.utcnow()
            ).set_author(
                name=ctx.author.name,
                icon_url=ctx.author.display_avatar
            ).set_thumbnail(
                url=f'https://cdn.discordapp.com/avatars/{_webhook.id}/{avatar_webhook.url}{format_1}?size=1024'
            ).to_dict()
            await webhook.send()
            await _webhook.delete()
        except disnake.Forbidden:
            await ctx.send("<:alert:739251822920728708>│`Não tenho permissão de gerenciar WEBHOOKS nesse "
                           "servidor.`")


def setup(bot):
    bot.add_cog(Pet(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mPET\033[1;32m foi carregado com sucesso!\33[m')

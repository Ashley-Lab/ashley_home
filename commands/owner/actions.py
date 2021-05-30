import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class ActionsClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='add_ban')
    async def add_ban(self, ctx, id_: int = None, *, reason: str = "SEM REGISTRAR O MOTIVO!"):
        """apenas desenvolvedores
        exemplo: ash add_ban <id> <reason>"""
        if id_ is None:
            return await ctx.send("<:alert:739251822920728708>│`O ID NÃO PODE SER VAZIO!`")
        guild = await self.bot.db.get_data("guild_id", id_, "guilds")
        if guild is None:
            user = await self.bot.db.get_data("user_id", id_, "users")
            if user is None:
                return await ctx.send("<:alert:739251822920728708>│`ID INVALIDO!`")
        answer = await self.bot.ban_(id_, reason)
        if answer:
            embed = discord.Embed(
                color=discord.Color.red(),
                description=f'<:confirmed:721581574461587496>│`Banimento adicionado com sucesso!`')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=discord.Color.red(),
                description=f'<:alert:739251822920728708>│`Esse ID já está dentro da lista negra!`')
            await ctx.send(embed=embed)

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='remove_ban')
    async def remove_ban(self, ctx, id_: int = None):
        """apenas desenvolvedores
        exemplo: ash add_ban <id>"""
        if id_ is None:
            return await ctx.send("<:alert:739251822920728708>│`O ID NÃO PODE SER VAZIO!`")
        guild = await self.bot.db.get_data("guild_id", id_, "guilds")
        if guild is None:
            user = await self.bot.db.get_data("user_id", id_, "users")
            if user is None:
                return await ctx.send("<:alert:739251822920728708>│`ID INVALIDO!`")
        answer = await self.bot.un_ban_(id_)
        if answer:
            embed = discord.Embed(
                color=discord.Color.red(),
                description=f'<:confirmed:721581574461587496>│`Banimento revogado com sucesso!`')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=discord.Color.red(),
                description=f'<:alert:739251822920728708>│`Esse ID não está dentro da lista negra!`')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ActionsClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mACTIONS\033[1;32m foi carregado com sucesso!\33[m')

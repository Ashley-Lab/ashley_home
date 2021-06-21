import re
import discord.utils

from config import data
from discord.ext import commands


def ash_perms(perms):
    ash = ["embed_links", "attach_files", "add_reactions", "read_messages", "send_messages", "external_emojis"]
    for t in perms:
        if t[0] in ash and not t[1]:
            return False
    return True


def check_it(**kwargs):
    permissions = ('add_reactions', 'administrator', 'attach_files', 'ban_members', 'change_nickname' 'connect',
                   'create_instant_invite' 'deafen_members', 'embed_links', 'external_emojis', 'kick_members',
                   'manage_channels', 'manage_emojis', 'manage_guild', 'manage_messages', 'manage_nicknames',
                   'manage_roles', 'manage_webhooks', 'mention_everyone', 'move_members', 'mute_members',
                   'priority_speaker', 'read_message_history', 'read_messages', 'send_messages', 'send_tts_messages',
                   'speak', 'use_voice_activation', 'view_audit_log')

    async def check_permissions(ctx, perms_, *, check=all):
        resolved = ctx.author.guild_permissions
        return check(getattr(resolved, name, None) == value for name, value in perms_.items())

    def predicate(ctx):
        if ctx.message.webhook_id is not None:
            return True

        _vip = False
        if ctx.guild is not None:
            if ctx.guild.id in ctx.bot.guilds_vips:
                _vip = True

        guild = ctx.bot.get_guild(ctx.bot.config['config']['default_guild'])
        if ctx.author.id not in [m.id for m in guild.members]:
            msg = "<:alert:739251822920728708>│`Voce precisa está dentro do meu servidor de suporte, para poder me " \
                  "usar.`\n**Obs:** Para entrar no servidor de suporte use o comando **ash invite** para receber o" \
                  " convite do servidor!\n**Nota:** `Servidores` **VIPS** `não precisam que seus membros estejam no " \
                  "servidor de suporte!`"
            if ctx.command.name in ["invite", "register", "register guild"] or _vip:
                pass
            else:
                raise commands.CheckFailure(msg)

        if isinstance(ctx.message.channel, (discord.DMChannel, discord.GroupChannel)):
            if ctx.command.name == "help" or ctx.command.name == "ajuda":
                pass
            else:
                if kwargs.get('no_pm', False):
                    pass
                else:
                    raise commands.NoPrivateMessage('<:alert:739251822920728708>│`Você não pode mandar comandos em '
                                                    'mensagens privadas!`')

        if not (isinstance(ctx.channel, (discord.DMChannel, discord.GroupChannel))) and kwargs.get('is_nsfw', False):
            if ctx.channel.is_nsfw() is False:
                raise commands.CheckFailure("<:alert:739251822920728708>│`Esse comando apenas pode ser usado"
                                            " em um canal` **nsfw!!**")

        if ctx.author.id == data['config']['owner_id'] and kwargs.get('is_owner', False):
            pass
        elif ctx.author.id in ctx.bot.staff and kwargs.get('is_owner', False):
            pass
        elif ctx.author.id != data['config']['owner_id'] and kwargs.get('is_owner', False):
            raise commands.CheckFailure("<:alert:739251822920728708>│`Apenas meu criador pode usar esse comando!`")

        if kwargs.get("check_role", False):
            role = discord.utils.find(lambda r: r.name in kwargs.get("roles", []), ctx.author.roles)
            if role is None:
                raise commands.CheckFailure("<:alert:739251822920728708>│`Você precisa de um cargo "
                                            "específico para usar esse comando!`")

        perms = dict()
        for perm_ in kwargs.keys():
            if perm_ in permissions:
                perms[perm_] = kwargs[perm_]
        return check_permissions(ctx, perms)

        # return True
    return commands.check(predicate)


regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def validate_url(url):
    return bool(regex.fullmatch(url))

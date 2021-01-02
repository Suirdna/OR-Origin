from client import exception, discord_manager, json_manager, permissions, origin
from client.config import config as c, language as l
import discord

async def create_embed(ctx, color, title, icon_url, thumbnail, author_name, embed_json, inline, author=False, channel=False, description=False):
    try:
        guild_l = await origin.get_language(ctx.guild.id if hasattr(ctx, 'guild') else ctx)

        if title:
            win = discord.Embed(
                color=color,
                title='{}'.format(c.DISCORD_SPLIT),
                description='{}'.format(description if description else '')
            )
        else:
            win = discord.Embed(
                color=color,
                description='{}'.format(description if description else '')
            )

        if thumbnail:
            win.set_thumbnail(url=thumbnail)

        if author_name and icon_url:
            win.set_author(name='{}'.format(author_name), icon_url=icon_url)

        for index, value1 in enumerate(embed_json):
            win.add_field(name='{}'.format(value1['name{}'.format(index + 1)]), value='{}'.format(value1['value{}'.format(index + 1)]), inline=inline)

        win.set_footer(text=l.embed_footer[guild_l]['embed1'], icon_url=c.CLIENT_ICON)

        if author:
            if hasattr(ctx, 'author'):
                return await ctx.author.send(embed=win)
            else:
                return await author.send(embed=win)
        else:
            if channel:
                return await channel.send(embed=win)
            else:
                if hasattr(ctx, 'send'):
                    return await ctx.send(embed=win)

    except Exception as error:
        await exception.error(error)

async def create_embed_command_listener(self, ctx, client, embed_json, author_name, status=False):
    try:
        guild_l = await origin.get_language(ctx.guild.id)

        if str(ctx.message.channel.type) == 'text':
            modules = await permissions.check_module_permission(ctx)
            thumbnail = c.CLIENT_ICON
            icon_url = thumbnail

            win = discord.Embed(
                title='{}'.format(c.DISCORD_SPLIT),
                color=discord.Color.gold()
            )

            win.set_thumbnail(url=thumbnail)
            win.set_author(name='{}'.format(author_name), icon_url=icon_url)

            if status == 'admin':
                if await json_manager.get_status(c.GUILD_PATH['special_member.json'].format(ctx.guild.id), 'user_id', ctx.author.id) or ctx.author.id == ctx.guild.owner.id or ctx.author.id == c.CLIENT_ADMINISTRATION_ID:
                    members = await json_manager.get_json(c.GUILD_PATH['special_member.json'].format(ctx.guild.id))
                    special2 = ''
                    special3 = ''
                    special4 = ''

                    for member in members:
                        user = await discord_manager.get_member(client, ctx.guild.id, member['user_id'])
                        if user:
                            special4 += '{} '.format(user.mention)

                            if member['user_status'] >= 2:
                                special3 += '{} '.format(user.mention)

                            if member['user_status'] >= 3:
                                special2 += '{} '.format(user.mention)

                    special1 = '{}'.format(ctx.guild.owner.mention)

                    for key1, value1 in embed_json.items():
                        if key1 == 'commands':
                            win.add_field(name='{}'.format(value1['name']), value='{}'.format(value1['value']), inline=False)

                        for module in modules:
                            if key1 == module:
                                win.add_field(name='{}'.format(value1['name']), value='{}'.format(value1['value']), inline=False)

                        if key1 == 'special1':
                            win.add_field(name='{}'.format(value1['name']), value='{}'.format(special1 if special1 else l.server[guild_l]['configuration']['extra_1']), inline=False)

                        if key1 == 'special2':
                            win.add_field(name='{}'.format(value1['name']), value='{}'.format(special2 if special2 else l.server[guild_l]['configuration']['extra_1']), inline=False)

                        if key1 == 'special3':
                            win.add_field(name='{}'.format(value1['name']), value='{}'.format(special3 if special3 else l.server[guild_l]['configuration']['extra_1']), inline=False)

                        if key1 == 'special4':
                            win.add_field(name='{}'.format(value1['name']), value='{}'.format(special4 if special4 else l.server[guild_l]['configuration']['extra_1']), inline=False)

                    await ctx.author.send(embed=win)
                else:
                    await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
            elif status == 'help':
                for key1, value1 in embed_json.items():
                    if key1 == 'commands':
                        win.add_field(name='{}'.format(value1['name']), value='{}'.format(value1['value']), inline=False)

                    for module in modules:
                        if key1 == module:
                            win.add_field(name='{}'.format(value1['name']), value='{}'.format(value1['value']), inline=False)

                await ctx.author.send(embed=win)
            elif status == 'about':
                for key1, value1 in embed_json.items():
                    win.add_field(name='{}'.format(value1['name']), value='{}'.format(value1['value']), inline=False)
                await ctx.send(embed=win)
        else:
            await ctx.send(l.module_permissions[guild_l]['msg_restricted_pm'])
    except Exception as error:
        await exception.error(error)
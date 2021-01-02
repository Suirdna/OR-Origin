from client import exception, file_manager, ini_manager, json_manager, permissions, origin
from client.external.hiscores import hiscores_kc
from client.config import config as c, language as l
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import discord, locale

class maNothing_KC_mod(commands.Cog):
    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    name = 'maNothing_KC_mod'
    hiscores2V = None

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    async def fun_kc(self, ctx):
        try:
            STATUS = False
            STRING = str(ctx.message.content).split()
            path = c.GUILD_PATH['rsn.json'].format(ctx.guild.id)
            DATA = await json_manager.get_json(path)

            if len(STRING) >= 2:
                RSN = None
                if DATA:
                    for data in DATA:
                        if data['user_id'] == ctx.author.id:
                            STATUS = True
                            RSN_LIST = data['rsn']
                            RSN_LIST.reverse()
                            RSN = RSN_LIST[0]

                    if STATUS:
                        path1 = c.PRIVATE_PATH['maNothing_KC_mod.ini']
                        ini = await ini_manager.get_ini(path1)
                        LIST1 = await json_manager.get_ini_list(path1, 'CONSTANT1', 'NAME')
                        LIST3 = await json_manager.get_ini_list(path1, 'CONSTANT1', 'PRE')
                        LIST2 = await json_manager.get_ini_list(path1, 'CONSTANT2', 'PNG')

                        RSN = RSN.replace(' ', '%20')
                        self.hiscores2V = hiscores_kc.Hiscores2V(RSN, LIST1, LIST3)
                        RSN = RSN.replace('%20', ' ')

                        BOSS_NAME = ''
                        for text in STRING[1:]:
                            BOSS_NAME += '{} '.format(text)
                        BOSS_NAME = BOSS_NAME.rstrip()
                        boss = self.hiscores2V.getKc(BOSS_NAME)

                        if boss:
                            await origin.get_locale()

                            INFO_PANEL_IMAGE = ini['CONSTANT2']['INFO_PANEL']
                            FONT_PATH = ini['CONSTANT2']['FONT']
                            INFO_PANEL_OBJECT = None

                            for index, name in enumerate(LIST1):
                                if name == boss['boss']:
                                    INFO_PANEL_OBJECT = LIST2[index]

                            with Image.open(INFO_PANEL_IMAGE).convert('RGBA') as im:
                                with Image.open(INFO_PANEL_OBJECT).convert('RGBA') as im2:
                                    size1 = im.size
                                    size2 = im2.size
                                    y = int(size1[1] / 2) - int(size2[1] / 2)
                                    im.paste(im2, (18, y), im2)

                                    draw = ImageDraw.Draw(im)
                                    font = ImageFont.truetype(FONT_PATH, 16)
                                    draw.text((85, y + 6), 'MANO RSN: ', (165, 165, 165), font=font)
                                    draw.text((85, y + 20), 'BOSAS: ', (165, 165, 165), font=font)
                                    draw.text((85, y + 33), 'KC: ', (165, 165, 165), font=font)
                                    draw.text((85, y + 46), 'RANKAS: ', (165, 165, 165), font=font)

                                    draw.text((145, y + 6), '{}'.format(RSN), (255, 255, 255), font=font)
                                    draw.text((128, y + 20), '{}'.format(boss['boss']), (255, 255, 255), font=font)
                                    draw.text((108, y + 33), '{}'.format(locale.format_string('%d', int(boss['kc']), grouping=True)), (255, 255, 255), font=font)
                                    draw.text((135, y + 46), '{}'.format(locale.format_string('%d', int(boss['rank']), grouping=True)), (255, 255, 255), font=font)

                                    TEMP_FILE = '{}_{}_{}.png'.format(RSN, boss['boss'], boss['kc'])
                                    im.save(TEMP_FILE, 'PNG')
                                    rank = open(TEMP_FILE, 'rb')
                                    await ctx.send(file=discord.File(rank))
                                    rank.close()
                                    await file_manager.delete_file(TEMP_FILE)
                        else:
                            await ctx.send('\🔴 *Patikra nepavyko. Bosas pavadinimu {} nerastas sistemoje. Norint pasižiūrėti bosų sąrašą, rašykite komandą* `.bosslist`'.format(BOSS_NAME))
                    else:
                        await ctx.send('\🔴 *Patikra nepavyko. Jūsų RSN nerastas sistemoje. Prašome užregistruoti RSN ir bandykite dar kartą. Komanda* `.rsn`')
                else:
                    await ctx.send('\🔴 *Patikra nepavyko. Jūsų RSN nerastas sistemoje. Prašome užregistruoti RSN ir bandykite dar kartą. Komanda* `.rsn`')
            else:
                await ctx.send('\🟢 *Pavyzdys* _**.kc Vorkath**_')
        except Exception as error:
            await exception.error(error)

    @staticmethod
    async def fun_bosslist(ctx):
        try:
            path1 = c.PRIVATE_PATH['maNothing_KC_mod.ini']

            LIST1 = await json_manager.get_ini_list(path1, 'CONSTANT1', 'NAME')
            LIST3 = await json_manager.get_ini_list(path1, 'CONSTANT1', 'PRE')

            LIST = "```"

            for index, name in enumerate(LIST1):
                LIST += '.kc {} ---> {}\n'.format(LIST3[index], name)

            LIST += "```"
            await ctx.send(LIST)
        except Exception as error:
            await exception.error(error)

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    def __init__(self, client):
        self.client = client
        self.name = 'maNothing_KC_mod'

    @commands.command()
    async def kc(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['admin.ini'], self.fun_kc, False)
            else:
                await ctx.send(l.module_permissions['LT']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def bosslist(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['admin.ini'], self.fun_bosslist, False)
            else:
                await ctx.send(l.module_permissions['LT']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

def setup(client):
    client.add_cog(maNothing_KC_mod(client))
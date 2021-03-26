import command_listener, event_listener
from client.external import preprocessor, admin, dc_bank, organizer, rsn_register, server, vote, xp_tracker, kc_tracker
from client.external.private import maNothing_KC_mod

#▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
#BOT CONSOLE INTERFACE

CLIENT_LOGO = [
    ' _____   ______ _____  ______ _____ __   _',
    '|     | |_____/   |   |  ____   |   | \  |',
    '|_____| |    \_ __|__ |_____| __|__ |  \_|',
]

CLIENT_SPLIT = '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬'

#▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
#BOT CONFIGURATION

CLIENT_NAME = 'Origin'
CLIENT_PREFIX = '.'
CLIENT_ICON = 'https://media.discordapp.net/attachments/714144907152850954/735094104895258654/logo.png'

CLIENT_ADMINISTRATION_ID = 
CLIENT_DISCORD = 'https://discord.gg/HjVyBWu'
CLIENT_INVITE = ''

CLIENT_AUTHOR = 'Andrius Lizunovas'
CLIENT_WEBSITE = ''
CLIENT_VERSION = 1.42
CLIENT_REGION = 'Europe/Berlin'
DEVELOPER_STATUS = True

if DEVELOPER_STATUS:
    CLIENT_ID = 
    CLIENT_TOKEN = ''
    DISCORD_NAME = 'Origin Dev'
else:
    CLIENT_ID = 
    CLIENT_TOKEN = ''
    DISCORD_NAME = 'Origin'
    
#▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
#BOT PATHS

CLIENT_STATUS = [
    '.help',
    '.admin',
    '.about',
]

CLIENT_PATH = {
    'guild': './guild/',
    'client': './client/',
    'default': '/default/',
    'data': '/data/',
    'logs': '/logs/',
    'logs2': 'logs/',
    'logs3': './logs/',
    'messages': 'messages/',
    'origin2': 'origin/',
    'json': 'json',
    'ini': 'ini',
    'pre': 'preprocessor',
    'embed': 'embeds',
    'global': 'global',
    'config': 'config/',
    'external': 'external/',
    'private': 'private/'
}

CLIENT_MODULES = [
    event_listener.event_listener.name,
    command_listener.command_listener.name,
    'client.external.{}'.format(preprocessor.preprocessor.name),
    'client.external.{}'.format(admin.admin.name),
    'client.external.{}'.format(dc_bank.dc_bank.name),
    'client.external.{}'.format(organizer.organizer.name),
    'client.external.{}'.format(rsn_register.rsn_register.name),
    'client.external.{}'.format(server.server.name),
    'client.external.{}'.format(vote.vote.name),
    'client.external.{}'.format(xp_tracker.xp_tracker.name),
    'client.external.{}'.format(kc_tracker.kc_tracker.name),
    'client.external.private.{}'.format(maNothing_KC_mod.maNothing_KC_mod.name)
]

CLIENT_PRIVATE_MODULES = [
    'client.external.private.{}'.format(maNothing_KC_mod.maNothing_KC_mod.name)
]

DONT_SHOW_MODULES = [
    'client.external.{}'.format(admin.admin.name),
    'client.external.{}'.format(dc_bank.dc_bank.name),
    'client.external.{}'.format(organizer.organizer.name),
    'client.external.{}'.format(rsn_register.rsn_register.name),
    'client.external.{}'.format(server.server.name),
    'client.external.{}'.format(vote.vote.name),
    'client.external.{}'.format(xp_tracker.xp_tracker.name),
    'client.external.{}'.format(kc_tracker.kc_tracker.name),
    'client.external.private.{}'.format(maNothing_KC_mod.maNothing_KC_mod.name)
]

CLIENT_INI = {
    admin.admin.name: '/{}.ini'.format(admin.admin.name),
    dc_bank.dc_bank.name: '/{}.ini'.format(dc_bank.dc_bank.name),
    organizer.organizer.name: '/{}.ini'.format(organizer.organizer.name),
    rsn_register.rsn_register.name: '/{}.ini'.format(rsn_register.rsn_register.name),
    xp_tracker.xp_tracker.name: '/{}.ini'.format(xp_tracker.xp_tracker.name),
    kc_tracker.kc_tracker.name: '/{}.ini'.format(kc_tracker.kc_tracker.name),
    vote.vote.name: '/{}.ini'.format(vote.vote.name),
}

CLIENT_JSON = {
    'bank': '/bank.json',
    'event': '/event.json',
    'muted_member': '/muted_member.json',
    'private': '/private.json',
    'recipe': '/recipe.json',
    'rsn': '/rsn.json',
    'special_member': '/special_member.json',
    'tracker': '/tracker.json',
    'kc_tracker': '/kc_tracker.json',
    'xp_rates': '/xp_rates.json',
    'kc_rates': '/kc_rates.json',
    'modules': '/modules.json',
    'server': '/server.json',
    'guild': './guild/guild.json',
}

CLIENT_PREPROCESSOR = {
    'voteban': '/voteban.json',
}

EMBED_PATH = {
    'admin': '/admin.json',
    'command_listener': '/command_listener.json',
    'dc_bank': '/dc_bank.json',
    'rsn': '/rsn.json',
    'organizer': '/organizer.json',
    'server': '/server.json',
    'tracker': '/tracker.json'
}

GUILD_PATH = {
    '{}.ini'.format(admin.admin.name): '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['ini'], CLIENT_INI[admin.admin.name]),
    '{}.ini'.format(dc_bank.dc_bank.name): '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['ini'], CLIENT_INI[dc_bank.dc_bank.name]),
    '{}.ini'.format(organizer.organizer.name): '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['ini'], CLIENT_INI[organizer.organizer.name]),
    '{}.ini'.format(rsn_register.rsn_register.name): '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['ini'], CLIENT_INI[rsn_register.rsn_register.name]),
    '{}.ini'.format(xp_tracker.xp_tracker.name): '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['ini'], CLIENT_INI[xp_tracker.xp_tracker.name]),
    '{}.ini'.format(kc_tracker.kc_tracker.name): '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['ini'], CLIENT_INI[kc_tracker.kc_tracker.name]),
    '{}.ini'.format(vote.vote.name): '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['ini'], CLIENT_INI[vote.vote.name]),

    '{}_g.ini'.format(dc_bank.dc_bank.name): '{}{}{}{}'.format(CLIENT_PATH['client'], CLIENT_PATH['config'], CLIENT_PATH['global'], CLIENT_INI[dc_bank.dc_bank.name]),
    '{}_g.ini'.format(organizer.organizer.name): '{}{}{}{}'.format(CLIENT_PATH['client'], CLIENT_PATH['config'], CLIENT_PATH['global'], CLIENT_INI[organizer.organizer.name]),
    '{}_g.ini'.format(xp_tracker.xp_tracker.name): '{}{}{}{}'.format(CLIENT_PATH['client'], CLIENT_PATH['config'], CLIENT_PATH['global'], CLIENT_INI[xp_tracker.xp_tracker.name]),
    '{}_g.ini'.format(kc_tracker.kc_tracker.name): '{}{}{}{}'.format(CLIENT_PATH['client'], CLIENT_PATH['config'], CLIENT_PATH['global'], CLIENT_INI[kc_tracker.kc_tracker.name]),

    'bank.json': '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['json'], CLIENT_JSON['bank']),
    'event.json': '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['json'], CLIENT_JSON['event']),
    'muted_member.json': '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['json'], CLIENT_JSON['muted_member']),
    'recipe.json': '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['json'], CLIENT_JSON['recipe']),
    'rsn.json': '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['json'], CLIENT_JSON['rsn']),
    'special_member.json': '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['json'], CLIENT_JSON['special_member']),
    'tracker.json': '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['json'], CLIENT_JSON['tracker']),
    'kc_tracker.json': '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['json'], CLIENT_JSON['kc_tracker']),

    'xp_rates.json': '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['json'], CLIENT_JSON['xp_rates']),
    'kc_rates.json': '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['json'], CLIENT_JSON['kc_rates']),
    'voteban.json': '{}{}{}{}{}'.format(CLIENT_PATH['guild'], '{}', CLIENT_PATH['data'], CLIENT_PATH['pre'], CLIENT_PREPROCESSOR['voteban']),
}

ORIGIN_PATH = {
    'embed.admin.json': '{}{}{}'.format(CLIENT_PATH['client'], CLIENT_PATH['embed'], EMBED_PATH['admin']),
    'embed.command_listener.json': '{}{}{}'.format(CLIENT_PATH['client'], CLIENT_PATH['embed'], EMBED_PATH['command_listener']),
    'embed.dc_bank.json': '{}{}{}'.format(CLIENT_PATH['client'], CLIENT_PATH['embed'], EMBED_PATH['dc_bank']),
    'embed.rsn.json': '{}{}{}'.format(CLIENT_PATH['client'], CLIENT_PATH['embed'], EMBED_PATH['rsn']),
    'embed.organizer.json': '{}{}{}'.format(CLIENT_PATH['client'], CLIENT_PATH['embed'], EMBED_PATH['organizer']),
    'embed.server.json': '{}{}{}'.format(CLIENT_PATH['client'], CLIENT_PATH['embed'], EMBED_PATH['server']),
    'embed.tracker.json': '{}{}{}'.format(CLIENT_PATH['client'], CLIENT_PATH['embed'], EMBED_PATH['tracker']),
    'private.json': '{}{}'.format(CLIENT_PATH['guild'], CLIENT_JSON['private']),
}

PRIVATE_PATH = {
    '{}.ini'.format(maNothing_KC_mod.maNothing_KC_mod.name): '{}{}{}{}'.format(CLIENT_PATH['client'], CLIENT_PATH['external'], CLIENT_PATH['private'], '{}.ini'.format(maNothing_KC_mod.maNothing_KC_mod.name)),
}

#▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
#DISCORD USER PERMISSIONS

EVENT_MODE = [
    0,
    1,
]

MODE_NAME = {
    'std': 'Standart',
    'rush': 'Rush'
}

#▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
#DISCORD USER PERMISSIONS

USER_PERMISSIONS = {
    'organizer': 1,
    'admin': 2,
    'dc_bank': 3
}

#▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
#DISCORD MESSAGE INTERFACE
DISCORD_SPLIT = '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬'

DISCORD_MESSAGES = {
    'ban_reason': 'Banned nickname applied',
    'dc_bank_role_add': 'Added top role by the system',
    'dc_bank_role_remove': 'Removed top role by the system',
    'event_role_added': 'Added event role by the system',
    'role_added': 'Added role by the system',
    'role_removed': 'Removed role by the system',
    'mute_reason': 'Added mute by the system',
    'unmute_reason': 'Removed mute by the system',
    'xp_event_winner': 'Added XP event winner role by the system',
    'xp_event_prize': 'Added XP event prize role by the system',
    'kc_event_winner': 'Added KC event winner role by the system',
    'kc_event_prize': 'Added KC event prize role by the system',
}

DISCORD_CHANNEL = {
    'LT': {
        'admin': '_**‹**_ *Administracijos skiltis*',
        'chat0': '_**‹**_ *Pagrindinė pokalbių skiltis*',
        'chat1': '_**‹**_ *Boto skiltis*',
        'dc_bank': '_**‹**_ *Buhalterijos skiltis*',
        'events': '_**‹**_ *Eventų skiltis*',
        'sponsor': '_**‹**_ *Sponsorių skiltis*',
        'thanks': '_**‹**_ *Padėkų skiltis*',
        'rsn': '_**‹**_ *RSN registracijos skiltis*',
        'xp_event': '_**‹**_ *XP eventų skiltis*',
        'kc_event': '_**‹**_ *KC eventų skiltis*'
    },
    'EN': {
        'admin': '_**‹**_ *Administration channel*',
        'chat0': '_**‹**_ *General chat channel*',
        'chat1': '_**‹**_ *Bot channel*',
        'dc_bank': '_**‹**_ *Accounting channel*',
        'events': '_**‹**_ *Event channel*',
        'sponsor': '_**‹**_ *Sponsor channel*',
        'thanks': '_**‹**_ *Thanks channel*',
        'rsn': '_**‹**_ *RSN registration channel*',
        'xp_event': '_**‹**_ *XP event channel*',
        'kc_event': '_**‹**_ *KC event channel*'
    }
}

#▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
#BOT INTERFACE MESSAGES

CLIENT_MESSAGES = {
    'client_online': 'System online',
    "dc_bank_buy": "GP bought",
    'dc_bank_create': 'Bank account created',
    'dc_bank_remote_create': 'Bank account created remotely',
    'dc_bank_recipe_plus': 'GP added',
    'dc_bank_recipe_minus': 'GP removed',
    'guild_join': 'Guild joined',
    'guild_rejoin': 'Guild rejoined',
    'organizer_add': 'Added event by the organizer',
    'organizer_remove': 'Removed event by the organizer',
    'xp_tracker_reset': 'Xp reset',
    'xp_tracker_update': 'Xp update',
    'kc_tracker_reset': 'Kc reset',
    'kc_tracker_update': 'Kc update',
    'client_error': 'Client error',
    'variable_init': '{} initialization'
}

#▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
#WEB SETTINGS
WEB_LINKS = {
    'generator': 'https://origin.clan.su/generator.html',
    'setup': 'https://origin.clan.su/setup.html',
    'discord_lt': 'https://discord.gg/MsjUymJ9pp',
    'discord_en': 'https://discord.gg/DM2qZKuvn6',
    'donation_link': CLIENT_INVITE
}

#▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
#GUILD SETTINGS

GUILD_CHANNELS = [
    'general',
    'general-chat',
    'chat',
    'pagrindinis',
    'pokalbiai',
    'chatas',
    'osrs-botas',
    'osrs-bot',
    'bot-channel'
]

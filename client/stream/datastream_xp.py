from client.stream import server_timer, json_manager, exception, logger, console_interface, origin
from client.config import config as c
from client.external.hiscores import hiscores_xp
import threading, time

class datastream(threading.Thread):

    t = None
    guild = None

    def __init__(self, guild):
        threading.Thread.__init__(self)
        self.guild = guild

    def run(self):
        self.t = threading.Thread(target=self.tracker_update, args=(self.guild,))
        self.t.setDaemon(True)
        self.t.start()

    @staticmethod
    def reset(EVENT_NAME, USER, data, current, guild_id):
        try:
            path1 = c.GUILD_PATH['tracker.json'].format(guild_id)
            target_keys = [EVENT_NAME, '{}_current'.format(EVENT_NAME)]
            target_values = [USER.stats[EVENT_NAME]['experience'], USER.stats[EVENT_NAME]['experience']]
            json_manager.update(path1, 'user_rsn', data['user_rsn'], target_keys, target_values)

            client_message = 'Guild id: {} | Event: {} | Rsn: {} | Registration XP: {} | Current_XP: {} | Hour: {} Status: {}'.format(guild_id, EVENT_NAME, data['user_rsn'], data[EVENT_NAME], USER.stats[EVENT_NAME]['experience'], current.strftime('%H:%M'), 'XP reset')
            console_interface.console_message('XP reset', client_message)
            logger.log_event(guild_id, 'xp_tracker', c.CLIENT_MESSAGES['xp_tracker_reset'], client_message)
        except Exception as error:
            exception.error(error)

    @staticmethod
    def event_in_progress(guild, value, mode):
        try:
            guild_t = origin.get_region(guild)
            path1 = c.GUILD_PATH['tracker.json'].format(guild)
            DATA1 = json_manager.get_data(path1)
            COUNTER = 0

            for data in DATA1:
                CHECK = True
                USERNAME = data['user_rsn']
                USERNAME = USERNAME.replace(' ', '%20')

                while CHECK:
                    USER = hiscores_xp.Hiscores(USERNAME, 'N')
                    if USER.status != 404:
                        if hasattr(USER, 'stats'):
                            while CHECK:
                                CHECK = False
                                if data[value['event_name']]:
                                    current = server_timer.get_current_time(guild_t)
                                    target_keys = ['{}_current'.format(value['event_name'])]
                                    target_values = [USER.stats[value['event_name']]['experience']]
                                    json_manager.update(path1, 'user_rsn', data['user_rsn'], target_keys, target_values)

                                    client_message = 'Guild id: {} | Guild time: {} | Event: {} | Mode: {} | Rsn: {} | Registration XP: {} | Current XP: {} | Status: {}'.format(guild, current.strftime('%H:%M'), value['event_name'], mode, data['user_rsn'], data[value['event_name']], USER.stats[value['event_name']]['experience'], 'XP update')
                                    console_interface.console_message('XP update', client_message)
                                    logger.log_event(guild, 'xp_tracker', c.CLIENT_MESSAGES['xp_tracker_update'], client_message)
                    else:
                        if COUNTER >= 10:
                            CHECK = False
                            COUNTER = 0
                        else:
                            COUNTER += 1

        except Exception as error:
            exception.error(error)

    def event_start(self, guild, value, mode):
        try:
            guild_t = origin.get_region(guild)
            path1 = c.GUILD_PATH['tracker.json'].format(guild)
            path2 = c.GUILD_PATH['xp_rates.json'].format(guild)
            DATA1 = json_manager.get_data(path1)
            DATA2 = json_manager.get_data(path2)

            current = server_timer.get_current_time(guild_t)
            COUNTER = 0
            USER = None

            for data in DATA1:
                CHECK = True
                USERNAME = data['user_rsn']
                USERNAME = USERNAME.replace(' ', '%20')

                while CHECK:
                    USER = hiscores_xp.Hiscores(USERNAME, 'N')
                    if USER.status != 404:
                        if hasattr(USER, 'stats'):
                            while CHECK:
                                CHECK = False

                                if data[value['event_name']]:
                                    target_keys = ['{}_current'.format(value['event_name'])]
                                    target_values = [USER.stats[value['event_name']]['experience']]
                                    json_manager.update(path1, 'user_rsn', data['user_rsn'], target_keys, target_values)

                                    client_message = 'Guild id: {} | Guild time: {} | Event: {} | Mode: {} | Rsn: {} | Registration XP: {} | Current XP: {} | Status: {}'.format(guild, current.strftime('%H:%M'), value['event_name'], mode, data['user_rsn'], data[value['event_name']], USER.stats[value['event_name']]['experience'], 'XP update')
                                    console_interface.console_message('XP update', client_message)
                                    logger.log_event(guild, 'xp_tracker', c.CLIENT_MESSAGES['xp_tracker_update'], client_message)
                    else:
                        if COUNTER >= 10:
                            CHECK = False
                            COUNTER = 0
                        else:
                            COUNTER += 1

                for value2 in DATA2:
                    for key, value3 in value.items():
                        if key == value['event_name']:
                            if (data['{}_current'.format(value['event_name'])] - data[value['event_name']]) >= value2[value['event_name']] and value['date_start'] == current.strftime('%m.%d') and value['time_start'] == current.hour:
                                self.reset(value['event_name'], USER, data, current, guild)
                            else:
                                pass

                            if (data['{}_current'.format(value['event_name'])] - data[value['event_name']]) >= value2[value['event_name']] * 2 and value['date_start'] == current.strftime('%m.%d') and value['time_start'] + 1 == current.hour:
                                self.reset(value['event_name'], USER, data, current, guild)
                            else:
                                pass

                            if (data['{}_current'.format(value['event_name'])] - data[value['event_name']]) >= value2[value['event_name']] * 3 and value['date_start'] == current.strftime('%m.%d') and value['time_start'] + 2 == current.hour:
                                self.reset(value['event_name'], USER, data, current, guild)
                            else:
                                pass

                            if (data['{}_current'.format(value['event_name'])] - data[value['event_name']]) >= value2[value['event_name']] * 4 and value['date_start'] == current.strftime('%m.%d') and value['time_start'] + 3 == current.hour:
                                self.reset(value['event_name'], USER, data, current, guild)
                            else:
                                pass

                            if (data['{}_current'.format(value['event_name'])] - data[value['event_name']]) >= value2[value['event_name']] * 5 and value['date_start'] == current.strftime('%m.%d') and value['time_start'] + 4 == current.hour:
                                self.reset(value['event_name'], USER, data, current, guild)
                            else:
                                pass

                            if (data['{}_current'.format(value['event_name'])] - data[value['event_name']]) >= value2['time_start'] + 5 == current.hour:
                                self.reset(value['event_name'], USER, data, current, guild)
                            else:
                                pass

        except Exception as error:
            exception.error(error)

    def tracker_update(self, guild):
        try:
            while True:
                guild_t = origin.get_region(guild)
                path2 = c.GUILD_PATH['event.json'].format(guild)
                LIST1 = json_manager.get_data(path2)
                guild_current = server_timer.get_current_time(guild_t)

                if LIST1:
                    for value in LIST1:
                        if value['type'] == 1 and value['status'] == 1:
                            if guild_current.month == int(value['date_start'][:2]):
                                if guild_current.day == int(value['date_start'][3:]):
                                    if value['time_start'] + 1 >= guild_current.hour and value['time_start'] + 1 <= guild_current.hour + 5:
                                        self.event_start(guild, value, c.MODE_NAME['std'])

                        if value['type'] == 1 and value['status'] == 1:
                            if guild_current.month == int(value['date_end'][:2]):
                                if guild_current.day == int(value['date_end'][3:]):
                                    if guild_current.hour + 6 >= value['time_end'] and guild_current.hour < value['time_end'] - 1:
                                        self.event_in_progress(guild, value, c.MODE_NAME['std'])

                        if value['type'] == 2 and value['status'] == 1:
                            if guild_current.month >= int(value['date_start'][:2]):
                                if guild_current.day >= int(value['date_start'][3:]):
                                    self.event_in_progress(guild, value, c.MODE_NAME['rush'])

                time.sleep(60*10)

        except Exception as error:
            exception.error(error)

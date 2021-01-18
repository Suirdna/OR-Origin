from client.stream import server_timer, json_manager, exception, logger, console_interface, origin
from client.config import config as c
from client.external.hiscores import hiscores_kc
import threading, time

class datastream(threading.Thread):

    t = None
    guild = None

    def __init__(self, guild):
        threading.Thread.__init__(self)
        self.guild = guild

    def run(self):
        self.t = threading.Thread(target=self.tracker_update_kc, args=(self.guild,))
        self.t.setDaemon(True)
        self.t.start()

    @staticmethod
    def reset(EVENT_NAME, USER, data, current, guild_id):
        try:
            USER_STATS = USER.getKc(EVENT_NAME)
            path1 = c.GUILD_PATH['kc_tracker.json'].format(guild_id)
            target_keys = [EVENT_NAME, '{}_current'.format(EVENT_NAME)]
            target_values = [int(USER_STATS['kc']), int(USER_STATS['kc'])]
            json_manager.update(path1, 'user_rsn', data['user_rsn'], target_keys, target_values)

            client_message = 'Guild id: {} | Event: {} | Rsn: {} | Registration KC: {} | Current_KC: {} | Guild time: {} Status: {}'.format(guild_id, EVENT_NAME, data['user_rsn'], data[EVENT_NAME], USER_STATS['kc'], current.strftime('%H:%M'), 'KC reset')
            console_interface.console_message('KC reset', client_message)
            logger.log_event(guild_id, 'kc_tracker', c.CLIENT_MESSAGES['kc_tracker_reset'], client_message)
        except Exception as error:
            exception.error(error)

    @staticmethod
    def event_in_progress(guild, value, mode):
        try:
            guild_t = origin.get_region(guild)
            path1 = c.GUILD_PATH['kc_tracker.json'].format(guild)
            path2 = c.GUILD_PATH['kc_tracker.ini'].format(guild)

            LIST1 = json_manager.get_ini_list(path2, 'CONSTANT1', 'NAME')
            LIST2 = json_manager.get_ini_list(path2, 'CONSTANT2', 'PRE')

            DATA1 = json_manager.get_data(path1)
            COUNTER = 0

            for data in DATA1:
                CHECK = True
                USERNAME = data['user_rsn']
                USERNAME = USERNAME.replace(' ', '%20')

                while CHECK:
                    USER = hiscores_kc.Hiscores2V(USERNAME, LIST1, LIST2)
                    if USER.getKc(value['event_name']):
                        while CHECK:
                            CHECK = False
                            if data[value['event_name']]:
                                current = server_timer.get_current_time(guild_t)
                                USER_STATS = USER.getKc(value['event_name'])
                                target_keys = ['{}_current'.format(value['event_name'])]
                                target_values = [int(USER_STATS['kc'])]
                                json_manager.update(path1, 'user_rsn', data['user_rsn'], target_keys, target_values)

                                client_message = 'Guild id: {} | Guild time: {} | Event: {} | Mode: {} | Rsn: {} | Registration KC: {} | Current KC: {} | Status: {}'.format(guild, current.strftime('%H:%M'), value['event_name'], mode, data['user_rsn'], data[value['event_name']], USER_STATS['kc'], 'KC update')
                                console_interface.console_message('KC update', client_message)
                                logger.log_event(guild, 'kc_tracker', c.CLIENT_MESSAGES['kc_tracker_update'], client_message)
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
            path1 = c.GUILD_PATH['kc_tracker.json'].format(guild)
            path2 = c.GUILD_PATH['kc_rates.json'].format(guild)
            path3 = c.GUILD_PATH['kc_tracker.ini'].format(guild)

            DATA1 = json_manager.get_data(path1)
            DATA2 = json_manager.get_data(path2)

            LIST1 = json_manager.get_ini_list(path3, 'CONSTANT1', 'NAME')
            LIST2 = json_manager.get_ini_list(path3, 'CONSTANT2', 'PRE')

            current = server_timer.get_current_time(region=guild_t)
            COUNTER = 0
            USER = None
            for data in DATA1:
                CHECK = True
                USERNAME = data['user_rsn']
                USERNAME = USERNAME.replace(' ', '%20')

                while CHECK:
                    USER = hiscores_kc.Hiscores2V(USERNAME, LIST1, LIST2)
                    if USER.status != 404:
                        if USER.getKc(value['event_name']):
                            while CHECK:
                                CHECK = False
                                if data[value['event_name']]:
                                    USER_STATS = USER.getKc(value['event_name'])
                                    target_keys = ['{}_current'.format(value['event_name'])]
                                    target_values = [int(USER_STATS['kc'])]
                                    json_manager.update(path1, 'user_rsn', data['user_rsn'], target_keys, target_values)

                                    client_message = 'Guild id: {} | Guild time: {} | Event: {} | Mode: {} | Rsn: {} | Registration KC: {} | Current_KC: {} | Status: {}'.format(guild, current.strftime('%H:%M'), value['event_name'], mode, data['user_rsn'], data[value['event_name']], USER_STATS['kc'], 'KC update')
                                    console_interface.console_message('KC update', client_message)
                                    logger.log_event(guild, 'kc_tracker', c.CLIENT_MESSAGES['kc_tracker_update'], client_message)
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

    def tracker_update_kc(self, guild):
        try:
            while True:
                guild_t = origin.get_region(guild)
                path2 = c.GUILD_PATH['event.json'].format(guild)
                LIST1 = json_manager.get_data(path2)
                guild_current = server_timer.get_current_time(region=guild_t)

                if LIST1:
                    for value in LIST1:
                        if value['type'] == 3 and value['status'] == 1:
                            if guild_current.month == int(value['date_start'][:2]):
                                if guild_current.day == int(value['date_start'][3:]):
                                    if value['time_start'] + 1 >= guild_current.hour and value['time_start'] + 1 <= guild_current.hour + 5:
                                        self.event_start(guild, value, c.MODE_NAME['std'])

                        if value['type'] == 3 and value['status'] == 1:
                            if guild_current.month == int(value['date_end'][:2]):
                                if guild_current.day == int(value['date_end'][3:]):
                                    if guild_current.hour <= value['time_end'] - 1:
                                        self.event_in_progress(guild, value, c.MODE_NAME['std'])

                        if value['type'] == 4 and value['status'] == 1:
                            if guild_current.month >= int(value['date_start'][:2]):
                                if guild_current.day >= int(value['date_start'][3:]):
                                    self.event_in_progress(guild, value, c.MODE_NAME['rush'])

                time.sleep(60*10)
        except Exception as error:
            exception.error(error)

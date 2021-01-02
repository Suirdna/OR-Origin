from client.stream import server_timer, file_manager, exception
from client.config import config as c

def log_event(data1, module, event, event_log):
    try:
        time = server_timer.get_server_current_time()

        path = '{}{}{}{}{}/'.format(
            c.CLIENT_PATH['guild'], str(data1.guild.id) if hasattr(data1, 'guild') else str(data1), c.CLIENT_PATH['logs'],
            c.CLIENT_PATH['origin2'], module
        )
        event_message_log = '{} | {} | {} | {}'.format(c.CLIENT_NAME, time.strftime('%y/%m/%d %H:%M:%S'), event, event_log)
        file_manager.create_directory(path, server_timer.get_server_current_date())
        file_manager.write_to_file('{}/{}/{}.txt'.format(path, server_timer.get_server_current_date(), module), 'a', event_message_log)
    except Exception as error:
        exception.error(error)

def log_error(module, event, event_log):
    try:
        time = server_timer.get_server_current_time()

        path = '{}{}'.format(
            c.CLIENT_PATH['origin'], c.CLIENT_PATH['logs2']
        )
        file_manager.create_directory(path, server_timer.get_server_current_date())
        event_message_log = '{} | {} | {} | {}'.format(c.CLIENT_NAME, time.strftime('%y/%m/%d %H:%M:%S'), event, event_log)
        file_manager.write_to_file('{}/{}/{}.txt'.format(path, server_timer.get_server_current_date(), module), 'a', event_message_log)
    except Exception as error:
        exception.error(error)
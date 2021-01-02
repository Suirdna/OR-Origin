from client import exception, file_manager, server_timer
from client.config import config as c

async def log_event(data1, module, event, event_log):
    try:
        time = await server_timer.get_server_current_time()

        path = '{}{}{}{}{}/'.format(
            c.CLIENT_PATH['guild'], str(data1.guild.id) if hasattr(data1, 'guild') else str(data1), c.CLIENT_PATH['logs'],
            c.CLIENT_PATH['origin2'], module
        )
        event_message_log = '{} | {} | {} | {}'.format(c.CLIENT_NAME, time.strftime('%y/%m/%d %H:%M:%S'), event, event_log)
        await file_manager.create_directory(path, await server_timer.get_server_current_date())
        await file_manager.write_to_file('{}/{}/{}.txt'.format(path, await server_timer.get_server_current_date(), module), 'a', event_message_log)
    except Exception as error:
        await exception.error(error)

async def log_error(module, event, event_log):
    try:
        time = await server_timer.get_server_current_time()
        date = await server_timer.get_server_current_date()

        path = '{}'.format(
            c.CLIENT_PATH['logs3']
        )
        await file_manager.create_directory(path, date)
        event_message_log = '{} | {} | {} | {}'.format(c.CLIENT_NAME, time.strftime('%y/%m/%d %H:%M:%S'), event, event_log)
        await file_manager.write_to_file('{}/{}/{}.txt'.format(path, date, module), 'a', event_message_log)
    except Exception as error:
        await exception.error(error)
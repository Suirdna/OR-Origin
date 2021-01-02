from client import exception, server_timer
from client.config import config as c

async def console():
    try:
        print(c.CLIENT_SPLIT)
        for string in c.CLIENT_LOGO:
            print(string)
        print(c.CLIENT_SPLIT)
        await console_message(c.CLIENT_MESSAGES['client_online'])
        print(c.CLIENT_SPLIT)
    except Exception as error:
        await exception.error(error)

async def console_message(data1, data2=None):
    try:
        time = await server_timer.get_server_current_time()
        time = time.strftime('%y/%m/%d %H:%M:%S')

        if data2:
            print('{} | {} | {} | {}'.format(time, c.CLIENT_NAME, data1, data2))
        else:
            print('{} | {}: {}'.format(time, c.CLIENT_NAME, data1))
    except Exception as error:
        await exception.error(error)
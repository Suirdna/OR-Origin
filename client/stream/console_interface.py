from client.stream import server_timer
from client.config import config as c

def console_message(data1, data2=None):
    time = server_timer.get_server_current_time()
    time = time.strftime('%y/%m/%d %H:%M:%S')

    if data2:
        print('{} | {} | {} | {}'.format(time, c.CLIENT_NAME, data1, data2))
    else:
        print('{} | {}: {}'.format(time, c.CLIENT_NAME, data1))

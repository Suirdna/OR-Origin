from client import console_interface, logger
from client.config import config as c
import os, sys

async def error(data, source=None):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    if hasattr(exc_tb, 'tb_frame'):
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        string = '{} {} {} {} {}'.format(exc_type, file_name, exc_tb.tb_lineno, data, 'File= {}'.format(source) if source else '')
        await logger.log_error('error', c.CLIENT_MESSAGES['client_error'], string)
        await console_interface.console_message(string)
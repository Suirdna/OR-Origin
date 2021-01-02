from client.stream import exception, file_manager
import configparser

def get_status(value1, value2, path):
    try:
        ini = configparser.ConfigParser()
        ini.read(path)
        if int(ini[value1][value2]) == 2:
            return True
        else:
            return False
    except Exception as error:
        exception.error(error, path)

def update_data(value1, value2, value3, path):
    try:
        ini = configparser.ConfigParser()
        ini.read(path)
        if ini.has_option(value1, value2):
            ini.set(value1, value2, str(value3))
            ini.write(file_manager.open_file(path, 'w'))
            return True
        else:
            return False
    except Exception as error:
        exception.error(error, path)

def get_data(value1, value2, path):
    try:
        ini = configparser.ConfigParser()
        ini.read(path)
        return ini[value1][value2]
    except Exception as error:
        exception.error(error, path)

def get_ini(path):
    try:
        ini = configparser.ConfigParser()
        ini.read(path)
        return ini
    except Exception as error:
        exception.error(error, path)

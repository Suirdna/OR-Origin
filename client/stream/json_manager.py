from client.stream import exception, ini_manager, file_manager
import json

def get_status(source1, keys, values):
    try:
        STATUS = False
        STATUS_COUNT = 0
        source = json.load(file_manager.open_file(source1, 'r'))
        for line in source['data']:
            if isinstance(keys, list):
                for index, key in enumerate(keys):
                    if line[key] == values[index]:
                        STATUS_COUNT += 1

                if STATUS_COUNT == len(keys):
                    STATUS = True
            else:
                if line[keys] == values:
                    STATUS = True
        return STATUS
    except Exception as error:
        exception.error(error, source1)

def open_file(source1, permission):
    try:
        file = open(source1, permission, encoding='utf8')
        return file
    except Exception as error:
        exception.error(error, source1)

def get_data(source1):
    try:
        data = []
        source = json.load(open_file(source1, 'r'))
        for value in source['data']:
            data.append(value)

        return data
    except Exception as error:
        exception.error(error, source1)

def update(source1, key, id, target_keys, target_values):
    try:
        source = json.load(open_file(source1, 'r'))
        for line in source['data']:
            if line[key] == id:
                if isinstance(target_keys, list):
                    for index, target_key in enumerate(target_keys):
                        line[target_key] = target_values[index]
                else:
                    line[target_keys] = target_values
        json.dump(source, open_file(source1, 'w'), indent=2)
    except Exception as error:
        exception.error(error, source1)

def get_ini_list(source1, section, value):
    try:
        ini = ini_manager.get_ini(source1)
        source = json.loads(ini.get('{}'.format(section), '{}'.format(value)))
        return source
    except Exception as error:
        exception.error(error, source1)
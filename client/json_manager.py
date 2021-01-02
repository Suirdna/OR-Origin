from client import exception, file_manager, ini_manager
import json

async def get_massive_status(source1, massive, key, source_id, target_id):
    try:
        STATUS = False
        source = json.load(await file_manager.open_file(source1, 'r'))
        for data1 in source['data']:
            if data1[key] == source_id:
                for data2 in data1[massive]:
                    if data2[key] == target_id:
                        STATUS = True
        return STATUS
    except Exception as error:
        await exception.error(error, source1)

async def get_status(source1, keys, values):
    try:
        STATUS = False
        STATUS_COUNT = 0
        source = json.load(await file_manager.open_file(source1, 'r'))
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
        await exception.error(error, source1)

async def get_ini_list(source1, section, value):
    try:
        ini = await ini_manager.get_ini(source1)
        source = json.loads(ini.get('{}'.format(section), '{}'.format(value)))
        return source
    except Exception as error:
        await exception.error(error, source1)

async def get_massive(source1, target_key, target_id, massive):
    try:
        source = json.load(await file_manager.open_file(source1, 'r'))
        for data in source['data']:
            if data[target_key] == target_id:
                return data[massive]
    except Exception as error:
        await exception.error(error, source1)

async def get_json(source1):
    try:
        source = json.load(await file_manager.open_file(source1, 'r'))
        return source['data']
    except Exception as error:
        await exception.error(error, source1)

async def get_list(source1):
    try:
        source = json.load(await file_manager.open_file(source1, 'r'))
        data = source['data']

        return data
    except Exception as error:
        await exception.error(error, source1)

async def get_data(source1):
    try:
        data = []
        source = json.load(await file_manager.open_file(source1, 'r'))
        for value in source['data']:
            data.append(value)

        return data
    except Exception as error:
        await exception.error(error, source1)

async def delete(source1, source_key, target_id):
    try:
        source = json.load(await file_manager.open_file(source1, 'r'))
        for index, line in enumerate(source['data']):
            if line[source_key] == target_id:
                del source['data'][index]
        json.dump(source, await file_manager.open_file(source1, 'w'), indent=2)
    except Exception as error:
        await exception.error(error, source1)

async def clear_and_update(source1, data):
    try:
        json.dump(data, await file_manager.open_file(source1, 'w'), indent=2)
    except Exception as error:
        await exception.error(error, source1)

async def update_massive(source1, key, id, target_key, target_value):
    try:
        source = json.load(await file_manager.open_file(source1, 'r'))
        for line in source['data']:
            if line[key] == id:
                line[target_key].append(target_value)
        json.dump(source, await file_manager.open_file(source1, 'w'), indent=2)
    except Exception as error:
        await exception.error(error, source1)

async def update(source1, key, id, target_keys, target_values):
    try:
        source = json.load(await file_manager.open_file(source1, 'r'))
        for line in source['data']:
            if line[key] == id:
                if isinstance(target_keys, list):
                    for index, target_key in enumerate(target_keys):
                        line[target_key] = target_values[index]
                else:
                    line[target_keys] = target_values
        json.dump(source, await file_manager.open_file(source1, 'w'), indent=2)
    except Exception as error:
        await exception.error(error, source1)

async def update_server_config(source1, target_key, target_value):
    try:
        source = json.load(await file_manager.open_file(source1, 'r'))
        source['data'][target_key] = target_value
        json.dump(source, await file_manager.open_file(source1, 'w'), indent=2)
    except Exception as error:
        await exception.error(error, source1)

async def create(source1, data):
    try:
        source = json.load(await file_manager.open_file(source1, 'r'))
        source['data'].append(data)
        json.dump(source, await file_manager.open_file(source1, 'w'), indent=2)
    except Exception as error:
        await exception.error(error, source1)
from client.stream import exception
import os

def open_file(source1, permission):
    try:
        file = open(source1, permission, encoding='utf8')
        return file
    except Exception as error:
        exception.error(error, source1)

def create_directory(path, name):
    try:
        os.makedirs('{}{}'.format(path, name), exist_ok=True)
    except Exception as error:
        exception.error(error, path)

def write_to_file(source1, permission, data1):
    try:
        with open(source1, permission) as data:
            data.write('{}\n'.format(data1))
    except Exception as error:
        exception.error(error, source1)
from client import exception
from distutils.dir_util import copy_tree
import os

async def write_to_file(source1, permission, data1):
    try:
        with open(source1, permission) as data:
            data.write('{}\n'.format(data1))
    except Exception as error:
        await exception.error(error, source1)

async def open_file(source1, permission):
    try:
        file = open(source1, permission, encoding='utf8')
        return file
    except Exception as error:
        await exception.error(error, source1)

async def get_guild_directory(path):
    try:
        data = os.listdir(path)
        list_of_guild_folders = []
        for folder in data:
            isDirectory = os.path.isdir(path + folder)
            if isDirectory:
                if folder.isdigit():
                    list_of_guild_folders.append(int(folder))

        return list_of_guild_folders
    except Exception as error:
        await exception.error(error, path)

async def copy_directory(path1, path2):
    try:
        copy_tree(path1, path2)
    except Exception as error:
        await exception.error(error, path1)

async def create_directory(path, name):
    try:
        os.makedirs('{}{}'.format(path, name), exist_ok=True)
    except Exception as error:
        await exception.error(error)

async def delete_file(source1):
    try:
        os.remove(source1)
    except Exception as error:
        await exception.error(error, source1)
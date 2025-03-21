import os
import sys
from datetime import datetime


def format_version(version_list):
    if len(version_list) == 0:
        return ""
    return f"{version_list[0]}.{version_list[1]}.{version_list[2]}"


def get_version(version_catalog) -> list[int]:
    version = []
    version_file_name = f"{version_catalog}/version.txt"
    if not os.path.exists(version_file_name):
        open(version_file_name, "x").close()
    with open(version_file_name, "r") as f:
        lines = f.readlines()

        if len(lines) == 0:
            return [0, 0, 0]

        for i, line in enumerate(lines):
            if i > 2: break
            version.append(int(line.split(' ')[1]))

    return version


def get_message():
    try:
        msg = sys.argv[4]
    except IndexError as e:
        return "No message"

    return msg


def upgrade_version(version_type, version_catalog):
    old_version_list = get_version(version_catalog)

    if old_version_list == [0, 0, 0]:
        log_version_into_file([1, 0, 0], [], "Initial version", version_catalog)
        write_version_into_file([1, 0, 0], version_catalog)
        return

    new_version_list = old_version_list.copy()

    if version_type == "major":
        new_version_list[0] = new_version_list[0] + 1
        new_version_list[1] = 0
        new_version_list[2] = 0
    elif version_type == "minor":
        new_version_list[1] = new_version_list[1] + 1
        new_version_list[2] = 0
    elif version_type == "patch":
        new_version_list[2] = new_version_list[2] + 1
    else:
        raise ValueError("No such version type: " + version_type)

    write_version_into_file(new_version_list, version_catalog)
    message = get_message()
    log_version_into_file(new_version_list, old_version_list, message, version_catalog)
    print(f"Version updated: {format_version(old_version_list)} -> {format_version(new_version_list)}")


def write_version_into_file(version_list, version_catalog):
    with open(f"{version_catalog}/version.txt", "w") as f:
        f.write(f"major: {version_list[0]}\n")
        f.write(f"minor: {version_list[1]}\n")
        f.write(f"patch: {version_list[2]}\n")
        f.write(f"version: {format_version(version_list)}")


def log_version_into_file(new_version, old_version, message, version_catalog):
    with open(f"{version_catalog}/version_log.txt", "a") as f:
        f.write(
            f"[{format_version(new_version)} <- {format_version(old_version)}] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] | {message}\n")


def get_last_log_msg_from_file(version_catalog):
    version_file = f"{version_catalog}/version_log.txt"
    if not os.path.exists(version_file):
        open(f"{version_catalog}/version_log.txt", "x").close()
    with open(f"{version_catalog}/version_log.txt", "r") as f:
        line = f.readlines()[-1]
        if len(line) == 0:
            return '-'
        return line.split('|')[1].strip()
    

def is_file_exists(filename):
    return os.path.isfile(filename)


def get_args_map():
    args_len = len(sys.argv)
    if args_len < 2:
        raise ValueError('Please, provide at least two arguments: catalog and version type')

    args_map = {}
    args_map['catalog'] = sys.argv[1]
    args_map['command_type'] = sys.argv[2]
    
    if args_map['command_type'] == 'upgrade_version':
        args_map['version_type'] = sys.argv[3]

    return args_map


args_map = get_args_map()
command_type = args_map['command_type']
version_catalog = args_map['catalog']

if command_type == 'get_current_version':
    print(format_version(get_version(version_catalog)))
elif command_type == 'get_last_log_msg':
    print(get_last_log_msg_from_file(version_catalog))
elif command_type == 'upgrade_version':
    version_type = args_map['version_type']
    upgrade_version(version_type, version_catalog)
else:
    raise ValueError("Unknow command type: " + command_type)
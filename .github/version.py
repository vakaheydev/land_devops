import os
import sys
from datetime import datetime


def format_version(version_list):
    if len(version_list) == 0:
        return ""
    return f"{version_list[0]}.{version_list[1]}.{version_list[2]}"


def get_version(version_catalog) -> list[int]:
    version = []
    version_file_name = f"{version_catalog}/version"
    if not os.path.exists(version_file_name):
        open(version_file_name, "w").close()
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
        msg = sys.argv[2]
    except IndexError as e:
        return "No message"

    return msg


def upgrade_version(version_type, version_catalog):
    old_version_list = get_version()

    if old_version_list == [0, 0, 0]:
        print("Version file was created with initial version 1.0.0")
        log_version_into_file([1, 0, 0], [], "Initial version")
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
    log_version_into_file(new_version_list, old_version_list, message)
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
            f"[{format_version(new_version)} <- {format_version(old_version)}] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] - {message}\n")


def get_log_msg_from_file(version_catalog):
    with open(f"{version_catalog}/version_log.txt", "r") as f:
        line = f.readline()
        return line.split['-'][1:]
    

def is_file_exists(filename):
    return os.path.isfile(filename)


def get_args_map():
    try:
        version_catalog = sys.argv[1]
        version_type = sys.argv[2]
    except IndexError as e:
        return 'no'
    
    if len(sys.argv) > 2:
        command_type = sys.argv[3]

    return {'catalog': version_catalog, 'version_type': version_type, 'command_type': command_type}


args_map = get_args_map()
command_type = args_map['command_type']
version_catalog = args_map['catalog']
version_type = args_map['version_type']

if command_type == 'get_current_version':
    print(get_version[version_catalog])
elif command_type == 'get_last_log_msg':
    print(get_log_msg_from_file(version_catalog))
else:
    upgrade_version(version_type, version_catalog)
print('Version script executed successfully')

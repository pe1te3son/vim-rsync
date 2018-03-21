#!/bin/python3
""" Sync files with rsync """
import subprocess
import pipes
from utils import print_error_msg, print_msg, print_success_msg


def run_rsync_file(file_path, options):
    """ Syncs remote file """
    server_path = options["SERVER_HOST"] + ":" + file_path

    try:

        subprocess.Popen([
            "rsync", "-a", file_path, server_path
            ], shell=False, stdin=None, stdout=None, stderr=subprocess.STDOUT).pid

        # time.sleep(5)
        print_msg("[ Done ]: " + server_path)

    except Exception as err:
        print(err)
        print_error_msg('Failed to sync file')


def run_rsync_app(app_file_path, options):
    supported_apps = options["APPS"]
    app_to_sync, app_name = get_app_path_to_sync(supported_apps, app_file_path)

    if app_to_sync and app_name:
        if exists_remote(options["SERVER_HOST"], app_to_sync, True):
            server_path = options["SERVER_HOST"] + ":" + app_to_sync[:app_to_sync.find(app_name) - 1]
            print_success_msg(app_to_sync)

            excludes = build_exclude_command(app_to_sync, options["EXCLUDES"]) or ""
            subprocess.Popen([
                "rsync", "-a", excludes, app_to_sync, server_path, "--delete"
                ], shell=False, stdin=None, stdout=None, stderr=subprocess.STDOUT).pid

        else:
            print("app not on remote server")


def build_exclude_command(app_path, exclude_folders):
    if not len(exclude_folders): return None

    command = ""
    for folder in exclude_folders:
        command += "--exclude=" + folder
    return command


def get_app_path_to_sync(supported_apps, app_path):
    for supported_app in supported_apps:
        match_idx = app_path.find(supported_app)
        if match_idx > -1:
            return app_path[:match_idx + len(supported_app)], supported_app
    return None, None


def exists_remote(host, path, isDir=False):
    """Test if a file exists at path on a host accessible with SSH."""

    test_option = "-d" if isDir else "-f"
    status = subprocess.call([
        'ssh', host, ("test %s {}" % test_option).format(pipes.quote(path))
        ])
    if status == 0:
        return True
    if status == 1:
        return False
    raise Exception('SSH failed')

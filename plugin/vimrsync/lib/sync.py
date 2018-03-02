#!/bin/python3
""" Sync files with rsync """
import subprocess
import pipes


def run_rsync_file(file_path, options):
    """ Syncs remote file """
    server_path = options["SERVER_HOST"] + ":" + file_path

    try:
        subprocess.check_output([
            "rsync", "-a", file_path, server_path
            ], stderr=subprocess.STDOUT)
        print("[ Success ]: " + server_path)
    except Exception as err:
        print(err)

    # if exists_remote(options.SERVER_HOST, file_path):
    #     call(["rsync", "-a", file_path, server_path])
    # else:
    #     user_input = input("[ " + file_path + " ]
    # does not exits. Create? y/n or sync (p)roject:")
    #     if user_input.lower() == "y":
    #         call(["rsync", "-a", file_path, server_path])


def run_rsync_app(app_path, options):
    supported_apps = options["APPS"]
    app_to_sync = get_app_path_to_sync(supported_apps, app_path)

    if app_to_sync:
        if exists_remote(options["SERVER_HOST"], app_to_sync, True):
            print("got it")
        else:
            print("app not on remote server")


def get_app_path_to_sync(supported_apps, app_path):
    for supported_app in supported_apps:
        match_idx = app_path.find(supported_app)
        if match_idx > -1:
            return app_path[:match_idx + len(supported_app)]
    return None


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

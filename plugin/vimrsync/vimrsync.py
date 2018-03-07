#!/bin/python3
""" Main """

from lib import sync


def initiate_file_sync(path_to_file, options):
    """Parse arguments and Init sync"""
    # parsed_args = getopt.getopt(args, "p:", ["all"])
    # sync_app = is_sync_app(utils.get_args_list(parsed_args[0]))
    # path_arg = get_arg_value(parsed_args[0], "-p")
    if is_valid_app(path_to_file, options["APPS"]):
        sync.run_rsync_file(path_to_file, options)


def is_valid_app(path_to_file, valid_apps=[]):
    if not len(valid_apps):
        return False

    for i in valid_apps:
        if path_to_file.find(i) > -1:
            return True

    return False


def initiate_app_sync(current_working_file, options):
    sync.run_rsync_app(current_working_file, options)


def is_sync_app(args_list):
    return "--all" in args_list


def get_arg_value(options, option_to_get):
    for opt, val in options:
        if opt == option_to_get:
            return val
    return None

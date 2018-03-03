import vim


def get_args_list(args):
    args, values = zip(*args)
    return list(args)


def print_error_msg(msg):
    vim.command(":echohl ErrorMsg | echo '" + msg + "' | echohl None")


def print_msg(msg):
    vim.command(":echo '" + msg + "'")


def print_success_msg(msg):
    vim.command(":echohl DiffAdd | echo '" + msg + "' | echohl None")

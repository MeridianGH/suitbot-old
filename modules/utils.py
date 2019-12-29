import modules.errors


def arg_parse(ctx):
    args = ctx.message.content.split()[1:]
    if len(args) < 1:
        raise modules.errors.InvalidArguments
    for index, arg in enumerate(args):
        if len(arg) < 2:
            args[index - 1:index + 1] = [' '.join(args[index - 1:index + 1])]
    return args


def format_seconds(time_seconds):
    """Formats some number of seconds into a string of format d days, x hours, y minutes, z seconds"""
    seconds = time_seconds
    hours = 0
    minutes = 0
    days = 0
    while seconds >= 60:
        if seconds >= 60 * 60 * 24:
            seconds -= 60 * 60 * 24
            days += 1
        elif seconds >= 60 * 60:
            seconds -= 60 * 60
            hours += 1
        elif seconds >= 60:
            seconds -= 60
            minutes += 1

    return f"{days}d {hours}h {minutes}m {seconds}s"

def anded(*args):

    if len(args) == 1:
        return args[0]

    result = args[0]

    for arg in args[1:]:
        result = result & arg

    return result


def ored(*args):

    if len(args) == 1:
        return args[0]

    result = args[0]

    for arg in args[1:]:
        result = result | arg

    return result

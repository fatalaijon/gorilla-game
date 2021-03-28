def trace(fun):
    """
    Print each function call
    Parameters:
        :fun: a function to decorate
    Returns:
        the original function wrapped in a decorator
    """
    def new_fun(*args, **kwargs):
        called = f"{fun.__name__}{args}"
        result = fun(*args, **kwargs)
        print(called, "->", result)
        return result

    return new_fun

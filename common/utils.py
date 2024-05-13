def round_num(digits: int = 4):
    def dec(func):
        def wrapper(*args, **kwargs):
            if callable(func):
                val = func(*args, **kwargs)
            else:
                val = func
            return round(val, digits)

        return wrapper

    return dec

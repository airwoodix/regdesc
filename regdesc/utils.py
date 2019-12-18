import builtins


def bin(value, width, *, strip_0b=False):
    """
    Left-padded binary representation of `value` on given `width`.
    """
    k = "" if strip_0b else "0b"
    fmt = "{{:0>{}}}".format(width)
    return k + fmt.format(builtins.bin(value)[2:])

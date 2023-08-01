import operator



'''
Various helper tools
'''



def validate(value, comparison, against):
    ops = {
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le,
        "==": operator.eq,
        "!=": operator.ne,
    }
    if not ops[comparison](value, against):
        raise ValueError(f"Value {value} failed validation ({comparison}{against})")
    return(value)


def calculate_value(value, sf):
        result = value * 10**sf
        return result


def decode_string(decoder):
    s = decoder.decode_string(32)  # get 32 char string
    s = s.partition(b"\0")[0]  # omit NULL terminators
    s = s.decode("utf-8")  # decode UTF-8
    return str(s)
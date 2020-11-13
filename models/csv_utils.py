from datetime import date


def fix_up_field(s):
    if s.isnumeric():
        return int(s)
    elif " 00:00:00" in s:
        return date(int(s[0:4]), int(s[5:7]), int(s[8:10]))
    else:
        return s


def fix_up(row):
    return {k: fix_up_field(v) for k, v in row.items()}
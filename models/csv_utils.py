from datetime import date


def fix_up_field(s):
    if s.isnumeric():
        return int(s)
    elif " 00:00:00" in s:
        parts = s.split(' ')
        y, m, d = parts[0].split('-')
        return date(int(y), int(m), int(d))
    else:
        return s


def fix_up(row):
    return {k: fix_up_field(v) for k, v in row.items()}

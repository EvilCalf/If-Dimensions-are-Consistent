def skip_ws(txt, pos):
    while pos < len(txt) and txt[pos].isspace():
        pos += 1
    return pos


def parse_str(txt, pos, allow_ws=False, delimiter=[',', ':', '}', ']']):
    while pos < len(txt):
        if not allow_ws and txt[pos].isspace():
            break
        if txt[pos] in delimiter:
            break
        pos += 1
    return pos


def parse_obj(txt, pos):
    obj = dict()

    while True:
        pos = skip_ws(txt, pos + 1)
        end = parse_str(txt, pos, True, [':'])
        if end >= len(txt):
            raise ValueError("unexpected end when parsing object key")
        key = txt[pos:end].strip()
        pos = skip_ws(txt, end + 1)
        if pos >= len(txt):
            raise ValueError("unexpected end when parsing object value")
        if txt[pos] == '[':
            value, pos = parse_array(txt, pos)
        elif txt[pos] == '{':
            value, pos = parse_obj(txt, pos)
        else:
            end = parse_str(txt, pos, True, [',', '}'])
            if end >= len(txt):
                raise ValueError("unexpected end when parsing object value")
            value = txt[pos:end].strip()
            pos = end

        obj[key] = value
        pos = skip_ws(txt, pos)
        if pos >= len(txt):
            raise ValueError("unexpected end when object value finish")
        if txt[pos] == '}':
            return obj, pos + 1


def parse_array(txt, pos):
    array = list()

    while True:
        pos = skip_ws(txt, pos + 1)
        if pos >= len(txt):
            raise ValueError("unexpected end when parsing array item")
        if txt[pos] == '[':
            value, pos = parse_array(txt, pos)
        elif txt[pos] == '{':
            value, pos = parse_obj(txt, pos)
        else:
            end = parse_str(txt, pos, True, [',', ']'])
            if end >= len(txt):
                raise ValueError("unexpected end when parsing array item")
            value = txt[pos:end].strip()
            pos = end

        array.append(value)
        pos = skip_ws(txt, pos)
        if pos >= len(txt):
            raise ValueError("unexpected end when array item finish")
        if txt[pos] == ']':
            return array, pos + 1


def parse(txt):
    if txt.startswith('json'):
        pos = txt.find(':')
        if pos != -1:
            pos = skip_ws(txt, pos + 1)
            if txt[pos] == '{':
                obj, pos = parse_obj(txt, pos)
                return obj
            elif txt[pos] == '[':
                array, pos = parse_array(txt, pos)
                return array
    raise ValueError("format error when parsing root")
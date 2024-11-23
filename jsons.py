#  Copyright (c) 2024.
#  702361946@qq.com
#  github.com/702361946

import json


def w_json(a, name: str, encoding: str = 'utf-8'):
    try:
        with open(f'{name}.json', 'w+', encoding=encoding) as f:
            json.dump(a, f, indent=4, ensure_ascii=False)
            return True

    except Exception as e:
        print(e)
        return False


def r_json(name: str, encoding: str = 'utf-8'):
    try:
        with open(f'{name}.json', 'r+', encoding=encoding) as f:
            a = json.load(f)
            return a

    except Exception as e:
        print(e)
        return None

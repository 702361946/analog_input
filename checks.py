from _dict import *

def mouse_button_check(button) -> int | bool:
    if button is None:
        button = 0
    elif not type_check(button, 'int'):
        print('button is int!')
        return False
    elif button > 2 or button < 0:
        print('button is 0,1,2')
        return False

    return button


def int_and_none_check(a: list[int | None]) -> bool:
    """
    检查是否为int&None并返回状态
    """
    try:
        for i in a:
            if i is not None:
                int(i)

        return True

    except ValueError:
        print('should be an integer')
        return False

    except Exception as e:
        print(e)
        return False


def type_check(a, _type: str) -> bool:
    if type(a).__name__ == _type:
        return True
    else:
        return False


def keys_check(a) -> bool | list[int]:
    if not type_check(a, 'int') and not type_check(a, 'list'):
        print('keys is int or list')
        return False
    elif type_check(a, 'list'):
        for i in a:
            if not type_check(i, 'int'):
                print('keys is list[int]')
                return False
    elif type_check(a, 'int'):
        a = [a]

    return a


def key_int_dict_check(a) -> bool | list[str]:
    down = []
    for i in a:
        try:
            if key_button[i]:
                down.append(i)

        except KeyError:
            print(f'no key:{i}')
            return False

        except Exception as e:
            print(e)
            return False

    a = []
    for i in down:
        a.append(key_button[i])

    return a

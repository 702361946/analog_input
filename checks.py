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


def type_check(a, _type: str) -> bool:
    if type(a).__name__ == _type:
        return True
    else:
        return False

import random
import time

import pydirectinput

from checks import *

"""
修饰器staticmethod
用以创建类的静态方法
"""
# 启用安全检查，当鼠标移动到屏幕左上角时，会抛出异常，可以用于中断程序
pydirectinput.FAILSAFE = True

# 全局等待时间
global_time = 0.0

# 鼠标(mouse)操作
class Mouse(object):
    """
    通用内容
    xy鼠标位置(一般为绝对,一参执行)
    button鼠标按键(0~2)(默认0&左键)
    所有等待时间均不可小于零且必须为浮点数(所有等待时间默认global_time)
    before_time执行前等待
    after_time执行后等待
    loop为循环次数(一般情况下默认为1,不能小于1)
    loop_before_time循环执行前等待(在循环内)
    loop_after_time循环执行后等待(在循环内)
    """
    @staticmethod
    def move(
            x: int = None,
            y: int = None,
            relative_if: bool = False,
            before_time: float = global_time,
            after_time: float = global_time
    ) -> bool:
        """
        x,y为绝对/相对坐标,取决于relative_if的值(F/T)
        """
        if (
                (type_check(x, 'int') is False and x is not None) or
                (type_check(y, 'int') is False and y is not None) or
                (type_check(relative_if, 'bool') is False) or
                (type_check(before_time, 'float') is False or before_time < 0) or
                (type_check(after_time, 'float') is False or after_time < 0)
        ):
            print('未按照标准提供值')
            return False

        if x or y:
            time.sleep(before_time)

            if relative_if:
                pydirectinput.move(x, y)

            else:
                pydirectinput.moveTo(x, y)

            time.sleep(after_time)

            return True

        else:
            print('xy均为None')
            return False

    @staticmethod
    def down(
            x: int = None,
            y: int = None,
            loop: int = 1,
            button: int = 0,
            before_time: float = global_time,
            after_time: float = global_time,
            loop_before_time: float = global_time,
            loop_after_time: float = global_time,
    ) -> bool:
        """
        点击
        """
        if (
                (type_check(x, 'int') is False and x is not None) or
                (type_check(y, 'int') is False and y is not None) or
                (type_check(loop, 'int') is False or loop < 1) or
                (type_check(button, 'int') is False or button < 0 or button > 2) or
                (type_check(before_time, 'float') is False or before_time < 0) or
                (type_check(after_time, 'float') is False or after_time < 0) or
                (type_check(loop_before_time, 'float') is False or loop_before_time < 0) or
                (type_check(loop_after_time, 'float') is False or loop_after_time < 0)
        ):
            print('未按照标准提供值')
            return False

        if holds[f'mouse_{button}']:
            print('按键已被按住')
            return False

        time.sleep(before_time)

        for i in range(loop):
            print(f'\\{i}\\')
            time.sleep(loop_before_time)

            pydirectinput.click(x, y, button=mouse_button[button])

            time.sleep(loop_after_time)

        time.sleep(after_time)

        return True

    @staticmethod
    def hold_down(
            x: int = None,
            y: int = None,
            button: int = 0,
            before_time: float = global_time,
            after_time: float = global_time,
    ) -> bool:
        """
        按下并按住
        """
        if (
                (type_check(x, 'int') is False and x is not None) or
                (type_check(y, 'int') is False and y is not None) or
                (type_check(button, 'int') is False or button < 0 or button > 2) or
                (type_check(before_time, 'float') is False or before_time < 0) or
                (type_check(after_time, 'float') is False or after_time < 0)
        ):
            print('未按照标准提供值')
            return False

        if holds[f'mouse_{button}']:
            print('按键已被按住')
            return False

        time.sleep(before_time)

        pydirectinput.mouseDown(x, y, button=mouse_button[button])
        holds[f'mouse_{button}'] = True

        time.sleep(after_time)

        return True

    @staticmethod
    def hold_up(
            x: int = None,
            y: int = None,
            button: int = 0,
            before_time: float = global_time,
            after_time: float = global_time,
    ) -> bool:
        """
        放开按住
        """
        if (
                (type_check(x, 'int') is False and x is not None) or
                (type_check(y, 'int') is False and y is not None) or
                (type_check(button, 'int') is False or button < 0 or button > 2) or
                (type_check(before_time, 'float') is False or before_time < 0) or
                (type_check(after_time, 'float') is False or after_time < 0)
        ):
            print('未按照标准提供值')
            return False

        if holds[f'mouse_{button}'] is False:
            print('按键未被按住')
            return False

        time.sleep(before_time)

        pydirectinput.mouseUp(x, y, button=mouse_button[button])
        holds[f'mouse_{button}'] = False

        time.sleep(after_time)

        return True

    @staticmethod
    def drag(
            start_x: int = None,
            start_y: int = None,
            end_x: int = None,
            end_y: int = None,
            loop: int = 1,
            button: int = 0,
            before_time: float = global_time,
            after_time: float = global_time,
            loop_before_time: float = global_time,
            loop_after_time: float = global_time,
            smooth_if: bool = False,
            smooth_time: float = global_time,
            smooth_count: int = None
    ) -> bool:
        """
        拖拽
        start_开始位置
        end_结束位置(必须提供其一)
        smooth平滑(要求必须提供一组x或y)
        smooth_time每一步平滑后等待时间
        smooth_count平滑次数(None随机抽值)
        """
        if (
                (type_check(start_x, 'int') is False and start_x is not None) or
                (type_check(start_y, 'int') is False and start_y is not None) or
                (type_check(end_x, 'int') is False and end_x is not None) or
                (type_check(end_y, 'int') is False and end_y is not None) or
                (type_check(loop, 'int') is False or loop < 1) or
                (type_check(button, 'int') is False or button < 0 or button > 2) or
                (type_check(before_time, 'float') is False or before_time < 0) or
                (type_check(after_time, 'float') is False or after_time < 0) or
                (type_check(loop_before_time, 'float') is False or loop_before_time < 0) or
                (type_check(loop_after_time, 'float') is False or loop_after_time < 0) or
                (type_check(smooth_if, 'bool') is False) or
                (type_check(smooth_time, 'float') is False or smooth_time < 0) or
                (type_check(smooth_count, 'int') is False and smooth_count is not None)
        ):
            print('未按照标准提供值')
            return False
        if holds[f'mouse_{button}']:
            print('按键已被按住')
            return False
        if end_x is None and end_y is None:
            print('终点必须提供一参')
            return False

        time.sleep(before_time)

        for i in range(loop):
            print(f'\\{i}\\')
            time.sleep(loop_before_time)

            Mouse.hold_down(x=start_x, y=start_y, button=button)

            if smooth_if:
                if smooth_count:
                    _random = smooth_count
                else:
                    _random = random.randint(0, 24)
                if start_x and end_x:
                    _x = (start_x - end_x) * -1 // _random
                    smooth_x = start_x + _x
                else:
                    _x = 0
                    smooth_x = start_x
                if start_y and end_y:
                    _y = (start_y - end_y) * -1 // _random
                    smooth_y = start_y + _y
                else:
                    _y = 0
                    smooth_y = start_y

                for _smooth in range(_random):
                    print(f'\\\\{_smooth}\\\\')
                    Mouse.move(x=smooth_x, y=smooth_y)
                    if smooth_x is not None:
                        smooth_x += _x
                    if smooth_y is not None:
                        smooth_y += _y
                    time.sleep(smooth_time)

            Mouse.hold_up(x=end_x, y=end_y, button=button)

            time.sleep(loop_after_time)

        time.sleep(after_time)
        return True


# 键盘操作
class Key(object):
    """
    通用内容
    key按键(参考_dict里的)
    所有等待时间均不可小于零且必须为浮点数(所有等待时间默认为global_time)
    before_time执行前等待
    after_time执行后等待
    loop为循环次数(一般情况下默认为1,不能小于1)
    loop_before_time循环执行前等待(在循环内)
    loop_after_time循环执行后等待(在循环内)
    """

    @staticmethod
    def down(
            key: int,
            loop: int = 1,
            before_time: float = global_time,
            after_time: float = global_time,
            loop_before_time: float = global_time,
            loop_after_time: float = global_time,
    ) -> bool:
        if (
                (type_check(key, 'int') is False) or
                (type_check(loop, 'int') is False) or
                (type_check(before_time, 'float') is False) or
                (type_check(after_time, 'float') is False) or
                (type_check(loop_before_time, 'float') is False) or
                (type_check(loop_after_time, 'float') is False)
        ):
            print('未按照标准提供值')
            return False
        if not key in key_button.keys():
            print('无此key,检查是否输入错误')
            return False

        time.sleep(before_time)

        for i in range(loop):
            print(f'\\{i}\\')
            time.sleep(loop_before_time)

            pydirectinput.press(key_button[key])

            time.sleep(loop_after_time)

        time.sleep(after_time)

        return True

    @staticmethod
    def hold_down(
            key: int,
            before_time: float = global_time,
            after_time: float = global_time,
    ) -> bool:
        if (
                (type_check(key, 'int') is False) or
                (type_check(before_time, 'float') is False) or
                (type_check(after_time, 'float') is False)
        ):
            print('未按照标准提供值')
            return False
        if not key in key_button.keys():
            print('无此key,检查是否输入错误')
            return False
        if holds[f'key_{key_button[key]}'] is True:
            print('按键已被按住')
            return False

        time.sleep(before_time)

        pydirectinput.keyDown(key_button[key])
        holds[f'key_{key_button[key]}'] = True

        time.sleep(after_time)

        return True


def key_hold_up(keys: int | list[int]) -> bool:
    """
    只接受小写&功能键
    """
    keys = keys_check(keys)
    if keys is False:
        return False

    # 去重
    down = []
    for s in keys:
        if not s in down:
            down.append(s)
    keys = down

    keys = key_int_dict_check(keys)
    if keys is False:
        return False

    for s in keys:
        if holds[f'key_{s}']:
            pydirectinput.keyUp(s)
            holds[f'key_{s}'] = False
        else:
            print(f'key:{s} no hold')
            return False

    return True


# def key_all(w_str: str, loop: int = 1, t_time: float = 0.0, t_time_down: float = 0.0) -> bool:
#     """
#     loop次数默认为1
#     t_time_down执行前等待
#     """
#     if not type_check(w_str, 'str'):
#         print('str!')
#         return False
#
#     if not type_check(t_time, 'float'):
#         print('t_time is float')
#         return False
#     elif t_time < 0:
#         print('t_time >= 0')
#         return False
#
#     if not type_check(t_time_down, 'float'):
#         print('t_time_down is float')
#         return False
#     elif t_time_down < 0:
#         print('t_time_down >= 0')
#         return False
#
#     t = 0
#     time.sleep(t_time_down)
#     while t < loop:
#         for s in w_str:
#             try:
#                 if s in re_key.keys():
#                     key_down(re_key[s], t_time=t_time)
#
#                 elif s in key_shift.keys():
#                     key_hold_down(104)
#                     key_down(key_shift[s], t_time=t_time)
#                     key_hold_up(104)
#
#                 elif s in key_cn.keys():
#                     key_down(104)
#                     key_hold_down(104)
#                     key_down(key_cn[s], t_time=t_time)
#                     key_hold_up(104)
#                     key_down(104)
#
#                 elif s in key_cn_shift.keys():
#                     key_down(104)
#                     key_hold_down(104)
#                     key_down(key_cn_shift[s], t_time=t_time)
#                     key_hold_up(104)
#                     key_down(104)
#
#                 else:
#                     print(f'no key:{s}')
#                     return False
#
#             except Exception as e:
#                 print(e)
#                 return False
#
#         t += 1
#
#     return True


def key_re_int(w_str: str | list) -> bool | list[int]:
    """
    用来检查输入是否存在于支持字典中并返回bool or list[int]
    """
    re = []
    if type_check(w_str, 'str'):
        w_str = [w_str]
    elif not type_check(w_str, 'list'):
        print('str or list')
        return False

    for s in w_str:
        try:
            if s in re_key.keys():
                re.append(re_key[s])

            elif s in key_shift.keys():
                re.append(key_shift[s])

            elif s in key_cn.keys():
                re.append(key_cn[s])

            elif s in key_cn_shift.keys():
                re.append(key_cn[s])

            else:
                print(f'no key:{s}')
                return False

        except Exception as e:
            print(e)
            return False

    return re


if __name__ == '__main__':
    for _i in range(1):
        print(_i)
        print(time.time())
        # Mouse.move(x = 1000, before_time=1.0, after_time=1.0)
        # Mouse.down(loop = 2, loop_after_time=3.0)
        # Mouse.drag(start_x=200, end_x=500)
        # Key.down(3, before_time=1.0, loop=3)
        print(time.time())
    pass

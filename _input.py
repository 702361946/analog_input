import random
import time

import pydirectinput

from _dict import *
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
    def hold_re(
            x: int = None,
            y: int = None,
            button: int = 0,
            before_time: float = global_time,
            after_time: float = global_time,
    ) -> bool:
        """
        反转状态(不知是否要把down和up删掉)
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

        time.sleep(before_time)

        if holds[f'mouse_{button}']:
            pydirectinput.mouseUp(x, y, button=mouse_button[button])
            holds[f'mouse_{button}'] = False
        else:
            pydirectinput.mouseDown(x, y, button=mouse_button[button])
            holds[f'mouse_{button}'] = True

        time.sleep(after_time)

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

    @staticmethod
    def hold_up(
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
        if holds[f'key_{key_button[key]}'] is False:
            print('按键未被按住')
            return False

        time.sleep(before_time)

        pydirectinput.keyUp(key_button[key])
        holds[f'key_{key_button[key]}'] = False

        time.sleep(after_time)

        return True

    @staticmethod
    def hold_re(
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

        time.sleep(before_time)

        if holds[f'key_{key_button[key]}'] is False:
            pydirectinput.keyDown(key_button[key])
            holds[f'key_{key_button[key]}'] = True
        else:
            pydirectinput.keyUp(key_button[key])
            holds[f'key_{key_button[key]}'] = False

        time.sleep(after_time)

        return True

    class Down(object):
        """
        基于down函数的补充
        中文暂不支持(没想好怎么写)
        """

        @staticmethod
        def all(
                key: int | list,
                loop: int = 1,
                before_time: float = global_time,
                after_time: float = global_time,
                loop_before_time: float = global_time,
                loop_after_time: float = global_time,
                down_before_time: float = global_time,
                down_after_time: float = global_time,
                in_key_check: bool = True
        ) -> bool:
            """
            全部,但要求全数字
            down_*_time是在按键间的等待
            """
            if (
                    (type_check(key, 'int') is False and type_check(key, 'list') is False) or
                    (type_check(loop, 'int') is False) or
                    (type_check(before_time, 'float') is False) or
                    (type_check(after_time, 'float') is False) or
                    (type_check(loop_before_time, 'float') is False) or
                    (type_check(loop_after_time, 'float') is False) or
                    (type_check(down_before_time, 'float') is False) or
                    (type_check(down_after_time, 'float') is False) or
                    (type_check(in_key_check, 'bool') is False)
            ):
                print('未按照标准提供值')
                return False
            if type_check(key, 'int'):
                key = [key]
            if in_key_check:
                for k in key:
                    if not k in key_button.keys():
                        print('无此key,检查是否输入错误')
                        return False

            time.sleep(before_time)

            for i in range(loop):
                print(f'\\{i}\\')
                time.sleep(loop_before_time)

                for k in key:
                    Key.down(k, after_time=down_after_time, before_time=down_before_time)

                time.sleep(loop_after_time)

            time.sleep(after_time)

            return True

        @staticmethod
        def all_shift(
                key: int | list,
                loop: int = 1,
                before_time: float = global_time,
                after_time: float = global_time,
                loop_before_time: float = global_time,
                loop_after_time: float = global_time,
                down_before_time: float = global_time,
                down_after_time: float = global_time,
                in_key_check: bool = True
        ) -> bool:
            """
            仅仅只是加个shift罢了
            检查等均由all执行
            需要注意在此期间shift都是处于按下状态!
            """
            if holds['key_shift'] is False:
                Key.hold_down(re_key['shift'])

            _bool = Key.Down.all(key, loop, before_time, after_time, loop_before_time, loop_after_time,
                                 down_before_time, down_after_time, in_key_check)

            Key.hold_up(re_key['shift'])

            return _bool

    class Return(object):
        """
        用以返回某些东西的类
        """

        @staticmethod
        def int(_str: str | list[str]) -> bool | list[int]:
            """
            返回一个list[int],但建议检查是否返回了False
            还有不要提供数字(要提供切勿提供大于等于10的),list格式必须为一键一位
            """
            re = []
            if type_check(_str, 'list') is False:
                _str = [str(_str)]  # 避免出现来个int导致神奇的问题

            for k in _str:
                if k in re_key.keys():
                    re.append(re_key[k])
                elif k in key_shift.keys():
                    re.append(key_shift[k])
                elif k in key_cn.keys():
                    re.append(key_cn[k])
                elif k in key_cn_shift.keys():
                    re.append(key_cn_shift[k])
                else:
                    print(f'键\\{k}/无对照')
                    return False

            return re

        @staticmethod
        def int_strs(_str: str) -> bool | list[int]:
            """
            一句话转list
            但基于int
            所以注意是否返回了False
            """
            if type_check(_str, 'str') is False:
                print('输入必须为str')
                return False

            strs = []
            for _s in _str:
                strs.append(_s)

            return Key.Return.int(strs)


if __name__ == '__main__':
    for _i in range(1):
        print(_i)
        print(time.time())
        # 在两个time.time中加测试用例
        print(time.time())
    pass

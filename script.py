import os
import time

import screeninfo

from _input import Mouse, global_time, Key
from jsons import *

script: dict = {
    'step': int,
    'resolution': str,
    'developer': str,
    'email': str
}
global_step = {'step': 0}  # 方便通过函数修改
global_execute = {}
global_value = {}  # 全局变量
"""
name: v
"""


def get_scripts_file_name():  # 没错,抄ai的
    # 存储找到的文件名（不包含扩展名）
    files_without_extension = []
    # 遍历scripts目录
    for filename in os.listdir('scripts'):
        # 检查文件名是否以指定扩展名结尾
        if filename.endswith('.json'):
            # 去掉扩展名并添加到列表中
            files_without_extension.append(os.path.splitext(filename)[0])
    return files_without_extension


def parse_script(a: str, _split: str = ';', _x_h: float = 1, _x_w: float = 1) -> bool | dict:
    """
    解析单行脚本并返回dict化后的内容
    """
    re = {}
    """
    re = {
        'method': str,
        'command': lambda后的可执行函数,需要检查是否存在键对
    }
    """
    try:
        a = a.split(_split)
        if len(a) < 2:
            raise ValueError('检查内容,确保至少有一个参数')
        else:
            re['method'] = a[0]
            del a[0]  # 后面这玩意就全是参了

        # 转化列表,使之变为[a,a,b,b,c,c]而不是[a=a,b=b,c=c]
        t = []
        for i in a:
            f = i.split('=')
            for _i in f:
                t.append(_i)
        a = t

        # 变化为dict,{a: a}
        t = {}
        for i in range(len(a)):
            i = i // 2 * 2  # 确保索引到a=a前面那个a
            t[a[i]] = a[i + 1]
        a = t

        # 有人推荐用match case,算了不换了
        """
        match re['method']:
            case 'str':
                pass
            case _:
                pass
        """
        if re['method'] == 'str':
            """
            {
                "name": str,
                "message": str,
                "split": str(此参可选)
            }
            """
            if "name" not in a.keys() or "message" not in a.keys():
                raise ValueError('请检查是否传入了name和message参')
            else:
                name = a['name']
                message = a['message']
                if "split" in a.keys():
                    _split = a['split']
                else:
                    _split = None

            if _split is not None:
                message = message.split(_split)
            else:
                message = [message]

            t = []
            for i in message:
                if i[0] == '!':
                    t.append(global_value[i[1: len(i)]])
                else:
                    t.append(i)

            message = ''
            for i in t:
                message = f"{message}{i}"

            global_value[name] = message
            return True

        elif re['method'] == 'list':
            """
            {
                "name": str,
                "list": list,
                "split": str
            }
            """
            if "name" not in a.keys() or "list" not in a.keys():
                raise ValueError('请检查是否传入了name和list参')
            else:
                name = a['name']
                _list = a['list']
                if "split" in a.keys():
                    _split = a['split']
                else:
                    _split = ","
                _list = _list.split(_split)

            t = []
            for i in _list:
                if i[0] == '!':
                    t.append(global_value[i[1: len(i)]])
                else:
                    t.append(i)
            _list = t

            global_value[name] = _list
            return True

        elif re['method'] == 'dict':
            """
                {
                    "name": str,
                    "dict": list,
                    "split": str,
                    "dict_split": str
                }
            """
            if "name" not in a.keys() or "dict" not in a.keys():
                raise ValueError('请检查是否传入了name和dict参')
            else:
                name = a['name']
                _dict = a['dict']
                if "split" in a.keys():
                    _split = a['split']
                else:
                    _split = ","
                if "dict_split" in a.keys():
                    dict_split = a['dict_split']
                else:
                    dict_split = ':'
                _dict = _dict.split(_split)

            # 处理键对
            t = {}
            for i in _dict:
                t[i.split(dict_split)[0]] = i.split(dict_split, maxsplit=2)[1]
            _dict = t

            for i in _dict.keys():
                if _dict[i][0] == '!':
                    _dict[i] = global_value[_dict[i][1: len(_dict[i])]]

            global_value[name] = _dict
            return True

        elif re['method'] == 'int':
            """
                {
                    "name": str,
                    "int": str
                }
            """
            if "name" not in a.keys() or "int" not in a.keys():
                raise ValueError('请检查是否传入了name和int参')
            else:
                name = a['name']
                _int = int(a['int'])

            global_value[name] = _int
            return True

        elif re['method'] == 'float':
            """
                {
                    "name": str,
                    "float": str
                }
            """
            if "name" not in a.keys() or "float" not in a.keys():
                raise ValueError('请检查是否传入了name和float参')
            else:
                name = a['name']
                _float = float(a['float'])

            global_value[name] = _float
            return True

        elif re['method'] == 'None':
            """
            {
                'name': str
            }
            """
            if "name" not in a.keys():
                raise ValueError('请检查是否传入了name和float参')
            else:
                name = a['name']

            global_value[name] = None
            return True

        elif re['method'] == 'print':
            """
                {
                    "message": str,
                    "split": str(此参可选)
                }
            """
            if "message" not in a.keys():
                raise ValueError('请检查是否传入了message参')
            else:
                message = a['message']
                if "split" in a.keys():
                    _split = a['split']
                else:
                    _split = None

            if _split is not None:
                message = message.split(_split)
            else:
                message = [message]

            t = []
            for i in message:
                if i[0] == '!':
                    t.append(global_value[i[1: len(i)]])
                else:
                    t.append(i)

            message = ''
            for i in t:
                message = f"{message}{i}"

            re['command'] = lambda: print(message)

        elif re['method'] == 'input':
            """
            {
                "name": str,
                "message": str,
                "split": str(此参可选)
            }
            """

            def __temp(_name: str, _message: str):
                global_value[_name] = input(_message)

            if "name" not in a.keys() or "message" not in a.keys():
                raise ValueError('请检查是否传入了name和message参')
            else:
                name = a['name']
                message = a['message']
                if "split" in a.keys():
                    _split = a['split']
                else:
                    _split = None

            if _split is not None:
                message = message.split(_split)
            else:
                message = [message]

            t = []
            for i in message:
                if i[0] == '!':
                    t.append(global_value[i[1: len(i)]])
                else:
                    t.append(i)

            message = ''
            for i in t:
                message = f"{message}{i}"

            re['command'] = lambda: __temp(name, message)

        elif re['method'] == 'mouse':
            """
            {
                'mode': str,
                'x': str -> int | None,
                'y': str -> int | None,
                'relative_if': str -> bool,
                'before_time': str -> float,
                'after_time': str -> float,
                'loop': str -> int,
                'button': str -> int,
                'loop_before_time': str -> float,
                'loop_after_time': str -> float,
                'start_x': str -> int,
                'start_y': str -> int,
                'end_x': str -> int,
                'end_y': str -> int,
            }
            """
            if "mode" not in a.keys():
                raise ValueError('请检查是否传入了mode参')
            else:
                mode = a['mode']

            """
                move
                down
                hold(为反转)
                drag
            """
            match mode:
                case 'move':
                    """
                    {
                        'x': int | None,(必填)
                        'y': int | None,(必填)
                        'relative_if': bool,(可选,默认为False)
                        'before_time': float,(可选,默认为global_time)
                        'after_time': float,(可选,默认为global_time)
                    }
                    """
                    relative_if = False
                    before_time = global_time
                    after_time = global_time
                    x = None
                    y = None
                    if "x" not in a.keys() or 'y' not in a.keys():
                        raise ValueError('请检查是否传入了x和y参')
                    else:
                        if a['x'] != 'None':
                            x = int(int(a['x']) * _x_w)
                        if a['y'] != 'None':
                            y = int(int(a['y']) * _x_h)
                    if 'relative_if' in a.keys() and 'relative_if' == 'True':
                        relative_if = True
                    if 'before_time' in a.keys():
                        before_time = float(a['before_time'])
                    if 'after_time' in a.keys():
                        after_time = float(a['after_time'])

                    re['command'] = lambda: Mouse.move(
                        x=x,
                        y=y,
                        relative_if=relative_if,
                        before_time=before_time,
                        after_time=after_time
                    )

                case 'down':
                    """
                    {
                        'x': int,
                        'y': int,
                        'before_time': float,
                        'after_time': float,
                        'loop': int,
                        'button': int,
                        'loop_before_time': float,
                        'loop_after_time': float,
                    }
                    """
                    before_time = global_time
                    after_time = global_time
                    loop = 1
                    button = 0
                    loop_before_time = global_time
                    loop_after_time = global_time
                    x = None
                    y = None
                    if "x" not in a.keys() or 'y' not in a.keys():
                        raise ValueError('请检查是否传入了x和y参')
                    else:
                        if a['x'] != 'None':
                            x = int(int(a['x']) * _x_w)
                        if a['y'] != 'None':
                            y = int(int(a['y']) * _x_h)
                    if 'before_time' in a.keys():
                        before_time = float(a['before_time'])
                    if 'after_time' in a.keys():
                        after_time = float(a['after_time'])
                    if 'loop' in a.keys():
                        loop = int(a['loop'])
                    if 'button' in a.keys():
                        button = int(a['button'])
                        if button > 2 or button < 0:
                            raise ValueError('button仅支持0~2')
                    if 'loop_before_time' in a.keys():
                        loop_before_time = float(a['loop_before_time'])
                    if 'loop_after_time' in a.keys():
                        loop_after_time = float(a['loop_after_time'])

                    re['command'] = lambda: Mouse.down(
                        x=x,
                        y=y,
                        button=button,
                        before_time=before_time,
                        after_time=after_time,
                        loop=loop,
                        loop_before_time=loop_before_time,
                        loop_after_time=loop_after_time
                    )

                case 'hold':
                    """
                    {
                        'x': int,
                        'y': int,
                        'before_time': float,
                        'after_time': float,
                        'button': int,
                    }
                    """
                    before_time = global_time
                    after_time = global_time
                    button = 0
                    x = None
                    y = None
                    if 'x' in a.keys():
                        if a['x'] != 'None':
                            x = int(int(a['x']) * _x_w)
                    if 'y' in a.keys():
                        if a['y'] != 'None':
                            y = int(int(a['y']) * _x_h)
                    if 'before_time' in a.keys():
                        before_time = float(a['before_time'])
                    if 'after_time' in a.keys():
                        after_time = float(a['after_time'])
                    if 'button' in a.keys():
                        button = int(a['button'])
                        if button > 2 or button < 0:
                            raise ValueError('button仅支持0~2')

                    re['command'] = lambda: Mouse.hold_re(
                        x=x,
                        y=y,
                        button=button,
                        before_time=before_time,
                        after_time=after_time,
                    )

                case 'drag':
                    """
                    {
                        'before_time': float,
                        'after_time': float,
                        'loop': int,
                        'button': int,
                        'loop_before_time': float,
                        'loop_after_time': float,
                        'start_x': int | None,
                        'start_y': int | None,
                        'end_x': int | None,
                        'end_y': int | None,
                    }
                    """
                    before_time = global_time
                    after_time = global_time
                    loop = 1
                    button = 0
                    loop_before_time = global_time
                    loop_after_time = global_time
                    start_x = None
                    start_y = None
                    end_x = None
                    end_y = None
                    if "end_x" not in a.keys() or 'end_y' not in a.keys():
                        raise ValueError('请检查是否传入了end_x和end_y参')
                    else:
                        if a['x'] != 'None':
                            x = int(int(a['x']) * _x_w)
                        if a['y'] != 'None':
                            y = int(int(a['y']) * _x_h)
                    if 'start_x' in a.keys():
                        start_x = int(a['start_x'])
                    if 'start_y' in a.keys():
                        start_y = int(a['start_y'])
                    if 'before_time' in a.keys():
                        before_time = float(a['before_time'])
                    if 'after_time' in a.keys():
                        after_time = float(a['after_time'])
                    if 'loop' in a.keys():
                        loop = int(a['loop'])
                    if 'button' in a.keys():
                        button = int(a['button'])
                        if button > 2 or button < 0:
                            raise ValueError('button仅支持0~2')
                    if 'loop_before_time' in a.keys():
                        loop_before_time = float(a['loop_before_time'])
                    if 'loop_after_time' in a.keys():
                        loop_after_time = float(a['loop_after_time'])

                    re['command'] = lambda: Mouse.drag(
                        start_x=start_x,
                        start_y=start_y,
                        end_x=end_x,
                        end_y=end_y,
                        button=button,
                        before_time=before_time,
                        after_time=after_time,
                        loop=loop,
                        loop_before_time=loop_before_time,
                        loop_after_time=loop_after_time
                    )

                case _:
                    raise TypeError('未知模式')

        elif re['method'] == 'key':
            """
            {
            'mode': str,(必填)
            'key': int | list,(必填)
            'key_one': bool,(可选,默认False)
            'loop': int,(可选)
            'before_time': float,(可选)
            'after_time': float,(可选)
            'loop_before_time': float,(可选)
            'loop_after_time': float,(可选)
            'down_before_time': float,(可选)
            'down_after_time': float,(可选)
            }
            """
            key_one = False
            if "mode" not in a.keys() or "key" not in a.keys():
                raise ValueError('请检查是否传入了mode和key参')
            else:
                mode = a['mode']
                key = a['key']
            if 'key_one' in a.keys():
                key_one = bool(a['key_one'])
            if key_one:
                key = Key.Return.int(key)
            else:
                key = Key.Return.int_strs(key)

            match mode:
                case 'down':
                    """
                    {
                        'key': list,
                        'loop': int,
                        'before_time': float,
                        'after_time': float,
                        'loop_before_time': float,
                        'loop_after_time': float,
                        'down_before_time': float,
                        'down_after_time': float,
                    }
                    """
                    loop = 1
                    before_time = global_time
                    after_time = global_time
                    loop_before_time = global_time
                    loop_after_time = global_time
                    down_before_time = global_time
                    down_after_time = global_time
                    if 'loop' in a.keys():
                        loop = int(a['loop'])
                    if 'before_time' in a.keys():
                        before_time = float(a['before_time'])
                    if 'after_time' in a.keys():
                        after_time = float(a['after_time'])
                    if 'loop_before_time' in a.keys():
                        loop_before_time = float(a['loop_before_time'])
                    if 'loop_after_time' in a.keys():
                        loop_after_time = float(a['loop_after_time'])
                    if 'down_before_time' in a.keys():
                        down_before_time = float(a['down_before_time'])
                    if 'down_after_time' in a.keys():
                        down_after_time = float(a['down_after_time'])

                    re['command'] = lambda: Key.Down.all(
                        key=key,
                        loop=loop,
                        before_time=before_time,
                        after_time=after_time,
                        loop_before_time=loop_before_time,
                        loop_after_time=loop_after_time,
                        down_before_time=down_before_time,
                        down_after_time=down_after_time,
                    )

                case 'hold':
                    """
                    {
                        'key': int,
                        'before_time': float,
                        'after_time': float,
                    }
                    """
                    before_time = global_time
                    after_time = global_time
                    if len(key) > 1:
                        raise ValueError('hold模式下key只能有一个键,而不是一段话')
                    else:
                        key = key[0]  # 貌似有点抽象,但不想换int
                    if 'before_time' in a.keys():
                        before_time = float(a['before_time'])
                    if 'after_time' in a.keys():
                        after_time = float(a['after_time'])

                    re['command'] = lambda: Key.hold_re(
                        key=key,
                        before_time=before_time,
                        after_time=after_time
                    )

                case _:
                    raise TypeError('未知模式')

        elif re['method'] == 'time':
            """
            {
                'time': float
            }
            """
            if 'time' not in a.keys():
                raise ValueError('请提供参time')
            else:
                _time = float(a['time'])

                re['command'] = lambda: time.sleep(_time)

        elif re['method'] == 'goto':
            """
            {
                'step': int
            }
            """
            if 'step' not in a.keys():
                raise ValueError('请提供参step')
            else:
                step = int(a['step'])

                def __temp(_step):
                    global_step['step'] = _step

                re['command'] = lambda: __temp(step)

        # elif re['method'] == 'if':
        #     pass

        else:
            raise TypeError('未知方法')

        return re

    except Exception as e:
        print(e)
        return False


def run(execute: dict, get_execute: bool = False) -> bool:
    """
    get_execute用于直接执行脚本
    """
    if get_execute is False:
        if 'info' in execute.keys():
            print(f'脚本信息\n"""\n{execute["info"]}\n"""')

        # 变形xy以适配设备
        if True:
            print('正在处理分辨率信息')
            [execute_w, execute_h] = execute['resolution'].split('x')
            # 获取所有显示器的信息
            monitors = screeninfo.get_monitors()
            # 通常第一个显示器是主显示器
            main_monitor = monitors[0]
            # 获取主显示器的宽度和高度
            user_w = main_monitor.width
            user_h = main_monitor.height

            _x_w = user_w / int(execute_w)
            _x_h = user_h / int(execute_h)

        split = None
        if 'split' in execute.keys():
            split = execute['split']

        for i in range(execute['step']):
            print(f'初始化脚本\\step:{i}')
            if f'{i}' in execute.keys():
                execute[f'{i}'] = parse_script(execute[f'{i}'], split, _x_h, _x_w)
            else:
                print(f'脚本步数缺失\\{i}')
                execute[f'{i}'] = False

            if execute[f'{i}'] is False:
                print('请联系脚本制造者')
                if 'developer' in execute.keys():
                    print(f'developer:{execute["developer"]}')
                if 'email' in execute.keys():
                    print(f'email:{execute["email"]}')

                return False

        # 覆盖global_execute
        for k in global_execute.keys():
            del global_execute[k]
        for k in execute.keys():
            global_execute[k] = execute[k]

        print('初始化完成')

    input('按下回车开始执行')
    global_step['step'] = 0
    while global_step['step'] < execute['step']:
        i = execute[f'{global_step["step"]}']
        if type(i).__name__ == 'dict':
            if 'command' in i.keys():
                i['command']()
        global_step['step'] += 1

    return True

if __name__ == '__main__':
    user_script = {
        'execute_json': False,
        'script_name': None
    }
    # global_value['fff'] = 'eeeee'
    while True:
        script_names = get_scripts_file_name()
        for name_i in range(len(script_names)):
            print(f'{name_i} : {script_names[name_i]}')

        user_input = input('输入脚本编号(输入exit退出程序)')
        # user_input = '0'
        if user_input == 'exit':
            break
        elif user_input.isdigit():
            if int(user_input) < len(script_names):
                script_name = script_names[int(user_input)]
                if user_script['execute_json'] and user_script['script_name'] == script_name:
                    # 用来减少重复使用同一脚本时
                    run(global_execute, get_execute=True)
                else:
                    script = r_json(f'scripts\\{script_name}')
                    if script is not None:
                        user_script['script_name'] = script_name
                        user_script['execute_json'] = run(script)
            else:
                print('输入的数字不在范围内')

        else:
            print('未知操作,请检查输入')

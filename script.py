import os

import screeninfo

from _input import *
from jsons import *

script: dict = {
    'step': int,
    'resolution': str,
    'developer': str,
    'email': str
}


def get_scripts_file_name():
    # 存储找到的文件名（不包含扩展名）
    files_without_extension = []
    # 遍历scripts目录
    for filename in os.listdir('scripts'):
        # 检查文件名是否以指定扩展名结尾
        if filename.endswith('.json'):
            # 去掉扩展名并添加到列表中
            files_without_extension.append(os.path.splitext(filename)[0])
    return files_without_extension


def parse_script(a: str) -> bool | dict:
    """
    解析单行脚本并返回dict化后的内容
    0 mouse
    1 key
    2 time
    """
    re = {}
    """
    re = {
        '_method': int,
        'button': int,
        'method': int,
        'x': int | None,
        'y': int | None,
        'time': float,
        'before_time': float,
        'after_time': float,
        'loop': int
    }
    """
    _i = 1
    try:
        # 鼠标
        if a[0] == '0':
            re['_method'] = 0

            if int(a[_i]) > 2 or int(a[_i]) < 0:
                print('鼠标按钮未知')
                return False
            re['button'] = int(a[_i])
            _i += 1

            if int(a[_i]) > 2 or int(a[_i]) < 0:
                print('鼠标方法未知')
                return False
            re['method'] = int(a[_i])
            _i += 1

            if int(a[_i]) == 0:
                re['x'] = None
                _i += 1
            else:
                # _i + 1即为x开头,_i为长度
                re['x'] = int(a[_i + 1: _i + int(a[_i]) + 1])
                _i += int(a[_i]) + 1

            if int(a[_i]) == 0:
                re['y'] = None
                _i += 1
            else:
                # 同x
                re['y'] = int(a[_i + 1: _i + int(a[_i]) + 1])
                _i += int(a[_i]) + 1

            if int(a[_i]) == 0:
                re['loop'] = 1
                _i += 1
            else:
                re['loop'] = int(a[_i + 1: _i + int(a[_i]) + 1])
                _i += int(a[_i]) + 1

            if int(a[_i]) == 0:
                re['before_time'] = 0.0
                _i += 1
            else:
                # 用round来进行小数位的舍取,以实现更为精确的数值
                re['before_time'] = round(int(a[_i + 2: _i + int(a[_i]) + 2]) * (10 ** -int(a[_i + 1])), int(a[_i + 1]))
                _i += int(a[_i]) + 2

            if int(a[_i]) == 0:
                re['after_time'] = 0.0
                _i += 1
            else:
                # 同before_time
                re['after_time'] = round(int(a[_i + 2: _i + int(a[_i]) + 2]) * (10 ** -int(a[_i + 1])), int(a[_i + 1]))
                _i += int(a[_i]) + 2

            # 结束处理

        # 键盘
        elif a[0] == '1':
            re['_method'] = 1

            if int(a[_i]) != 0 and int(a[_i]) != 1:
                print('按键方法未知')
                return False
            re['method'] = int(a[_i])
            _i += 1

            if int(a[_i]) == 0:
                print('按键长度不为0')
                return False
            if int(a[_i + 1]) == 0:
                re['button'] = Key.Return.int(a[_i + 2: _i + int(a[_i]) + 2])
            elif int(a[_i + 1]) == 1:
                re['button'] = Key.Return.int_strs(a[_i + 2: _i + int(a[_i]) + 2])
            else:
                print('按键标识未知')
                return False
            if re['button'] is False:
                print(f'请检查内容\\{a[_i + 2: _i + int(a[_i]) + 2]}')
                return False
            _i += int(a[_i]) + 2

            if int(a[_i]) == 0:
                re['loop'] = 1
                _i += 1
            else:
                re['loop'] = int(a[_i + 1: _i + int(a[_i]) + 1])
                _i += int(a[_i]) + 1

            if int(a[_i]) == 0:
                re['before_time'] = 0.0
                _i += 1
            else:
                # 用round来进行小数位的舍取,以实现更为精确的数值
                re['before_time'] = round(int(a[_i + 2: _i + int(a[_i]) + 2]) * (10 ** -int(a[_i + 1])), int(a[_i + 1]))
                _i += int(a[_i]) + 2

            if int(a[_i]) == 0:
                re['after_time'] = 0.0
                _i += 1
            else:
                # 同before_time
                re['after_time'] = round(int(a[_i + 2: _i + int(a[_i]) + 2]) * (10 ** -int(a[_i + 1])), int(a[_i + 1]))
                _i += int(a[_i]) + 2

        # 等待时间
        elif a[0] == '2':
            re['_method'] = 2

            if int(a[_i]) == 0:
                re['time'] = 0.0
                _i += 1
            else:
                re['time'] = round(float(a[_i + 2: _i + int(a[_i]) + 2]) * 10 ** -int(a[_i + 1]), int(a[_i + 1]))
                _i += int(a[_i]) + 2

        else:
            print('未知类型')
            return False

    except ValueError:
        print(f'值错误\\i{_i}')
        return False

    return re


def run(execute: dict, get_execute: bool = False) -> bool:
    """
    get_execute用于直接执行脚本
    """
    if get_execute is False:
        if 'info' in execute.keys():
            print(f'脚本信息\n"""\n{execute["info"]}\n"""')

        for i in range(execute['step']):
            print(f'初始化脚本\\{execute['step']}\\{i}')
            if f'{i}' in execute.keys():
                execute[f'{i}'] = parse_script(execute[f'{i}'])
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

        # 变形xy以适配设备
        if True:
            print('正在适配分辨率')
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

            for _i in range(execute['step']):
                if execute[str(_i)]['_method'] == 0:
                    if execute[str(_i)]['x'] is not None:
                        execute[str(_i)]['x'] = execute[str(_i)]['x'] * _x_w
                    if execute[str(_i)]['y'] is not None:
                        execute[str(_i)]['y'] = execute[str(_i)]['y'] * _x_h

        print('初始化完成')
        w_json(execute, 'execute')

    input('按下回车开始执行')

    for _i in range(execute['step']):
        i = execute[f'{_i}']
        if i['_method'] == 0:
            if i['method'] == 0:
                Mouse.move(
                    x=i['x'],
                    y=i['y'],
                    before_time=i['before_time'],
                    after_time=i['after_time']
                )
            elif i['method'] == 1:
                Mouse.down(
                    x=i['x'],
                    y=i['y'],
                    before_time=i['before_time'],
                    after_time=i['after_time'],
                    button=i['button'],
                    loop=i['loop']
                )
            elif i['method'] == 2:
                Mouse.hold_re(
                    x=i['x'],
                    y=i['y'],
                    before_time=i['before_time'],
                    after_time=i['after_time'],
                    button=i['button'],
                )

        if i['_method'] == 1:
            if i['method'] == 0:
                Key.Down.all(
                    key=i['button'],
                    loop=i['loop'],
                    before_time=i['before_time'],
                    after_time=i['after_time']
                )
            elif i['method'] == 1:
                time.sleep(i['before_time'])
                for k in i['button']:
                    Key.hold_re(key=k)
                time.sleep(i['after_time'])

        if i['_method'] == 2:
            time.sleep(i['time'])

    return True

if __name__ == '__main__':
    user_script = {
        'execute_json': False,
        'script_name': None
    }
    while True:
        script_names = get_scripts_file_name()
        for name_i in range(len(script_names)):
            print(f'{name_i} : {script_names[name_i]}')

        user_input = input('输入脚本编号(输入exit退出程序)')
        if user_input == 'exit':
            break
        elif user_input.isdigit():
            if int(user_input) < len(script_names):
                script_name = script_names[int(user_input)]
                if user_script['execute_json'] and user_script['script_name'] == script_name:
                    # 用来减少重复使用同一脚本时
                    run(r_json('execute'), get_execute=True)
                else:
                    script = r_json(f'scripts\\{script_name}')
                    if script is not None:
                        user_script['script_name'] = script_name
                        user_script['execute_json'] = run(script)
            else:
                print('输入的数字不在范围内')

        else:
            print('未知操作,请检查输入')

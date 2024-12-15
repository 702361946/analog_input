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
global_v = {} # 全局变量
"""
name: v
"""


def get_scripts_file_name(): # 没错,抄ai的
    # 存储找到的文件名（不包含扩展名）
    files_without_extension = []
    # 遍历scripts目录
    for filename in os.listdir('scripts'):
        # 检查文件名是否以指定扩展名结尾
        if filename.endswith('.json'):
            # 去掉扩展名并添加到列表中
            files_without_extension.append(os.path.splitext(filename)[0])
    return files_without_extension


def parse_script(a: str, _split: str = ';') -> bool | dict:
    """
    解析单行脚本并返回dict化后的内容
    """
    re = {}
    """
    re = {
        'method': str,
        'command': lambda后的可执行函数
    }
    """
    try:
        a = list(a.split(_split)) # 保证是list
        if len(a) < 2:
            raise ValueError('检查内容,确保至少有一个参数')
        else:
            re['method'] = a[0]
            del a[0] # 后面这玩意就全是参了

        # 转化列表,使之变为[a,a,b,b,c,c]而不是[a=a,b=b,c=c]
        t = []
        for i in a:
            f = i.split('=')
            for _i in f:
                t.append(_i)
        a = t

        if re['method'] == 'str':
            """
            {
                "name": str,
                "message": str
            }
            """
            name = None
            message = None
            for i in range(len(a)):
                if a[i] == 'name':
                    name = a[i + 1]
                if a[i] == 'message':
                    message = a[i + 1]
            if name is None or message is None:
                raise ValueError('请检查是否传入了name和message参')
            else:
                global_v[name] = message
                return True

        elif re['method'] == 'list':
            pass

        elif re['method'] == 'dict':
            pass

        elif re['method'] == 'print':
            pass

        elif re['method'] == 'input':
            pass

        elif re['method'] == 'mouse':
            pass

        elif re['method'] == 'key':
            pass

        elif re['method'] == 'time':
            pass

        else:
            raise TypeError('未知方法')

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

        for i in range(execute['step']):
            print(f'初始化脚本\\step:{i}')
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
                if execute[str(_i)]['method'] == 'mouse':
                    if execute[str(_i)]['x'] is not None:
                        execute[str(_i)]['x'] = execute[str(_i)]['x'] * _x_w
                    if execute[str(_i)]['y'] is not None:
                        execute[str(_i)]['y'] = execute[str(_i)]['y'] * _x_h

        print('初始化完成')
        w_json(execute, 'execute')

    input('按下回车开始执行')

    for _i in range(execute['step']):
        i = execute[f'{_i}']
        if i['method'] == 'print':
            pass
        elif i['method'] == 'input':
            pass
        elif i['method'] == 'mouse':
            pass
        elif i['method'] == 'key':
            pass
        elif i['method'] == 'time':
            pass
        else:
            print('可能为无输出方法')
            pass

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
        # user_input = '0'
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

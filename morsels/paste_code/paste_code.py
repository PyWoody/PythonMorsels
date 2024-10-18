import code
import re
import textwrap


def paste_code():
    print('Paste your code block')
    exec_code = ''
    try:
        while line := input():
            for sub_line in line.splitlines():
                exec_code += sub_line + '\n'
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        exec_code = textwrap.dedent(exec_code)
        exec_code = ''.join(i.rstrip() + '\n' for i in exec_code.splitlines())
        exec(exec_code, globals())
        code.InteractiveConsole(locals=globals()).interact(banner='')

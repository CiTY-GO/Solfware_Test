def echo_green(msg: str):
    return f'printf "\033[32m{msg}\033[0m\n";'

def echo_red(msg: str):
    return f'printf "\033[31m{msg}\033[0m\n";'
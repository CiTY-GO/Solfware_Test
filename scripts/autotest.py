import os
from utils import echo_green,echo_red

# 解析输入参数
def parse_params(input_file_path: str):
    with open(input_file_path, 'r') as f:
        lines = f.readlines()
    
    params = []
    for line in lines:
        # check validation
        assert line[:4] == '-P [' and line[-2:] == ']\n'
        # TODO: 还要做转义字符的处理，这里只是把位于-P []之中的内容提取出来
        params.append(line[4:-2])
    
    return params
# 植入错误宏
def insert_fault(fault_seed_file:str,num):
    line_number = num
    with open(fault_seed_file, 'r') as f:
        lines = f.readlines()
    lines[line_number]=lines[line_number][2:-2]
    with open(fault_seed_file, 'w') as f:
        f.write(lines)
        
def recover_fault(fault_seed_file:str,num):
    line_number = num
    with open(fault_seed_file, 'r') as f:
        lines = f.readlines()
    lines[line_number]='/*'+lines[line_number]+'*/'
    with open(fault_seed_file, 'w') as f:
        f.write(lines)

def run_by_version(code_version):
    # 项目根路径
    BASE_PATH = '/home/ubuntu/RGtest/grep'
    # 源代码目录路径
    SRC_PATH = os.path.join(BASE_PATH, 'versions.alt/versions.seeded/v1/')
    # 输入数据（命令行参数）文件路径
    FAULT_PATH = os.path.join(BASE_PATH, 'versions.alt/versions.seeded/v1/FaultSeeds.h')
    # 植入宏（命令行参数）文件路径
    INPUT_FILE_PATH = os.path.join(BASE_PATH, 'testplans.alt/v1/v0.cov.universe')
    # 输出目录路径
    OUTPUT_PATH = os.path.join(BASE_PATH, f'outputs.alt/v1/')
    # 日志文件路径
    LOG_FILE_PATH = os.path.join(OUTPUT_PATH, f'log{code_version}.txt')
    
    params = parse_params(INPUT_FILE_PATH)
    # 1. 植入错误宏 TODO
    # 2. 编译，运行，测试 => gcov文件，最后清理
    os.system(f'''
        cd {OUTPUT_PATH};
        rm -rf version{code_version};
        rm -f log{code_version}.txt;
        mkdir version{code_version};
        {echo_green('START code version {code_version}')}
    ''')
    OUTPUT_PATH = os.path.join(BASE_PATH, f'outputs.alt/v1/version{code_version}')
    for i in range(len(params)):
        # if i <= 150 or i > 156:
        #     continue
        # print(params[i])
        # os.system(f'echo {params[i]}')
        os.system(f'''
        cd {SRC_PATH};          
        make build;
        {echo_green('COMPILE finished. generated [grep.exe] [grep.gcno]')}
        
        echo "INPUT {i}: {params[i]}" >> {LOG_FILE_PATH};
        
        cd {os.path.join(BASE_PATH, 'scripts')};
        echo "RUN {i}" >> {LOG_FILE_PATH};
        {os.path.join(SRC_PATH, 'grep.exe')} {params[i]} < ./stdin.txt >> {LOG_FILE_PATH};
        {echo_green('RUN finished. generated [grep.gcda]')}
        
        
        cd {SRC_PATH};
        echo "TEST {i}" >> {LOG_FILE_PATH};
        gcov grep.c >> {LOG_FILE_PATH};
        {echo_green('TEST finished. generated [grep.c.gcov] [wchar.h.gcov]')}
        
        echo >> {LOG_FILE_PATH};
        
        mv ./grep.c.gcov {os.path.join(OUTPUT_PATH, f'grep.c.{code_version}_{i}.gcov')};
        {echo_green('MOVE [grep.c.gcov] to output directory')}
        rm ./grep.exe ./grep.gcno ./grep.gcda ./wchar.h.gcov;
        {echo_green('CLEAR finished')}
        {echo_green(f'[CASE {i} DONE]')}
    ''')


if __name__ == '__main__':
    run_by_version(0)
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
def insert_fault(fault_seed_file:str,code_version):
    if  code_version == 19:
        return
    line_number = code_version
    with open(fault_seed_file, 'r') as f:
        lines = f.readlines()
    lines[line_number]=lines[line_number][2:-3]+'\n'
    with open(fault_seed_file, 'w') as f:
        for line in lines:
            f.write(line)
# 恢复错误宏        
def recover_fault(fault_seed_file:str,code_version):
    if  code_version == 19:
        return
    line_number = code_version
    with open(fault_seed_file, 'r') as f:
        lines = f.readlines()
    lines[line_number]='/*'+lines[line_number][:-1]+'*/\n'
    with open(fault_seed_file, 'w') as f:
        for line in lines:
            f.write(line)

def run_by_version():
    
        # 项目根路径
        BASE_PATH = '/home/ubuntu/RGtest/grep'
        # 源代码目录路径
        SRC_PATH = os.path.join(BASE_PATH, 'versions.alt/versions.seeded/v1/')
        # 植入宏（命令行参数）文件路径
        FAULT_PATH = os.path.join(BASE_PATH, 'versions.alt/versions.seeded/v1/FaultSeeds.h')
        # 输入数据（命令行参数）文件路径
        INPUT_FILE_PATH = os.path.join(BASE_PATH, 'testplans.alt/v1/v0.cov.universe')
        

        for code_version in range(20):
            #version19 为 未植入错误宏的版本
            if code_version >= 1:
                continue
            # 输出目录路径
            OUTPUT_PATH = os.path.join(BASE_PATH, f'outputs.alt/v1/')
            # 日志文件路径
            LOG_FILE_PATH = os.path.join(OUTPUT_PATH, f'log{code_version}.txt')
            
            params = parse_params(INPUT_FILE_PATH)
            
            # 1. 植入错误宏 
            insert_fault(FAULT_PATH,code_version)
            os.system(f'''{echo_red(f'INSERT FAULT {code_version}')}''')
            # 2. 编译，运行，测试 => gcov文件，最后清理
            os.system(f'''
                cd {OUTPUT_PATH};
                rm -rf version{code_version};
                rm -f log{code_version}.txt;
                mkdir version{code_version};
                {echo_green(f'START code version {code_version}')}
            ''')

            OUTPUT_PATH = os.path.join(BASE_PATH, f'outputs.alt/v1/version{code_version}')
            for i in range(len(params)):
                if i<150 or i>156 :
                    continue
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
            recover_fault(FAULT_PATH,code_version)


if __name__ == '__main__':
    run_by_version()

    # 测试植入错误宏
    # 项目根路径
    # BASE_PATH = '/home/ubuntu/RGtest/grep'
    # FAULT_PATH = os.path.join(BASE_PATH, 'versions.alt/versions.seeded/v1/FaultSeeds.h')
    # 1. 植入错误宏 
    # insert_fault(FAULT_PATH,0)
    # 2. 恢复错误
    # recover_fault(FAULT_PATH,1)

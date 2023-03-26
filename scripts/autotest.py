import os
from utils import echo_green,echo_red
from parse_params import parse_params
from fault_implant import insert_fault,recover_fault


def run_by_version():
    
        # 项目根路径
        BASE_PATH = '/home/ubuntu/RGtest/grep'
        # 源代码目录路径
        SRC_PATH = os.path.join(BASE_PATH, 'versions.alt/versions.seeded/v1/')
        ORG_PATH = os.path.join(BASE_PATH, 'versions.alt/versions.orig/v1/')
        # 植入宏（命令行参数）文件路径
        FAULT_PATH = os.path.join(BASE_PATH, 'versions.alt/versions.seeded/v1/FaultSeeds.h')
        # 输入数据（命令行参数）文件路径
        INPUT_FILE_PATH = os.path.join(BASE_PATH, 'testplans.alt/v1/v0.cov.universe')
        

        for code_version in range(19):
            #version19 为 未植入错误宏的版本
            if code_version != 0:
                continue
            # 输出目录路径
            OUTPUT_PATH = os.path.join(BASE_PATH, f'outputs.alt/v1/')
            # 日志文件路径
            LOG_FILE_PATH = os.path.join(OUTPUT_PATH, f'log{code_version}.txt')
            
            #diff 文件路径
            Diff_FILE_PATH = os.path.join(OUTPUT_PATH, f'diff.txt')
            Diff_1_FILE_PATH = os.path.join(OUTPUT_PATH, f'diff1.txt')

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
                cd ./version{code_version};
                {echo_green(f'START code version {code_version}')}
            ''')
            
            OUTPUT_PATH = os.path.join(BASE_PATH, f'outputs.alt/v1/version{code_version}')
            
            for i in range(len(params)):
                if i > 50:
                    continue
                os.system(f'''
                cd {OUTPUT_PATH};
                mkdir {i}
                ''')
                Right_cmd_PATH = os.path.join(OUTPUT_PATH, f'{i}/test0.txt')
                Error_cmd_PATH = os.path.join(OUTPUT_PATH, f'{i}/test.txt')
                Static_info_PATH = os.path.join(OUTPUT_PATH, f'{i}/Static_info.txt')
                Comp_info_PATH = os.path.join(OUTPUT_PATH, f'{i}/comp_info.txt')
                
                # print(params[i])
                # os.system(f'echo {params[i]}')

                os.system(f'''
                cd {SRC_PATH};          
                make build;
                {echo_green('COMPILE finished. generated [grep.exe] [grep.gcno]')}
                ''')
                
                os.system(f'''
                    echo "BEGIN_INPUT" >> {LOG_FILE_PATH};
                    echo {params[i]} >> {LOG_FILE_PATH};
                    echo "END_INPUT" >> {LOG_FILE_PATH};

                    cd {os.path.join(BASE_PATH, 'scripts')};
                    echo "RUN {i}" >> {LOG_FILE_PATH};
                    {os.path.join(SRC_PATH, 'grep.exe')} {params[i]} < ./stdin.txt >> {Error_cmd_PATH};
                    {os.path.join(ORG_PATH, 'grep.exe')} {params[i]} < ./stdin.txt >> {Right_cmd_PATH};
                    {echo_green('RUN finished. generated [grep.gcda]')}>>{LOG_FILE_PATH};
                    
                    
                    cd {SRC_PATH};
                    echo "TEST {i}" >> {LOG_FILE_PATH};
                    gcov -bfr grep.c >> {Static_info_PATH};

                    echo "" >> {Diff_FILE_PATH}
                    
                    echo "{code_version} -th fault and the {i} case " >> {Diff_FILE_PATH}
                    diff {Right_cmd_PATH} {Error_cmd_PATH} 
                    diff {Right_cmd_PATH} {Error_cmd_PATH} | tee -a {Comp_info_PATH} {Diff_FILE_PATH}
                    cmp --silent {Right_cmd_PATH} {Error_cmd_PATH} || echo "{code_version} -th fault and the {i} case failed " >> {Diff_1_FILE_PATH}

                    {echo_green('TEST finished.(with branch coverage) generated [grep.c.gcov] [wchar.h.gcov]')}
                    
                    echo >> {LOG_FILE_PATH};
                ''')
                

                os.system(f'''
                    cd {SRC_PATH};
                    mv ./grep.c.gcov {os.path.join(OUTPUT_PATH, f'grep.c.{code_version}_{i}.gcov')};
                    {echo_green('MOVE [grep.c.gcov] to output directory')}
                    rm ./grep.gcda ;
                    {echo_green('CLEAR finished')}
                    {echo_green(f'[CASE {i} DONE]')}
                ''')

            os.system(f'''
                    cd {SRC_PATH};
                    rm ./grep.exe ./grep.gcno
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

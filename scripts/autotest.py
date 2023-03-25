import os
from utils import echo_green,echo_red
from parse_params import parse_params
from fault_implant import insert_fault,recover_fault


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
            if code_version != 0:
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
                cd ./version{code_version};
                mkdir out;
                {echo_green(f'START code version {code_version}')}
            ''')
            os.system(f'''
                cd {SRC_PATH};          
                make build;
                {echo_green('COMPILE finished. generated [grep.exe] [grep.gcno]')}
            ''')
            OUTPUT_PATH = os.path.join(BASE_PATH, f'outputs.alt/v1/version{code_version}')
            LOG_FILE_PATH2 = os.path.join(OUTPUT_PATH, f'out/temp2.txt')
            LOG_FILE_PATH3 = os.path.join(OUTPUT_PATH, f'out/temp3.txt')
            for i in range(len(params)):
                if i > 3:
                    continue
                print(params[i])
                # os.system(f'echo {params[i]}')
                os.system(f'''
                    echo "BEGIN_INPUT" >> {LOG_FILE_PATH};
                    echo {params[i]} >> {LOG_FILE_PATH};
                    echo "END_INPUT" >> {LOG_FILE_PATH};

                    cd {os.path.join(BASE_PATH, 'scripts')};
                    echo "RUN {i}" >> {LOG_FILE_PATH};
                    {os.path.join(SRC_PATH, 'grep.exe')} {params[i]} < ./stdin.txt >> {LOG_FILE_PATH};
                    {echo_green('RUN finished. generated [grep.gcda]')}
                    
                    
                    cd {SRC_PATH};
                    echo "TEST {i}" >> {LOG_FILE_PATH};
                    gcov grep.c >> {LOG_FILE_PATH};

                
                    lcov -d . -c -o {i}.info --rc lcov_branch_coverage=1 >>{LOG_FILE_PATH2};
                    mv {i}.info {os.path.join(OUTPUT_PATH,f'out/')};


                    {echo_green('TEST finished.(with branch coverage) generated [grep.c.gcov] [wchar.h.gcov]')}
                    
                    echo >> {LOG_FILE_PATH};
                ''')
                if i == 0:
                    os.system(f'''
                    mk {os.path.join(OUTPUT_PATH,f'out/')}out.info
                    ''')
                elif i == 1:
                     os.system(f'''
                    lcov -a  {os.path.join(OUTPUT_PATH,f'out/0.info')} -a {os.path.join(OUTPUT_PATH,f'out/0.info')} -o {os.path.join(OUTPUT_PATH,f'out/')}out.info --rc lcov_branch_coverage=1 >>{LOG_FILE_PATH3};
                     ''')
                else:
                     os.system(f'''
                    lcov -a  {os.path.join(OUTPUT_PATH,f'out/out.info')} -a {os.path.join(OUTPUT_PATH,f'out/')}{i}.info -o {os.path.join(OUTPUT_PATH,f'out/')}out.info --rc lcov_branch_coverage=1 >>{LOG_FILE_PATH3};
                     ''')

                os.system(f'''
                    cd {SRC_PATH};
                    mv ./grep.c.gcov {os.path.join(OUTPUT_PATH, f'grep.c.{code_version}_{i}.gcov')};
                    {echo_green('MOVE [grep.c.gcov] to output directory')}
                    rm ./grep.gcda ./wchar.h.gcov;
                    {echo_green('CLEAR finished')}
                    {echo_green(f'[CASE {i} DONE]')}
                ''')

                if i ==198:
                    os.system(f'''
                        genhtml --branch-coverage {os.path.join(OUTPUT_PATH,f'out/')}out.info --output-directory {os.path.join(OUTPUT_PATH,f'out/out')}{code_version};
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

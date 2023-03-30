import os
from utils import echo_green,echo_red
from parse_params import parse_params
from path import TEST_CASE_FILE_PATH

from common import clear_and_init, exec_test_case, insert_fault_and_compile

def Xrun_by_version(code_version):

    # 项目根路径
    BASE_PATH = '/home/ubuntu/RGtest/grep'
    # 源代码目录路径
    SRC_PATH = os.path.join(BASE_PATH, 'versions.alt/versions.seeded/v1/')
    # ORG_PATH = os.path.join(BASE_PATH, 'versions.alt/versions.orig/v1/')
    # 植入宏（命令行参数）文件路径
    FAULT_FILE_PATH = os.path.join(BASE_PATH, 'versions.alt/versions.seeded/v1/FaultSeeds.h')
    # 输入数据（命令行参数）文件路径
    INPUT_FILE_PATH = os.path.join(BASE_PATH, 'testplans.alt/v1/v0.cov.universe')
    # 输出目录路径
    OUTPUT_PATH = os.path.join(BASE_PATH, f'outputs.alt/v1/')
    
    # #diff 文件路径
    # Diff_FILE_PATH = os.path.join(OUTPUT_PATH, f'diff.txt')
    # Diff_1_FILE_PATH = os.path.join(OUTPUT_PATH, f'diff1.txt')

    
    
    
    
    OUTPUT_PATH = os.path.join(BASE_PATH, f'outputs.alt/v1/version{code_version}')
    
    for i in range(len(params)):
        if i > 5:
            continue
        os.system(f'''
        cd {OUTPUT_PATH};
        mkdir {i}
        ''')
        
        #请参考文档了解以下结果输出路径的详细说明

        #正确版本用例输出结果路径
        Right_cmd_PATH = os.path.join(OUTPUT_PATH, f'{i}/test0.txt')
        #错误版本用例结果输出路径
        Error_cmd_PATH = os.path.join(OUTPUT_PATH, f'{i}/test.txt')

        #分支覆盖结果输出路径
        Static_info_PATH = os.path.join(OUTPUT_PATH, f'{i}/Static_info.txt')

        #比较结果输出路径
        Comp_info_PATH = os.path.join(OUTPUT_PATH, f'{i}/comp_info.txt')
        

        # print(params[i])
        # os.system(f'echo {params[i]}')

        
        

        #以下代码中diff命令没有给出正确的输出
        #TODO：diff
        
        os.system(f'''
            echo "BEGIN_INPUT" >> {LOG_FILE_PATH};
            echo {params[i]} >> {LOG_FILE_PATH};
            echo "END_INPUT" >> {LOG_FILE_PATH};

            cd {os.path.join(BASE_PATH, 'scripts')};
            echo "RUN {i}" >> {LOG_FILE_PATH};
            {os.path.join(SRC_PATH, 'grep.exe')} {params[i]} < ./stdin.txt >> {Error_cmd_PATH};
            {os.path.join(ORG_PATH, 'grep.exe')} {params[i]} < ./stdin.txt >> {Right_cmd_PATH};
            {echo_green('RUN finished. generated [grep.gcda]')}>>{LOG_FILE_PATH};
            
            
            

            echo "" >> {Diff_FILE_PATH}
            
            echo "{code_version} -th fault and the {i} case " >> {Diff_FILE_PATH}
            diff {Right_cmd_PATH} {Error_cmd_PATH} 
            diff {Right_cmd_PATH} {Error_cmd_PATH} | tee -a {Comp_info_PATH} {Diff_FILE_PATH}
            cmp --silent {Right_cmd_PATH} {Error_cmd_PATH} || echo "{code_version} -th fault and the {i} case failed " >> {Diff_1_FILE_PATH}

            {echo_green('TEST finished.(with branch coverage) generated [grep.c.gcov] [wchar.h.gcov]')}
            
            echo >> {LOG_FILE_PATH};
        ''')
        

if __name__ == '__main__':
    run_by_version(0)
    #version19 为 未植入错误宏的版本
    # for i in range(19): 
    #     if i >5:
    #         continue
    #     run_by_version(i)

    # 测试植入错误宏
    # 项目根路径
    # BASE_PATH = '/home/ubuntu/RGtest/grep'
    # FAULT_PATH = os.path.join(BASE_PATH, 'versions.alt/versions.seeded/v1/FaultSeeds.h')
    # 1. 植入错误宏 
    # insert_fault(FAULT_PATH,0)
    # 2. 恢复错误
    # recover_fault(FAULT_PATH,1)

import os
from fault_implant import insert_fault, recover_fault
from parse_params import parse_params
from tqdm import tqdm


def my_print(msg: str):
    pass
    # print(msg)

class RunVersion:
    def __init__(self, code_version):
        self.code_version = code_version
        # 项目根路径
        self.BASE_PATH = '/home/ubuntu/RGtest/grep'
        # 源代码目录路径
        self.SRC_PATH = os.path.join(self.BASE_PATH, 'versions.alt/versions.seeded/v1/')
        # 输出目录路径
        self.OUTPUT_PATH = os.path.join(self.BASE_PATH, f'outputs.alt/v1/')
        # 植入宏（命令行参数）文件路径
        self.FAULT_FILE_PATH = os.path.join(self.BASE_PATH, 'versions.alt/versions.seeded/v1/FaultSeeds.h')
        # 输入数据（命令行参数）文件路径
        self.TEST_CASE_FILE_PATH = os.path.join(self.BASE_PATH, 'testplans.alt/v1/v0.cov.universe')
        # 自动化脚本目录路径
        self.SCRIPT_PATH = os.path.join(self.BASE_PATH, 'scripts/')

        # 日志文件路径
        self.LOG_FILE_PATH = os.path.join(self.OUTPUT_PATH, f'log_{code_version}.txt')
        # 输出的GCOV文件目录
        self.OUTPUT_GCOV_PATH = None
        # grep.exe输出的结果目录
        self.OUTPUT_EXEC_PATH = None
        # 累加结果的gcda文件
        self.OUTPUT_HTML_PATH = None

    def clear_and_init(self):
        """
        对于每个版本，在执行所有工作前先清理之前的输出，再初始化
        对于版本i, 他的所有输出在OUTPUT_PATH/version_{i}中
        以下是目录层级结构：
            log_{i}.txt
            version_{i}
                gcov
                    - version_{i}_{j}.gcov
                exec
                    - version_{i}_{j}.txt
                html
                    - html相关文件
        """
        os.system(f'''
            cd {self.OUTPUT_PATH};
            rm -rf version_{self.code_version};
            rm -f log_{self.code_version}.txt;
            mkdir version_{self.code_version};
            cd ./version_{self.code_version};
            mkdir gcov;
            mkdir exec;
        ''')
        my_print(f'START code version {self.code_version}')
        self.OUTPUT_GCOV_PATH = os.path.join(self.OUTPUT_PATH, f'version_{self.code_version}/gcov/')
        self.OUTPUT_EXEC_PATH = os.path.join(self.OUTPUT_PATH, f'version_{self.code_version}/exec/')
        self.OUTPUT_HTML_PATH = os.path.join(self.OUTPUT_PATH, f'version_{self.code_version}/html/')

    def insert_fault_and_compile(self):
        # 1. 植入错误宏 
        insert_fault(self.FAULT_FILE_PATH, self.code_version)
        my_print(f'INSERT FAULT {self.code_version}')
        
        # 2. 编译
        os.system(f'''
            cd {self.SRC_PATH};          
            make build;
            ''')
        my_print('COMPILE finished. generated [grep.exe] [grep.gcno]')
        # 3. 恢复错误宏
        recover_fault(self.FAULT_FILE_PATH, self.code_version)

    def exec_test_case(self, idx, param):
        os.system(f'''
            echo "INPUT" >> {self.LOG_FILE_PATH};
            echo "{param}" >> {self.LOG_FILE_PATH};

            echo "RUN {idx}" >> {self.LOG_FILE_PATH};
            cd {self.SCRIPT_PATH};
            {os.path.join(self.SRC_PATH,'grep.exe')} < ./stdin.txt >> {os.path.join(self.OUTPUT_EXEC_PATH, f'version_{self.code_version}_{idx}.txt')} 2>&1 {param}
        ''')
        my_print('RUN finished. generated [grep.gcda]')

    def exec_gcov(self, idx):
        os.system(f'''
            cd {self.SRC_PATH};
            echo "TEST {idx}" >> {self.LOG_FILE_PATH};
            gcov -bfr grep.c >> {self.LOG_FILE_PATH};

            mv ./grep.c.gcov {os.path.join(self.OUTPUT_GCOV_PATH, f'version_{self.code_version}_{idx}.gcov')};
            
        ''')
        my_print('MOVE [grep.c.gcov] to output directory')
        my_print('CLEAR finished')
        my_print(f'[CASE {idx} DONE]')

    def finish(self):
        os.system(f'''
            cd {self.SRC_PATH};
            rm ./grep.exe ./grep.gcno ./grep.gcda;
        ''')
    
    def lcov_and_show(self):
        # 1. 生成 coverage.info 数据文件
        
        # 2. 根据这个数据文件生成报告
        os.system(f'''
        cd {self.SRC_PATH};
        lcov --capture --directory . --output-file coverage.info --rc lcov_branch_coverage=1;
        genhtml --branch-coverage coverage.info --output-directory {self.OUTPUT_HTML_PATH};
        mv ./coverage.info {os.path.join(self.OUTPUT_PATH, f'version_{self.code_version}/')};
        ''')
        
        
    
    def run(self):
        self.clear_and_init()
        self.insert_fault_and_compile()
        # exit(0)
        params = parse_params(self.TEST_CASE_FILE_PATH)
        for i in tqdm(range(len(params)), f'V{self.code_version}'):
        # for i in range(len(params)):
            param = params[i]
            self.exec_test_case(i, param)
            self.exec_gcov(i)
        self.lcov_and_show()
            # print(f'{i} / {len(params)}')
        self.finish()


if __name__ == '__main__':
    for i in range(19):
        RunVersion(i).run()
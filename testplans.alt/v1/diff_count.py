import difflib
import os




if __name__ == '__main__':
    # 项目根路径
    BASE_PATH = '/home/ubuntu/RGtest/grep'
    INPUT_FILE_PATH = os.path.join(BASE_PATH, 'testplans.alt/v1/v0.cov.universe')
    OUTPUT_FILE_PATH = os.path.join(BASE_PATH, 'testplans.alt/v1/testplan2.txt')
    with open( INPUT_FILE_PATH) as file_in, open(OUTPUT_FILE_PATH, 'w') as file_out:
        for line in file_in:
            line = line.replace('-P [', '')
            line = line.replace('e[ ]\[', 'e ')
            line = line.replace('dat]', 'dat')
            line = line.replace('][ ] -I [ ]\[', ' -I ')
            line = line.replace('] -I [', ' -I ')
            line = line.replace('f]', 'f')
            line = line.replace('.../', '../../../')
            #line = line.replace('\\', '\\\\\\\\')
            file_out.write(line)


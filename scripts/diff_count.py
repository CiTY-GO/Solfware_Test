import difflib
import os


def exist(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False



def diff_count(filename1: str, filename2: str) -> int:
    with open(filename1, 'r') as file1, open(filename2, 'r') as file2:
        diff = difflib.ndiff(file1.readlines(), file2.readlines())
    count = 0
    for line in diff:
        if line.startswith('-') or line.startswith('+'):
            count += 1
    return count

def diff_version(v1, v2):
    BASE_PATH = '/home/ubuntu/RGtest/grep/outputs.alt/v1/'
    num_of_testcase = 199

    for i in range(num_of_testcase):
        
        v1_path = os.path.join(BASE_PATH, f'version_{v1}/exec/version_{v1}_{i}.txt')
        v2_path = os.path.join(BASE_PATH, f'version_{v2}/exec/version_{v2}_{i}.txt')
        if exist(v1_path) == False or exist(v2_path) == False:
            continue
        cnt = diff_count(v1_path, v2_path)
        if cnt != 0:
            print(f'diff count case{i}: V{v1} vs V{v2} => {cnt}')


if __name__ == '__main__':
    diff_version(0, 10)
            

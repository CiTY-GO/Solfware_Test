import difflib
import os


def exist(file_path):
    return os.path.exists(file_path)

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
    not_exist_indices = []
    right_cnt = 0
    for i in range(num_of_testcase):
        
        v1_path = os.path.join(BASE_PATH, f'version_{v1}/exec/version_{v1}_{i}.txt')
        v2_path = os.path.join(BASE_PATH, f'version_{v2}/exec/version_{v2}_{i}.txt')
        if not exist(v1_path) or not exist(v2_path):
            not_exist_indices.append(i)
            continue
        cnt = diff_count(v1_path, v2_path)
        if cnt == 0:
            right_cnt += 1

    return [right_cnt, num_of_testcase - len(not_exist_indices)]

if __name__ == '__main__':
    right_version = 18
    diff_data = []
    for i in range(18):
        diff_data.append(diff_version(i, right_version))
    print(diff_data)

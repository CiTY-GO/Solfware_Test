import difflib
import os

def diff_count(filename1: str, filename2: str) -> int:
    with open(filename1, 'r') as file1, open(filename2, 'r') as file2:
        diff = difflib.ndiff(file1.readlines(), file2.readlines())
    count = 0
    for line in diff:
        if line.startswith('-') or line.startswith('+'):
            count += 1
    return count


if __name__ == '__main__':
    BASE_PATH = '/home/ubuntu/RGtest/grep/outputs.alt/v1/'
    version_list = [0, 1, 2]
    num_of_testcase = 199
    for i in range(num_of_testcase):
        right_version_path = os.path.join(BASE_PATH, f'version0/grep.c.0_{i}.gcov')
        for j in version_list[1:]:
            curr_version_path = os.path.join(BASE_PATH, f'version{j}/grep.c.{j}_{i}.gcov')
            cnt = diff_count(right_version_path, curr_version_path)
            print(right_version_path)
            print(curr_version_path)
            print(f'diff count case{i}: V0 vs V{j} => {cnt}')

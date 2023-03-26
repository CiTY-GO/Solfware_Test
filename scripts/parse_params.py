# 解析输入参数
def parse_params(input_file_path: str):
    with open(input_file_path, 'r') as f:
        lines = f.readlines()
    
    params = []
    for line in lines:
        # check validation
        assert line[:4] == '-P [' and line[-2:] == ']\n'
        line = line.replace('-P [', '')
        line = line.replace('e[ ]\[', 'e ')
        line = line.replace('dat]', 'dat')
        line = line.replace('][ ] -I [ ]\[', ' -I ')
        line = line.replace('] -I [', ' -I ')
        line = line.replace('f]', 'f')
        line = line.replace('.../', '../../../')
        params.append(line)
    
    return params
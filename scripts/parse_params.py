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
# 植入错误宏
def insert_fault(fault_seed_file:str,code_version):
    if  code_version == 18:
        return
    line_number = code_version
    with open(fault_seed_file, 'r') as f:
        lines = f.readlines()
    lines[line_number]=lines[line_number][2:-3]+'\n'
    with open(fault_seed_file, 'w') as f:
        for line in lines:
            f.write(line)
# 恢复错误宏        
def recover_fault(fault_seed_file:str,code_version):
    if  code_version == 18:
        return
    line_number = code_version
    with open(fault_seed_file, 'r') as f:
        lines = f.readlines()
    lines[line_number]='/*'+lines[line_number][:-1]+'*/\n'
    with open(fault_seed_file, 'w') as f:
        for line in lines:
            f.write(line)

#!/bin/bash          

# Step 1: Remove the comment symbols at the beginning of each line
cp FaultSeeds.h  Seed_temp.h
                     # 从 Seed.h 文件中，将 /* 替换为空格，然后将结果写入 Seed_temp.h 文件中

# Step 2: Remove one comment line at a time
n=$(wc -l < Seed_temp.h)  # 统计 Seed_temp.h 文件中的行数，并将结果赋值给变量 n
for (( i=1; i<=$n; i++ )); do    # 循环 n 次，每次处理一行注释
    sed -e "${i}s|/\* ||; ${i} s| \*/||" Seed_temp.h > FaultSeeds.h #覆盖到源文件
    make build	#编译程序
    ./grep.exe 	#运行程序
    # 在gcov_result.txt末尾添加一行注入错误的信息并换行
    sed -n "${i}p" FaultSeeds.h >> gcov_result.txt
    echo "" >> gcov_result.txt    
    gcov -brf grep.c >> gcov_result.txt
			#生成 Gcov 报告   
done

cp Seed_temp.h FaultSeeds.h  #将原FaultSeeds.h 文件恢复

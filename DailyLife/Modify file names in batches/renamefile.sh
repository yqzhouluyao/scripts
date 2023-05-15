#!/bin/bash

# 指定文件夹路径，你需要将这个路径替换为你的具体路径
DIR_PATH="/Users/zhouluyao/Downloads/diaosi"

# 切换到指定的文件夹
cd "$DIR_PATH"

# 使用find命令找到所有的mp4文件
find . -type f -name '*.mp4' | while read -r file; do
    # 使用basename和sed提取出Sxx.Exx.1080P的部分，同时去掉多余的点号
    newname=$(basename "$file" | sed -E 's/.*((S[0-9]{2}\.E[0-9]{2}\.1080P)\..*mp4)$/\1/' | tr -d '.')
    # 打印出正在处理的文件名以及新的文件名
    echo "Processing: $file"
    echo "New name: $newname"
    # 如果新文件名和原文件名不同，并且新文件名不为空，那么就重命名文件
    if [ "$newname" != "$(basename "$file")" ] && [ ! -z "$newname" ]; then
        mv -v "$file" "$(dirname "$file")/$newname"
    fi
done


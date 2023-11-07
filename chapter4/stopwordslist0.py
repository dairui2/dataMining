import jieba.posseg as pseg

def filter_text_by_flag_and_save(input_file, output_file):
    # 读取原始文本
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # 需要排除的特定词性
    excluded_flag = ['m', 'c', 'q', 'u', 'ud', 'ug', 'uj', 'r', 't', 'd', 'p', 'w', 'x',
                     'ul']  ##数量词,连词,量词,助词,代词,时间,副词,介词,标点符号,标点符号,时态助词

    # 分词处理并筛选词性
    words = pseg.cut(text)
    filtered_words = [word for word, flag in words if flag  in  excluded_flag]

    # 将筛选后的词汇加入停用词文件
    with open(output_file, 'a+', encoding='utf-8') as f:
        for word in filtered_words:
            f.write(word + '\n')

    # 读取原始文本
    with open(output_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 去重并排序
    lines = sorted(set(lines))

    # 保存到新文件
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line)



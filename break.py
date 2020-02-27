import pandas as pd


def break_excel_ID():
    x_head_key = [
        '用户手机号', '用户姓名', '影像结果编号', '检查编号', '序列编号', '开始时间', '提交时间', '自定义内容',
        '阴阳性', '病灶', '影像工具', '影像结果类型', '影像结果', '分类'
    ]

    csv_file = '影像标注结果.csv'

    df = pd.read_csv(csv_file, header=0)
    df.columns = x_head_key

    # 对数据进行分组处理
    grouped = df.groupby(
        x_head_key[4])  # according different categories to group by the df

    file = 'track_by_id\\'

    for value, group in grouped:
        filename = file + str(value) + '.csv'
        try:
            f = open(filename, 'w')
            if f:
                # 清空文件内容
                f.truncate()

            # 将新数据写入文件
            group.to_csv(filename,
                         header=0,
                         index=False,
                         mode='a',
                         encoding="utf-8")
        except UnicodeEncodeError:
            print("编码错误, 该数据无法写到文件中, 直接忽略该数据")


break_excel_ID()
import csv
import json
import os
import re

import pandas as pd

import toJson

for root, dirs, files in os.walk("track_by_id/"):
    for file in files:
        with open(root + "/" + file, 'r', encoding='UTF-8') as f:
            print("序列编号：" + file)
            reader = csv.reader(f)
            result = list(reader)
            isequal=0
            for i in range(len(result)):
                if isequal!=0:
                    i=i-isequal
                if i >= len(result):
                    break
                flag = 0
                name1 = result[i][1]
                position1 = "json:" + result[i][12]
                position1 = re.sub('"', '', position1)
                position1 = toJson.parse(position1)
                rx = (float(position1['position'][0]) +
                      float(position1['position'][1])) / 2.0
                ry = (float(position1['position'][2]) +
                      float(position1['position'][3])) / 2.0
                rz = (float(position1['position'][4]) +
                      float(position1['position'][5])) / 2.0
                for j in range(len(result)):
                    if j >= len(result):
                        break
                    name2 = result[j][1]
                    if name1 == name2:
                        continue
                    position2 = "json:" + result[j][12]
                    position2 = re.sub('"', '', position2)
                    position2 = toJson.parse(position2)
                    #if(rx<datas[1]*1&&rx>datas[0]*1&&ry<datas[3]*1&&ry>datas[2]*1&&rz>datas[4]*1&&rz<datas[5]*1)
                    if rx < float(position2['position'][1]) and rx > float(
                            position2['position'][0]
                    ) and ry < float(position2['position'][3]) and ry > float(
                            position2['position'][2]) and rz > float(
                                position2['position'][4]) and rz < float(
                                    position2['position'][5]):
                        flag = 1
                        result.pop(i)
                        isequal=isequal+1
                        break
                if flag == 0:
                    data = pd.DataFrame({
                        "序列编号": [result[i][4]],
                        "病灶": [result[i][9]],
                        "影像工具": [result[i][10]],
                        "影像结果": [result[i][12]],
                        "自定义内容": [result[i][7]],
                        "分类": [result[i][13]]
                    })
                    data.to_csv("比对后.csv", mode="a", header=0, index=0)

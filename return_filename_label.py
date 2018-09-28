# -*- coding: utf-8 -*-

import os
import random
import csv

def return_filename_label():
    
    file_label_list = []
    PATH = ['guangdong Industry/guangdong_round1_train2_20180916',
            'guangdong Industry/guangdong_round1_train1_20180903']
    DEFECT_DICT = {'正常':0,'不导电':1,'擦花':2,'横条压凹':3,'桔皮':4,
                   '漏底':5,'碰伤':6,'起坑':7,'凸粉':8,'涂层开裂':9,
                   '脏点':10,'其他':11}
    for path in PATH:
        for dirpath,dirnames,filenames in os.walk(path):
            for filename in filenames:
                label = [0]*12
                if len(filename) < 13:
                    print '异常文件名:'+filename
                    continue
                if filename[6].isdigit():
                    key = filename[:6]
                    if key not in DEFECT_DICT:
                        key = '其他'
                    label[int(DEFECT_DICT[key])] = 1
                    file_label_list.append([os.path.join(dirpath,filename),key,
                                            DEFECT_DICT[key],label])
                elif filename[9].isdigit():
                    key = filename[:9]
                    if key not in DEFECT_DICT:
                        key = '其他'
                    label[int(DEFECT_DICT[key])] = 1
                    file_label_list.append([os.path.join(dirpath,filename),key,
                                            DEFECT_DICT[key],label])
                else:
                    key = filename[:12]
                    if key not in DEFECT_DICT:
                        key = '其他'
                    label[int(DEFECT_DICT[key])] = 1
                    file_label_list.append([os.path.join(dirpath,filename),key,
                                            DEFECT_DICT[key],label])
    random.shuffle(file_label_list)
    return file_label_list

def test_filename():
    
    test_file_name = []
    TEST_PATH = 'guangdong Industry/guangdong_round1_test_a_20180916'
    
    for dirpath,dirnames,filenames in os.walk(TEST_PATH):
        for filename in filenames:
            test_file_name.append(filename)
    return test_file_name

def write_submit(test_file_names,y_):
    name = 'submit.csv'
    csvfile = open(name,'w')
    writer = csv.writer(csvfile)
    for i in range(len(test_file_names)):
        if y_[i] == 0:
            writer.writerow([test_file_names[i],'norm'])
        elif y_[i] > 11:
            writer.writerow([test_file_names[i],'defect11'])
        else:
            writer.writerow([test_file_names[i],'defect'+str(y_[i])])
    csvfile.close()

test_filenames = test_filename()
print test_filenames[random.randint(0,439)]

file_label = return_filename_label()
for i in file_label[random.randint(0,2385)]:
    print i 

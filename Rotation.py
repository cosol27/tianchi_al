#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 14:16:13 2018

@author: zhou
"""
import os
import cv2 as cv
import numpy as np
import math
#from matplotlib import pyplot as plt
import time
import random

def HoughLinesP_Trans(img_path):
    if not os.path.exists(img_path):
        print 'file does not exist: ' +img_path
        return
    
    # 1、读取输入文件
    img = cv.imread(img_path)
    b,g,r = cv.split(img)
    
#    img = cv.merge([r,g,b])
    
    # 2、r通道 阈值检测
    ret, thresh = cv.threshold(r,1.17*r.mean(),255,cv.THRESH_BINARY)
#    plt.figure(figsize=(12,9))
#    plt.imshow(thresh)
    
    # 3、高斯滤波
    filt = cv.medianBlur(thresh, 21)
#    plt.figure(figsize=(12,9))
#    plt.imshow(filt)
    
    # 4、检测边缘
    canny = cv.Canny(filt,50,100)
#    plt.figure(figsize=(12,9))
#    plt.imshow(canny)
    
    # 5、霍夫直线变换
    lines = cv.HoughLinesP(canny,1,np.pi/180,150,minLineLength=120,maxLineGap=100)
    
    if type(lines) == type(None):
#        print 'No need HoughLinesP_Trans'
        return img
    
    lineimg = np.ones(canny.shape,dtype=np.uint8)
    lineimg = lineimg * 255
    
#    Thresh = 1.0* np.pi / 180
#    pi2 = np.pi/2

    THETA = []
    for line in lines:
        x1, y1, x2, y2 = line[0]    
        if x2 - x1 == 0:
            continue
        theta = 1.0 * (y2 - y1) / (x2 - x1)

        cv.line(lineimg, (x1, y1), (x2, y2), (0, 255, 0), 2)
        THETA.append(theta)
    
    if len(THETA) == 0:
        print 'Error', img_path
        return img
    
    else:
        angle = math.atan(sum(THETA)*1.0/len(THETA))
        angle = angle * (180 / np.pi)
    
    h, w = img.shape[:2]
    center = (w//2, h//2)
    
    # 随机旋转-180，180
    M = cv.getRotationMatrix2D(center, random.uniform(-180,180) - angle, 1.0)
    rotated = cv.warpAffine(img, M, (w, h), flags=cv.INTER_CUBIC,
                            borderMode=cv.BORDER_REPLICATE)    
    return rotated
#    plt.figure(figsize=(12,9))
#    plt.imshow(lineimg,cmap='gray')

    b,g,r = cv.split(rotated)
#    rotated = cv.merge([r,g,b])
#    plt.figure(figsize=(12,9))
#    plt.imshow(rotated)



    # r通道二值化图 通过M矩阵旋转
    r_lineimg = cv.warpAffine(filt, M, (w, h), flags=cv.INTER_CUBIC,
                              borderMode=cv.BORDER_REPLICATE)
    # 查找轮廓
    r_canny = cv.Canny(r_lineimg,50,100)
#    plt.figure(figsize=(12,9))
#    plt.imshow(r_lineimg,cmap='gray')
    # 霍夫直线
    r_lines = cv.HoughLinesP(r_canny,1,np.pi/180,150,
                             minLineLength=120,maxLineGap=100)
    if type(r_lines) == type(None):
#        print 'No need HoughLinesP_Trans'
        return img
    

    r_lineimg = np.ones(r_canny.shape,dtype=np.uint8)
    r_lineimg = r_lineimg * 255

    # 获取y列表
    y_list=[]
#    THETA = []
    for r_line in r_lines:
        x1,y1,x2,y2 = r_line[0]
        # 过滤斜度过大的直线
        if x1 != x2 and abs(1.0*(y1-y2)/(x1-x2)) > 0.15:
            continue
        y_list.extend([y1,y2])
        cv.line(r_lineimg, (x1, y1), (x2, y2), (0, 255, 0), 2)

    if len(y_list) == 0:
        print 'column y is 0'
        return rotated
    if max(y_list)-min(y_list) < 100:
        print 'one single line' + img_path
        if r[0:max(y_list),:].mean() > r.mean():
            return rotated[0:max(y_list),:]
        else:
            return rotated[max(y_list):,:]
#    return rotated[min(y_list):max(y_list),:]
    return 0


start = time.clock()

#num = 300
adj_count = {'正常':48,'不导电':56,'擦花':158,'横条压凹':48,'桔皮':101,'漏底':277,
             '碰伤':74,'起坑':65,'凸粉':45,'涂层开裂':53,'脏点':244,'其他':194}
defect_name = ['正常','不导电','擦花','横条压凹','桔皮',
               '漏底','碰伤','起坑','凸粉','涂层开裂','脏点']
count = 0
for dirpath,dirnames,filenames in os.walk('guangdong Industry/guangdong_round1_train2_20180916'):
    
    print '读取: %s %d' % (dirpath,len(filenames))
    if len(filenames) == 0:
        continue
    count += len(filenames)
#    for dn in defect_name:
#        if dn in dirpath and '其他' not in dirpath:
#            save_path = dirpath.replace('guangdong_round1_train2_20180916','train')
#            for filename in filenames:
#                if filename.split('.')[-1] != 'jpg':
#                    continue
#                if not os.path.exists(save_path):
#                    os.makedirs(save_path)
#                img = HoughLinesP_Trans(os.path.join(dirpath,filename))
#                cv.imwrite(os.path.join(save_path,filename),img)
#            for i in range(adj_count[dn]):
#                rd = random.randint(0,len(filenames)-1)
#                if filenames[rd].split('.')[-1] != 'jpg':
#                    i -= 1
#                    continue
#                img = HoughLinesP_Trans(os.path.join(dirpath,filenames[rd]))
#                cv.imwrite(os.path.join(save_path,str(i)+'.jpg'),img)
    
#    if '无瑕疵' in dirpath:
#        save_path = dirpath.replace('guangdong_round1_train2_20180916','train')
#        for filename in filenames:
#            if filename.split('.')[-1] != 'jpg':
#                continue
#            if not os.path.exists(save_path):
#                os.makedirs(save_path)
#            img = HoughLinesP_Trans(os.path.join(dirpath,filename))
#            cv.imwrite(os.path.join(save_path,filename),img)
#        for i in range(adj_count['正常']):
#            rd = random.randint(0,len(filenames)-1)
#            if filenames[rd].split('.')[-1] != 'jpg':
#                i -= 1
#                continue
#            img = HoughLinesP_Trans(os.path.join(dirpath,filenames[rd]))
#            cv.imwrite(os.path.join(save_path,str(i)+'.jpg'),img)
            
#    elif '其他' in dirpath:
##        print '读取: %s %d' % (dirpath,len(filenames))
#        save_path = dirpath.replace('guangdong_round1_train2_20180916','train')
#        for filename in filenames:
#            if filename.split('.')[-1] != 'jpg':
#                continue
#            if not os.path.exists(save_path):
#                os.makedirs(save_path)
#            img = HoughLinesP_Trans(os.path.join(dirpath,filename))
#            cv.imwrite(os.path.join(save_path,filename),img)
#        for i in range(int(1.38*len(filenames))):
#            rd = random.randint(0,len(filenames)-1)
#            if filenames[rd].split('.')[-1] != 'jpg':
#                i -= 1
#                continue
#            img = HoughLinesP_Trans(os.path.join(dirpath,filenames[rd]))
#            cv.imwrite(os.path.join(save_path,str(i)+'.jpg'),img)
            
#    else:
#        save_path = dirpath.replace('guangdong_round1_train2_20180916','train')
#        for filename in filenames:
#            if filename.split('.')[-1] != 'jpg':
#                continue
#            if not os.path.exists(save_path):
#                os.makedirs(save_path)
#            img = HoughLinesP_Trans(os.path.join(dirpath,filename))
#            cv.imwrite(os.path.join(save_path,filename),img)
        
#        for i in range(num - len(filenames)):
#            rd = random.randint(0,len(filenames)-1)
#            if filenames[rd].split('.')[-1] != 'jpg':
#                i -= 1
#                continue
#            img = HoughLinesP_Trans(os.path.join(dirpath,filenames[rd]))
#            cv.imwrite(os.path.join(save_path,str(i)+'.jpg'),img) 
    
    print '已运行%f' % (time.clock()-start)
print count

#for dirpath,dirnames,filenames in os.walk('guangdong Industry/guangdong_round1_test_a_20180916'):
#    print '读取: %s %d' % (dirpath,len(filenames))
#    
#    save_path = dirpath.replace('guangdong_round1_test_a_20180916','test')
#    for filename in filenames:
#            if filename.split('.')[-1] != 'jpg':
#                continue
#            if not os.path.exists(save_path):
#                os.makedirs(save_path)
#            img = HoughLinesP_Trans(os.path.join(dirpath,filename))
#            cv.imwrite(os.path.join(save_path,filename),img)
    



#img = HoughLinesP_Trans('53.jpg')
#plt.figure(figsize=(12,9))
#plt.imshow(img)
save_path_test = 'guangdong Industry/test'
save_path_train = 'guangdong Industry/train'
#if not os.path.exists(path):
#    os.makedirs(path)
#cv.imwrite(os.path.join(path,'sav1.jpg'),img)



#PATH = ['guangdong Industry/guangdong_round1_test_a_20180916',
#        'guangdong Industry/guangdong_round1_train2_20180916']
#for path in PATH:
#    for dirpath,dirname,filenames in os.walk(path):
#        for filename in filenames:
#            if filename.split('.')[-1] != 'jpg':
#                continue
#            print 'process......' + os.path.join(dirpath,filename)
#            img = HoughLinesP_Trans(os.path.join(dirpath,filename))
#            if 'test' in path:
#                save_path = dirpath.replace('guangdong_round1_test_a_20180916','test')
#            elif 'train' in path:
#                save_path = dirpath.replace('guangdong_round1_train2_20180916','train')
#            if not os.path.exists(save_path):
#                os.makedirs(save_path)
#            cv.imwrite(os.path.join(save_path,filename),img)
#        print 'running......' + str(time.clock()-start)

print 'done'


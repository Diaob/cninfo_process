# coding=utf-8
#
# Author: ECNU 虾饺
# 用来修复巨潮反爬虫机制带来的PDF文件损坏
#

import spider
import os
import io

pdf_save = './pdf/'

#第0月的31其实就是上年的12月
final_day = [31,31,28,31,30,31,30,31,31,30,31,30,31]

#add_zero
def az(num):
    if num < 10:
        str_num = '0' + str(num)
        return str_num
    else:
        return str(num)

def recheck(code,file):
    if os.path.getsize(file) <= 15000:
        txt_path = './txt/' + file[6:len(file)-4] + '.txt'
        cmd = 'node extract_text.js ' +  file + " " + txt_path
        print(cmd)
        os.system(cmd)
        if os.path.exists(txt_path) == False:
            spider.search(code)


def checkIsHtml(file):
    isHtml = False
    filepath = pdf_save + file
    if os.path.getsize(filepath) <= 15000:
        try:
            with io.open(filepath, encoding='UTF-8') as htmlfile:
                lines = htmlfile.readlines()
                for line in lines:
                    if "html" in line:
                        isHtml = True
                        break
        except:
            return False

    if isHtml:
        cmd = "mv " + filepath + " " + filepath[:-4] + ".txt"
        os.system(cmd)
        return True
    else:
        return False
        

for file in os.listdir(pdf_save):

    global rangetime
    rangetime = '2001-01-01+~+2020-04-03'

    if os.path.getsize(pdf_save + file) <= 15000:
'''
        if checkIsHtml(file):
            continue
'''      
        code = file[0:6]
        date = file[7:15]

        day = int(date[6:8])
        month = int(date[3:5])
        year = int(date[0:2])
        
        next_day = day + 1
        previous_day = day - 1
        next_month = month
        previous_month = month
        
        if day == final_day[month]:
            next_day = 1
            next_month += 1
        elif day == 1:
            previous_day = final_day[month - 1]
            previous_month -= 1
        elif next_month > 12:
            next_month = 1
        elif previous_month < 1:
            previous_month = 12

        

        time = '20' + str(az(year)) + '-' + str(az(previous_month)) + '-' \
               + str(az(previous_day)) + '+~+20' + str(az(year)) + '-' \
               + str(az(next_month)) + '-' + str(az(next_day))

        rangetime = time
 
        spider.search(code)

        #recheck(code,pdf_save + file)
        

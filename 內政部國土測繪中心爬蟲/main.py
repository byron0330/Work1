import datetime
import time

import numpy as np
import pandas as pd
import os,sys
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import xlsxwriter
from utils.requests_data import get_soup

start=datetime.datetime.now()
proc_data_list=[]
read_data_list = []
def find_readdata_file():#尋找最新xlsx檔案
    path=os.getcwd() #指定資料夾路徑
    number=-1
    file_list=os.listdir(path)
    file_list.sort(key=lambda fn:os.path.getatime(path+"\\" + fn) #將檔案照時間排序
              if not os.path.isdir(path + "\\" + fn) else 0)
    while 1==1:
        if "readdata" not in file_list[number]:#確定抓到的檔案名稱為"readdata"後即跳出迴圈
            number=number-1
        else :
            break
    return(file_list[number]) #回傳最新檔案名稱"

def read_origin_data():
    data = pd.read_excel(io=find_readdata_file(), usecols=[0,2,3,4])
    return data

def proc_data(data):
    url=("https://api.nlsc.gov.tw/other/MarkBufferAnlys/bus/{lon}/{lat}/{radius}".format(lon=round(data[1],4), lat=round(data[2],4), radius=int(data[3])))
    json=get_soup(url)
    serNo=0
    for i in json :
        proc_data={
            'pointNo':int(data[0]),
            'serNo':serNo,
            'type':i['type'],
            'lon': i['lon'],
            'lat': i['lat'],
            'id': i['id'],
            'name': i['name'],
            'sname': i['sname'],
            'addr': i['addr'],
            'tel': i['tel'],
            'distance': i['distance'],
            }
        serNo += 1
        proc_data_list.append(proc_data)
    if json ==[]:
        proc_data = {
            'pointNo': int(data[0]),
            'serNo': 1,
            'type': np.NAN,
            'lon': np.NAN,
            'lat': np.NAN,
            'id': np.NAN,
            'name': np.NAN,
            'sname': np.NAN,
            'addr': np.NAN,
            'tel': np.NAN,
            'distance': np.NAN,
        }
        proc_data_list.append(proc_data)


def save_data(proc_data_list):
    data = pd.DataFrame(proc_data_list).sort_values(by=['pointNo','serNo'])
    data.to_excel("{}.xlsx".format(datetime.datetime.now().strftime("%Y%m%d_%H%M")), index=None,engine='xlsxwriter')
    end=datetime.datetime.now()
    print("startTime :{start}".format(start=start))
    print("endTime : {end}".format(end=end))
    print("procTime :{proc}秒".format(proc=(end-start).seconds))
    print("執行成功，存檔名稱為：" + "{}.xlsx".format(datetime.datetime.now().strftime("%Y%m%d_%H%M")))

#####Main
try:
    try:
        data = read_origin_data()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print("讀取資料失敗")
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        executor.map(proc_data,data.values)
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    print("爬取資料失敗")
save_data(proc_data_list)
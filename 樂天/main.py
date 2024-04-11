import datetime
import pandas as pd
import os,sys
import xlsxwriter
from utils.requests_data import get_soup
from utils.rakuten_helper import proc_infopage

def find_new_file():#尋找最新xlsx檔案
    path=os.getcwd() #指定資料夾路徑
    number=-1
    file_list=os.listdir(path)
    file_list.sort(key=lambda fn:os.path.getatime(path+"\\" + fn) #將檔案照時間排序
              if not os.path.isdir(path + "\\" + fn) else 0)
    while 1==1:
        if ".xlsx" not in file_list[number]:#確定抓到的檔案名稱為".xlsx"後即跳出迴圈
            number=number-1
        else :
            break
    return(file_list[number]) #回傳最新檔案名稱"

def proc_data(shop_list,origin_data):
    data=[]
    for shop in shop_list:
        proc=proc_infopage(shop)
        print(shop)
        if proc.shopCrawResult=="成功":
            proc.get_basic_data()
            proc.get_shopProfile()
            proc.get_shopProdClass()
            proc.get_shopServiceNum()
            proc.get_shopScore()
            proc.get_shopScoreAmt()
            proc.get_shopShipSpeed()
            proc.get_shopDistrict()
            proc.get_shopTag()
            proc.get_shopPayment()
            proc.get_shopDelivery()
        data.append(proc.get_data())

    data = pd.DataFrame(data)
    data = pd.concat([origin_data,data])
    try:#儲存檔案，檔名為現在日期+時間 ex：20221220_1430 (2022年12月20日 14點30分)
        data.to_excel("{}.xlsx".format(datetime.datetime.now().strftime("%Y%m%d_%H%M")),index=None,encoding="utf-8-sig",engine='xlsxwriter')
        print("執行成功，存檔名稱為："+"{}.xlsx".format(datetime.datetime.now().strftime("%Y%m%d_%H%M")))
    except Exception as e:
        print("權限被拒絕：您的excel文件已打開，請關閉文件")

if __name__ == "__main__":
    try:
        if len(sys.argv) ==2 :
            shop_list = []
            workType = sys.argv[1] #讀取使用者輸入的workType
            soup,code= get_soup("https://www.rakuten.com.tw/shop/")
            data = soup.select("div.category-content ul li a")

            if workType=='1': #更新最新檔案
                try:
                    select_file_name = find_new_file()#抓出最新檔案
                    read_file = pd.read_excel(io=select_file_name) #讀取抓到的最新檔案
                    for shop in data:
                        shop_id = shop['href'].split('/')[2]
                        if shop_id not in read_file["shopId"].values:
                            shop_list.append(shop_id)
                        else:                   #如果讀取的檔案中已有相同的ID名稱，則跳過不爬取此店家
                            continue
                    proc_data(shop_list,read_file,) #參數依序為：過濾後的店家ID列表、讀取的資料
                except Exception as e:
                    print("讀取檔案失敗，請確認資料夾中已有現存的xlsx檔案")

            elif workType=='0': #全部爬取
                for shop in data:
                    shop_list.append(shop['href'].split('/')[2])
                proc_data(shop_list,None,)  #參數依序為：全部店家ID列表、讀取的資料(workType==0時沒有所以設None)。

            else: #若使用者輸入時輸入0、1以外的參數，則會print以下訊息。
                print("執行模式輸入錯誤，0為全部爬取資料存成新檔，1為更新目前最新檔案")
        else:
            print("輸入參數數量有誤，請輸入python main.py +執行模式(1 or 0)")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print("爬取店家資料失敗")

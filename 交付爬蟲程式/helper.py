import requests,time,json,subprocess
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from decrypt_yungching import decrypt_yungching_data
s = requests.session()

def connect():
    commond = 'rasdial.exe Hinet 連線帳號 連線密碼'
    subprocess.call(commond,shell=True)

def disconnect():
    commond = 'rasdial.exe Hinet /DISCONNECT'
    subprocess.call(commond,shell=True)

def reconnect(): #切換IP時使用
    disconnect()
    time.sleep(5.5)
    connect()
    time.sleep(0.5)
    
def set_headers(): #先前版本需使用，自七月永慶更改為AES加密後停用
    options = Options()
    options.add_argument('--headless')  # 無頭模式，不開啟瀏覽器視窗
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://buy.yungching.com.tw/")
    
    # 等載入，可以使用 time.sleep 或 WebDriverWait
    import time
    time.sleep(3)

    # 取得所有 cookies
    cookies = driver.get_cookies()
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    driver.quit()
    cookie=""
    for i in cookie_dict.keys():
        cookie+=i+"="+cookie_dict[i]+","
    global headers
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    "Content-Type" : "application/json;charset=UTF-8", 
    "Referer" : "https://buy.yungching.com.tw/list/",
    "cookie" :  cookie[:-1]      
    }
    print(headers)

def get_TotalPage(city,area): #取得總頁數
    url = f"https://buy.yungching.com.tw/api/v2/list?area={city}-{area}&pinType=0&isAddRoom=true&pg=1&ps=30"
    r = requests.get(url,)
    result = decrypt_yungching_data(json.loads(r.text)["data"])
    totalCount = result["pa"]["totalItemCount"]
    totalPage = result["pa"]["totalPageCount"]
    return totalCount , totalPage


def get_data(city,area,page): #取得清單頁物件資料
    url = f"https://buy.yungching.com.tw/api/v2/list?area={city}-{area}&pinType=0&isAddRoom=true&od=80&pg={page}&ps=30"
    r = requests.get(url)
    data = decrypt_yungching_data(json.loads(r.text)["data"])
    house_list = data["list"]
    return house_list

def get_detail(oid): #取得詳細頁物件資料
    url = f"https://buy.yungching.com.tw/api/v2/house?id={oid}"
    r = s.get(url,)
    if r.status_code == 200:
        data = json.loads(r.text)
        result = decrypt_yungching_data(data["data"])
        print(result)
        return result
    else:
        print(r.status_code)
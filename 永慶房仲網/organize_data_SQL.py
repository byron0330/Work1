import helper
from datetime import datetime
from bs4 import BeautifulSoup
import re,requests,json
import SQL
s = requests.session()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}

buildType = {
    "住宅大樓":"1",
    "電梯大樓":"1",
    "華廈":"1",
    "公寓" : "2",
    "套房" :"3",
    "別墅" : "4",
    "透天厝" : "4",
    "店面" : "5",
    "辦公商業大樓" : "6",
    "廠房" : "6",
    "農舍" : "7",
    "車位":"7",
    "土地":"8",
    "其他":"8",
}

def get_area(city,area):
    if city =="新竹市":
        return "新竹市"
    if city =="嘉義市":
        return "嘉義市"
    return area

def get_street(address , city , area):
    address = address.replace(city,"")
    address = address.replace(area,"")
    return address
    
def get_room_count(room_count):
    try:
        return float(room_count)
    except:
        return None
    
def get_floor(floor_count):
    try:
        return int(floor_count)
    except:
        return None

def get_img(img_url):
    img_url = img_url.replace("{","")
    img_url = img_url.replace("}","")
    img_url = img_url.replace("height=1","height=0")
    url = "https:"+ img_url
    return url

def get_parking(parking):
    if parking == "":
        return False
    else:
        return True

def get_f1(f1):
    try:
        return float(f1)
    except:
        return None
    
def get_f2(f2):
    try:
        return float(f2)
    except:
        return None

def get_TEL2(house_data):
    try:
        if house_data["ivrInfo"]["extension"] == "":
            return house_data["ivrInfo"]["tel"]
        else:
            phone = house_data["ivrInfo"]["tel"]
            ext = house_data["ivrInfo"]["extension"]
            tel2 = f"{phone} ({ext})"
            return tel2
    except:
        return None

def get_MonthlyPI(text):
    if text != None and text != "" :
        text= text.replace(",","")
        numbers = re.findall(r'\d+', text)
        result = int(numbers[0]) if numbers else None
        return int(result)
    else :
        return None
    
def get_list(tag_list):
    result = ""
    if tag_list != None and tag_list!= "":
        for i in tag_list:
            result += i+","
        return result
    else:
        return None
        
def get_size(Size):
    try:
        Size = float(Size)
        return Size
    except:
        return None

class organize():
    def __init__(self,CITY):
        self.city =CITY

    def organize_data(self, house,area,):
        try:
            date = datetime.today().strftime("%Y%m%d_%H%M"),
            url = "https://buy.yungching.com.tw/house/"+str(house["caseSId"])
            detail= helper.get_detail(house["caseSId"])
            print(detail)
            # print(detail)
            # time.sleep(50000)
            data={
                "CId" : 6,
                "Vision" : 6,
                "Oid" : house["caseSId"],
                "City" : self.city,
                "Area" : get_area(self.city , area),
                "Street" : get_street(house['address'] , self.city , area),
                "Address":house['address'],
                "TotalPrice":float(house["price"]),
                "CaseName":house["caseName"],
                "ImgUrl" : get_img(house["cover"]),
                "TotalAreaSize" : float(house["pinInfo"]["regArea"]),
                "MainAreaSize" :get_f1(house["pinInfo"]["mainArea"]),
                "HouseType" : house["caseTypeName"],
                "RoomCount" : get_room_count(house["patternInfo"]["room"]),
                "HallCount" : get_room_count(house["patternInfo"]["livingRoom"]),
                "BathroomCount" : get_room_count(house["patternInfo"]["bathRoom"]),
                "TargetFloorNumberFrom" : get_floor(house["floorInfo"]["fromFloor"]),
                "TargetFloorNumberTo" : get_floor(house["floorInfo"]["toFloor"]),
                "HouseFloorCount" : get_floor(house["floorInfo"]["upFloor"]),
                "AgencyPageUrl" : url,
                "Parking" : get_parking(house["carPrice"]),
                "CreateDateTime" : date,
                "RefreshDateTime" : date,
                "LastRefreshDetail" :date,
                "HouseYear" : get_f2(house["buildAge"]),
                "BuildingType" : buildType[house["caseTypeName"]],
                "Community" : house["communityInfo"]["communityName"],
                "AttachSize" : get_size(house["pinInfo"]["porchArea"]),
                "LandAreaSize" : get_size(house["pinInfo"]["landArea"]),
                "ParkingType" : house["parking"],
                "Longitude" : detail["geoInfo"]["longitude"],
                "Latitude" : detail["geoInfo"]["latitude"],
                "AgencySalerName" : detail["shopInfo"]["name"],
                "AgencyName" :None,
                "AgencyCompanyName" :detail["shopInfo"]["companyName"],
                "AgencyStoreName" :detail["shopInfo"]["shopName"],
                "AgencyStoreAddress" :detail["shopInfo"]["address"],
                "AgencyPhone":get_TEL2(detail),
                "AgencyMobile":None,
                "Feature1" : detail["caseFeature"].replace("\n",""),
                "Feature2" : get_list(detail['highLights']),
                "MonthlyPayGuard" : detail['manageInfo']['manageExpense'],
                "HouseMaterial":detail["buiStrn"],
                "NearBySchool":get_list(detail['schoolInfo']),
                "HouseDirection":detail['dirFace'],
                "Online":1,
                "Process":False,
                "BachId":datetime.today().strftime("%Y%m%d"),
                }
            # print(data)
        
            if data['TotalAreaSize'] >0: 
                print(data)
                SQL.insert_house_data(data)
                print(f"已存入資料：{data['Oid']}")
                return 1
            else:
                return 0
        except Exception as e :
            print(e.__traceback__.tb_lineno)
            print(e)
            return 0
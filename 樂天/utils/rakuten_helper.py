import datetime
import warnings
import numpy as np

from utils.requests_data import get_soup

remove_word = [' ', '\n', '\r',"(",")"]
warnings.filterwarnings("ignore")

class proc_infopage:
    def __init__(self,shop):
        self.shopUrl="https://www.rakuten.com.tw/shop/{}/".format(shop)
        self.shopId = shop
        try:
            self.soup,status_code= get_soup(self.shopUrl+"info/")
            if status_code==200 : #200代表成功抓到店家網站
                self.shopCrawResult="成功"
                self.shopNote = "html標籤變更或無標籤:shopCompName、shopPrincipal、shopName、shopAdmin、shopAddress、shopPhoneNum、shopFaxNum、"
            elif status_code==410:#410代表店家終止服務
                self.shopCrawResult="終止服務"
                self.shopNote ="html標籤變更或無標籤:"
            else:
                self.shopNote="網頁不存在"
                self.shopCrawResult="失敗"
        except Exception as e: #get_soup出錯
            self.shopNote = "網頁不存在"
            self.shopCrawResult="失敗"

    def get_shopProfile(self):#店家簡介文字/圖片的原始碼
        try:
            self.shopProfile = self.soup.select("div.b-text.b-editable")
            if self.shopProfile ==[]:
                self.shopProfile=np.NAN
                self.shopNote += "shopProfile、"
        except Exception as e:  # 錯誤訊息
            self.shopProfile=np.nan
            self.shopNote+="shopProfile、"

    def get_basic_data(self): ##店家簡介資料
        self.shopCompName=np.NAN
        self.shopPrincipal =np.NAN
        self.shopName=np.NAN
        self.shopAdmin=np.NAN
        self.shopAddress=np.NAN
        self.shopPhoneNum=np.NAN
        self.shopFaxNum=np.NAN
        try:
            shop_data = self.soup.select('table.b-table.b-table-bordered.b-table-condensed tr')
            for data in shop_data:
                title=data.th.text.replace("\n","")
                if title=="公司名稱":
                    self.shopCompName =data.td.text
                    self.shopNote = self.shopNote.replace("shopCompName、", "")
                elif title=="公司代表":
                    self.shopPrincipal = data.td.text
                    self.shopNote = self.shopNote.replace("shopPrincipal、", "")
                elif title=="店家名稱":
                    self.shopName = data.td.text
                    self.shopNote = self.shopNote.replace("shopName、", "")
                elif title=="店家管理員":
                    self.shopAdmin = data.td.text
                    self.shopNote = self.shopNote.replace("shopAdmin、", "")
                elif title=="店家地址":
                    self.shopAddress = data.td.text
                    self.shopNote = self.shopNote.replace("shopAddress、", "")
                elif title=="店家電話號碼":
                    self.shopPhoneNum = data.td.text
                    self.shopNote = self.shopNote.replace("shopPhoneNum、", "")
                elif title == "店家傳真號碼":
                    self.shopFaxNum = data.td.text
                    self.shopNote=self.shopNote.replace("shopFaxNum、","")
                else :
                    continue
        except Exception as e:  # 錯誤訊息
            self.shopNote = "html標籤變更或無標籤:shopCompName、shopPrincipal、shopName、shopAdmin、shopAddress、shopPhoneNum、shopFaxNum、"

    def get_shopProdClass(self):#商品類別
        self.shopProdClass=""
        remove_list=[]
        commodity_data = self.soup.select('ul.b-list-expand-tree li h3.b-list-item a')
        remove_data=self.soup.select('ul.b-list-expand-tree li ul li h3.b-list-item a')

        for cls in remove_data:
            remove_list.append(cls.text)

        try:
            for cls in commodity_data:
                if cls.text not in remove_list:
                    self.shopProdClass+=cls.text+"|"
                else:
                    continue
            self.shopProdClass=self.shopProdClass.strip('|')
        except Exception as e:  # 錯誤訊息
            self.shopProdClass=np.NAN
            self.shopNote += "shopProdClass、"

    def get_shopServiceNum(self):#左側服務電話
        self.shopServiceNum=np.NAN
        try:
            self.shopServiceNum=self.soup.find("div",class_="qa-product-shopContact-Number").text
        except :
            self.shopServiceNum=np.NAN
            self.shopNote += "shopServiceNum、"

    def get_shopScore(self):#滿意度評分
        self.shopScore=np.NAN
        try:
            self.shopScore=self.soup.find("span",class_="b-rating-average b-text-def").text
            for word in remove_word:
                self.shopScore = self.shopScore.replace(word, "")
            self.shopScore=float(self.shopScore)
        except :  # 錯誤訊息
            self.shopScore=np.NAN
            self.shopNote += "shopScore、"

    def get_shopScoreAmt(self):#滿意度評分筆數
        self.shopScoreAmt=np.NAN
        try:
            self.shopScoreAmt=self.soup.find("div",class_="b-content shop-review").text.replace(str(self.shopScore),"")
            for word in remove_word:
                self.shopScoreAmt=self.shopScoreAmt.replace(word,"")
            self.shopScoreAmt=int(self.shopScoreAmt)
        except: # 錯誤訊息
            self.shopScoreAmt = np.NAN
            self.shopNote += "shopScoreAmt、"

    def get_shopShipSpeed(self):#出貨速度
        try:
            self.shopShipSpeed=self.soup.select_one("div.shipping-speed__PC").text.replace("\n","")
        except Exception as e:  # 錯誤訊息
            self.shopShipSpeed=np.NAN
            self.shopNote+="shopShipSpeed、"

    def get_shopDistrict(self):#地區
        self.shopDistrict=np.NAN
        try:
            try:
                self.shopDistrict=self.soup.select_one('p.b-caption.qa-product-region').text.replace("地區: ","")
            except:
                self.shopDistrict = self.soup.select_one('p.b-caption.qa-product-country').text.replace("Country Name: ","")
        except Exception as e:  # 錯誤訊息
            self.shopDistrict=np.NAN
            self.shopNote+="shopDistrict、"

    def get_shopTag(self):#其他註記
        try:
            self.shopTag=""
            tag_data=self.soup.select("div.badge-area")
            for tag in tag_data:
                self.shopTag=self.shopTag+tag.text.replace("\n","")+"|"
            self.shopTag=self.shopTag.strip('|')
            if self.shopTag=="":
                self.shopTag=np.NAN
                self.shopNote += "shopTag、"
        except Exception as e:  # 錯誤訊息
            self.shopTag=np.NAN
            self.shopNote+="shopTag、"

    def get_shopPayment(self):#付款方式
        try:
            self.shopPayment=""
            data=self.soup.select('h3.payment-option-name')
            for mode in data:
                self.shopPayment = self.shopPayment + mode.text.replace("\n", "") + "|"#付款方式##付款方式 #付款方式
            self.shopPayment=self.shopPayment.strip('|')
            if self.shopPayment == "":
                self.shopPayment = np.NAN
                self.shopNote += "shopPayment、"
        except Exception as e:  # 錯誤訊息
            self.shopPayment = np.NAN
            self.shopNote += "shopPayment、"

    def get_shopDelivery(self):#配送方式
        try:
            self.shopDelivery=""
            data = self.soup.select('h3.shipping-option-name')
            for mode in data:
                self.shopDelivery = self.shopDelivery + mode.text.replace("\n", "") + "|"
            self.shopDelivery=self.shopDelivery.strip('|')
            if self.shopDelivery=="":
                self.shopDelivery = np.NAN
                self.shopNote += "shopDelivery、"
        except Exception as e:  # 錯誤訊息
            self.shopDelivery = np.NAN
            self.shopNote+="shopDelivery、"

    def get_data(self,):
        if self.shopNote=="html標籤變更或無標籤:":
            self.shopNote=np.NAN
        else :
            self.shopNote=self.shopNote.strip("、")
        if self.shopCrawResult=="成功":
            data = {
                'shopUrl': self.shopUrl,                #商店首頁網址
                'shopInfoUrl': self.shopUrl+"/info",    #商店資訊網址
                'shopProfile': self.shopProfile,        #商店簡介文字
                'shopId': self.shopId,                  #商店ID
                'shopCompName': self.shopCompName,      #公司名稱
                'shopPrincipal': self.shopPrincipal,    #商業負責人
                'shopName':self.shopName,               #商店名稱
                'shopAdmin': self.shopAdmin,            #店家管理員
                'shopPhoneNum': self.shopPhoneNum,      #商店電話號碼
                'shopFaxNum': self.shopFaxNum,          #商店傳真號碼
                'shopServiceNum':self.shopServiceNum,   #服務電話
                'shopAddress': self.shopAddress,        #商店地址
                'shopScore': self.shopScore,            #滿意度
                'shopScoreAmt': self.shopScoreAmt,      #滿意度評分筆數
                'shopShipSpeed': self.shopShipSpeed,    #出貨速度
                'shopPayment': self.shopPayment,        #付款方式
                'shopDelivery': self.shopDelivery,      #配送方式
                'shopProdClass': self.shopProdClass,    #商品類別
                'shopDistrict': self.shopDistrict,      #地區
                'shopTag': self.shopTag,                #其他註記
                'shopCrawResult':self.shopCrawResult,   #網站爬取結果
                'shopInsertTime': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),#存入時間
                'shopNote':self.shopNote,               #備註
                }
        else:
            data = {
                'shopUrl': self.shopUrl,
                'shopInfoUrl': self.shopUrl + "/info",
                'shopProfile': np.NAN,
                'shopId': self.shopId,
                'shopCompName': np.NAN,
                'shopPrincipal': np.NAN,
                'shopName': np.NAN,
                'shopAdmin': np.NAN,
                'shopPhoneNum': np.NAN,
                'shopFaxNum': np.NAN,
                'shopServiceNum': np.NAN,
                'shopAddress': np.NAN,
                'shopScore': np.NAN,
                'shopScoreAmt': np.NAN,
                'shopShipSpeed': np.NAN,
                'shopPayment': np.NAN,
                'shopDelivery': np.NAN,
                'shopProdClass': np.NAN,
                'shopDistrict': np.NAN,
                'shopTag': np.NAN,
                'shopCrawResult': self.shopCrawResult,
                'shopInsertTime': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                'shopNote': self.shopNote,
            }
        return(data)


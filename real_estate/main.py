import webbrowser
import os
from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
from city import data
from town import T_data
from community import proc_same_community_data
city = (input("請輸入縣市"))
town = (input("請輸入區域"))
starty =input("請輸入起始年分")
startm = input("請輸入起始月份")
endy = input("請輸入結束年份")
endm = input("請輸入結束月份")
url='http://127.0.0.1:5000/?city={}&town={}&starty={}&startm={}&endy={}&endm={}'.format(data[city], T_data[data[city]][town], starty, startm, endy, endm)
proc_data_list=[]
proc_data_list2=[]
community_list=[]
def proc_data(data):
    if proc_data_list==[]:
        for i in data :
            proc_data={
                '門牌':i['a'],
                '社區簡稱':i['bn'],
                '總價(萬元)':i['tp'],
                '交易日期': i['e'],
                '單價(萬元/坪)': i['p'],
                '總面積': i['s'],
                '主建物佔比(%)': i['bs'],
                '型態': i['b'],
                '屋齡': i['g'],
                '樓別/樓高': i['f'],
                }
            proc_data_list.append(proc_data)
            if i['bn'] !='' and i['bn'] not in community_list:
                community_list.append(i['bn'])
        community_data=(proc_same_community_data(community_list,city,town))
    else :
        for i in data :
            if i['bn'] in community_list:
                proc_data={
                    '門牌':i['a'],
                    '社區簡稱':i['bn'],
                    '總價(萬元)':i['tp'],
                    '交易日期': i['e'],
                    '單價(萬元/坪)': i['p'],
                    '總面積': i['s'],
                    '主建物佔比(%)': i['bs'],
                    '型態': i['b'],
                    '屋齡': i['g'],
                    '樓別/樓高': i['f'],
                    }
                proc_data_list2.append(proc_data)
        os.system('taskkill /F /IM chrome.exe')
        save_data()

def save_data():
    path = os.path.join(os.getcwd(), "{}{}_{}年{}月_{}年{}月.xlsx".format(city,town,starty,startm,endy,endm))  # 設定路徑及檔名
    writer = pd.ExcelWriter(path, engine='xlsxwriter',)
    pd.DataFrame(proc_data_list).to_excel(writer, sheet_name='查詢結果',index=False)
    data2=pd.DataFrame(proc_data_list2).sort_values('社區簡稱')
    data2.to_excel(writer,sheet_name="相同社區案例",index=False)
    writer.save()  # 存檔生成excel檔案
    print("執行成功，存檔名稱為：" + "{}{}_{}年{}月_{}年{}月.xlsx".format(city, town, starty, startm, endy,endm))

def open():
    webbrowser.open_new(url)


app = Flask(__name__, static_url_path='/static', template_folder='.',static_folder='static')

@app.route('/')
def index():
    return render_template("query_price.html")

@app.route('/SERVICE/QueryPrice/<param>')
def getParam(param):
    q = request.args.get('q')
    url='https://lvr.land.moi.gov.tw/SERVICE/QueryPrice/{}?q={}'.format(param, q)
    res = requests.get(url)
    proc_data(res.json())
    return jsonify({'name':param})

if __name__ == '__main__':
    app.run(open())
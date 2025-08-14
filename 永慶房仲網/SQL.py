import pymssql
from datetime import datetime

# 連線資訊設定
server ='server'  #server
database = 'database'  # #資料庫
username = 'username'  # 用戶名
password = 'password'  # 密碼

# conn = pymssql.connect(server=server, user=username, password=password, database=database)

def insert_house_data(data):
    # 新增資料至SQL
    set_clause = ", ".join([f"{key}" for key in data.keys()]) 
    set_clause2 = ", ".join([f"%s" for key in data.keys()])
    sql = f"""
    INSERT INTO Tmp (
        {set_clause}
    ) VALUES (
        {set_clause2}
    )
    """
    # 轉換日期格式
    def format_date(date_str):
        try:
            return datetime.strptime(date_str, '%Y%m%d_%H%M').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None
        
    data["CreateDateTime"] = format_date(data["CreateDateTime"])
    data["RefreshDateTime"] = format_date(data["RefreshDateTime"])
    data["LastRefreshDetail"] = format_date(data["DownDate"])

    data["Parking"] = 1 if data["Parking"] else 0
    data["Process"] = 1 if data["Process"] else 0
    values = [data[key] for key in data.keys()]
    # 執行
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql, values)
            conn.commit()
            
        except Exception as e:
            print(f"發生錯誤: {e}")
            conn.rollback()
    
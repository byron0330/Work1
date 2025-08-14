import pymssql
from datetime import datetime

# 连接到 SQL Server
server ='server'  #server
database = 'database'  # #資料庫
username = 'username'  # 用戶名
password = 'password'  # 密碼

# conn = pymssql.connect(server=server, user=username, password=password, database=database)

def insert_house_data(data):
    # SQL 插入语句，使用 %s 占位符（参数化查询）
    set_clause = ", ".join([f"{key}" for key in data.keys()]) 
    set_clause2 = ", ".join([f"%s" for key in data.keys()])
    sql = f"""
    INSERT INTO Tmp (
        {set_clause}
    ) VALUES (
        {set_clause2}
    )
    """
    # 确保日期格式正确
    def format_date(date_str):
        try:
            return datetime.strptime(date_str, '%Y%m%d_%H%M').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None  # 返回 None 表示日期格式错误
    # 转换日期格式
    data["CreateDateTime"] = format_date(data["CreateDateTime"])
    data["RefreshDateTime"] = format_date(data["RefreshDateTime"])
    data["LastRefreshDetail"] = format_date(data["DownDate"])

    # 转换布尔值为 SQL Server 的 BIT 类型
    data["Parking"] = 1 if data["Parking"] else 0
    data["Process"] = 1 if data["Process"] else 0
    values = [data[key] for key in data.keys()]
    # 执行插入操作
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql, values)
            conn.commit()
            
        except Exception as e:
            print(f"發生錯誤: {e}")
            conn.rollback()
    # print("Data inserted successfully!")
    
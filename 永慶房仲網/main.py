from datetime import datetime
from bs4 import BeautifulSoup
from organize_data_SQL import organize
import requests, time, json, schedule
import city
import helper
import logging

# === Logger 基本設定 ===
logger = logging.getLogger("crawler")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")

# 輸出到螢幕
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


file_handler = logging.FileHandler("crawler.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# ======================



def crawler(county, area):
    page = 1
    reconnect_count = 1
    save_data_count = 0
    totalCount, totalPage = helper.get_TotalPage(county, area)
    logger.info(f"{county}-{area}: 共有 {totalPage} 頁，{totalCount} 筆資料")
    a = organize(county)
    while page <= totalPage:
        logger.info(f"第 {page} 頁")
        house_list = helper.get_data(county, area, page)
        for house in house_list:
            save_data_count += a.organize_data(house, area)
            time.sleep(1)
        if reconnect_count == 4:
            helper.set_headers()
            helper.reconnect()
            reconnect_count = 0
        page += 1
        reconnect_count += 1
        time.sleep(2)
        logger.info("================")
    return save_data_count

def start():
    for i in city.area:
        # helper.reconnect()
        county = i[0:3]
        area = i.replace(county, "")
        save_data_count = crawler(county, area)
        logger.info(f"{county}-{area} 已成功爬取 {save_data_count} 筆資料")
        time.sleep(10)

if __name__ == "__main__":
    # 每 6 小時執行一次
    schedule.every(6).hours.do(start)

    logger.info("排程已啟動，每 6 小時執行一次爬蟲任務")
    start()
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            logger.exception(f"排程執行時發生未預期錯誤：{e}")
        finally:
            time.sleep(1)

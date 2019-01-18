import os
import time
from mdb_helper import Mdb_helper
import spider_base as Spi_base
from urls import urls

# 全局参数
# urls

def _main():
    mhelper = Mdb_helper()

    for url in urls:
        # 获取页面html
        soup = Spi_base.get_page(url)
        items = soup.find_all("div", class_="item")

        for item in items:
            time.sleep(2)
            try:
                time_now = time.strftime("%F %R")
                # 获取code
                car_code = item.find_all("date")[0].text

                #print(car_code + " begin ...")
                Spi_base.write_log("\n[" + time_now + "] >> " + car_code + " begin ...")
                
                # 根据code判断是否已经存储过
                num = mhelper.doc_query_count({"code": car_code}, "cars")
                if num < 1:
                    # 获取其他数据
                    car_url = item.a.get("href")
                    car_title = item.img.get("title")
                    car_date = item.find_all("date")[1].text

                    Spi_base.write_log("... save documents ...")

                    # 将数据写入
                    msql = {"code": car_code, "title": car_title, "url": car_url,
                            "pub_date": car_date, "ext_date": time_now}
                    mhelper.doc_insert(msql, "cars")

                    # 获取详细页面
                    car_detail = Spi_base.get_page(car_url)
                    # 获取图片
                    detail_container = car_detail.find(
                        "div", class_="container")

                    cover_img = detail_container.find(
                        "a", class_="bigImage").get("href")
                    sample = detail_container.find(
                        "div", id="sample-waterfall")

                    # 确保文件夹存在
                    path = "./transparent/" + car_code + "-" + car_title + "/"
                    if not os.path.exists(path):
                        os.makedirs(path)

                    # 判断如果没有sample-waterfall
                    if(sample):
                        a_sample = detail_container.find(
                            "div", id="sample-waterfall").find_all("a")
                        sample_img = [a.get("href") for a in a_sample]
                        Spi_base.write_log(
                            "... save pics p[" + str(len(sample_img))+"] ...")

                        # 存储sample文件
                        i = 1
                        for s_img in sample_img:
                            Spi_base.down_file(s_img, path + car_code + "-" + str(i))
                            i += 1
                    else:
                        Spi_base.write_log("... save pics one ...")

                    # 存储cover文件
                    Spi_base.down_file(cover_img, path + car_code + "-cover")

                    # TODO: 获取视频、其他数据
                    # magnet:?xt=urn:btih:5A7B3C6694D079727FC506A8249E9D984DCACA7B&dn=%5B88q.me%5Dhunta-536
                # 如果有已经了,则停止
                else:
                    Spi_base.write_log("...this url stopped")
                    break
                Spi_base.write_log("... done")
            except Exception as e:
                Spi_base.write_log("Error: " + str(e))

# while True:
#     time_now = time.strftime("%H")
#     if(time_now == "16"):
#         _main()    
#     time.sleep(3600)

_main()

#>> sc create SeedSpider binPath= "C:\Users\dell\AppData\Local\Programs\Python\Python37\Python.exe --E:\Personal\seed-spider\seed_spider.py"
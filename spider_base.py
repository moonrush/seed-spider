# 获取页面的BeautifulSoup，即格式化的页面html
def get_page(url):
    import requests
    from bs4 import BeautifulSoup

    res = requests.get(url)
    soup = BeautifulSoup(res.text,features="html.parser")

    return soup

# 转存文件
def down_file(url, path):
    import os
    from urllib import request

    # 获取url的文件名及扩展名
    # filename = os.path.basename(url)
    extraname = os.path.splitext(url)[1]

    save_path = path + extraname
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; X64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}
    try:
        req = request.Request(url, headers=headers)
        data = request.urlopen(req).read()
        with open(save_path, 'wb') as f:
            f.write(data)
            f.close()
    except Exception as e:
        print(str(e))

# 写log文件
def write_log(text, path = "./log.txt"):
    import os
    with open(path, 'a') as f:
        f.write(text)
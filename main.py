from utils import bilibili_100,bili_views,bili_views2,set_cookies
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os

if __name__=="__main__":

    #config
    # 基本配置
    USER_AGENT = [
        'Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.229 Version/11.62',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.9.168 Version/11.52',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.51 Safari/537.36 Edg/90.0.818.27'
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
    ]

    chrome_options=Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-javascript")
    #chrome_options.add_argument('--disable-setuid-sandbox')
    #chrome_options.add_argument('--single-process')
    chrome_options.add_argument('start-maximized')
    #chrome_options.add_argument('--window-size=1960,1080')
    chrome_options.add_argument('--user-agent={}'.format(USER_AGENT[2]))
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--disable-3d-apis")

    danmaku = False
    PC = 'ywicc'

    result_path = {'hdu':'D:\\result','ywicc':'E:\\result'}
    tshark = {'hdu':['C:\\Program Files\\Wireshark\\tshark.exe','4'],'ywicc':['D:\\Programs\Wireshark\\tshark.exe','8']}
    
    #if os.path.exists(result_path):
     #   print('result folder exists')
        #sys.exit()
    root_path = os.getcwd()
    if not os.path.exists('top100.csv'):
        videos_list = pd.DataFrame(columns=['id','title','play_time','danmaku','proxy','tshark_state','url'])
        videos_list = bilibili_100()
    else:
        videos_list = pd.read_csv('top100.csv')
    #videos_info.to_excel()
    cookies_path = os.path.join(result_path[PC],'bilibili_cookie.json')
    if not os.path.exists(cookies_path):
        set_cookies(cookies_path)

    for j in range(1,50,1):
        work_date = time.strftime("%Y-%m-%d", time.localtime())
        work_date = work_date + str(j)
        pcap_path = os.path.join(result_path[PC],work_date)

        for i in range(0,100,1):
            bili_views(i,180,videos_list=videos_list,result_path=pcap_path,cookies_path=cookies_path,chrome_options=chrome_options,tshark=tshark[PC])  #超过900秒的视频就跳过
        print(videos_list.head(10))
    #videos_info.to_csv('top100_{}.csv'.format(work_date),encoding="utf_8-sig",index=False)
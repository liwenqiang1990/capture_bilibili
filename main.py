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
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--no-gpu')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--single-process')
    #chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('--window-size=1960,1080')
    chrome_options.add_argument('--user-agent={}'.format(USER_AGENT[2]))

    danmaku = False

    #if os.path.exists(result_path):
     #   print('result folder exists')
        #sys.exit()
    root_path = os.getcwd()
    if not os.path.exists('top100.csv'):
        videos_info = pd.DataFrame(columns=['id','title','play_time','danmaku','proxy','tshark_state','url'])
        bilibili_100()
    else:
        videos_info = pd.read_csv('top100.csv')
    #videos_info.to_excel()

    for j in range(26,50,1):
        work_date = time.strftime("%Y-%m-%d", time.localtime())
        work_date = work_date + str(j)
        result_path = os.path.join('D:\\result',work_date)

        for i in range(0,20,1):
            bil_views(i,181)  #超过900秒的视频就跳过
        print(videos_info.head(10
                           ))
    #videos_info.to_csv('top100_{}.csv'.format(work_date),encoding="utf_8-sig",index=False)
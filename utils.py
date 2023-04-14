from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import subprocess
import pandas as pd
import sys
from selenium.common.exceptions import TimeoutException

def parse_time(time_str):
    time_array = time_str.split(':')
    return (int(time_array[0])*60+int(time_array[1]))


def bilibili_100():
    browser = webdriver.Chrome()

    browser.get('https://www.bilibili.com/v/popular/rank/all')
    handle = browser.current_window_handle
    item = browser.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/ul/li')
    
    videos_list = pd.DataFrame(data=None,columns=
                              ['id','title','play_time','danmaku','proxy','tshark_state','url'])
    
    #videos_list['id'] = item_list
    i = 0
    for e in item:
        link = e.find_element_by_tag_name('a')
        url = link.get_attribute('href')
        videos_list.loc[i]['url'] = url
        try:
            link.click()
        except:
            print("can't open new window")
        handles = browser.window_handles
        for newhandle in handles:
            if newhandle!=handle:
                browser.switch_to.window(newhandle)
                try:
                    play_time = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="bilibiliPlayer"]/div[1]/div[1]/div[11]/div[2]/div[2]/div[1]/div[2]/div/span[3]'))
                    )
                    videos_list.loc[i]['play_time'] = play_time.text
                    title = browser.find_element_by_xpath('//*[@id="viewbox_report"]/h1')
                    videos_list.loc[i]['title'] = title.text
                except:
                    print("can't find play_time!")
                finally:
                    browser.close()
        browser.switch_to.window(handle)
        i=i+1
        if i == 10:
            time.sleep(10)
    browser.close()
    browser.quit()
    videos_list['id'] = videos_list['url'].str[-12:]
    videos_list.to_csv('top100.csv',encoding="utf_8-sig",index=False)
    return videos_list

def auto_tshark(work_path,id,t,tshark):
    duration='duration:'+str(t)
    pcap_name = os.path.join(work_path,id+'.pcap')
    option = [tshark[0],'-i',tshark[1],'-a',duration,'-F','pcap','-w',pcap_name]
    print(option)
    p = subprocess.Popen(option,stdout=subprocess.PIPE,stderr = subprocess.PIPE)
    return p

def bili_views(i,threshold,videos_list,result_path,chrome_options,tshark):
    av = videos_list.loc[i]['id']
    t = parse_time(videos_list.loc[i]['play_time'])+5 #多抓10秒包
    if t>(threshold+10):
        return
    t = 60
    work_path = os.path.join(result_path,str(i)+'_'+av)
    if not os.path.exists(work_path):
        os.makedirs(work_path)

    browser = webdriver.Chrome(options=chrome_options)

    # 访问网页
    url = videos_list.loc[i,'url']
    start_time = time.time()
    p = auto_tshark(work_path,av,t+5,tshark)
    print(url)
    browser.get(url)
    browser.save_screenshot(os.path.join(work_path,'start.png'))
    # 2倍速播放
    # js_2 = '''document.querySelector('video').playbackRate=2'''
    # browser.execute_script(js_2) # 执行js的方法
    # 播放
    try:
        danmaku_buttom = WebDriverWait(browser, 5).until(
                        EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/input[1]'))
                      )
        danmaku_buttom.click()
    except:
        print('danmaku_button error')

    videos_list.loc[i,'danmaku'] = 'off'
    #try:
    #    next_button = WebDriverWait(browser, 5).until(
    #                     EC.presence_of_element_located((By.XPATH,'/html[1]/body[1]/div[2]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[10]/div[2]/div[2]/div[1]/div[1]/div[1]/span[1]'))
    #    )
    #    next_button.click()
    #    print('播放方式1')
    #except TimeoutException:
    #    print("连播错误1")

    play_time = time.time()

    print('第{}个视频播放成功,准备时间{}'.format(i,play_time-start_time))
    p.communicate()
    #获取进度条//
    current_time = browser.find_element_by_xpath('//*[@id="bilibili-player"]/div/div/div[1]/div[1]/div[10]/div[2]/div[2]/div[1]/div[2]/div/span[1]')
    current_time = current_time.text
    print(f'current_time:{current_time}')  #transform: scaleX(1);表示播放完毕
    browser.save_screenshot(os.path.join(work_path,'end.png'))
    end_time = time.time()
    #return code为0表示正常tshark运行正常结束
    tshark_state = 'return code{},tshark_time{},work_time{},{}\n'.format(p.returncode,t,end_time-start_time,current_time)
    print(tshark_state)
    videos_list.loc[i,'tshark_state']=tshark_state
    browser.close() # 关闭当前页面
    browser.quit() # 关闭浏览器
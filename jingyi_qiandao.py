# -*- coding: utf-8 -*
'''
new Env('精易签到');
'''

import os
import requests
import datetime
from notify import send  # 导入青龙消息通知模块

#签到
def jingyi_checkin():

    #读取环境变量里面的COOKIES
    Formhash_Cookie=os.environ['JY_COOKIE']
    if '@' in Formhash_Cookie:
        #COOKIES格式正确
        Formhash_Cookie1=Formhash_Cookie.split('@')
        FormhashJYs = Formhash_Cookie1[0]
        CookieJYs = Formhash_Cookie1[1]

    else:
        #COOKIES格式错误
        condition = "error"
        allMessage="💔Cookie环境变量格式不对! 如：Formhash@Cookie"
        send('精易签到', allMessage + '\n\n本通知 By HY-jingyi\n通知时间:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),condition)
        

    url = "https://bbs.125.la/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1"
    post_data='formhash='+FormhashJYs+'&submit=1&targerurl=&todaysay=&qdxq=kx'

    #print(html_code)
    attempts = 0
    success = False
    #循环执行5次，我这前2次都会提示ancc_tokenV2，所以加了个循环
    while attempts < 5 and not success:

        print('签到执行第'+str(attempts+1)+'次')

        try:

            headers = {
                'Accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.192.400 QQBrowser/11.5.5250.400',
                'Referer': 'https://bbs.125.la/plugin.php?id=dsu_paulsign:sign',
                'Cookie': CookieJYs,
            }


            html_code = requests.post(url, post_data, headers=headers)

            print(html_code.text)


            if 'status' in html_code.text:

                html_code =html_code.json()

                #print(html_code['status'])

                success = True

                if html_code['status'] == '1':
                    # 签到成功
                    condition='correct'
                    allMessage = "🌷签到成功\n积累签到次数:" + html_code['data']['days'] + "\n" + "本月签到次数:" + html_code['data']['mdays'] + "\n" + "当前总有奖励:" + html_code['data']['reward'] + "\n" + "上一次签到是:" + html_code['data']['qtime']
                    send('精易签到', allMessage + '\n\n本通知 By HY-jingyi\n通知时间:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),condition)
                else:
                    # 签到失败
                    condition = "error"
                    allMessage =html_code['msg']
                    send('精易签到', allMessage + '\n\n本通知 By HY-jingyi\n通知时间:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),condition)
                    
                break

            else:

                if 'ancc_tokenV2' in html_code.text:
                    Cookie1=html_code.text.split("__ancc_tokenV2' + '=' + '")
                    Cookie2=Cookie1[1].split(";")
                    CookieJYs +='; __ancc_tokenV2='+Cookie2[0]
                attempts += 1
                if attempts == 5:
                    # 签到错误
                    condition = "error"
                    allMessage = "💔签到未知错误2："+ str(e)
                    send('精易签到', allMessage + '\n\n本通知 By HY-jingyi\n通知时间:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),condition)
                    break
                    


        except Exception as e:
            attempts += 1
            if attempts == 5:
                # 签到错误
                condition = "error"
                allMessage = "💔签到未知错误："+ str(e)
                send('精易签到', allMessage + '\n\n本通知 By HY-jingyi\n通知时间:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),condition)
                break

if __name__ == "__main__":

    jingyi_checkin()

import requests, json, time
import re

# 获得b站直播弹幕数据 最新的5条
# 检测关键词
# 自动发送弹幕



target = [] #缓存弹幕用的列表

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Cookie': "buvid4=94F2D686-C139-3174-2566-45F6750F319E79400-024041009-v39mg1nbJFInxrB205ZuEw%3D%3D; _uuid=7BD106422-C10B2-C8C7-7F210-439F4F5D8810985114infoc; iflogin_when_web_push=0; nostalgia_conf=2; enable_web_push=DISABLE; i-wanna-go-back=1; rpdid=|(u)Yukm~m~R0J'u~uk~RJuRk; CURRENT_QUALITY=120; LIVE_BUVID=AUTO3017127553553286; buvid_fp_plain=undefined; hit-dyn-v2=1; DedeUserID=12686542; DedeUserID__ckMd5=25df501ad50132e4; FEED_LIVE_VERSION=V_HEADER_LIVE_NEW_POP; CURRENT_BLACKGAP=0; buvid3=1B50AF35-C611-547C-22F4-549B88A769AF98504infoc; b_nut=1713345096; header_theme_version=CLOSE; bp_article_offset_12686542=921708580260806680; fingerprint=3f5e199e06c2107dc361960cb5aab523; CURRENT_FNVAL=4048; bp_video_offset_12686542=925422000413868105; SESSDATA=961ef613%2C1730105195%2Cdd6d9%2A51CjAMNUS769AAKgfoCa_AFir5bolYKVdxeoyGBEB6QdB0d6i3Gy6bbacwRrpII7yLDr4SVlNSOGU2TnBDdF83c3h4azdWTkhTTFJzNU1BbElrNWt3VEE1M2RNUlZRQVZIVXBzTmtUdHlETEpTcTJYNnhiejNQd0JsaWkxZE9DMnZBVGR1NzRTU2xBIIEC; bili_jct=bfecb7122afbaa70259e8b8623c23226; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTQ4Mjg3MDUsImlhdCI6MTcxNDU2OTQ0NSwicGx0IjotMX0.nfvxQi6BGcKjqLGM85QnFL2zk0QGKiYY1MRAxxw0i4c; bili_ticket_expires=1714828645; home_feed_column=5; buvid_fp=3f5e199e06c2107dc361960cb5aab523; b_lsid=D67B262F_18F3F8656B6; sid=8u9mgllu; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1714569508,1714655618,1714737264,1714757820; browser_resolution=1707-853; bsource=search_baidu; bp_t_offset_12686542=927368879008645124; PVID=15; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1714762622",
    'Origin': 'https://live.bilibili.com'
}

key = ['啥游戏', '什么游戏', '游戏名','1']    #关键词 列表
Cache_len = 5    # 缓存最新的 5条弹幕
cache_uid = []  # 缓存触发关键词弹幕的id 为了不重复发送弹幕
Danmu = '签到'  # 要发送的弹幕
Roomid = 4443409     #直播间

def getHistory(roomid):
    # 得到最新的一条弹幕
    url_hisapi = f'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid={roomid}&room_type=0'

    response = json.loads(requests.get(url=url_hisapi, headers=headers).text)
    response = response['data']['room']     #所有的 用户的 弹幕列表
    response = response['data']['admin']    #房管的 弹幕列表
    lastest_5 = response[-Cache_len:]
    #text = response[len(response) - 1]['text']  # 最后一条弹幕的内容

    return lastest_5


def sendDanmu(text,roomid): # 发送弹幕
    url = 'https://api.live.bilibili.com/msg/send'

    ti = int(time.time())  # 当前时间
    roomid = '{}'.format(roomid)  # 直播间id

    data = {
        'bubble': '0',
        'msg': text,                                        # 发送内容
        'color': '5816798',
        'mode': '1',
        'room_type': '0',
        'jumpfrom': '0',
        'reply_mid': '0',
        'reply_attr': '0',
        'replay_dmid': '',
        'statistics': {"appId": 100, "platform": 5},        #你的浏览器的 statistics
        'fontsize': '25',
        'rnd': '{}'.format(ti),                             # 发送时间
        'roomid': roomid,                                   # 直播id
        'csrf': 'bfecb7122afbaa70259e8b8623c23226',         #你的浏览器的 csrf
        'csrf_token': 'bfecb7122afbaa70259e8b8623c23226'    ##你的浏览器的 csrf_token
    }
    print(requests.post(url=url, headers=headers, data=data))



def matche_Keywords(text, key): #匹配关键词
    if re.findall(r'\b(' + '|'.join(key) + r')\b', text):
        return True
    else:
        return False



while True:
    lastest = getHistory(roomid=Roomid) #最新的弹幕

    for i in lastest:
        if i not in target:       # 避免重复弹幕 仅做内容判断
            if len(target) > 4:  # 保持存储弹幕列表的长度 少于5条
                del target[0]   # 删除第一个元素
            print(i['text'],len(target))                #debug
            target.append(i)  # 说明是最新的弹幕 存到列表
            # 进行正则判断是否是关键词
            if matche_Keywords(text=i['text'], key=key) and Danmu != '':  # 如果匹配到关键词
                if i['uid'] not in cache_uid:   #记录每个提问人的id，不重复回答 同一人的问题
                    sendDanmu(text=Danmu, roomid=Roomid)
                    cache_uid.append(i['uid'])
    time.sleep(1)

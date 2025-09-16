import hashlib
import json
import re
import time

import requests

secret = 'NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt'

song_url = 'https://wwwapi.kugou.com/play/songinfo'

def params_sign(params):
    p = secret
    for key, value in params.items():
        p += str.format(key + '=' + value)
    p += secret
    return p

headers = {
    'cookie':'kg_mid=a1aa86537909eeb9e53c5b118b9a4eb7; kg_dfid=3Mq3IA2bsFak3vlLBn2QJOBu; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1756095053,1756648890; HMACCOUNT=53A4FC87CF7B571C; kg_mid_temp=a1aa86537909eeb9e53c5b118b9a4eb7; KuGoo=KugooID=594878988&KugooPwd=F54682185DEDB20EC6FC9D265AEDC290&NickName=%u8bd7%u7dd4%u30b8%u2606%u0051%u0049%u54e5&Pic=http://imge.kugou.com/kugouicon/165/20100101/20100101192931478054.jpg&RegState=1&RegFrom=&t=8dc853b798535a3f87cd8c3b5fd2852d0441a9e47f5863152e63d02df1b02ac6&a_id=1014&ct=1756648908&UserName=%u006b%u0067%u006f%u0070%u0065%u006e%u0035%u0039%u0034%u0038%u0037%u0038%u0039%u0038%u0038&t1=; KugooID=594878988; t=8dc853b798535a3f87cd8c3b5fd2852d0441a9e47f5863152e63d02df1b02ac6; a_id=1014; UserName=kgopen594878988; mid=a1aa86537909eeb9e53c5b118b9a4eb7; dfid=3Mq3IA2bsFak3vlLBn2QJOBu; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1756649206',
    'referer': 'https://www.kugou.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
}
def getSongById(idlist):
    data = []
    for id in idlist:
        params = {
            'appid': '1014',
            'clienttime': round(time.time()*1000).__str__(),# Math.round((new Date).getTime() / 1e3)
            'clientver': '20000',
            'dfid': '0RAlwo34Xjlq1NwN9D094GgB',
            'encode_album_audio_id': id,
            'mid': '037d535e69fb5f3211a7e937b1bae005',
            'platid': '4',
            'srcappid': '2919',
            'token': '8dc853b798535a3f87cd8c3b5fd2852dcd00fcdd0ac002d54c8cb6c6ee99c927',
            'userid': '594878988',
            'uuid': '037d535e69fb5f3211a7e937b1bae005'
        }
        # 拼接参数
        p = secret
        for key, value in params.items():
            p += str.format(key + '=' + value)
        p += secret
        # 计算签名
        params['signature'] = hashlib.md5(p.encode()).hexdigest()
        song_res = requests.get(song_url, params=params, headers=headers)
        result = song_res.json()
        data.append(result['data'])
        print(result['data']['audio_name'],result['data']['author_name'],result['data']['play_backup_url'])
    return data

def search(keyword,page=1):
    # rank_url = 'https://www.kugou.com/yy/rank/home/1-33163.html?from=rank'
    # response = requests.get(rank_url, headers=headers)
    # data_id_pat = re.compile('data-eid="(.*?)">', re.I | re.M)
    # ids = re.findall(data_id_pat, response.text)
    search_url = 'https://complexsearch.kugou.com/v2/search/song'
    search_param = {
      "appid": "1014",
      "bitrate": "0",
      "callback": "callback123",
      "clienttime": round(time.time()*1000).__str__(),
      "clientver": "1000",
      "dfid": "0RAlwo34Xjlq1NwN9D094GgB",
      "filter": "5",
      "inputtype": "0",
      "iscorrection": "1",
      "isfuzzy": "0",
      "keyword": keyword,
      "mid": "037d535e69fb5f3211a7e937b1bae005",
      "page": page.__str__(),
      "pagesize": "10",
      "platform": "WebFilter",
      "privilege_filter": "0",
      "srcappid": "2919",
      "token": "8dc853b798535a3f87cd8c3b5fd2852dca1e58e66ca140fac30a017e9188622c",
      "userid": "594878988",
      "uuid": "037d535e69fb5f3211a7e937b1bae005"
    }
    signature = params_sign(search_param)
    search_param['signature'] = hashlib.md5(signature.encode()).hexdigest()
    song_res = requests.get(search_url, params=search_param, headers=headers)
    pat = re.compile(',"EMixSongID":"(.*?)",',re.I|re.M)
    total_pat = re.compile(',"total":(.*?),')
    total = int(re.findall(total_pat, song_res.text)[0])
    song_ids = re.findall(pat, song_res.text)
    res = {
        'total': total,
        'data': getSongById(song_ids)
    }
    return res
    # jsonp = song_res.text
    # # 提取 JSON 部分
    # start = jsonp.find('(') + 1
    # end = jsonp.rfind(')')
    # json_str = jsonp[start:end]
    # # 解析为 Python 字典
    # data = json.loads(json_str)
    # print(data)
if __name__ == '__main__':
    data = search('毛不易')
    print(data)

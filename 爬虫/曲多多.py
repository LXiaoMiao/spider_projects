import requests
import json
from pydub import AudioSegment

search_url = 'https://agm-api.hifiveai.com/search'
# 由于post参数为request payload
headers = {
    'content-type': 'application/json;charset=UTF-8'  # 必须添加content-type
}

# 爬取pages页 content类型 歌曲
content = '悲伤'
pages = 250
for page in range(pages):
    data = {
        'content': content,
        'page': str(page),
        'size': '10'
    }
    # 获取音乐id及name
    search_json = requests.post(search_url, data=json.dumps(data), headers=headers)  # data形式必须为json
    search_list = json.loads(search_json.text)
    for i in range(10):
        music_name = search_list['data']['list'][i]['name']
        wave_path = music_id = search_list['data']['list'][i]['wavePath']
        mixed_url = wave_path.replace('wave', 'mixed').replace('json', 'mp3')

        # 爬取音乐内容并保存
        music = requests.get(mixed_url).content
        try:
            file_name = r'{}.mp3'.format(music_name)
            with open(file_name, 'wb') as f:
                f.write(music)

            # 取前15秒
            song = AudioSegment.from_mp3(file_name)
            song = song[:15000]
            song.export(file_name)
            print(music_name, mixed_url)
        except:
            print(music_name, '文件名异常！')
    print("第 {} 页 爬取&解析 完成".format(page))



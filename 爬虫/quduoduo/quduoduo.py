import os
import json
import logging
from pathlib import Path
from typing import List, Iterable
from collections import namedtuple

import requests
from requests import Response
from pydub import AudioSegment


logging.basicConfig(level=logging.INFO)
MusicInfo = namedtuple('MusicInfo', [
    'music_name',
    'music_content'
])
Tags = {
    '快乐': '442',
    '愉快': '443',
    '兴奋': '444',
    '无忧无虑': '445',
    '悲伤': '449',
    '伤心': '450',
    '孤独': '451',
    '失望': '452',
    '烦躁': '453',
    '性感': '474',
    '亲密': '475',
    '爱': '479'
}


class QuDuoDuo:
    def __init__(self, tag):
        self.search_url = 'https://agm-api.hifiveai.com/search'
        self.headers = {
            'content-type': 'application/json;charset=UTF-8'
        }
        self.mode = Tags[tag]
        self.file_dir: Path = Path('.').joinpath('music')
        self.confirm_file_dir()

    def confirm_file_dir(self):
        if self.file_dir.exists():
            return
        os.mkdir(self.file_dir)

    def req_info(self, page: int = 1, size: int = 10) -> List:
        response: Response = requests.post(self.search_url, headers=self.headers, data=json.dumps({
            'newTags': self.mode,
            'page': page,
            'size': size
        }))
        return response.json().get('data').get('list')

    def crawling(self, page: int = 1):
        song_list: List = self.req_info(page)
        song_info = self.extract(song_list)
        self.save(song_info)
        logging.info(f"QuDuoDuo page {page} is saved")

    def save(self, song_info: Iterable):
        # extract the first 25 seconds of the song and save
        for song in song_info:
            try:
                file_name = f"{song.music_name}.mp3"
                with open(self.file_dir.joinpath(file_name), 'wb') as f:
                    f.write(song.music_content)
            except OSError:
                logging.error(f'{song.music_name} ---- Filename Error')
            else:
                song = AudioSegment.from_mp3(self.file_dir.joinpath(file_name))
                song = song[:15000]
                song.export(self.file_dir.joinpath(file_name))

    @staticmethod
    def extract(songs: List) -> List[MusicInfo]:
        song_result = []
        for song in songs:
            wave_path = song.get('wavePath')
            mixed_url = wave_path.replace('wave', 'mixed').replace('json', 'mp3')
            music_content = requests.get(mixed_url).content

            song_result.append(MusicInfo(
                music_name=song.get('name'),
                music_content=music_content
            ))
        return song_result


if __name__ == '__main__':
    spider = QuDuoDuo('快乐')
    for i in range(1, 2):
        spider.crawling(i)

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
Headers = {
    'content-type': 'application/json;charset=UTF-8'
}
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
    def __init__(self):
        self.search_url = 'https://agm-api.hifiveai.com/search'

    def req(self, mode: str = "快乐", page: int = 1, size: int = 10) -> List:
        response: Response = requests.post(self.search_url, headers=Headers, data=json.dumps({
            'newTags': Tags[mode],
            'page': page,
            'size': size
        }))
        return response.json().get('data', {'list': []}).get('list')

    def crawling(self, mode: str = "快乐", page: int = 1):
        filepath = self.confirm_file_dir(mode)
        song_list: List = self.req(mode, page)
        song_info = self.extract(song_list)
        self.save(song_info, filepath)
        logging.info(f"QuDuoDuo-{mode} page {page} is saved")

    @staticmethod
    def save(song_info: Iterable, filepath: Path):
        # extract the first 15 seconds of the song and save
        for song in song_info:
            try:
                file_name = f"{song.music_name}.mp3"
                with open(filepath.joinpath(file_name), 'wb') as f:
                    f.write(song.music_content)
            except OSError:
                logging.error(f'{song.music_name} ---- Filename Error')
            else:
                song = AudioSegment.from_mp3(filepath.joinpath(file_name))
                song = song[:15000]
                song.export(filepath.joinpath(file_name))

    @staticmethod
    def confirm_file_dir(filename: str) -> Path:
        file_dir: Path = Path('.').joinpath(filename)
        if not file_dir.exists():
            os.mkdir(file_dir)
        return file_dir

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
    spider = QuDuoDuo()
    for i in range(1, 3):
        spider.crawling(mode="快乐", page=i)
    for i in range(1, 3):
        spider.crawling(mode="失望", page=i)

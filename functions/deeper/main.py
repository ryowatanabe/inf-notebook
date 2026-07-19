import requests
import gzip
from sys import argv
from time import sleep
from io import BytesIO
from pickle import dump,HIGHEST_PROTOCOL
from urllib.parse import urljoin
from logging import getLogger

from flask import Flask
from google.cloud import storage

BUCKETNAME = None
FILENAME = None
DEEPER_APIBASEURL = None
DEEPER_APIVERSION = None
DEEPER_APIKEY = None

DIFFICULTIES = {
    'B': 'BEGINNER',
    'N': 'NORMAL',
    'H': 'HYPER',
    'A': 'ANOTHER',
    'L': 'LEGGENDARIA',
}

DEEPER_APIURL = urljoin(DEEPER_APIBASEURL, DEEPER_APIVERSION)

logger = getLogger()

app = Flask(__name__)

@app.route('/')
def http_index(request=None):
    data = generate_data(list(range(1, 12+1)))
    if not data:
        return 'Data generate failed.'
    
    if not upload_file(data):
        return 'Failed upload file.'
    
    return 'Upload successful.'

def upload_file(data: dict) -> bool:
    '''リソースデータとしてGoogle Cloud Storageにアップロードする
    '''
    buffer = BytesIO()
    with gzip.open(buffer, 'wb') as f:
        dump(data, f, protocol=HIGHEST_PROTOCOL)
    buffer.seek(0)

    client = storage.Client()
    if not client:
        return False
    
    bucket = client.bucket(BUCKETNAME)
    if not bucket:
        return False
    
    blob = bucket.blob(FILENAME)
    blob.upload_from_file(buffer, content_type='application/gzip')

    return True

def generate_data(levels:list[int]) -> dict:
    '''APIを呼んでデータを取得する

    取得したlistデータを、曲名と難易度をキーのdictに変換する。
    '''
    data = {}
    for level in levels:
        data_level = api_request('songs', params={'level': str(level)})
        if not data_level:
            return None

        generated_at = data_level['generated_at']
        total_players = int(data_level['total_players'])

        for song in data_level['songs']:
            title = song['title']
            if not title in data.keys():
                data[title] = {}
            
            difficulty = DIFFICULTIES[song['difficulty']]
            play_count = int(song['play_count'])
            data[title][difficulty] = {
                'id': song['id'],
                'generated_at': generated_at,
                'd_star': song['d_star'],
                'notes': song['notes'],
                'played_rate': int((int(song['play_count']) / total_players) * 100),
                'assist_rate': int((int(song['assist_count']) / play_count) * 100),
                'easy_rate': int((int(song['easy_count']) / play_count) * 100),
                'normal_rate': int((int(song['normal_count']) / play_count) * 100),
                'hard_rate': int((int(song['hard_count']) / play_count) * 100),
                'exhard_rate': int((int(song['exhard_count']) / play_count) * 100),
                'fc_rate': int((int(song['fc_count']) / play_count) * 100),
                'max_ex': int(song['max_ex']),
            }
        
        sleep(1.1)

    return data

def api_request(path:str, **kwargs):
    headers = kwargs.pop('headers', {})
    headers['X-DEEPER-API-Key'] = DEEPER_APIKEY
    res = requests.get(urljoin(DEEPER_APIURL, path), headers=headers, **kwargs)

    try:
        res.raise_for_status()
    except requests.HTTPError as ex:
        logger.exception(ex)
        logger.exception(res.json())
        return None

    return res.json()

if __name__ == '__main__':
    debug = '-debug' in argv
    app.run(host='127.0.0.1', port=8000, debug=debug)

from io import BytesIO
from uuid import uuid1
from datetime import datetime,timezone
from logging import getLogger

if __name__ == '__main__':
    logger = getLogger()
else:
    logger = getLogger(__name__)
logger.debug(f'loaded {logger.name}')

from PIL.Image import Image

imagesize = (1280, 720)

def get_imagevalue(image: Image) -> bytes:
    if image is None:
        return None
    
    if image.height == 1080:
        image = image.resize(imagesize)

    bytes = BytesIO()
    image.save(bytes, format='PNG')
    ret = bytes.getvalue()
    bytes.close()

    return ret

def save_imagevalue(data: bytes, filepath: str):
    '''画像データを画像ファイルに保存する
    
    Args:
        data(bytes): 対象のデータ
        filepath(str): 保存先のファイルパス
    '''
    with open(filepath, 'wb') as f:
        f.write(data)

def generate_filename(extension: str):
    '''
    現在の日時と生成したUUIDからファイル名を生成する
    
    Args:
        extension(str): 拡張子
    '''
    return f'{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid1()}.{extension}'

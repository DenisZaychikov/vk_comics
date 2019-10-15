import requests
import json
import random
from dotenv import load_dotenv
import os
import os.path
import tempfile

API_VERSION = '5.101'
IMG_FORMAT = '.jpg'
GROUP_ID = 187184436


def get_current_comic_num():
    url = 'http://xkcd.com/info.0.json'
    res = requests.get(url).json()

    return res['num']


def get_comic_info(random_comic_num):
    url = f'http://xkcd.com/{random_comic_num}/info.0.json'
    res = requests.get(url).json()

    return res['img'], res['title'], res['num'], res['alt']


def get_server_address():
    method = 'photos.getWallUploadServer'
    req_url = f'https://api.vk.com/method/{method}'
    params = {
        'access_token': vk_access_token,
        'v': API_VERSION,
        'group_id': GROUP_ID
    }

    res = requests.get(req_url, params=params).json()

    if 'error' in res:
        raise requests.exceptions.HTTPError(res['error'])

    return res['response']['upload_url'], res['response']['album_id']


def upload_photo_to_server(img_file, upload_url):
    res = requests.post(upload_url, files={'photo': img_file}).json()

    if 'error' in res:
        raise requests.exceptions.HTTPError(res['error'])

    return res['server'], res['photo'], res['hash']


def save_img_on_wall(server, photo, hash):
    method = 'photos.saveWallPhoto'
    req_url = f'https://api.vk.com/method/{method}'
    params = {
        'access_token': vk_access_token,
        'v': API_VERSION,
        'group_id': GROUP_ID,
        'server': server,
        'photo': photo,
        'hash': hash
    }

    res = requests.post(req_url, params=params).json()

    if 'error' in res:
        raise requests.exceptions.HTTPError(res['error'])

    return res['response'][0]['id'], res['response'][0]['owner_id']


def post_img_on_wall(img_comment, media_id, owner_id):
    photo_id = f'photo{owner_id}_{media_id}'
    method = 'wall.post'
    req_url = f'https://api.vk.com/method/{method}'
    params = {
        'access_token': vk_access_token,
        'v': API_VERSION,
        'owner_id': f'-{GROUP_ID}',
        'attachments': photo_id,
        'message': img_comment
    }

    res = requests.post(req_url, params=params)
    if not res.ok:
        raise requests.exceptions.HTTPError(f'status code: {res.status_code}')


if __name__ == '__main__':
    load_dotenv()
    vk_access_token = os.getenv("VK_TOKEN")
    current_comic_num = get_current_comic_num()
    random_comic_num = random.randint(1, current_comic_num)
    img_link, img_title, img_num, img_comment = get_comic_info(random_comic_num)
    upload_url, album_id = get_server_address()

    file_name = 'image.jpg'

    with tempfile.TemporaryDirectory(dir=os.getcwd()) as temp_dir:
        file_path = os.path.join(temp_dir, file_name)
        with open(file_path, 'wb') as file:
            res = requests.get(img_link)
            file.write(res.content)

        with open(file_path, 'rb') as img_file:
            server, photo, hash = upload_photo_to_server(img_file, upload_url)
        media_id, owner_id = save_img_on_wall(server, photo, hash)
        post_img_on_wall(img_comment, media_id, owner_id)

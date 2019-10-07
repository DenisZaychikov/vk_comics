import requests
import json
import random
from dotenv import load_dotenv
import os

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


def create_img_name(img_title, img_num):
    return f'{img_title}_{img_num}{IMG_FORMAT}'


def save_img(img_name, img_link):
    with open(img_name, 'wb') as img_file:
        res = requests.get(img_link)
        img_file.write(res.content)


def get_server_address():
    method = 'photos.getWallUploadServer'
    req_url = f'https://api.vk.com/method/{method}'
    params = {
        'access_token': vk_access_token,
        'v': API_VERSION,
        'group_id': GROUP_ID
    }

    res = requests.get(req_url, params=params).json()

    return res['response']['upload_url'], res['response']['album_id']


def upload_photo_to_server(img_name, upload_url):
    with open(img_name, 'rb')as img_file:
        res = requests.post(upload_url, files={'photo': img_file}).json()

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

    return res.ok


if __name__ == '__main__':
    load_dotenv()
    vk_access_token = os.getenv("VK_TOKEN")
    current_comic_num = get_current_comic_num()
    random_comic_num = random.randint(1, current_comic_num)
    img_link, img_title, img_num, img_comment = get_comic_info(random_comic_num)
    img_name = create_img_name(img_title, img_num)
    save_img(img_name, img_link)
    upload_url, album_id = get_server_address()
    server, photo, hash = upload_photo_to_server(img_name, upload_url)
    media_id, owner_id = save_img_on_wall(server, photo, hash)
    response = post_img_on_wall(img_comment, media_id, owner_id)
    if response:
        os.remove(img_name)

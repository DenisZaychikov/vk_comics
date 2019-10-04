import requests
import json


client_id = '7156952'
vk_access_token = '62004d03cfccf9424aa67cfeff739e88dd09499a43ed4d4f10d44240a9e8aecfaf8eb102a97772797b86e'
api_version = '5.101'


def get_comics_info():
    url = 'http://xkcd.com/353/info.0.json'
    res = requests.get(url).json()
    return res['img'], res['title']

def save_comics(img_name, img_link):
    with open(f'{img_name}.jpg', 'wb') as img_file:
        res = requests.get(img_link)
        img_file.write(res.content)




def get_server_address():
    method = 'photos.getWallUploadServer'
    req_url = f'https://api.vk.com/method/{method}'
    group_id = 187184436
    params = {
        'access_token': vk_access_token,
        'v': api_version,
        'group_id': group_id
        }

    res = requests.get(req_url, params=params).json()
    upload_url = res['response']['upload_url']


def upload_photo_to_server():
    with open('comic1.jpg', 'rb')as img_file:
        res = requests.post(upload_url, files={'photo': img_file})#.json()
        print(res.headers['Content-Type'])


if __name__ == '__main__':
    img_link, img_name = get_comics_info()
    with open('file.json', 'w') as file:
        json.dump(info, file, indent=2, ensure_ascii=False)






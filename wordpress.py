import requests
from typing import List
import json

DOMAIN = 'https://thich2hand.com'
AUTH_URL = f'{DOMAIN}/wp-json/jwt-auth/v1/token/'
MEDIA_URL = f'{DOMAIN}/wp-json/wp/v2/media/'
RENT_APARTMENT = f'{DOMAIN}/wp-json/wp/v2/cho-thue-can-ho/'

CODE_CREATED = 201
CODE_OK = 200
CODE_BAD_REQUEST = 400

PRIVATE_STATUS = "private"
PUBLISH_STATUS = "publish"


class SomethingWrongException(Exception):

    def __init__(self):
        self.message = "Something went wrong"


class WordPressServices():

    @classmethod
    def get_token(cls, username: str, password: str) -> str:
        data = {
            'username': username,
            'password': password
        }
        response = requests.post(AUTH_URL, data=data)
        if response.status_code == CODE_OK:
            return response.json()['token']
        raise Exception('Wrong Authentication')

    @classmethod
    def get_rent_apartments(cls, token: str, page: int = 1) -> dict:
        headers = {
            'Authorization': f'Bearer {token}'
        }
        paging_url = f'{RENT_APARTMENT}?page={page}'
        response = requests.get(paging_url, headers=headers)
        if response.status_code == CODE_OK:
            return response.json()
        if response.status_code == CODE_BAD_REQUEST:
            raise Exception('Wrong paging')
        raise SomethingWrongException()

    @classmethod
    def post_img(cls, token: str, img: bytes, fileName: str) -> dict:
        headers = {
            'Authorization': f'Bearer {token}',
        }
        files=[('file', (fileName,img))]
        response = requests.post(MEDIA_URL, headers=headers, files=files)
        if response.status_code == CODE_CREATED:
            return response.json()
        raise SomethingWrongException()

    @classmethod
    def post_rent_apartment(
            cls, 
            token: str,

            title: str,
            featured_media: int,
            status: str,
            odoo_id: int,
            album_anh_thue: List[int],
            ma_tin_thue: str,
            gia_thue: int,
            dien_tich_thue: str,
            so_phong_ngu_thue: int,
            so_nha_ve_sinh_thue: int,
            # loai_can_ho_cho_thue: List[str],
            link_youtube: str,
            ) -> dict:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
            
        excerpt = f"Căn hộ {so_phong_ngu_thue} phòng ngủ, \
                           {so_nha_ve_sinh_thue} nhà vệ sinh"
        data = json.dumps({
            "title": title,
            "featured_media": featured_media,
            "status": status,
            "excerpt": excerpt,
            # "gia-thue" : gia_thue,
            "meta": {
                "odoo-id": odoo_id,
                "album-anh-thue": album_anh_thue,
                "ma-tin-thue": ma_tin_thue,
                "gia-thue": gia_thue,
                "dien-tich-thue": dien_tich_thue,
                "so-phong-ngu-thue": so_phong_ngu_thue,
                "so-nha-ve-sinh-thue": so_nha_ve_sinh_thue,
                # "loai-can-ho-cho-thue": ["Apartment", "Dual key", "Duplex", "Shophouse"],
                "link-youtube": link_youtube,
            }
        })
        response = requests.post(RENT_APARTMENT, headers=headers, data=data)
        if response.status_code == CODE_CREATED:
            return response.json()
        raise SomethingWrongException()

    @classmethod
    def update_rent_apartment(
            cls, 
            token: str,

            wp_id: int,

            title: str,
            featured_media: int,
            status: str,
            odoo_id: int,
            album_anh_thue: List[int],
            ma_tin_thue: str,
            gia_thue: int,
            dien_tich_thue: str,
            so_phong_ngu_thue: int,
            so_nha_ve_sinh_thue: int,
            # loai_can_ho_cho_thue: List[str],
            link_youtube: str,
            ) -> dict:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
            
        excerpt = f"Căn hộ {so_phong_ngu_thue} phòng ngủ, \
                           {so_nha_ve_sinh_thue} nhà vệ sinh"
        data = json.dumps({
            "title": title,
            "featured_media": featured_media,
            "status": status,
            "excerpt": excerpt,
            "meta": {
                "odoo-id": odoo_id,
                "album-anh-thue": album_anh_thue,
                "ma-tin-thue": ma_tin_thue,
                "gia-thue": gia_thue,
                "dien-tich-thue": dien_tich_thue,
                "so-phong-ngu-thue": so_phong_ngu_thue,
                "so-nha-ve-sinh-thue": so_nha_ve_sinh_thue,
                # "loai-can-ho-cho-thue": ["Apartment", "Dual key", "Duplex", "Shophouse"],
                "link-youtube": link_youtube,
            }
        })
        rent_update = f'{RENT_APARTMENT}/{wp_id}'
        response = requests.post(rent_update, headers=headers, data=data)
        if response.status_code == CODE_OK:
            return response.json()
        raise SomethingWrongException()

    @classmethod
    def hide_rent_apartment(
            cls, 
            token: str,
            wp_id: int,
            ) -> dict:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        data = json.dumps({"status": PRIVATE_STATUS})
        rent_update = f'{RENT_APARTMENT}/{wp_id}'
        response = requests.post(
            rent_update, 
            headers=headers, 
            data=data
            )
        print(response.status_code)
        print(response.json())
        if response.status_code == CODE_OK:
            return response.json()
        raise SomethingWrongException()


if __name__ == '__main__':
    username = "admin"
    password = "OjRV Du8h RMg5 OHKr GJ5L GkCc"
    token = WordPressServices.get_token(username=username, password=password)
    # rent_apartments = WordPressServices.get_rent_apartments(token=token, page=2)
    fileName = './test.png'
    with open(fileName, 'rb') as f:
        im_bytes = f.read()

    im = WordPressServices.post_img(token=token, img=im_bytes, fileName="test.png")
    # print(im)
    # print("--------------------------")
    # print(im["id"])

    # doc_name and photos

    body = {
        "title": "Tra Da",
        "featured_media": im['id'],
        "status": "publish",
        "odoo_id": "28592862",
        "album_anh_thue": [im['id'],im['id']],
        "ma_tin_thue": "Tra Da Via He",
        "gia_thue": "99999000",
        "dien_tich_thue": "70,84m2",
        "so_phong_ngu_thue": "5",
        "so_nha_ve_sinh_thue": "10",
        # "loai_can_ho_cho_thue": ["Apartment", "Dual key", "Duplex", "Shophouse"],
        "link_youtube": "https://www.youtube.com/"
    }
    rent_apartment = WordPressServices.post_rent_apartment(token=token, **body)
    # # rent_apartment = WordPressServices.update_rent_apartment(token=token, wp_id=2899, **body)
    # # rent_apartment = WordPressServices.hide_rent_apartment(token=token, wp_id=2899)
    print(rent_apartment)

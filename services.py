# # -*- coding: utf-8 -*-
import json
import base64
import requests

AUTH_URL = "{domain}/wp-json/jwt-auth/v1/token/"
MEDIA_URL = "{domain}/wp-json/wp/v2/media/"
POST_URL = "{domain}/wp-json/wp/v2/{type}/"

CODE_TOO_LARGE = 413
CODE_CREATED = 201
CODE_OK = 200
CODE_BAD_REQUEST = 400
CODE_ALREADY_TRASHED = 410

DELETE_STATUS = "trash"
PRIVATE_STATUS = "private"
PUBLISH_STATUS = "publish"


class SomethingWrongException(Exception):
    def __init__(self):
        self.message = "Something went wrong"


class WordpressService:
    @classmethod
    def get_token(cls, domain: str, username: str, password: str) -> str:
        data = {"username": username, "password": password}
        response = requests.post(AUTH_URL.format_map({"domain": domain}), data=data)
        if response.status_code == CODE_OK:
            return response.json()["token"]
        raise Exception("Wrong Authentication")

    @classmethod
    def get_posts(
        cls, domain: str, token: str, type_url: str, page: int = 1
    ) -> dict:
        headers = {"Authorization": f"Bearer {token}"}
        paging_url = f"{POST_URL.format_map({'domain': domain, 'type': type_url})}?page={page}"
        response = requests.get(paging_url, headers=headers)
        if response.status_code == CODE_OK:
            return response.json()
        if response.status_code == CODE_BAD_REQUEST:
            raise Exception("Wrong paging")
        raise SomethingWrongException()

    @classmethod
    def post_img(cls, domain: str, token: str, img: bytes, fileName: str) -> dict:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        files = [("file", (fileName, img))]
        response = requests.post(
            MEDIA_URL.format_map({"domain": domain}), headers=headers, files=files
        )
        if response.status_code == CODE_CREATED:
            return response.json()
        if response.status_code == CODE_TOO_LARGE:
            raise Exception(code=CODE_TOO_LARGE, message="File too large")
        raise SomethingWrongException()

    @classmethod
    def post_post(
        cls,
        token: str,
        domain: str,
        type_url: str,
        wp_id: int = None,
        is_update: bool = False,
        body: dict = None,
    ) -> dict:
        if is_update and not wp_id:
            raise Exception("WP_ID is required when update")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        api_endpoint = POST_URL.format_map({"domain": domain, "type": type_url})
        if is_update:
            api_endpoint = f"{api_endpoint}{wp_id}/"
        response = requests.post(api_endpoint, headers=headers, data=json.dumps(body))
        if response.status_code in {CODE_CREATED, CODE_OK}:
            return response.json()
        raise SomethingWrongException()

    @classmethod
    def hide_post(
        cls,
        domain: str,
        token: str,
        wp_id: int,
        type_url: str,
    ) -> dict:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        data = json.dumps({"status": PRIVATE_STATUS})
        update = (
            f"{POST_URL.format_map({'domain': domain,'type': type_url})}{wp_id}"
        )
        response = requests.post(update, headers=headers, data=data)
        if response.status_code == CODE_OK:
            return response.json()
        raise SomethingWrongException()

    @classmethod
    def delete_post(
        cls,
        domain: str,
        token: str,
        wp_id: int,
        type_url: str,
    ) -> dict:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        update = (
            f"{POST_URL.format_map({'domain': domain,'type': type_url})}{wp_id}"
        )
        response = requests.delete(update, headers=headers)
        if response.status_code in (CODE_OK, CODE_ALREADY_TRASHED):
            return response.json()
        raise SomethingWrongException()

    # /<-- wordpress services -->

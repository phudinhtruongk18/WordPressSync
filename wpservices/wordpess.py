import requests
from http import HTTPStatus

AUTH_URL = "{domain}/wp-json/jwt-auth/v1/token/"
MEDIA_URL = "{domain}/wp-json/wp/v2/media/"
POST_URL = "{domain}/wp-json/wp/v2/{type}/"

CODE_TOO_LARGE = HTTPStatus.REQUEST_ENTITY_TOO_LARGE
CODE_CREATED = HTTPStatus.CREATED
CODE_OK = HTTPStatus.OK
CODE_BAD_REQUEST = HTTPStatus.BAD_REQUEST
CODE_ALREADY_TRASHED = HTTPStatus.GONE

DELETE_STATUS = "trash"
PRIVATE_STATUS = "private"
PUBLISH_STATUS = "publish"


class SomethingWrongException(Exception):
    def __init__(self):
        self.message = "Something went wrong"


class WordpressService:
    @staticmethod
    def get_token(domain: str, username: str, password: str) -> str:
        data = {"username": username, "password": password}
        response = requests.post(AUTH_URL.format_map({"domain": domain}), data=data)
        if response.status_code == CODE_OK:
            return response.json()["token"]
        raise Exception("Wrong Authentication")

    @staticmethod
    def get_posts(
        domain: str, token: str, type_url: str, page: int = 1
    ) -> dict:
        headers = {"Authorization": f"Bearer {token}"}
        paging_url = f"{POST_URL.format_map({'domain': domain, 'type': type_url})}?page={page}"
        response = requests.get(paging_url, headers=headers)
        if response.status_code == CODE_OK:
            return response.json()
        if response.status_code == CODE_BAD_REQUEST:
            raise Exception("Wrong paging")
        raise SomethingWrongException()

    @staticmethod
    def post_img(domain: str, token: str, img: bytes, fileName: str) -> dict:
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

    @staticmethod
    def post_post(
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
        response = requests.post(api_endpoint, headers=headers, json=body)
        if response.status_code in {CODE_CREATED, CODE_OK}:
            return response.json()
        raise SomethingWrongException()

    @staticmethod
    def hide_post(
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
        response = requests.post(update, headers=headers, json={"status": PRIVATE_STATUS})
        if response.status_code == CODE_OK:
            return response.json()
        raise SomethingWrongException()

    @staticmethod
    def delete_post(
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

from enum import Enum
import json
from apscheduler.schedulers.background import BackgroundScheduler
import time
import config
from log.LoggerSetUp import logger
import requests


class Method(Enum):
    GET = "get"
    POST = "post"


class _ApiClient(object):
    '''
    Base Class for Feishu API call
    should not call ApiClient() for new clents.
    use Apibase.client instead
    '''

    _tenant_access_token: str
    scheduler = BackgroundScheduler()

    def __init__(self) -> None:
        pass

    def get_all_pages(self, method: Method, path: str, query: dict[str, str] = dict(), headers: dict[str, str] = dict(), body: object = None, page_size: int = 50) -> list[object] | None:
        '''
        for params, see: request()

        this function calls multiple times of request() 
        and iterate all pages by "page_token" & "page_size" & "has_more"
        page_size: in [10,100]

        return: the list of all "data.items" in pages, or None if fail
        '''

        if(page_size < 10 or page_size > 50):
            return None

        page_token: str = ""
        all_list: list[object] = []
        has_more: bool = True
        query["page_size"] = str(page_size)

        while has_more:
            if page_token: query["page_token"] = page_token
            resp = client.request(method=method, path=path,
                                  query=query, headers=headers, body=body)
            if resp is None:
                return None

            l: list[dict] = resp.get("items")
            has_more = bool(resp.get("has_more", False))
            page_token = str(resp.get("page_token", ""))
            
            all_list.extend(l)

        return all_list


    def request(self, method: Method, path: str, query: dict[str, str] = dict(), headers: dict[str, str] = dict(), body: object = None) -> dict[str, object] | None:
        '''
        param path: the part after host (config.LARK_HOST) | eg. "http://feishu.com/aaa" -> "/aaa"
        param body: will be encoded into JSON, ignored if method = GET

        About Header:
        default add Authorization and content-type
        and Authorization in [param headers] will overlap it

        return: 
        "data" section of json body
        and None if error occurs

        '''

        url = _ApiClient._url(path)
        
        # 日，python的默认参数居然是全局单例
        headers = headers.copy()

        if "Authorization" not in headers.keys():
            headers["Authorization"] = "Bearer " + self._tenant_access_token
        headers["content-type"] = "application/json; charset=utf-8"

        try:
            resp: requests.Response
            if method == Method.GET:
                resp = requests.get(url, params=query, headers=headers)
            else:
                resp = requests.post(
                    url, params=query, headers=headers, data=json.dumps(body))

            if not _ApiClient._response_ok(resp):
                logger.error({
                    "url": url,
                    "query": query,
                    "headers": headers,
                    "data": json.dumps(body),
                    "error": "response incorrect",
                    "response": resp.content
                })
                return None
            return resp.json().get("data")

        except:
            logger.error({
                "url": url,
                "query": query,
            })
            return None

    @staticmethod
    def _response_ok(resp: requests.Response) -> bool:
        '''check if the response contains error information'''

        if resp.status_code != 200:
            return False

        response_dict = resp.json()
        code = response_dict.get("code", -1)

        if code != 0:
            return False

        return True

    @staticmethod
    def _url(path: str) -> str:
        return f"{config.LARK_HOST.strip('/')}/{path.strip('/')}"

    def _authorize_tenant_access_token(self) -> bool:
        '''
        get token once

        return: True if success
        '''

        # get tenant_access_token and set, implemented based on Feishu open api capability. doc link: https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/auth-v3/auth/tenant_access_token_internal

        url = _ApiClient._url(
            "/open-apis/auth/v3/tenant_access_token/internal")
        req_body = {
            "app_id": config.APP_ID,
            "app_secret": config.APP_SECRET
        }
        response: requests.Response = requests.post(url, req_body)
        if not _ApiClient._response_ok(response):
            logger.error({
                "error": "cannot get tenant_access_token",
                "response": response
            })
            return False

        self._tenant_access_token = str(
            response.json().get("tenant_access_token"))
        logger.info("got tenant_access_token: "+self._tenant_access_token)
        return True

    def start_token_timer(self):
        '''
        token expires in 120min, and only in last 30min can we refresh it.

        so refresh it per 105min（之前写了个80min，我是什么憨批）
        '''
        if not self._authorize_tenant_access_token():
            logger.error("cannot get feishu token")

        self.scheduler.add_job(self._authorize_tenant_access_token, "interval", minutes=105)
        self.scheduler.start()

# The singleton of ApiClient
client = _ApiClient()

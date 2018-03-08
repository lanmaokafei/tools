#!/usr/bin/env python3
# encoding: utf-8
"""
@version: 0.1
@author: xyj
@license: MIT License
@contact: xieyingjun@vip.qq.com
@Created on 2018/3/6 15:12

根据新浪微博提供API改编
参照廖雪峰写的新浪微博API改编

"""
import requests
import json
import time
from urllib.parse import urlencode


class WeiBoSdk:
    _http = requests.session()

    # API URL API地址
    API_URL = 'https://api.weibo.com/'  # 新浪微博API地址
    AUTH_URL = 'https://api.weibo.com/oauth2/authorize'  # 验证授权地址
    ACCESS_TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'  # 换取Access Token

    def __init__(self, app_key, app_secret, redirect_uri, token=None):
        """
        :param app_key: 申请应用时分配的AppKey
        :param app_secret: 申请应用时分配的AppSecret
        :param redirect_uri: 授权回调地址
        """

        # APP CONFIG  APP配置
        self.client_id = app_key  # 申请应用时分配的AppKey
        self.client_secret = app_secret  # 申请应用时分配的AppSecret
        self.redirect_uri = redirect_uri  # 授权回调地址

        if token:
            self.access_token(token)

    @property
    def authorize_url(self):
        """
        :return:返回APP授权请求地址
        """
        data = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code'
        }
        return f'{self.AUTH_URL}?{urlencode(data)}'

    def fetch_access_token(self, code):
        """
        :param code:用户同意授权后返回的CODE
        :return:获取用户授权的唯一凭证
        """
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        token = self._post(self.ACCESS_TOKEN_URL, data=data)
        # token = json.load(result.text)
        # self._assert_error(token)
        token['expires_overdue'] = int(time.time()) + int(token.pop('expires_in'))
        self.access_token(token)

    def _assert_error(self, d):
        """
        检查返回json中是否包含Error错误信息
        :param d: 需要检查json
        :return: 如果有Error信息返回一个显示错误
        """
        if 'error' in d or 'error_code' in d:
            raise RuntimeError(f'错误代码:{d.get("error_code","")},{d.get("error", "")}')

    def access_token(self, token):
        """
        将返回token解出来
        :param token: fetch_access_token中返回的json
        :return:
        """
        self.token = token
        self.uid = token.get('uid')
        self.access_token = token.get('access_token')
        self.expires_at = token.get('expires_at')
        self._http.params = {'access_token': self.access_token}

    def _request(self, method, url_or_endpoint, **kwargs):
        """
        统一访问接口
        :param method: 提交类型
        :param url_or_endpoint:提交网址或终结点
        :param kwargs: 提交字典
        :return:
        """
        # 判断传入为URL地址或终结点
        if not url_or_endpoint.startswith(('http://', 'https://')):
            url = f'{self.API_URL}{url_or_endpoint}'
        else:
            url = url_or_endpoint

        result = self._http.request(method=method, url=url, **kwargs)

        # 请求返回检查
        try:
            result.raise_for_status()
        except requests.RequestException as error:
            raise RuntimeError(f'请求异常:{error}')

        # 将返回结果json解释成字典
        data = json.loads(result.content.decode('utf-8', 'ignore'), strict=False)

        # 判断返回结果是否包含Error信息
        self._assert_error(data)

        return data

    def _get(self, url, **kwargs):
        """
        GET方法提交
        :param url: 提交地址
        :param kwargs: 提交参数字典
        :return:
        """
        return self._request(method='get', url_or_endpoint=url, **kwargs)

    def _post(self, url, **kwargs):
        """
        POST方法提交
        :param url:提交地址
        :param kwargs: 提交参数字典
        :return:
        """
        return self._request(method='post', url_or_endpoint=url, **kwargs)

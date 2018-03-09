# tools
###
# 自己用的一点小工具

## 微博SDK使用
```
>>>from weibo_sdk import WeiBoSdk
>>>w = WeiBoSdk(app_key, app_secret, redirect_uri)
>>>w.authorize_url  # 获取登陆链接，将返回结果粘贴到浏览器中登陆
'https://api.weibo.com/oauth2/authorize?client_id=xxxx&redirect_uri=127.0.0.1&response_type=code'
# 浏览器中登陆回调地址http://127.0.0.1/?code=xxxxxxxxxxxxx
将code=xxxxxxxxxxxxx复制
>>>c.fetch_access_token('xxxxxxxxxxxxx')
>>>c.token  # 获取登陆后的token
{'access_token': 'xxxxxxxxxxxxx', 'remind_in': '157679999', 'uid': 'xxxxxxxxxxxxx', 'isRealName': 'true', 'expires_overdue': 1678257751}
```
    
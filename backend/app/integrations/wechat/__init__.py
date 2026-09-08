"""微信 Integration：OAuth 与模板通知 Client。不创建 User、不写 Booking。"""

from app.integrations.wechat.notify import WechatNotifyClient
from app.integrations.wechat.oauth import MOCK_CODE, MOCK_OPENID, WechatOAuthClient

__all__ = [
    "MOCK_CODE",
    "MOCK_OPENID",
    "WechatNotifyClient",
    "WechatOAuthClient",
]

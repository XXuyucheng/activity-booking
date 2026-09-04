"""微信 Integration：OAuth Client。不创建 User、不写 Booking。"""

from app.integrations.wechat.oauth import MOCK_CODE, MOCK_OPENID, WechatOAuthClient

__all__ = ["MOCK_CODE", "MOCK_OPENID", "WechatOAuthClient"]

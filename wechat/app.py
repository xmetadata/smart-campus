# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os

from flask import Flask, request, abort, render_template, jsonify
from wechatpy import parse_message, create_reply, WeChatClient
from wechatpy.utils import check_signature
from wechatpy.oauth import WeChatOAuth, WeChatOAuthException
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)

# set token or get from environments
TOKEN = 'duapp'
AES_KEY = os.getenv('WECHAT_AES_KEY', '')
APPID = 'wxc7f53c870e7700ab'
APPSECRET = 'd4624c36b6795d1d99dcf0547af5443d'

app = Flask(__name__)


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    encrypt_type = request.args.get('encrypt_type', 'raw')
    msg_signature = request.args.get('msg_signature', '')
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == 'GET':
        echo_str = request.args.get('echostr', '')
        return echo_str

    # POST request
    if encrypt_type == 'raw':
        # plaintext mode
        msg = parse_message(request.data)
        if msg.type == 'text':
            reply = create_reply(msg.content, msg)
        else:
            reply = create_reply('Sorry, can not handle this for now', msg)
        return reply.render()
    else:
        # encryption mode
        from wechatpy.crypto import WeChatCrypto

        crypto = WeChatCrypto(TOKEN, AES_KEY, APPID)
        try:
            msg = crypto.decrypt_message(
                request.data,
                msg_signature,
                timestamp,
                nonce
            )
        except (InvalidSignatureException, InvalidAppIdException):
            abort(403)
        else:
            msg = parse_message(msg)
            if msg.type == 'text':
                reply = create_reply(msg.content, msg)
            else:
                reply = create_reply('Sorry, can not handle this for now', msg)
            return crypto.encrypt_message(reply.render(), nonce, timestamp)


@app.route('/wmenu', methods=['GET', 'POST'])
def wmenu():
    wechat_client = WeChatClient(APPID, APPSECRET)
    wechat_client.menu.create({
        "button": [
            {
                "type": "click",
                "name": "今日歌曲",
                "key": "V1001_TODAY_MUSIC"
            },
            {
                "type": "click",
                "name": "歌手简介",
                "key": "V1001_TODAY_SINGER"
            },
            {
                "name": "菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "搜索",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "view",
                        "name": "视频",
                        "url": "http://v.qq.com/"
                    },
                    {
                        "type": "click",
                        "name": "赞一下我们",
                        "key": "V1001_GOOD"
                    }
                ]
            }
        ],
        "matchrule": {
            "group_id": "2",
            "sex": "1",
            "country": "中国",
            "province": "广东",
            "city": "广州",
            "client_platform_type": "2"
        }
    })
    return "Hello, World!"

@app.route('/wauth', methods=['GET', 'POST'])
def wauth():
    code = request.args.get('code')
    print 'code==>', code
    oauth = WeChatOAuth(APPID, APPSECRET, 'http://sc-wc.xmetadata.com')
    print 'code==>'
    # print 'check_access_token==>', oauth.check_access_token(code)
    access_token = oauth.fetch_access_token(code)
    print access_token
    user_info = oauth.get_user_info(access_token)
    return jsonify(user_info)

@app.route('/wtemp', methods=['GET', 'POST'])
def wtemp():
    wechat_client = WeChatClient(APPID, APPSECRET)
    # wechat_client.template.set_industry(1, 4)
    # wechat_client.template.add('MT00001')
    print wechat_client.template.get_industry()
    print wechat_client.template.get_all_private_template()
    wechat_client.message.send_template('oDMjOw45l88jjv_a94q3rHC4uJ9g', 'Vf-FbPofgwDeBlNqDGUwVjikDW50BmgTFfJIX0qGhYU', {'username': 'Duyajun'})
    return 'huhu'

if __name__ == '__main__':
    app.run('0.0.0.0', 5001, debug=True)

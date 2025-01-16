# ================================================= #
# @file serve.py
# @brief 媒体部统一认证服务端
# @author Wesley
# @date 2025-01-13
# @version 2.0.0
# ================================================= #
##########################################
##        Made By Wesley in 2025         #
##########################################

import os,sys,re
import time
import datetime
import json
import traceback
import flask
from flask import request,render_template,redirect
from flask_cors import CORS
import pymysql
import hashlib
import random 
from pymysql.converters import escape_string
import pymysql.cursors
from itertools import chain
import requests
import threading
import ast
from gevent import pywsgi
from urllib import parse
import base64
from io import BytesIO
# import uvicorn


VERSION = "v2_0_0" #20250113

REQ_METHODS = ["GET","POST"]

URLPREFIX = "/v2/OAuth"
WECHATPREFIX = "/v2/WxAuth"
MINIPROGRAMPREFIX = "/v2/mini-api"

MysqlServer = "121.40.69.157"

# mysql config
mysql_config = {
    'host': MysqlServer,
    'user': 'sql_admin',
    'password': 'Admin@mtb_oa2024',
    'db': 'mtb-oa',
    'cursorclass': pymysql.cursors.DictCursor
}

# 维护模式
maintain_reason = "停服维护中。请咨询管理员。"

# 获取当前时间
start_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
start_time = int(time.time())

## 通用类代码
def get_milliTimestamp():
    """获取毫秒级时间戳"""
    return int(round(time.time() * 1000))

def get_timestamp():
    """获取时间戳"""
    return int(round(time.time()))

def get_time():
    """获取YYYY-MM-DD hh:mm:ss"""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

def get_dayOfWeek():
    """获取当前星期数"""
    return time.strftime("%w")

def get_weekOfYear():
    """获取当前周数"""
    return time.strftime("%W")
def sha256(data: str):
    """hash256加密"""
    hash256 = hashlib.sha256()
    hash256.update(data.encode('utf-8'))
    return(hash256.hexdigest())

def md5(data: str):
    """md5加密"""
    hashmd5 = hashlib.md5()
    hashmd5.update(data.encode('utf-8'))
    return(hashmd5.hexdigest())

def getIp(request):
    """获取访问者IP地址"""
    try:
        ip = request.headers["X-Real-IP"]
        if ip == "" or ip == None:
            ip = request.remote_addr
    except:
        ip = request.remote_addr
    return ip

def escape(s):
    """防SQL注入"""
    return escape_string(s)

# [START] MAIN FUNCTION CODE AREA

# Tools
def  synthesisReturnData(CODE:int|str,MSG:str="Invalid Result",DATA=None):
    """合成返回数据"""
    try:
        if DATA == None and (type(DATA) != str or (type(DATA) != list or type(DATA) != dict)):
            return ({"errcode":CODE,"errmsg":MSG},200)
        return ({"errcode":CODE,"errmsg":MSG,"data":DATA},200)
    except:
        return ({"errcode":-1001,"errmsg":"Invalid Result"},200)

def getRequestToken(request):
    """获取请求是否携带Token"""
    try:
        token = request.headers["Token"]
        if token == "" or token == None:
            token = False
    except:
        token = False
    return token

def getMaintainStatus():
    """获取维护模式状态"""
    try:
        with pymysql.connect(**mysql_config) as conn:
            with conn.cursor() as cursor:
                sql = 'select * from `system` where `name` = "maintain_mode"'
                cursor.execute(sql)
                result = cursor.fetchone()
                if not result:
                    return False
                if result["text"] == 1:
                    return True
                return False
    except:
        return False

# 业务代码
def login(USER_CODE:str,PASSWORD:str):
    """认证登录"""
    data = {}
    try:
        if USER_CODE == "None" or PASSWORD == "None":
            return synthesisReturnData(-1001,"Invalid Parameter")
        TOKEN = ""
        # 维护模式
        if getMaintainStatus():
            return synthesisReturnData(-2,maintain_reason)
        else:
            if findTokenByUserCode(USER_CODE) != "":
                # 当前用户已经登录了，移除当前登录态
                cancelToken(USER_CODE)
            with pymysql.connect(**mysql_config) as conn:
                with conn.cursor() as cursor:
                    sql = 'select * from `user` where code = %s and password = %s and type = 0'
                    cursor.execute(sql, (escape_string(USER_CODE),
                                escape_string(sha256(PASSWORD))))
                    result = cursor.fetchone()
                    if result:
                        login_times = get_time()
                        with pymysql.connect(**mysql_config) as conn:
                            with conn.cursor() as cursor:
                                sql = "UPDATE `user` SET `login_time` = %s WHERE id = %s"
                                cursor.execute(sql, (str(login_times),int(result["id"])))
                                conn.commit()
                        TOKEN = registerToken(USER_code=USER_CODE, group=result["group"], password=PASSWORD,class_str=result["class"], name=result["name"], share_device=result["share_device"], id=result["id"], login_time=login_times, join_time=result["join_time"], reg_time=result["reg_time"], grade=result["grade"], openid=result["openid"], remark=result["remark"])
                        data = getTokenInfo(TOKEN)
                        data["password"] = None
                        data["token"] = TOKEN
                        return synthesisReturnData(0,"ok",data)
        return synthesisReturnData(-20001,"Account or password error")
    except:
        print(traceback.format_exc())
        return synthesisReturnData(-1,f"System Error: {traceback.format_exc()}")

def registerToken(USER_code: str, password: str, name: str, class_str: str,group: int, share_device: int, id: str, login_time: int,join_time: str,reg_time: str,grade: str,openid: str,remark: str,loginType: str="web-sso"):
    """注册Token"""
    cleanTimeoutToken()
    
    if not cancelToken(USER_code):
        return ""
    if getMaintainStatus():
        return ""
    TOKEN_CONSTITUTE = str({"login_time":f"{get_milliTimestamp()}","usercode":f"{USER_code}","passowrd":f"{password}","KEY":f"{random.randint(1,100000)}"})
    TOKEN = sha256(TOKEN_CONSTITUTE).upper()
    with pymysql.connect(**mysql_config) as conn:
        with conn.cursor() as cursor:
            sql = 'INSERT INTO `login-status`(`TOKEN`, `usercode`, `name`, `class`, `group`, `grade`, `password`, `share_device`, `reg_time`, `join_time`, `openid`, `remark`, `login_type`, `login_time`, `timeout`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, (TOKEN,USER_code,name,class_str,group,grade,password,share_device,reg_time,join_time,openid,remark,loginType,login_time,get_timestamp()))
            conn.commit()
    tokenRenewal(TOKEN)
    return TOKEN

def cancelToken(codeOrToken:str):
    """注销Token"""
    cleanTimeoutToken()
    with pymysql.connect(**mysql_config) as conn:
        with conn.cursor() as cursor:
            sql = 'DELETE FROM `login-status` WHERE TOKEN = %s OR usercode = %s'
            cursor.execute(sql, (codeOrToken,codeOrToken))
            conn.commit()
    if tokenExists(codeOrToken):
        return False
    return True

def cleanTimeoutToken():
    """清除过期Token"""
    # 数据库版
    NotCleanRemark = []
    with pymysql.connect(**mysql_config) as conn:
        with conn.cursor() as cursor:
            sql = 'DELETE FROM `login-status` WHERE timeout < %s AND remark NOT LIKE "_NoCleanToken"'
            cursor.execute(sql, (get_timestamp()))
            conn.commit()

def findTokenByUserCode(USER_code: str):
    """按照用户Code查找Token"""
    cleanTimeoutToken()
    with pymysql.connect(**mysql_config) as conn:
        with conn.cursor() as cursor:
            sql = 'SELECT * FROM `login-status` WHERE usercode = %s'
            cursor.execute(sql, (USER_code))
            result = cursor.fetchone()
            return result
    return False

def verifyTokenEffective(token:str):
    """校验token是否有效"""
    return tokenExists(token)

def tokenExists(Token:str):
    """查找Token是否在存在"""
    cleanTimeoutToken()
    with pymysql.connect(**mysql_config) as conn:
        with conn.cursor() as cursor:
            sql = 'SELECT * FROM `login-status` WHERE TOKEN = %s'
            cursor.execute(sql, (Token))
            result = cursor.fetchone()
            if result:
                return True
            return False

def getLoginUserInfo_ByToken(Token:str):
    """获取token对应的用户信息"""
    try:
        if tokenExists(Token):
            return getTokenInfo(Token)
        return False
    except Exception as err:
        print(err)
        return False

def getTokenInfo(Token:str):
    """获取Token信息"""
    with pymysql.connect(**mysql_config) as conn:
        with conn.cursor() as cursor:
            sql = 'SELECT * FROM `login-status` WHERE TOKEN = %s'
            cursor.execute(sql, (Token))
            result = cursor.fetchone()
            return result

def tokenRenewal(Token:str):
    """Token续期"""
    # 每小时只能续期一次，每次只能续期90分钟即5400秒
    try:
        if tokenExists(Token):
            TOKENRenewalLimit = getTokenInfo(Token)["renewalLimit"]
            if TOKENRenewalLimit:
                if TOKENRenewalLimit < get_timestamp():
                    return False
            with pymysql.connect(**mysql_config) as conn:
                with conn.cursor() as cursor:
                    selectSql = "SELECT * FROM `login-status` WHERE TOKEN = %s"
                    cursor.execute(selectSql, (Token))
                    result = cursor.fetchone()
                    sql = 'UPDATE `login-status` SET `timeout`=%s, `renewalLimit`=%s WHERE TOKEN = %s'
                    cursor.execute(sql, (result["timeout"] + 5400,get_timestamp() + 3600,Token))
                    conn.commit()
                    return True
    except:
        print(traceback.format_exc())


# 初始化SSO服务
app = flask.Flask(__name__)
# 允许跨域
CORS(app)

# SSO-HTTP[404]
@app.errorhandler(404)
def not_found(error):
    return synthesisReturnData(-1,"不支持的页面")

# SSO-HTTP[500]
@app.errorhandler(500)
def serve_error(error):
    return synthesisReturnData(-3,"服务器错误")


# 路由开始
# 其他功能
@app.route(f'{URLPREFIX}/maintain', methods=REQ_METHODS)
def Route_Maintain():
    """维护模式-路由"""
    try:
        return synthesisReturnData(0,"ok",{"maintain":getMaintainStatus()})
    except:
        return synthesisReturnData(-1,"系统错误")

@app.route(f'{URLPREFIX}/getBackgroundImage', methods=REQ_METHODS)
def Route_GetBackgroundImage():
    """获取背景图片"""
    GET_data = request.args
    data = []
    try:
        resolution = str(GET_data.get("resolution"))
        randomly = str(GET_data.get("random"))
        if resolution=='None':
            resolution = "middle"
    except Exception as err:
        print(f"ERR: {err}")
    url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=-1&n=8&mkt=zh-CN"
    try:
        response = requests.get(url=url)
        getres = json.loads(response.text)["images"]
        # asdsada = 0
        for i in getres:
            a = {}
            a["Fullcopyright"] = i["copyright"]
            pattern = re.compile(r'\(©[\s\S]+\)')
            pattern2 = re.compile(r'©[^/]+')
            
            try:
                b = pattern.search(i["copyright"]).group()
                c = pattern2.search(i["copyright"]).group()
            except:
                b = i["copyright"]
                c = i["copyright"]
            a["title"] = i["copyright"].replace(" "+b,"")
            a["copyright"] = c.replace("(", "").replace(")","")

            if resolution == "UHD":
                a["url"] = "https://cn.bing.com"+i["url"].replace("1920x1080","UHD")
            elif resolution == "small":
                a["url"] = "https://cn.bing.com"+i["url"].replace("1920x1080","1280x720")
            else:
                a["url"] = "https://cn.bing.com"+i["url"]
            data.append(a)
            # asdsada += 1
        if randomly == 'true':
            #随机一张
            ran = random.randint(0,7)
            data = data[ran]
        return synthesisReturnData(0,"ok",data)
    except Exception as err:
        print(err)
    return synthesisReturnData(-1,"System Error",traceback.format_exc())

# 正牌功能
@app.route(f"{URLPREFIX}/login", methods=REQ_METHODS)
def Route_Login():
    """登录-路由"""
    POST_data = request.form
    try:
        try:
            account = str(POST_data.get("account"))
            password = str(POST_data.get("password"))
        except:
            return synthesisReturnData(-1001,"Invalid Parameter")
        return login(account,password)
    except:
        return synthesisReturnData(-1,"Running Function Error In Router",traceback.format_exc())

@app.route(f"{URLPREFIX}/relogin", methods=REQ_METHODS)
def Route_ReLogin():
    """重新登录-路由"""
    TOKEN = getRequestToken(flask.request)
    try:
        # 判断TOKEN是否过期
        if not verifyTokenEffective(TOKEN):
            return synthesisReturnData(-1004,"Token Expired")
        # 若没过期，续期token后返回用户数据
        tokenRenewal(TOKEN)
        return synthesisReturnData(0,"ok",getLoginUserInfo_ByToken(TOKEN))
    except:
        return synthesisReturnData(-1,"Running Function Error In Router",traceback.format_exc())
        

@app.route(f"{URLPREFIX}/logout", methods=REQ_METHODS)
def Route_Logout():
    """登出-路由"""
    try:
        if verifyTokenEffective(getRequestToken(flask.request)):
            cancelToken(getRequestToken(flask.request))
        if tokenExists(getRequestToken(flask.request)):
            return synthesisReturnData(-1,"Can't logout because the user's token can't remove form the group",traceback.format_exc())
        else:
            return synthesisReturnData(0,"ok")
    except:
        print(traceback.format_exc())
        return synthesisReturnData(-1,"Running Function Error In Router",traceback.format_exc())

@app.route(f"{URLPREFIX}/getLoginUserInfo", methods=REQ_METHODS)
def Route_GetLoginUserInfo():
    """获取登录用户信息-路由"""
    TOKEN = getRequestToken(flask.request)
    if not getLoginUserInfo_ByToken(TOKEN):
        return synthesisReturnData(0,"ok",{})
    return synthesisReturnData(0,"ok",getLoginUserInfo_ByToken(TOKEN))

@app.route(f"{URLPREFIX}/checkToken", methods=REQ_METHODS)
def Route_CheckToken():
    """验证Token-路由"""
    try:
        return synthesisReturnData(0,"ok",{"token":getRequestToken(flask.request),"verify":verifyTokenEffective(getRequestToken(flask.request))})
    except:
        return synthesisReturnData(-1,"Running Function Error In Router",traceback.format_exc())

@app.route(f"{URLPREFIX}/changePassword", methods=REQ_METHODS)
def Route_ChangePassword():
    """更改密码-路由"""
    POST_data = request.form
    TOKEN = getRequestToken(flask.request)
    try:
        old_passwd = str(POST_data.get("oldpassword"))
        new_passwd = str(POST_data.get("newpassword"))
        if old_passwd == "" or new_passwd == "":
            return synthesisReturnData(-1001,"Invalid Parameter")
    except:
        return synthesisReturnData(-1001,"Invalid Parameter")
    tokenRenewal(TOKEN)

    old_passwd_hash = sha256(old_passwd)
    new_passwd_hash = sha256(new_passwd)

    if old_passwd_hash == "" or new_passwd_hash == "":
        return synthesisReturnData(-10001,"Cannot encrypt the password info")

    user_code = getTokenInfo(TOKEN)["usercode"]

    with pymysql.connect(**mysql_config) as conn:
        with conn.cursor() as cursor:
            sql = 'select * from user WHERE `type` = 0 AND `code` = %s'
            cursor.execute(sql, (escape_string(user_code)))
            result = cursor.fetchone()
            if not result:
                return synthesisReturnData(-10002,"Cannot find this user Account")
            if result["password"] != old_passwd_hash:
                return synthesisReturnData(-10003,"Old password is wrong")

        with conn.cursor() as cursor:
            sql = 'UPDATE user SET password = %s WHERE code = %s'
            cursor.execute(sql, (new_passwd_hash, escape_string(user_code)))
            conn.commit()
    return synthesisReturnData(0,"ok")

@app.route(f"{URLPREFIX}/getServerTime", methods=REQ_METHODS)
def getServerTime():
    """获取服务器时间"""
    return synthesisReturnData(0,"ok",{"time":get_milliTimestamp()})


## SSO 统一认证系统 代码结束 ##

# [START]ROUTE CODE AREA
@app.route("/api/LatestVersion", methods=["GET","POST"])
def __RETURN_VERSION__():
    """返回最新版本号"""
    RESULT = synthesisReturnData(0,"ok",{"version":VERSION})
    return RESULT


# 微信业务

LoginStatus = {}
# codeType: login | authorize
# 关于Key码的Status值定义说明：400-未扫码（初始） | 401-已扫码，未确认 | 402-已扫码，操作取消 | 403-已扫码，已确认 | 404-已扫码，但由于某种原因无法完成授权 | 405-不存在（已过期）
CodeGroup = {}

WxApi = "https://api.weixin.qq.com"

def getAccessToken():
    try:
        textmod = {
            "grant_type": "client_credential",
            "appid": "wx1797985f865315af",
            "secret": "1352dd201ea10f59c1561075f110ca11",
            "force_refresh": "false"
        }
        textmod = parse.urlencode(textmod)
        header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get(url='%s%s%s' % (f"{WxApi}/cgi-bin/token", '?', textmod), headers=header_dict)
        res = req.text
        if "errcode" in res:
            return False
        res = json.loads(res)
        return res
    except Exception as e:
        print(e)
        return False

def getStableAccessToken():
    try:
        data = {
            "grant_type": "client_credential",
            "appid": "wx1797985f865315af",
            "secret": "1352dd201ea10f59c1561075f110ca11",
            "force_refresh": False
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            'Content-Type': 'application/json'
        }
        req = requests.post(url=f"{WxApi}/cgi-bin/stable_token",json=data, headers=headers)
        res = req.text
        if "errcode" in res:
            return False
        res = json.loads(res)
        return res
        
    except Exception as e:
        print(e)
        return False

# type: login | authorize
def getMiniprogramQRCode(page="pages/index/index",key:str="",validity=300000,is_hyaline=False,type="login" ):
    global CodeGroup
    if not key:
        summerKey = sha256(f"{ get_milliTimestamp() }{ start_time }{random.randint(0,9999999)}")
        # 从1-4 和 8-12 组合
        key = summerKey[0:4] + summerKey[8:12]
    try:
        ACCESS_TOKEN = getStableAccessToken()
        if not ACCESS_TOKEN:
            return (False,"GetAccessTokenFail")
        ACCESS_TOKEN = ACCESS_TOKEN["access_token"]
        createTime = int(time.time() * 1000)
        # "env_version": "develop",
        # release
        data = {
            "page": page,
            "scene": f"t={key},p={type}",# t: token/key p: type
            "is_hyaline": is_hyaline,
            "env_version": "release",
            "auto_color": True,
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            'Content-Type': 'application/json'
        }
        req = requests.post(url=f"{WxApi}/wxa/getwxacodeunlimit?access_token={ACCESS_TOKEN}",json=data, headers=headers)
        res = req.text
        if "errcode" in res:
            return (False,json.loads(res)['errmsg'])
        ls_f=base64.b64encode(BytesIO(req.content).read())
        img_b64 = f"data:image/png;base64,{str(ls_f,encoding='utf-8')}"
        # 记录key码
        keyInfo = {
            "img_base64": img_b64,
            "createTime": createTime,
            "validity": validity,
            "timeoutTime": get_timestamp() + (validity/1000),
            "type": type,
            "status": 400,
            "key": key,
        }
        CodeGroup[key] = keyInfo
        return (True,keyInfo)
        
    except Exception as e:
        return (False,e)

def cleanTimeoutCode():
    global CodeGroup
    CodeGroup = {key: value for key, value in CodeGroup.items() if value["timeoutTime"] >= get_timestamp()}

# def cleanTimeoutCode():
#     global CodeGroup
#     keys_to_delete = []
#     for key in CodeGroup.keys():
#         if CodeGroup[key]["timeoutTime"] < get_timestamp():
#             keys_to_delete.append(key)
#     for key in keys_to_delete:
#         del CodeGroup[key]
def renewalCode(key):
    global CodeGroup
    if key not in CodeGroup:
        return False
    CodeGroup[key]["timeoutTime"] = get_timestamp() + (CodeGroup[key]["validity"]/2000)
    return True

@app.route(f"{MINIPROGRAMPREFIX}/getAccessToken", methods=["GET","POST"])
def Route_WxMinGetAccessToken():
    result = getStableAccessToken()
    if not result:
        return synthesisReturnData("WGAT:1001","获取AccessToken(Stable)失败")
    return synthesisReturnData(0,"ok",result)

@app.route(f"{WECHATPREFIX}/getMiniProgramCode", methods=["GET","POST"])
def Route_WxMinGetMiniProgramCode():
    cleanTimeoutCode()
    QRcode = getMiniprogramQRCode()
    if not QRcode[0]:
        return synthesisReturnData("WGPC:1001","获取小程序码失败")
    return synthesisReturnData(0,"ok",QRcode[1])

@app.route(f"{MINIPROGRAMPREFIX}/scanCode", methods=["GET","POST"])
def Route_WxMinScanCode():
    cleanTimeoutCode()
    POST_data = request.form
    try:
        key = str(POST_data.get("key")) if POST_data.get("key") else request.values.get("key")
    except:
        return synthesisReturnData(-1001,"Invalid Parameter")
    if key not in CodeGroup:
        return synthesisReturnData("WSC:1001","key码不存在")
    # 设置status为401
    CodeGroup[key]["status"] = 401
    return synthesisReturnData(0,"ok",CodeGroup[key])
@app.route(f"{MINIPROGRAMPREFIX}/operateCode", methods=["GET","POST"])
def Route_WxMinOperateCode():
    cleanTimeoutCode()
    POST_data = request.form
    try:
        key = str(POST_data.get("key")) if POST_data.get("key") else request.values.get("key")
        mode = str(POST_data.get("mode")) if POST_data.get("mode") else request.values.get("mode")
        openid = str(POST_data.get("openid")) if POST_data.get("openid") else request.values.get("openid")
    except:
        return synthesisReturnData(-1001,"Invalid Parameter")
    if key not in CodeGroup:
        return synthesisReturnData("WOC:1001","key码不存在")
    renewalCode(key)
    if mode == "cancel":
        # 设置status为402
        CodeGroup[key]["status"] = 402
    elif mode == "confirm":
        # 开始登录，查找数据库中对应的openid
        if openid:
            with pymysql.connect(**mysql_config) as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT * FROM `user` WHERE openid = %s"
                    cursor.execute(sql, (openid))
                    result = cursor.fetchone()
                    if not result:
                        return synthesisReturnData("WOC:1002","openid不存在")
                    # 如果codeType为login则进入登录程序，否则默认授权
                    if CodeGroup[key]["type"] == "login":
                        # 登录程序 | 注册TOKEN
                        TOKEN = registerToken(
                            USER_code=result["code"],
                            group=result["group"],
                            password=None,
                            class_str=result["class"],
                            name=result["name"],
                            share_device=result["share_device"],
                            id=result["id"],
                            login_time=get_time(),
                            join_time=result["join_time"],
                            reg_time=result["reg_time"],
                            grade=result["grade"],
                            openid=result["openid"],
                            remark=result["remark"],
                            loginType="Miniprogram"
                        )
                        userdata = {
                            "token": TOKEN
                        }
                    else:
                        # 授权 | 设置用户信息
                        userdata = {}
                    # 提取公共部分
                    userdata.update({
                        "id": result["id"],
                        "code": result["code"],
                        "name": result["name"],
                        "group": result["group"],
                        "class": result["class"],
                        "openid": result["openid"],
                    })
                    CodeGroup[key]["data"] = userdata
                    # 设置status为403
                    CodeGroup[key]["status"] = 403
                    return synthesisReturnData(0,"ok",CodeGroup[key])
        # 设置status为404
        CodeGroup[key]["status"] = 404
        return synthesisReturnData("WOC:1002","openid不存在")
    else:
        return synthesisReturnData("WOC:1003","参数错误")
    return synthesisReturnData(0,"ok",CodeGroup[key])

@app.route(f"{WECHATPREFIX}/checkCodeStatus", methods=["GET","POST"])
def Route_WxMinCheckCodeStatus():
    POST_data = request.form
    cleanTimeoutCode()
    try:
        key = str(POST_data.get("key"))
    except:
        return synthesisReturnData(-1001,"Invalid Parameter")
    if key not in CodeGroup:
        return synthesisReturnData(0,"ok",{"key": key, "status": 405})
        # return synthesisReturnData("WCCS:1002","key码不存在")
    return synthesisReturnData(0,"ok",CodeGroup[key])










# [END]ROUTE CODE AREA


# 运行
if __name__ == '__main__':
    print(f"【媒体部 统一认证服务】")
    print(f"后端版本：{VERSION}")
    app.run(host='0.0.0.0', port=50001, debug=False)
    # uvicorn.run(app,port=30000)
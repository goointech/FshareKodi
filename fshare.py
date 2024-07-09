import requests
import json
import os

Fshare_app_key = "dMnqMMZMUnN5YpvKENaEhdQQ5jxDqddt"
Fshare_User_Agent = "fshare_tkvv"

def buildLinkDown(link_view,token_,session_id_): 
    response_ = requests.post(url="https://api.fshare.vn/api/session/download", data=json.dumps({
                    "zipflag" : 0,
                    "url" : link_view,
                    "password" : "",
                    "token": token_
                }), headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Cache-Control": "no-cache",
                    "Cookie":"session_id="+session_id_
                }, timeout=3*60)
     
    if response_.status_code == 200:
        data_ =  json_load(response_.content) 
        if "location" in data_:
            return data_["location"]
    return ""


def loginFshare(user_,pass_):
    session_id = ""
    token_ = ""
    response_ = requests.post(url="https://api.fshare.vn/api/user/login", data=json.dumps({
                    "user_email" : user_,
                    "password":	pass_,
                    "app_key" : Fshare_app_key
                }), headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Cache-Control": "no-cache",
                    "User-Agent": Fshare_User_Agent
                }, timeout=3*60)
    
    if response_.status_code == 200:
        data_ =  json_load(response_.content) 
        if "msg" in data_ and data_["msg"]=="Login successfully!" and "token" in data_ and "session_id" in data_:
            session_id = data_["session_id"]
            token_ = data_["token"]
    return session_id,token_


def json_load(str):
    try:
    # đọc JSON trừ chuổi
        return json.loads(str)
    except:
        return None
    
def getListPhim():
    response_ = requests.post(url="https://thuvienhd.xyz/?feed=fsharejson&search=&page=1", data=json.dumps({}), headers={
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "Cache-Control": "no-cache",
                            "User-Agent": "Min.Cafe 27.1"
                        }, timeout=3*60)
    if response_.status_code == 200:
#         [
#     {
#         'genre': 'Drama',
#         'icon': os.path.join(ICONS_DIR, 'Drama.png'),
#         'fanart': os.path.join(FANART_DIR, 'Drama.jpg'),
#         'movies': [
#             {
#                 'title': 'The Stranger',
#                 'url': 'http://download014.fshare.vn/dl/EU4YZAX70M3e4Ab9cQQCRa9idJWsWQoiRqoEgBgDwYt1kKHV0hgRMvfAbFohUGzRRcb0DaiaTHigHwWc/Inside.Out.2.2024.1080p.TELESYNC.x265.COLLECTiVE.mkv',
#                 'poster': 'https://publicdomainmovie.net/wikimedia.php?id=Movie-Mystery-Magazine-July-1946.jpg',
#                 'plot': 'Dùng thử',
#                 'year': 1946,
#             }
#         ]
#     }
# ]
        data_  = json_load(response_.content)
        rs_data = []
        for d_ in data_:
            if "title" in d_ and "image" in d_ and "links" in d_:
                movide_new = {
                    "genre":d_["title"],
                    'icon': d_["image"],
                    'fanart': d_["image"],
                    "movies": []
                }
                list_link = d_["links"]
                for ll in list_link:
                    if "title" in ll and "link" in ll:
                        movide_new["movies"].append({
                            'title': ll["title"],
                            'url': ll["link"],
                            'poster': d_["image"],
                            'plot': d_["title"],
                            'year': 0,
                        })

                rs_data.append(movide_new)
        return rs_data
    return []

# if __name__ == '__main__':
#     # Call the router function and pass the plugin call parameters to it.
#     # We use string slicing to trim the leading '?' from the plugin call paramstring
#     # router(sys.argv[2][1:])

#     data_select_link = ""
#     data_thuvienHD = getListPhim()
#     print("data_thuvienHD===>",data_thuvienHD)
#     # # print(data_thuvienHD)
#     # if "links" in data_thuvienHD[0]:
#     #     if "link" in data_thuvienHD[0]["links"][0]:
#     #         data_select_link = data_thuvienHD[0]["links"][0]["link"]
#     # # elif "link" in data_thuvienHD[0]:
#     # #     data_select_link = data_thuvienHD[0]["link"]

#     # print("getListPhim===>",data_select_link)
#     # session_id,token_ = loginFshare("fshare_tkvv@fshare.vn","1234@abcd")
#     # print("token_===>",token_)
#     # print("session_id===>",session_id) 
#     # print("buildLinkDown===>",buildLinkDown(data_select_link,token_,session_id))

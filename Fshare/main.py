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

# Get the plugin url in plugin:// notation.
URL = sys.argv[0]
# Get a plugin handle as an integer number.
HANDLE = int(sys.argv[1])
# Get addon base path
ADDON_PATH = translatePath(Addon().getAddonInfo('path'))
ICONS_DIR = os.path.join(ADDON_PATH, 'resources', 'images', 'icons')
FANART_DIR = os.path.join(ADDON_PATH, 'resources', 'images', 'fanart')

Fshare_app_key = "dMnqMMZMUnN5YpvKENaEhdQQ5jxDqddt"
Fshare_User_Agent = "fshare_tkvv"

# Public domain movies are from https://publicdomainmovie.net
# Here we use a hardcoded list of movies simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some website or online service.
VIDEOS = [
        {
            'genre': 'Drama',
            'icon': os.path.join(ICONS_DIR, 'Drama.png'),
            'fanart': os.path.join(FANART_DIR, 'Drama.jpg'),
            'movies': [
                {
                    'title': 'The Stranger',
                    'url': 'http://download014.fshare.vn/dl/EU4YZAX70M3e4Ab9cQQCRa9idJWsWQoiRqoEgBgDwYt1kKHV0hgRMvfAbFohUGzRRcb0DaiaTHigHwWc/Inside.Out.2.2024.1080p.TELESYNC.x265.COLLECTiVE.mkv',
                    'poster': 'https://publicdomainmovie.net/wikimedia.php?id=Movie-Mystery-Magazine-July-1946.jpg',
                    'plot': 'Dùng thử',
                    'year': 1946,
                }
            ]
        }
    ]

def json_load(str):
    try:
    # đọc JSON trừ chuổi
        return json.loads(str)
    except:
        return None
    
def getListPhim():
    try:
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
    except Exception as inst: 
        exc_type, exc_obj, exc_tb = sys.exc_info() 
        getPyFormData("TelegramSendBot", {
                            "content":"Lỗi tại:"+str(exc_tb.tb_lineno)+", loại:"+str(exc_type) +"-Lỗi:"+str(inst),
                            "telegram_user":"thanhlm22"
                        })  
    return []

def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{}?{}'.format(URL, urlencode(kwargs))


def get_genres():
    """
    Get the list of video genres

    Here you can insert some code that retrieves
    the list of video sections (in this case movie genres) from some site or API.

    :return: The list of video genres
    :rtype: list
    """
    VIDEOS = getListPhim()
    return VIDEOS


def get_videos(genre_index):
    """
    Get the list of videofiles/streams.

    Here you can insert some code that retrieves
    the list of video streams in the given section from some site or API.

    :param genre_index: genre index
    :type genre_index: int
    :return: the list of videos in the category
    :rtype: list
    """
    return VIDEOS[genre_index]


def list_genres():
    """
    Create the list of movie genres in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(HANDLE, 'Public Domain Movies')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(HANDLE, 'movies')
    # Get movie genres
    genres = get_genres()
    # Iterate through genres
    for index, genre_info in enumerate(genres):
        # Create a list item with a text label.
        list_item = xbmcgui.ListItem(label=genre_info['genre'])
        # Set images for the list item.
        list_item.setArt({'icon': genre_info['icon'], 'fanart': genre_info['fanart']})
        # Set additional info for the list item using its InfoTag.
        # InfoTag allows to set various information for an item.
        # For available properties and methods see the following link:
        # https://codedocs.xyz/xbmc/xbmc/classXBMCAddon_1_1xbmc_1_1InfoTagVideo.html
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType('video')
        info_tag.setTitle(genre_info['genre'])
        info_tag.setGenres([genre_info['genre']])
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&genre_index=0
        url = get_url(action='listing', genre_index=index)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)


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

def list_videos(genre_index):
    """
    Create the list of playable videos in the Kodi interface.

    :param genre_index: the index of genre in the list of movie genres
    :type genre_index: int
    """
    genre_info = get_videos(genre_index)
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(HANDLE, genre_info['genre'])
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(HANDLE, 'movies')
    # Get the list of videos in the category.
    videos = genre_info['movies']

    #vì session chỉ thời gian là hết nên cứ login lại
    session_id,token_ = loginFshare("fshare_tkvv@fshare.vn","1234@abcd")

    videos_new = []
    for video in videos:
        link_view = buildLinkDown(video['url'],token_,session_id)
        if link_view!="":
            video['url']=link_view  
            videos_new.append(video)

    # Iterate through videos.
    for video in videos_new:
        # Create a list item with a text label
        list_item = xbmcgui.ListItem(label=video['title'])
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use only poster for simplicity's sake.
        # In a real-life plugin you may need to set multiple image types.
        list_item.setArt({'poster': video['poster']})
        # Set additional info for the list item via InfoTag.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType('movie')
        info_tag.setTitle(video['title'])
        info_tag.setGenres([genre_info['genre']])
        info_tag.setPlot(video['plot'])
        info_tag.setYear(video['year'])
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=https%3A%2F%2Fia600702.us.archive.org%2F3%2Fitems%2Firon_mask%2Firon_mask_512kb.mp4
        
        url = get_url(action='play', video=video['url'])
        #build lại các url của videos 
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    # offscreen=True means that the list item is not meant for displaying,
    # only to pass info to the Kodi player
    play_item = xbmcgui.ListItem(offscreen=True)
    play_item.setPath(path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    formLogin()
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if not params:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_genres()
    elif params['action'] == 'listing':
        # Display the list of videos in a provided category.
        list_videos(int(params['genre_index']))
    elif params['action'] == 'play':
        # Play a video from a provided URL.
        play_video(params['video'])
    else:
        # If the provided paramstring does not contain a supported action
        # we raise an exception. This helps to catch coding errors,
        # e.g. typos in action names.
        raise ValueError(f'Invalid paramstring: {paramstring}!')

def getPyFormData(key__request, data__request={}):
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
    return {}

def formLogin():
    # Create a window instance.
    window = MyWindow('Hello, World!')
    # Show the created window.
    window.doModal()
    # Delete the window instance when it is no longer used.
    del window 

class MyWindow(pyxbmct.AddonDialogWindow):

    def __init__(self, title=''):
        # You need to call base class' constructor.
        super(MyWindow, self).__init__(title)
        # Set the window width, height and the grid resolution: 2 rows, 3 columns.
        self.setGeometry(350, 150, 2, 3)
        # Create a text label.
        label = pyxbmct.Label('This is a PyXBMCt window.', alignment=pyxbmct.ALIGN_CENTER)
        # Place the label on the window grid.
        self.placeControl(label, 0, 0, columnspan=3)
        # Create a button.
        button = pyxbmct.Button('Close')
        # Place the button on the window grid.
        self.placeControl(button, 1, 1)
        # Set initial focus on the button.
        self.setFocus(button)
        # Connect the button to a function.
        self.connect(button, self.close)
        # Connect a key action to a function.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

if __name__ == '__main__':
    # 
    # getPyFormData("TelegramSendBot", {
    #                         "content":"aaaaa", 
    #                         "telegram_user":"thanhlm22"
    #                     })

    VIDEOS = getListPhim()
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])

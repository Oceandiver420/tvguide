import sys
import xbmc,xbmcaddon,xbmcvfs,xbmcgui
import sqlite3
import re
import urllib
from HTMLParser import HTMLParser

ADDON = xbmcaddon.Addon(id='script.tvguide.fullscreen')
orig_title = sys.argv[1]
title = urllib.quote_plus(orig_title)

f = xbmcvfs.File('special://home/addons/script.tvguide.fullscreen/resources/favourites.xml')
data = f.read()

search_addons = {}
match = re.findall('<favourite name="(.*?)" thumb="(.*?)">(.*?)</favourite>',data)
for m in match:
    name = m[0]
    thumb = m[1]
    action = m[2]
    xbmc.log(name)
    xbmc.log(thumb)
    xbmc.log(action)
    action = HTMLParser().unescape(action)
    xbmc.log(action)
    action = re.sub('\?sf_options.*?options_sf','',action)
    action = re.sub('\[%SF%\]',title,action)
    xbmc.log(action)
    p = re.search('plugin://(.*?)/',action)
    if p:
        plugin = p.group(1)
        try:
            a = xbmcaddon.Addon(plugin)
            if a:
                search_addons[name] = action
        except: pass
    
d = xbmcgui.Dialog()
names = sorted(search_addons.keys())
which = d.select('Search: %s' % orig_title,names)
if which:
    xbmc.log(repr(type(which)))
    xbmc.executebuiltin(search_addons[names[which]])

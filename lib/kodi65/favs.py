# -*- coding: utf8 -*-

# Copyright (C) 2016 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

from kodi65 import ListItem
from kodi65 import utils
from kodi65 import kodijson


def get_favs_by_type(fav_type):
    """
    returns dict list containing favourites with type *fav_type
    """
    return [fav for fav in get_favs() if fav["type"] == fav_type]


def get_fav_path(fav):
    """
    get builtin for fav according to type
    """
    if fav["type"] == "media":
        return "PlayMedia(%s)" % (fav["path"])
    elif fav["type"] == "script":
        return "RunScript(%s)" % (fav["path"])
    elif "window" in fav and "windowparameter" in fav:
        return "ActivateWindow(%s,%s)" % (fav["window"], fav["windowparameter"])
    else:
        utils.log("error parsing favs")


def get_favs():
    """
    returns dict list containing favourites
    """
    items = []
    data = kodijson.get_favourites()
    if "result" not in data or data["result"]["limits"]["total"] == 0:
        return []
    for fav in data["result"]["favourites"]:
        path = get_fav_path(fav)
        item = ListItem(label=fav["title"],
                        path="plugin://script.extendedinfo/?info=action&&id=" + path)
        item.set_artwork({'thumb': fav["thumbnail"]})
        item.set_properties({'type': fav["type"],
                             'builtin': path})
    return items


def get_icon_panel(number):
    """
    get icon panel with index *number, returns dict list based on skin strings
    """
    items = []
    offset = number * 5 - 5
    for i in xrange(1, 6):
        infopanel_path = utils.get_skin_string("IconPanelItem%i.Path" % (i + offset))
        items.append({'label': utils.get_skin_string("IconPanelItem%i.Label" % (i + offset)),
                      'path': "plugin://script.extendedinfo/?info=action&&id=" + infopanel_path,
                      'thumb': utils.get_skin_string("IconPanelItem%i.Icon" % (i + offset)),
                      'id': "IconPanelitem%i" % (i + offset),
                      'type': utils.get_skin_string("IconPanelItem%i.Type" % (i + offset))})
    return items

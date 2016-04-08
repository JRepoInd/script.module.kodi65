# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmcgui
import xbmc

from kodi65 import addon

C_LIST_SIMPLE = 3
C_LIST_DETAIL = 6
C_BUTTON_GET_MORE = 5
C_LABEL_HEADER = 1


class SelectDialog(xbmcgui.WindowXMLDialog):
    ACTION_PREVIOUS_MENU = [9, 92, 10]

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.items = kwargs.get('listing')
        self.listitems = [i.get_listitem() for i in self.items] if self.items else []
        self.listitem = None
        self.index = -1

    def onInit(self):
        self.list = self.getControl(C_LIST_DETAIL)
        self.getControl(C_LIST_SIMPLE).setVisible(False)
        self.getControl(C_BUTTON_GET_MORE).setVisible(False)
        self.getControl(C_LABEL_HEADER).setLabel(addon.LANG(32151))
        self.list.addItems(self.listitems)
        self.setFocus(self.list)

    def onAction(self, action):
        if action in self.ACTION_PREVIOUS_MENU:
            self.close()
        elif action == xbmcgui.ACTION_CONTEXT_MENU:
            self.close()

    def onClick(self, control_id):
        if control_id in [C_LIST_SIMPLE, C_LIST_DETAIL]:
            self.index = int(self.list.getSelectedPosition())
            self.listitem = self.items[self.index]
            self.close()

    def onFocus(self, control_id):
        pass


def open_selectdialog(self, listitems):
    """
    open selectdialog, return listitem dict and index
    """
    xbmc.executebuiltin("Dialog.Close(busydialog)")
    w = SelectDialog('DialogSelect.xml', addon.PATH,
                     listing=listitems)
    w.doModal()
    return w.listitem, w.index

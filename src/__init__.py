"""
nki add-on "paste plain"
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Copyright: 2019-ijgnd
           Ankitects Pty Ltd and contributors

This add-on uses Octicons-diff-modified.svg which
is covered by the following copyright and permission notice:

    MIT License

    Copyright (c) 2019 GitHub Inc.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import json
import os

from anki.hooks import addHook
from aqt import mw
from aqt.qt import *


def gc(arg, fail=False):
    conf = mw.addonManager.getConfig(__name__)
    if conf:
        return conf.get(arg, fail)
    return fail


def insert_plain(self):
    clip = self.mw.app.clipboard()
    try:
        textonly = clip.mimeData().text()
    except:
        textonly = ""
    if not textonly:
        return
    # mod = textonly.replace("\n","<br>").replace(" ","&nbsp;")
    mod = "<div>" + textonly.replace("\n", "</div><div>").replace(" ", "&nbsp;") + "</div>"
    self.web.eval("document.execCommand('inserthtml', false, %s);" % json.dumps(mod))


def keystr(k):
    key = QKeySequence(k)
    return key.toString(QKeySequence.NativeText)


def editorContextMenu(ewv, menu):
    e = ewv.editor
    if gc("context_menu_entry", False):
        a = menu.addAction("Paste as Plain Text ({})".format(keystr(gc("shortcut_paste_plain",""))))
        a.triggered.connect(lambda _, ed=e: insert_plain(e))
addHook('EditorWebView.contextMenuEvent', editorContextMenu)


if gc("show button"):
    addon_path = os.path.dirname(__file__)
    def setupEditorButtonsFilterFD(buttons, editor):
        b = editor.addButton(
            os.path.join(addon_path, "Octicons-diff-modified"),
            "paste_plain_button",
            lambda e=editor: insert_plain(e),
            tip="Paste plain text ({})".format(keystr(gc("shortcut_paste_plain", ""))),
            keys=gc("shortcut_paste_plain", "")
            )
        buttons.extend([b])
        return buttons
    addHook("setupEditorButtons", setupEditorButtonsFilterFD)
else:
    def SetupShortcuts(cuts, self):
        if gc("shortcut_paste_plain", False):
            cuts.append((gc("shortcut_paste_plain"), lambda e=self: insert_plain(e)))
    addHook("setupEditorShortcuts", SetupShortcuts)

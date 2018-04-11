#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import logging
import signal
import subprocess
from functools import partial
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtWidgets import (
    QWidget, QSystemTrayIcon, QMenu, QApplication, QMessageBox)
from PyQt5.QtCore import QCoreApplication

logger = logging.getLogger(__name__)



class OpenCCTray(QSystemTrayIcon):
    """OpenCC tray."""

    CONFIG_S2T = 0
    CONFIG_T2S = 1

    def __init__(self, icon, parent=None):
        """Constructor."""
        QSystemTrayIcon.__init__(self, icon, parent)

        self.menu = None
        self._load_menu()

    def _load_menu(self):
        """According to config to load menu."""
        if self.menu:
            self.menu.clear()

        menu = QMenu()
        s2t_action = menu.addAction(self.tr("Simplified -> Traditional"))
        t2s_action = menu.addAction(self.tr("Traditional -> Simplified"))
        s2t_action.triggered.connect(self._translate_s2t)
        t2s_action.triggered.connect(self._translate_t2s)

        menu.addSeparator()

        aboutAction = menu.addAction(self.tr("About"))
        aboutAction.triggered.connect(self._about)
        exit_action = menu.addAction(self.tr("Exit"))
        exit_action.triggered.connect(self._quit)

        self.setContextMenu(menu)
        self.menu = menu

    def _translate(self, config):
        CONFIG_FILE = {
            self.CONFIG_S2T: "/usr/lib/x86_64-linux-gnu/opencc/zhs2zht.ini",
            self.CONFIG_T2S: "/usr/lib/x86_64-linux-gnu/opencc/zht2zhs.ini"
        }
        xsel_input = subprocess.Popen(['xsel', '--clipboard', '-o'],
                                      stdout=subprocess.PIPE)
        opencc = subprocess.Popen(['opencc', '-c', CONFIG_FILE[config]],
                                  stdin=xsel_input.stdout,
                                  stdout=subprocess.PIPE)
        xsel_output = subprocess.Popen(['xsel', '--clipboard', '-i'],
                                       stdin=opencc.stdout,
                                       stdout=subprocess.PIPE)
        end_of_pipe = xsel_output.stdout
        result = ''.join(end_of_pipe)

    def _translate_s2t(self):
        self._translate(self.CONFIG_S2T)

    def _translate_t2s(self):
        self._translate(self.CONFIG_T2S)

    def _about(self):
        """Launch about dialog."""
        QMessageBox.about(None, "opencc-tray", """opencc-tray

Homepage: https://github.com/elleryq/opencc-tray
Author: Yan-ren Tsai""")

    def _quit(self):
        """Quit."""
        QCoreApplication.instance().quit()


def main():
    """Main entry."""
    # Accept ctrl-c
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    pixmaps_dir = os.path.join(
        os.path.dirname(__file__),
        "pixmaps"
    )
    pixmap = os.path.join(pixmaps_dir, "tray.png")

    w = QWidget()
    tray_icon = OpenCCTray(QtGui.QIcon(pixmap), w)

    tray_icon.show()
    rc = app.exec_()

    del tray_icon
    del w
    del app

    sys.exit(rc)

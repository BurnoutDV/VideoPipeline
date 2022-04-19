#!/usr/bin/env python
# coding: utf-8

# Copyright 2022 by BurnoutDV, <development@burnoutdv.com>
#
# This file is part of [CHANGE]VideoPipeline.
#
# [CHANGE]VideoPipeline is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# [CHANGE]VideoPipeline is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0-only <https://www.gnu.org/licenses/gpl-3.0.en.html>

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator
from gui_logic import VideoPipelineGui

if __name__ == "__main__":
    anApp = QApplication(sys.argv)
    i18n = QTranslator()
    i18n.load("VideoPipeline")
    anApp.installTranslator(i18n)

    main = VideoPipelineGui()
    main.show()
    try:
        sys.exit(anApp.exec())
    except KeyboardInterrupt:
        sys.exit()


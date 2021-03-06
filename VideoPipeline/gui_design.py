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

from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtWidgets import *
from PySide6 import QtCore, QtWidgets
import hard_definitions

# TODO: add ToolTip Hints
# Update Interface Design

class VideoPipelineMainInterface(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        #
        policy_minimum_expanding = QSizePolicy()
        policy_minimum_expanding.Policy = QSizePolicy.MinimumExpanding
        # window setup
        self.setBaseSize(1280, 720)
        self.setMinimumSize(800, 600)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint & QtCore.Qt.WindowMaximizeButtonHint)
        self.setWindowTitle(self.tr("VideoPipeline Version") + f" - {hard_definitions.VERSION}")
        self.setAcceptDrops(True)

        self.the_main_widget = QWidget()
        self.setCentralWidget(self.the_main_widget)
        # widgets
        lay_main_half = QHBoxLayout()
        lay_left_side = QVBoxLayout()
        lay_left_btn = QHBoxLayout()
        lay_right_side = QVBoxLayout()
        lay_right_lay = QVBoxLayout()  # was form layout which it basically is
        # left side widgets
        self.w_schedule_view = QColumnView()
        self.w_btn_schedule_start = QPushButton(self.tr("Start"), MaximumWidth=100)
        self.w_btn_schedule_stop = QPushButton(self.tr("Stop"), MaximumWidth=100)
        self.w_btn_schedule_abort = QPushButton(self.tr("Abort"), MaximumWidth=100)
        self.w_btn_schedule_delete = QPushButton(self.tr("Delete"), MaximumWidth=100)
        # right side widgets
        self.w_input_file_name = QLineEdit(ReadOnly=True, MinimumWidth=200)
        self.w_input_file_name.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.w_input_file_btn = QPushButton(self.tr("Load"))
        self.w_project_combo = QComboBox(MinimumWidth=200)
        self.w_project_combo.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.w_project_btn = QPushButton("...")
        self.w_encoder_combo = QComboBox(MinimumWidth=200)
        self.w_encoder_combo.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.w_encoder_btn = QPushButton("...")  # QToolButton for (edit as new, edit)
        # who would have thought that labels are the primary image widget Oo
        self.w_video_preview1 = QLabel(BaseSize=QtCore.QSize(355, 200))
        self.w_video_preview2 = QLabel(BaseSize=QtCore.QSize(355, 200))
        self.w_video_preview3 = QLabel(BaseSize=QtCore.QSize(355, 200))
        self.w_details_tabs = QTabWidget()
        self.w_details_project = QWidget()
        self.w_details_encoding = QWidget()
        self.w_details_variables = QWidget()
        self.w_details_schedules = QWidget()
        self.w_details_mediainfo = QWidget()

        # +++ tabs - project
        self.w_proj_title = QLineEdit()
        self.w_proj_desc = QTextEdit()
        self.w_proj_tags = QTextEdit()

        # +++ tabs - encoding
        self.w_enc_presets = QComboBox()
        self.w_enc_preset_new = QPushButton("New")
        self.w_enc_preset_del = QPushButton("Del", Disabled=True)
        self.w_enc_preset_save = QPushButton("Save", Disabled=True)
        self.w_enc_preset_options = QToolButton()
        self.w_enc_video_codec = QComboBox(Disabled=True)
        self.w_enc_video_codec.addItems(["x264"])
        self.w_enc_video_slider = QSlider(orientation=QtCore.Qt.Orientation.Horizontal, singleStep=1, PageStep=10,
                                          Maximum=510, Minimum=0, tickInterval=10, TickPosition=QSlider.TicksBothSides)
        self.w_enc_video_quality = QDoubleSpinBox(singleStep=0.1, Decimals=1, Maximum=51, Minimum=0)
        self.w_enc_video_rescale = QComboBox()
        self.w_enc_video_rescale.addItems([""]+hard_definitions.rescale_presets)
        self.w_enc_video_frame_reduce = QCheckBox(self.tr("Reduce to 30 fps"))
        self.w_enc_audio_codec = QComboBox(Disabled=True)
        self.w_enc_audio_codec.addItems(["vorbis"])
        self.w_enc_audio_archive = QCheckBox(self.tr("Archive Audio"))
        # vorbis audio quality goes from 0 to 10
        self.w_enc_audio_slider = QSlider(orientation=QtCore.Qt.Orientation.Horizontal, singleStep=1, PageStep=10,
                                          Maximum=100, Minimum=10, tickInterval=10, TickPosition=QSlider.TicksBothSides)
        self.w_enc_audio_quality = QDoubleSpinBox(singleStep=0.1, Decimals=1, Maximum=10, Minimum=1)

        # +++ tabs - variables
        self.w_variables_table = QTableWidget(ColumnCount=2,
                                              HorizontalHeaderLabels=[self.tr("Variable"), self.tr("Value")])
        self.w_variables_table.verticalHeader().setVisible(False)
        self.w_variables_table.horizontalHeader().setStretchLastSection(True)
        self.w_variables_table.horizontalHeader().setSectionsClickable(False)

        # +++ things into layout +++
        # main
        main_spliter = QSplitter()
        main_left_container = QWidget()
        main_right_container = QWidget()
        main_left_container.setLayout(lay_left_side)
        main_right_container.setLayout(lay_right_side)
        main_spliter.addWidget(main_left_container)
        main_spliter.addWidget(main_right_container)
        lay_main_half.addWidget(main_spliter)
        #lay_main_half.addLayout(lay_left_side)
        #lay_main_half.addLayout(lay_right_side)
        # left side
        lay_left_side.addWidget(self.w_schedule_view)
        lay_left_btn.addWidget(self.w_btn_schedule_start)
        lay_left_btn.addWidget(self.w_btn_schedule_stop)
        lay_left_btn.addWidget(self.w_btn_schedule_abort)
        lay_left_btn.addStretch(1)
        lay_left_btn.addWidget(self.w_btn_schedule_delete)
        lay_left_side.addLayout(lay_left_btn)

        # right side
        lay_right_side.addLayout(lay_right_lay)
        _ = QHBoxLayout()
        _.addWidget(self.w_input_file_name)
        _.addWidget(self.w_input_file_btn)
        lay_right_lay.addLayout(_)
        _ = QHBoxLayout()
        _.addWidget(self.w_project_combo)
        _.addWidget(self.w_project_btn)
        lay_right_lay.addLayout(_)
        _ = QHBoxLayout()
        _.addWidget(self.w_encoder_combo)
        _.addWidget(self.w_encoder_btn)
        lay_right_lay.addLayout(_)
        preview_scroll = QScrollArea()
        preview_container = QHBoxLayout()
        preview_container.addStretch(10)
        preview_container.addWidget(self.w_video_preview1)
        preview_container.addWidget(self.w_video_preview2)
        preview_container.addWidget(self.w_video_preview3)
        preview_container.addStretch(10)
        preview_scroll.setLayout(preview_container)
        lay_right_lay.addWidget(preview_scroll)

        lay_right_side.addWidget(self.w_details_tabs)
        self.w_details_tabs.addTab(self.w_details_project, self.tr("Project"))
        self.w_details_tabs.addTab(self.w_details_encoding, self.tr("Encoding"))
        self.w_details_tabs.addTab(self.w_details_variables, self.tr("Variables"))
        self.w_details_tabs.addTab(self.w_details_schedules, self.tr("Schedule"))
        self.w_details_tabs.addTab(self.w_details_mediainfo, self.tr("Media Info"))

        # ### tabbed view ###
        # +++ project tab - i like those group frames but making them on the fly is somewhat annoying
        proj_lay = QVBoxLayout()
        temp = QGroupBox(self.tr("Title"))
        temp2 = QHBoxLayout()
        temp2.addWidget(self.w_proj_title)
        temp.setLayout(temp2)
        proj_lay.addWidget(temp)
        temp = QGroupBox(self.tr("Description"))
        temp2 = QHBoxLayout()
        temp2.addWidget(self.w_proj_desc)
        temp.setLayout(temp2)
        proj_lay.addWidget(temp)
        temp = QGroupBox(self.tr("Tags"))
        temp2 = QHBoxLayout()
        temp2.addWidget(self.w_proj_tags)
        temp.setLayout(temp2)
        proj_lay.addWidget(temp)
        self.w_details_project.setLayout(proj_lay)

        # +++ encoding tab  - tried grid layout, exploding in my face, old fashioned is the way for me
        encoding_grid = QVBoxLayout()
        # *
        temp = QHBoxLayout()
        temp.addWidget(self.w_enc_presets)
        temp.addWidget(self.w_enc_preset_new)
        temp.addWidget(self.w_enc_preset_del)
        temp.addWidget(self.w_enc_preset_save)
        # *
        encoding_grid.addLayout(temp)
        encoding_grid.addWidget(self.w_enc_video_codec)
        # *
        temp = QHBoxLayout()
        temp.addWidget(self.w_enc_video_slider)
        temp.addWidget(self.w_enc_video_quality)
        # *
        encoding_grid.addLayout(temp)
        encoding_grid.addWidget(self.w_enc_video_rescale)
        encoding_grid.addWidget(self.w_enc_video_frame_reduce)
        encoding_grid.addLayout(temp)
        encoding_grid.addWidget(self.w_enc_audio_codec)
        # *
        temp = QHBoxLayout()
        temp.addWidget(self.w_enc_audio_slider)
        temp.addWidget(self.w_enc_audio_quality)
        # *
        encoding_grid.addLayout(temp)
        encoding_grid.addWidget(self.w_enc_audio_archive)
        encoding_grid.addStretch(1)
        self.w_details_encoding.setLayout(encoding_grid)

        # +++ variables tab
        variables_lay = QHBoxLayout()  # unnecessary complex for later extension
        variables_lay.addWidget(self.w_variables_table)
        self.w_details_variables.setLayout(variables_lay)


        self.the_main_widget.setLayout(lay_main_half)
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
from PySide6 import QtCore
import hard_definitions


# TODO: add support for b-frames and parameter g..and read up what 'g' actually do
# TODO: add ToolTip Hints

class EncoderPresetDialogue(QDialog):
    def __init__(self, encoder_preset=None, parent=None):
        """
        Spawns a new encoder Settings Dialogue

        :param dict encoder_preset: if None use all encoder defaults
        :param parent: parent Widget/Window
        """
        super().__init__(parent)

        self.setWindowTitle(self.tr("Encoder Preset Settings"))
        self.setMinimumWidth(240)
        self.setMinimumHeight(580)

        # widgets
        self.w_enc_presets = QComboBox()
        self.w_enc_preset_new = QPushButton("New")
        self.w_enc_preset_del = QPushButton("Del", Disabled=True)
        self.w_enc_preset_save = QPushButton("Save", Disabled=True)
        self.w_enc_preset_options = QToolButton()
        self.w_enc_video_codec = QComboBox(Disabled=True)
        self.w_enc_video_codec.addItems(["x264"])
        self.w_enc_video_src = QSpinBox(Maximum=20)
        self.w_enc_video_slider = QSlider(orientation=QtCore.Qt.Orientation.Horizontal, singleStep=1, PageStep=10,
                                          Maximum=510, Minimum=0, tickInterval=10, TickPosition=QSlider.TicksBothSides)
        self.w_enc_video_quality = QDoubleSpinBox(singleStep=0.1, Decimals=1, Maximum=51, Minimum=0)
        self.w_enc_audio_codec = QComboBox(Disabled=True)
        self.w_enc_audio_codec.addItems(["vorbis"])
        # vorbis audio quality goes from 0 to 10
        self.w_enc_audio_slider = QSlider(orientation=QtCore.Qt.Orientation.Horizontal, singleStep=1, PageStep=10,
                                          Maximum=100, Minimum=10, tickInterval=10, TickPosition=QSlider.TicksBothSides)
        self.w_enc_audio_quality = QDoubleSpinBox(singleStep=0.1, Decimals=1, Maximum=10, Minimum=1)

        # audio merge options
        # ? these are like super specific for my kind of project
        self.w_aud_merge_tr1 = QSlider(orientation=QtCore.Qt.Orientation.Horizontal, singleStep=1, PageStep=6,
                                          Maximum=24, Minimum=-24, tickInterval=1, TickPosition=QSlider.TicksBothSides)
        self.w_aud_merge_tr2 = QSlider(orientation=QtCore.Qt.Orientation.Horizontal, singleStep=1, PageStep=6,
                                       Maximum=24, Minimum=-24, tickInterval=1, TickPosition=QSlider.TicksBothSides)
        self.w_aud_merge_src_1 = QSpinBox(Minimum=0, Maximum=20, SingleStep=1)
        self.w_aud_merge_src_2 = QSpinBox(Minimum=0, Maximum=20, SingleStep=1)
        self.w_aud_merge_info1 = QLabel()
        self.w_aud_merge_info2 = QLabel()

        # transformation
        self.w_enc_audio_archive = QCheckBox(self.tr("Archive Audio"))
        self.w_enc_video_rescale = QComboBox()
        self.w_enc_video_rescale.addItems([""] + hard_definitions.rescale_presets)
        self.w_enc_video_frame_reduce = QComboBox()
        self.w_enc_video_frame_reduce.addItems([""] + hard_definitions.reframe_presets)

        self.w_dialogue = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)

        # +++ layout +++
        #  phantom things
        h0 = QHBoxLayout()
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        group_audio = QGroupBox(self.tr("Audio merge control"))
        group_audio_lay = QVBoxLayout()
        group_audio.setLayout(group_audio_lay)
        gr_aud_1 = QGroupBox(self.tr("Track 1 Audio Boost"))
        gr_aud_1_lay = QVBoxLayout()
        gr_aud_1.setLayout(gr_aud_1_lay)
        gr_aud_2 = QGroupBox(self.tr("Track 2 Audio Boost"))
        gr_aud_2_lay = QVBoxLayout()
        gr_aud_2.setLayout(gr_aud_2_lay)
        h3 = QHBoxLayout()
        h4 = QHBoxLayout()
        group_trans = QGroupBox(self.tr("Transform Input"))
        group_trans_lay = QVBoxLayout()
        group_trans.setLayout(group_trans_lay)
        h5 = QHBoxLayout()
        h6 = QHBoxLayout()

        #  real elements
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.w_enc_video_codec)
        h0.addWidget(QLabel(self.tr("Video Track Source: ")))
        h0.addWidget(self.w_enc_video_src)
        h0.addStretch(1)
        self.layout.addLayout(h0)
        h1.addWidget(self.w_enc_video_slider)
        h1.addWidget(self.w_enc_video_quality)
        self.layout.addLayout(h1)
        self.layout.addWidget(self.w_enc_audio_codec)
        h2.addWidget(self.w_enc_audio_slider)
        h2.addWidget(self.w_enc_audio_quality)
        self.layout.addLayout(h2)
        # Audio Stuff
        gr_aud_1_lay.addWidget(self.w_aud_merge_tr1)
        group_audio_lay.addWidget(gr_aud_1)
        gr_aud_2_lay.addWidget(self.w_aud_merge_tr2)
        group_audio_lay.addWidget(gr_aud_2)
        h3.addWidget(QLabel(self.tr("Track 1 Source")))
        h3.addWidget(self.w_aud_merge_src_1)
        h3.addStretch(1)
        h3.addWidget(self.w_aud_merge_info1)
        group_audio_lay.addLayout(h3)
        h4.addWidget(QLabel(self.tr("Track 2 Source")))
        h4.addWidget(self.w_aud_merge_src_2)
        h4.addStretch(1)
        h4.addWidget(self.w_aud_merge_info2)
        group_audio_lay.addLayout(h4)
        self.layout.addWidget(group_audio)
        # Transform
        h5.addWidget(QLabel(self.tr("Up/Downsample Fps")))
        h5.addWidget(self.w_enc_video_frame_reduce)
        group_trans_lay.addLayout(h5)
        h6.addWidget(QLabel(self.tr("Rescale Output")))
        h6.addWidget(self.w_enc_video_rescale)
        group_trans_lay.addLayout(h6)
        group_trans_lay.addWidget(self.w_enc_audio_archive)
        self.layout.addWidget(group_trans)
        self.setLayout(self.layout)
        self.layout.addWidget(self.w_dialogue)
        self.layout.addStretch(1)

        # actions

        self.w_dialogue.accepted.connect(self.accept)
        self.w_dialogue.rejected.connect(self.reject)
        self.w_aud_merge_tr1.valueChanged.connect(self.a_update_aud_merge_info)
        self.w_aud_merge_tr2.valueChanged.connect(self.a_update_aud_merge_info)
        self.w_enc_video_slider.valueChanged.connect(self.a_video_slider_sync)
        self.w_enc_video_quality.valueChanged.connect(self.a_video_quality_sync)
        self.w_enc_audio_slider.valueChanged.connect(self.a_audio_slider_sync)
        self.w_enc_audio_quality.valueChanged.connect(self.a_audio_quality_sync)

        # data setup
        self._init_data(encoder_preset)

    def _init_data(self, ep: dict):
        """
        Sets the Widget to an appropriate Value based on the program default, if not exist to program default
        :param dict ep: encoder preset, abbreviated because i type it 20 times in this
        :return:
        """
        self.w_enc_video_src.setValue(ep.get('vid_src', hard_definitions.vp_vid_stream))
        #  EncoderPresetDialogue.set_combo_box(self.w_enc_video_codec, hard_definitions.vp_vid_codec)
        self.w_enc_video_quality.setValue(ep.get('vid_quality', hard_definitions.vp_vid_crf))
        #  EncoderPresetDialogue.set_combo_box(self.w_enc_audio_codec, hard_definitions.vp_aud_codec)
        self.w_enc_audio_quality.setValue(ep.get('aud_quality', hard_definitions.vp_aud_quality))
        # * i am already amazed how i am super inconsistent with index starting by 1 and 0 left and right
        self.w_aud_merge_src_1.setValue(ep.get('aud_src1', hard_definitions.vp_aud_stream0))
        self.w_aud_merge_src_2.setValue(ep.get('aud_src2', hard_definitions.vp_aud_stream1))
        self.w_aud_merge_tr1.setValue(ep.get('aud_adj1', hard_definitions.vp_aud_stream0_boost))
        self.w_aud_merge_tr2.setValue(ep.get('aud_adj2', hard_definitions.vp_aud_stream1_boost))
        self.a_update_aud_merge_info()
        EncoderPresetDialogue.set_combo_box(self.w_enc_video_rescale, ep.get('vid_rescale', ''))
        EncoderPresetDialogue.set_combo_box(self.w_enc_video_frame_reduce, ep.get('vid_sample', ''))
        if ep.get('aud_archive', False):
            self.w_enc_audio_archive.setChecked(True)

    def get_data(self):
        """
        Returns an encoding preset dictionary
        :return:
        """
        ep = {
            "vid_src": self.w_enc_video_src.value(),
            "vid_quality": self.w_enc_video_quality.value(),
            "vid_codec": self.w_enc_video_codec.currentText(),
            "aud_src1": self.w_aud_merge_src_1.value(),
            "aud_src2": self.w_aud_merge_src_2.value(),
            "aud_quality": self.w_enc_audio_quality.value(),
            "aud_codec": self.w_enc_audio_codec.currentText(),
            "aud_adj1": self.w_aud_merge_tr1.value(),
            "aud_adj2": self.w_aud_merge_tr2.value(),
            "vid_rescale": self.w_enc_video_rescale.currentText(),
            "vid_sample": self.w_enc_video_frame_reduce.currentText(),
            "aud_archive": False
        }
        if self.w_enc_audio_archive.isChecked():
            ep['aud_archive'] = True
        return ep

    def a_update_aud_merge_info(self):
        self.w_aud_merge_info1.setText(f"{self.w_aud_merge_tr1.value()} dB")
        self.w_aud_merge_info2.setText(f"{self.w_aud_merge_tr2.value()} dB")

    def a_video_slider_sync(self):
        """
        Syncs from Slider to Spin Box
        """
        self.w_enc_video_quality.setValue(self.w_enc_video_slider.value() / 10)

    def a_video_quality_sync(self):
        """
        Syncs quality back to the slider
        """
        self.w_enc_video_slider.setValue(round(self.w_enc_video_quality.value() * 10))

    def a_audio_slider_sync(self):
        """
        Syncs from Slider to Spin Box
        """
        self.w_enc_audio_quality.setValue(self.w_enc_audio_slider.value() / 10)

    def a_audio_quality_sync(self):
        """
        Syncs quality back to the slider
        """
        self.w_enc_audio_slider.setValue(round(self.w_enc_audio_quality.value() * 10))

    @staticmethod
    def set_combo_box(widget: QComboBox, value):
        """
        Sets the Combo Box to the given value if it exists
        :param widget:
        :param value:
        :return: True if the value was found and set, else false
        :rtype: bool
        """
        index = widget.findText(value, QtCore.Qt.MatchFixedString)
        if index > 0:
            widget.setCurrentIndex(index)
            return True
        return False

